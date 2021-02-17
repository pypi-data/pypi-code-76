# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import logging
from .exception_handlers import (
    exception_cqrs_catch_all,
    exception_cqrs_conflict,
    exception_cqrs_forbidden,
    exception_cqrs_not_found,
    exception_cqrs_validation,
)
from .generic_loader import GenericEngine, log_record_factory
from .session_manager import SessionRetriever, session_manager_factory
from minty.cqrs import CQRS
from minty.infrastructure import InfrastructureFactory
from minty_pyramid.renderer import jsonapi
from pyramid.config import Configurator
from uuid import uuid4


class Engine(GenericEngine):
    """Pyramid configurator."""

    __slots__ = [
        "config",
        "domains",
        "command_wrapper_middleware",
        "query_middleware",
    ]

    def __init__(
        self,
        domains: list,
        command_wrapper_middleware: list = None,
        query_middleware: list = None,
    ):
        if command_wrapper_middleware is None:
            command_wrapper_middleware = []
        if query_middleware is None:
            query_middleware = []
        self.command_wrapper_middleware = command_wrapper_middleware
        self.query_middleware = query_middleware
        self.domains = domains
        self.config = None

    def setup(self, global_config: dict, **settings) -> object:
        """Set up the application by loading the injecting the CQRS layer.

        :param global_config: Global configuration
        :type global_config: dict
        :return: Returns the Configurator from Pyramid
        :rtype: object
        """
        infra_factory = InfrastructureFactory(
            settings["minty_service.infrastructure.config_file"]
        )
        config = Configurator(settings=settings)

        cqrs = CQRS(
            domains=self.domains,
            infrastructure_factory=infra_factory,
            command_wrapper_middleware=self.command_wrapper_middleware,
            query_middleware=self.query_middleware,
        )

        config.add_request_method(
            lambda r: uuid4(), name="request_id", property=True, reify=True
        )

        config.add_request_method(
            lambda r, n: cqrs.infrastructure_factory.get_infrastructure(
                context=r.host, infrastructure_name=n
            ),
            name="get_infrastructure",
            property=False,
        )

        config.add_request_method(
            lambda r, n: cqrs.infrastructure_factory_ro.get_infrastructure(
                context=r.host, infrastructure_name=n
            ),
            name="get_infrastructure_ro",
            property=False,
        )

        config.add_request_method(
            lambda r: infra_factory,
            name="infrastructure_factory",
            property=True,
            reify=True,
        )

        config.add_request_method(
            lambda r: r.infrastructure_factory.get_config(context=r.host),
            name="configuration",
            property=True,
            reify=True,
        )

        ### Add renderer
        config.add_renderer(None, jsonapi())

        config.include(_build_cqrs_setup(cqrs))
        if settings.get("session_manager", False):
            session_manager = session_manager_factory(
                infra_factory=infra_factory
            )
            config.include(
                _build_http_session_manager(
                    session_manager,
                    cookie_name=settings.get(
                        "session_cookie_name", "minty_session"
                    ),
                )
            )

        config.add_view(view=exception_cqrs_not_found, name="not_found")
        config.add_view(view=exception_cqrs_forbidden, name="forbidden")
        config.add_view(view=exception_cqrs_conflict, name="conflict")
        config.add_view(view=exception_cqrs_validation, name="validation")
        config.add_view(view=exception_cqrs_catch_all, name="catch_all")

        config.add_tween("minty_pyramid.generic_loader.RequestTimer")
        config.add_tween("minty_pyramid.generic_loader.RequestDataLogger")

        config.add_subscriber(
            "minty_pyramid.generic_loader.new_response_callback",
            "pyramid.events.NewResponse",
        )

        config.scan()
        self.config = config
        return config


def _build_cqrs_setup(cqrs):
    """Create a callable for setting up the "CQRS" methods request objects.

    :param cqrs: A configured CQRS object
    :type cqrs: CQRS
    :return: A function, callable by Pyramid, to register the CQRS
        method(s)
    :rtype: callable
    """

    def setup_cqrs_request(config):
        """Add the CQRS accessors to the Pyramid request objects.

        :param config: Pyramid configurator instance
        :type config: Configurator
        :return: Nothing
        :rtype: None
        """

        def get_query_instance(
            request, domain: str, user_uuid: str, user_info=None
        ):
            cqrs_instance = cqrs.get_query_instance(
                correlation_id=request.request_id,
                domain=domain,
                context=request.host,
                user_uuid=user_uuid,
            )
            # TODO pass user_info in parameters instead setting like so
            cqrs_instance.query_instance.user_info = user_info
            return cqrs_instance

        config.add_request_method(get_query_instance, "get_query_instance")

        def get_command_instance(
            request, domain: str, user_uuid: str, user_info=None
        ):
            cqrs_instance = cqrs.get_command_instance(
                correlation_id=request.request_id,
                domain=domain,
                context=request.host,
                user_uuid=user_uuid,
            )
            # TODO pass user_info in parameters instead setting like so
            cqrs_instance.command_instance.user_info = user_info
            return cqrs_instance

        config.add_request_method(get_command_instance, "get_command_instance")

    return setup_cqrs_request


def _build_http_session_manager(
    session_manager: SessionRetriever, cookie_name: str = "minty_cookie"
):
    """Create a callable to set up the `retrieve_session` method on request objects.

    :param session_manager: A configured SessionRetriever object
    :type session_manager: SessionRetriever
    :param cookie_name: Name of the cookie the session-id is stored in
    :type cookie_name: str
    :return: A function, callable by Pyramid, to register the session_manager
        method(s)
    :rtype: callable
    """

    def setup_session_request(config):
        """Add the SessionRetriver accessors to the Pyramid request objects.

        :param config: Pyramid configurator instance
        :type config: Configurator
        :return: Nothing
        :rtype: None
        """

        def session_id(request):
            try:
                return request.cookies[cookie_name]
            except KeyError:
                return "<session cookie not found>"

        config.add_request_method(
            session_id, "session_id", property=True, reify=True
        )

        def retrieve_session(request):
            session = session_manager.retrieve(request.cookies[cookie_name])
            return session

        config.add_request_method(retrieve_session, "retrieve_session")

    return setup_session_request


# Add a "req" key, containing the MDC to logging output in minty-pyramid
# applications.
old_factory = logging.getLogRecordFactory()
logging.setLogRecordFactory(log_record_factory)
