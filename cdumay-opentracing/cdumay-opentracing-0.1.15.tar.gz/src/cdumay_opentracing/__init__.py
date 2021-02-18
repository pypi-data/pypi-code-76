#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from typing import AnyStr, Optional, Any, Dict

import jaeger_client
import opentracing
import six
from jaeger_client import SpanContext
from jaeger_client.constants import SAMPLED_FLAG, DEBUG_FLAG
from jaeger_client.thrift_gen.jaeger.ttypes import Tag
from opentracing.ext import tags as ext_tags


def tag2value(tag: Tag) -> (AnyStr, Optional[Any]):
    """Try to get find basic value from tag"""
    for attr in ('vBinary', 'vStr', 'vDouble', 'vBool', 'vLong'):
        value = getattr(tag, attr)
        if value:
            return tag.key, value
    return tag.key, None


class Span(jaeger_client.Span):
    """Implements jaeger_client.Span"""
    FORMAT = opentracing.Format.TEXT_MAP
    TAGS = []

    @classmethod
    def span_from_object(cls, obj: Any) -> "Span":
        """Create span from an object"""
        if obj:
            ctx = dict()
            for attr in ('trace_id', 'span_id', 'parent_id', 'flags'):
                ctx[attr] = getattr(obj, attr, None)
            context = jaeger_client.SpanContext(**ctx)

            return cls(
                context=context, tracer=opentracing.tracer,
                operation_name=getattr(obj, 'operation_name', None),
                tags=getattr(obj, 'tags', dict()),
                start_time=getattr(obj, 'start_time', None)
            )

    @classmethod
    def span_from_dict(cls, obj: Dict) -> "Span":
        """Create span from a dict"""
        if len(obj) > 0:
            ctx = dict()
            for attr in ('trace_id', 'span_id', 'parent_id', 'flags'):
                ctx[attr] = obj.get(attr, None)
            context = jaeger_client.SpanContext(**ctx)

            return cls(
                context=context, tracer=opentracing.tracer,
                operation_name=obj.get('operation_name'), tags=obj.get('tags'),
                start_time=obj.get('start_time')
            )

    @classmethod
    def span_serialize(cls, span: Any) -> Dict:
        """Serialize span into dict"""
        return dict(
            trace_id=span.context.trace_id, span_id=span.context.span_id,
            parent_id=span.context.parent_id, flags=span.context.flags,
            operation_name=span.operation_name, start_time=span.start_time,
            tags=dict([tag2value(x) for x in span.tags])
        )

    @classmethod
    def name(cls, obj: Any) -> AnyStr:
        """ Extract span name from the given object"""
        return str(obj)

    @classmethod
    def extract_span(cls, obj: Dict) -> "Span":
        """Extract data form a dict"""
        return cls.span_from_dict(obj)

    @classmethod
    def inject_span(cls, span: Any, obj: Dict):
        """Append Span into a context"""
        obj.update(cls.span_serialize(span))

    @classmethod
    def extract(cls, obj: Any) -> SpanContext:
        """ Extract span context from the given object"""
        return opentracing.tracer.extract(cls.FORMAT, obj)

    @classmethod
    def inject(cls, span: SpanContext, obj: Any):
        """ Injects the span context into a `carrier` object."""
        opentracing.tracer.inject(span, cls.FORMAT, obj)

    @classmethod
    def extract_tags(cls, obj: Any) -> Dict:
        """ Extract tags from the given object"""
        return dict(
            [(attr, getattr(obj, attr, None)) for attr in cls.TAGS]
        )

    @classmethod
    def _inject_object(cls, span, obj, **kwargs):
        """ Trigger to execute just before closing the span

        :param jaeger_client.Span span: the SpanContext instance
        :param Any obj: Object to use as context
        :param dict kwargs: additional data
        """

    @classmethod
    def _postrun(cls, span, obj, **kwargs):
        """ Trigger to execute just before closing the span

        :param jaeger_client.Span span: the SpanContext instance
        :param Any obj: Object to use as context
        :param dict kwargs: additional data
        """

    def __init__(self, context, tracer, obj=None, operation_name=None,
                 tags=None, start_time=None):
        super(Span, self).__init__(
            context=context, tracer=tracer,
            operation_name=operation_name or self.name(obj),
            tags=tags, start_time=start_time
        )
        self.obj = obj
        self._inject_object(self, obj)

    def finish(self, finish_time=None):
        self._postrun(self, self.obj)
        jaeger_client.Span.finish(self, finish_time)


