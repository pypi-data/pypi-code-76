# -*- test-case-name: twisted.test.test_strports -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Construct listening port services from a simple string description.

@see: L{twisted.internet.endpoints.serverFromString}
@see: L{twisted.internet.endpoints.clientFromString}
"""


from twisted.application.internet import StreamServerEndpointService
from twisted.internet import endpoints


def service(description, factory, reactor=None):
    """
    Return the service corresponding to a description.

    @param description: The description of the listening port, in the syntax
        described by L{twisted.internet.endpoints.serverFromString}.
    @type description: C{str}

    @param factory: The protocol factory which will build protocols for
        connections to this service.
    @type factory: L{twisted.internet.interfaces.IProtocolFactory}

    @rtype: C{twisted.application.service.IService}
    @return: the service corresponding to a description of a reliable stream
        server.

    @see: L{twisted.internet.endpoints.serverFromString}
    """
    if reactor is None:
        from twisted.internet import reactor

    svc = StreamServerEndpointService(
        endpoints.serverFromString(reactor, description), factory
    )
    svc._raiseSynchronously = True
    return svc


def listen(description, factory):
    """
    Listen on a port corresponding to a description.

    @param description: The description of the connecting port, in the syntax
        described by L{twisted.internet.endpoints.serverFromString}.
    @type description: L{str}

    @param factory: The protocol factory which will build protocols on
        connection.
    @type factory: L{twisted.internet.interfaces.IProtocolFactory}

    @rtype: L{twisted.internet.interfaces.IListeningPort}
    @return: the port corresponding to a description of a reliable virtual
        circuit server.

    @see: L{twisted.internet.endpoints.serverFromString}
    """
    from twisted.internet import reactor

    name, args, kw = endpoints._parseServer(description, factory)
    return getattr(reactor, "listen" + name)(*args, **kw)


__all__ = ["service", "listen"]
