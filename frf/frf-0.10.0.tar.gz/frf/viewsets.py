"""Declares various viewset implementations."""
from frf.views import APIView


class GenericViewSet(APIView):
    """A generic viewset implementation and base class for all viewsets. A
    :class:`GenericViewSet` represents a RESTful API resource for which
    operation may be defined. It has no endpoints by itself - the
    :class:`GenericViewSet` class must be subclassed in order to create a
    RESTFUL API resource.

    Endpoints are created by implementing any of the :meth:`create`,
    :meth:`list`, :meth:`retrieve`, :meth:`update` or :meth:`delete` methods
    on a subclass of :class:`frf.GenericViewSet`.
    """
    __module__ = 'frf'