class Tracer(jaeger_client.Tracer):
    """Implement jaeger_client.Tracer"""

    def start_span(self, operation_name=None, child_of=None, references=None,
                   tags=None, start_time=None, span_factory=Span, obj=None):
        """
        Start and return a new Span representing a unit of work.

        :param operation_name: name of the operation represented by the new
            span from the perspective of the current service.
        :param child_of: shortcut for 'child_of' reference
        :param references: (optional) either a single Reference object or a
            list of Reference objects that identify one or more parent
            SpanContexts. (See the Reference documentation for detail)
        :param tags: optional dictionary of Span Tags. The caller gives up
            ownership of that dictionary, because the Tracer may use it as-is
            to avoid extra data copying.
        :param start_time: an explicit Span start time as a unix timestamp per
            time.time()
        :param ExtendedSpan span_factory: Alternate span factory
        :param Any obj: object to use as context

        :return: Returns an already-started Span instance.
        """
        tags = tags or dict()
        parent = child_of
        if parent is None:
            if obj:
                parent = span_factory.extract(obj)

        if references:
            if isinstance(references, list):
                # TODO only the first reference is currently used
                references = references[0]
            parent = references.referenced_context

        # allow Span to be passed as reference, not just SpanContext
        if issubclass(parent.__class__, Span):
            parent = parent.context

        rpc_server = tags and \
                     tags.get(
                         ext_tags.SPAN_KIND) == ext_tags.SPAN_KIND_RPC_SERVER

        if parent is None or parent.is_debug_id_container_only:
            trace_id = self.random_id()
            span_id = trace_id
            parent_id = None
            flags = 0
            baggage = None
            if parent is None:
                sampled, sampler_tags = \
                    self.sampler.is_sampled(trace_id, operation_name)
                if sampled:
                    flags = SAMPLED_FLAG
                    tags = tags or {}
                    for k, v in six.iteritems(sampler_tags):
                        tags[k] = v
            elif self.is_debug_allowed(operation_name):  # have debug id
                flags = SAMPLED_FLAG | DEBUG_FLAG
                tags = tags or {}
                tags[self.debug_id_header] = parent.debug_id
        else:
            trace_id = parent.trace_id
            if rpc_server and self.one_span_per_rpc:
                # Zipkin-style one-span-per-RPC
                span_id = parent.span_id
                parent_id = parent.parent_id
            else:
                span_id = self.random_id()
                parent_id = parent.span_id
            flags = parent.flags
            baggage = dict(parent.baggage)

        span_ctx = jaeger_client.SpanContext(trace_id=trace_id, span_id=span_id,
                                             parent_id=parent_id, flags=flags,
                                             baggage=baggage)

        if obj:
            tags.update(span_factory.extract_tags(obj))

        span = span_factory(
            context=span_ctx, tracer=self, operation_name=operation_name,
            tags=tags, start_time=start_time, obj=obj
        )
        self._emit_span_metrics(span=span, join=rpc_server)
        return span


class Config(jaeger_client.Config):
    def create_tracer(self, reporter, sampler, throttler=None):
        """ Create a new tracer

        :param jaeger_client.reporter.Reporter reporter: the reporter
        :param jaeger_client.sampler.Sampler sampler: the sampler
        :param jaeger_client.throttler.RemoteThrottler throttler: a remote throttler
        :return: a tracer
        :rtype cdumay_opentracing.Tracer
        """
        return Tracer(
            service_name=self.service_name,
            reporter=reporter,
            sampler=sampler,
            metrics_factory=self._metrics_factory,
            trace_id_header=self.trace_id_header,
            baggage_header_prefix=self.baggage_header_prefix,
            debug_id_header=self.debug_id_header,
            tags=self.tags,
            max_tag_value_length=self.max_tag_value_length,
            extra_codecs=self.propagation,
            throttler=throttler,
        )
