# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for implementations of L{IReactorUNIX}.
"""


from stat import S_IMODE
from os import stat, close, urandom, unlink, fstat
from tempfile import mktemp, mkstemp
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, socket
from pprint import pformat
from hashlib import md5
from struct import pack
from typing import Optional, Sequence, Type
from unittest import skipIf

try:
    from socket import AF_UNIX as _AF_UNIX
except ImportError:
    AF_UNIX = None
else:
    AF_UNIX = _AF_UNIX

from zope.interface import Interface, implementer

from twisted.internet import interfaces, base
from twisted.internet.address import UNIXAddress
from twisted.internet.defer import Deferred, fail, gatherResults
from twisted.internet.endpoints import UNIXServerEndpoint, UNIXClientEndpoint
from twisted.internet.error import (
    ConnectionClosed,
    FileDescriptorOverrun,
    CannotListenError,
)
from twisted.internet.interfaces import (
    IFileDescriptorReceiver,
    IReactorUNIX,
    IReactorSocket,
    IReactorFDSet,
)
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.protocol import ServerFactory, ClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet.test.connectionmixins import EndpointCreator
from twisted.internet.test.reactormixins import ReactorBuilder
from twisted.internet.test.test_core import ObjectModelIntegrationMixin
from twisted.internet.test.test_tcp import (
    StreamTransportTestsMixin,
    WriteSequenceTestsMixin,
    MyClientFactory,
    MyServerFactory,
)
from twisted.internet.test.connectionmixins import ConnectableProtocol
from twisted.internet.test.connectionmixins import ConnectionTestsMixin
from twisted.internet.test.connectionmixins import StreamClientTestsMixin
from twisted.internet.test.connectionmixins import runProtocolsWithReactor
from twisted.python.compat import nativeString
from twisted.python.failure import Failure
from twisted.python.log import addObserver, removeObserver, err
from twisted.python.runtime import platform
from twisted.python.reflect import requireModule
from twisted.python.filepath import _coerceToFilesystemEncoding

sendmsg = requireModule("twisted.python.sendmsg")
sendmsgSkipReason = ""
if requireModule("twisted.python.sendmsg") is not None:
    sendmsgSkipReason = (
        "sendmsg extension unavailable, " "extended UNIX features disabled"
    )


class UNIXFamilyMixin:
    """
    Test-helper defining mixin for things related to AF_UNIX sockets.
    """

    def _modeTest(self, methodName, path, factory):
        """
        Assert that the mode of the created unix socket is set to the mode
        specified to the reactor method.
        """
        mode = 0o600
        reactor = self.buildReactor()
        unixPort = getattr(reactor, methodName)(path, factory, mode=mode)
        unixPort.stopListening()
        self.assertEqual(S_IMODE(stat(path).st_mode), mode)


def _abstractPath(case):
    """
    Return a new, unique abstract namespace path to be listened on.
    """
    return md5(urandom(100)).hexdigest()


class UNIXCreator(EndpointCreator):
    """
    Create UNIX socket end points.
    """

    requiredInterfaces = (
        interfaces.IReactorUNIX,
    )  # type: Optional[Sequence[Type[Interface]]]

    def server(self, reactor):
        """
        Construct a UNIX server endpoint.
        """
        # self.mktemp() often returns a path which is too long to be used.
        path = mktemp(suffix=".sock", dir=".")
        return UNIXServerEndpoint(reactor, path)

    def client(self, reactor, serverAddress):
        """
        Construct a UNIX client endpoint.
        """
        return UNIXClientEndpoint(reactor, serverAddress.name)


class SendFileDescriptor(ConnectableProtocol):
    """
    L{SendFileDescriptorAndBytes} sends a file descriptor and optionally some
    normal bytes and then closes its connection.

    @ivar reason: The reason the connection was lost, after C{connectionLost}
        is called.
    """

    reason = None

    def __init__(self, fd, data):
        """
        @param fd: A C{int} giving a file descriptor to send over the
            connection.

        @param data: A C{str} giving data to send over the connection, or
            L{None} if no data is to be sent.
        """
        self.fd = fd
        self.data = data

    def connectionMade(self):
        """
        Send C{self.fd} and, if it is not L{None}, C{self.data}.  Then close the
        connection.
        """
        self.transport.sendFileDescriptor(self.fd)
        if self.data:
            self.transport.write(self.data)
        self.transport.loseConnection()

    def connectionLost(self, reason):
        ConnectableProtocol.connectionLost(self, reason)
        self.reason = reason


@implementer(IFileDescriptorReceiver)
class ReceiveFileDescriptor(ConnectableProtocol):
    """
    L{ReceiveFileDescriptor} provides an API for waiting for file descriptors to
    be received.

    @ivar reason: The reason the connection was lost, after C{connectionLost}
        is called.

    @ivar waiting: A L{Deferred} which fires with a file descriptor once one is
        received, or with a failure if the connection is lost with no descriptor
        arriving.
    """

    reason = None
    waiting = None

    def waitForDescriptor(self):
        """
        Return a L{Deferred} which will fire with the next file descriptor
        received, or with a failure if the connection is or has already been
        lost.
        """
        if self.reason is None:
            self.waiting = Deferred()
            return self.waiting
        else:
            return fail(self.reason)

    def fileDescriptorReceived(self, descriptor):
        """
        Fire the waiting Deferred, initialized by C{waitForDescriptor}, with the
        file descriptor just received.
        """
        self.waiting.callback(descriptor)
        self.waiting = None

    def dataReceived(self, data):
        """
        Fail the waiting Deferred, if it has not already been fired by
        C{fileDescriptorReceived}.  The bytes sent along with a file descriptor
        are guaranteed to be delivered to the protocol's C{dataReceived} method
        only after the file descriptor has been delivered to the protocol's
        C{fileDescriptorReceived}.
        """
        if self.waiting is not None:
            self.waiting.errback(
                Failure(
                    Exception("Received bytes ({!r}) before descriptor.".format(data))
                )
            )
            self.waiting = None

    def connectionLost(self, reason):
        """
        Fail the waiting Deferred, initialized by C{waitForDescriptor}, if there
        is one.
        """
        ConnectableProtocol.connectionLost(self, reason)
        if self.waiting is not None:
            self.waiting.errback(reason)
            self.waiting = None
        self.reason = reason


class UNIXTestsBuilder(UNIXFamilyMixin, ReactorBuilder, ConnectionTestsMixin):
    """
    Builder defining tests relating to L{IReactorUNIX}.
    """

    requiredInterfaces = (IReactorUNIX,)

    endpoints = UNIXCreator()

    def test_mode(self):
        """
        The UNIX socket created by L{IReactorUNIX.listenUNIX} is created with
        the mode specified.
        """
        self._modeTest("listenUNIX", self.mktemp(), ServerFactory())

    @skipIf(
        not platform.isLinux(),
        "Abstract namespace UNIX sockets only " "supported on Linux.",
    )
    def test_listenOnLinuxAbstractNamespace(self):
        """
        On Linux, a UNIX socket path may begin with C{'\0'} to indicate
        a socket in the abstract namespace.  L{IReactorUNIX.listenUNIX}
        accepts such a path.
        """
        # Don't listen on a path longer than the maximum allowed.
        path = _abstractPath(self)
        reactor = self.buildReactor()
        port = reactor.listenUNIX("\0" + path, ServerFactory())
        self.assertEqual(port.getHost(), UNIXAddress("\0" + path))

    def test_listenFailure(self):
        """
        L{IReactorUNIX.listenUNIX} raises L{CannotListenError} if the
        underlying port's createInternetSocket raises a socket error.
        """

        def raiseSocketError(self):
            raise OSError("FakeBasePort forced socket.error")

        self.patch(base.BasePort, "createInternetSocket", raiseSocketError)
        reactor = self.buildReactor()
        with self.assertRaises(CannotListenError):
            reactor.listenUNIX("not-used", ServerFactory())

    @skipIf(
        not platform.isLinux(),
        "Abstract namespace UNIX sockets only " "supported on Linux.",
    )
    def test_connectToLinuxAbstractNamespace(self):
        """
        L{IReactorUNIX.connectUNIX} also accepts a Linux abstract namespace
        path.
        """
        path = _abstractPath(self)
        reactor = self.buildReactor()
        connector = reactor.connectUNIX("\0" + path, ClientFactory())
        self.assertEqual(connector.getDestination(), UNIXAddress("\0" + path))

    def test_addresses(self):
        """
        A client's transport's C{getHost} and C{getPeer} return L{UNIXAddress}
        instances which have the filesystem path of the host and peer ends of
        the connection.
        """

        class SaveAddress(ConnectableProtocol):
            def makeConnection(self, transport):
                self.addresses = dict(
                    host=transport.getHost(), peer=transport.getPeer()
                )
                transport.loseConnection()

        server = SaveAddress()
        client = SaveAddress()

        runProtocolsWithReactor(self, server, client, self.endpoints)

        self.assertEqual(server.addresses["host"], client.addresses["peer"])
        self.assertEqual(server.addresses["peer"], client.addresses["host"])

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_sendFileDescriptor(self):
        """
        L{IUNIXTransport.sendFileDescriptor} accepts an integer file descriptor
        and sends a copy of it to the process reading from the connection.
        """
        from socket import fromfd

        s = socket()
        s.bind(("", 0))
        server = SendFileDescriptor(s.fileno(), b"junk")

        client = ReceiveFileDescriptor()
        d = client.waitForDescriptor()

        def checkDescriptor(descriptor):
            received = fromfd(descriptor, AF_INET, SOCK_STREAM)
            # Thanks for the free dup, fromfd()
            close(descriptor)

            # If the sockets have the same local address, they're probably the
            # same.
            self.assertEqual(s.getsockname(), received.getsockname())

            # But it would be cheating for them to be identified by the same
            # file descriptor.  The point was to get a copy, as we might get if
            # there were two processes involved here.
            self.assertNotEqual(s.fileno(), received.fileno())

        d.addCallback(checkDescriptor)
        d.addErrback(err, "Sending file descriptor encountered a problem")
        d.addBoth(lambda ignored: server.transport.loseConnection())

        runProtocolsWithReactor(self, server, client, self.endpoints)

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_sendFileDescriptorTriggersPauseProducing(self):
        """
        If a L{IUNIXTransport.sendFileDescriptor} call fills up
        the send buffer, any registered producer is paused.
        """

        class DoesNotRead(ConnectableProtocol):
            def connectionMade(self):
                self.transport.pauseProducing()

        class SendsManyFileDescriptors(ConnectableProtocol):
            paused = False

            def connectionMade(self):
                self.socket = socket()
                self.transport.registerProducer(self, True)

                def sender():
                    self.transport.sendFileDescriptor(self.socket.fileno())
                    self.transport.write(b"x")

                self.task = LoopingCall(sender)
                self.task.clock = self.transport.reactor
                self.task.start(0).addErrback(err, "Send loop failure")

            def stopProducing(self):
                self._disconnect()

            def resumeProducing(self):
                self._disconnect()

            def pauseProducing(self):
                self.paused = True
                self.transport.unregisterProducer()
                self._disconnect()

            def _disconnect(self):
                self.task.stop()
                self.transport.abortConnection()
                self.other.transport.abortConnection()

        server = SendsManyFileDescriptors()
        client = DoesNotRead()
        server.other = client
        runProtocolsWithReactor(self, server, client, self.endpoints)

        self.assertTrue(server.paused, "sendFileDescriptor producer was not paused")

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_fileDescriptorOverrun(self):
        """
        If L{IUNIXTransport.sendFileDescriptor} is used to queue a greater
        number of file descriptors than the number of bytes sent using
        L{ITransport.write}, the connection is closed and the protocol connected
        to the transport has its C{connectionLost} method called with a failure
        wrapping L{FileDescriptorOverrun}.
        """
        cargo = socket()
        server = SendFileDescriptor(cargo.fileno(), None)

        client = ReceiveFileDescriptor()
        result = []
        d = client.waitForDescriptor()
        d.addBoth(result.append)
        d.addBoth(lambda ignored: server.transport.loseConnection())

        runProtocolsWithReactor(self, server, client, self.endpoints)

        self.assertIsInstance(result[0], Failure)
        result[0].trap(ConnectionClosed)
        self.assertIsInstance(server.reason.value, FileDescriptorOverrun)

    def _sendmsgMixinFileDescriptorReceivedDriver(self, ancillaryPacker):
        """
        Drive _SendmsgMixin via sendmsg socket calls to check that
        L{IFileDescriptorReceiver.fileDescriptorReceived} is called once
        for each file descriptor received in the ancillary messages.

        @param ancillaryPacker: A callable that will be given a list of
            two file descriptors and should return a two-tuple where:
            The first item is an iterable of zero or more (cmsg_level,
            cmsg_type, cmsg_data) tuples in the same order as the given
            list for actual sending via sendmsg; the second item is an
            integer indicating the expected number of FDs to be received.
        """
        # Strategy:
        # - Create a UNIX socketpair.
        # - Associate one end to a FakeReceiver and FakeProtocol.
        # - Call sendmsg on the other end to send FDs as ancillary data.
        #   Ancillary data is obtained calling ancillaryPacker with
        #   the two FDs associated to two temp files (using the socket
        #   FDs for this fails the device/inode verification tests on
        #   macOS 10.10, so temp files are used instead).
        # - Call doRead in the FakeReceiver.
        # - Verify results on FakeProtocol.
        #   Using known device/inodes to verify correct order.

        # TODO: replace FakeReceiver test approach with one based in
        # IReactorSocket.adoptStreamConnection once AF_UNIX support is
        # implemented; see https://twistedmatrix.com/trac/ticket/5573.

        from socket import socketpair
        from twisted.internet.unix import _SendmsgMixin
        from twisted.python.sendmsg import sendmsg

        def deviceInodeTuple(fd):
            fs = fstat(fd)
            return (fs.st_dev, fs.st_ino)

        @implementer(IFileDescriptorReceiver)
        class FakeProtocol(ConnectableProtocol):
            def __init__(self):
                self.fds = []
                self.deviceInodesReceived = []

            def fileDescriptorReceived(self, fd):
                self.fds.append(fd)
                self.deviceInodesReceived.append(deviceInodeTuple(fd))
                close(fd)

        class FakeReceiver(_SendmsgMixin):
            bufferSize = 1024

            def __init__(self, skt, proto):
                self.socket = skt
                self.protocol = proto

            def _dataReceived(self, data):
                pass

            def getHost(self):
                pass

            def getPeer(self):
                pass

            def _getLogPrefix(self, o):
                pass

        sendSocket, recvSocket = socketpair(AF_UNIX, SOCK_STREAM)
        self.addCleanup(sendSocket.close)
        self.addCleanup(recvSocket.close)

        proto = FakeProtocol()
        receiver = FakeReceiver(recvSocket, proto)

        # Temp files give us two FDs to send/receive/verify.
        fileOneFD, fileOneName = mkstemp()
        fileTwoFD, fileTwoName = mkstemp()
        self.addCleanup(unlink, fileOneName)
        self.addCleanup(unlink, fileTwoName)

        dataToSend = b"some data needs to be sent"
        fdsToSend = [fileOneFD, fileTwoFD]
        ancillary, expectedCount = ancillaryPacker(fdsToSend)
        sendmsg(sendSocket, dataToSend, ancillary)

        receiver.doRead()

        # Verify that fileDescriptorReceived was called twice.
        self.assertEqual(len(proto.fds), expectedCount)

        # Verify that received FDs are different from the sent ones.
        self.assertFalse(set(fdsToSend).intersection(set(proto.fds)))

        # Verify that FDs were received in the same order, if any.
        if proto.fds:
            deviceInodesSent = [deviceInodeTuple(fd) for fd in fdsToSend]
            self.assertEqual(deviceInodesSent, proto.deviceInodesReceived)

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_multiFileDescriptorReceivedPerRecvmsgOneCMSG(self):
        """
        _SendmsgMixin handles multiple file descriptors per recvmsg, calling
        L{IFileDescriptorReceiver.fileDescriptorReceived} once per received
        file descriptor. Scenario: single CMSG with two FDs.
        """
        from twisted.python.sendmsg import SCM_RIGHTS

        def ancillaryPacker(fdsToSend):
            ancillary = [(SOL_SOCKET, SCM_RIGHTS, pack("ii", *fdsToSend))]
            expectedCount = 2
            return ancillary, expectedCount

        self._sendmsgMixinFileDescriptorReceivedDriver(ancillaryPacker)

    @skipIf(
        platform.isMacOSX(),
        "Multi control message ancillary sendmsg not supported on Mac.",
    )
    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_multiFileDescriptorReceivedPerRecvmsgTwoCMSGs(self):
        """
        _SendmsgMixin handles multiple file descriptors per recvmsg, calling
        L{IFileDescriptorReceiver.fileDescriptorReceived} once per received
        file descriptor. Scenario: two CMSGs with one FD each.
        """
        from twisted.python.sendmsg import SCM_RIGHTS

        def ancillaryPacker(fdsToSend):
            ancillary = [(SOL_SOCKET, SCM_RIGHTS, pack("i", fd)) for fd in fdsToSend]
            expectedCount = 2
            return ancillary, expectedCount

        self._sendmsgMixinFileDescriptorReceivedDriver(ancillaryPacker)

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_multiFileDescriptorReceivedPerRecvmsgBadCMSG(self):
        """
        _SendmsgMixin handles multiple file descriptors per recvmsg, calling
        L{IFileDescriptorReceiver.fileDescriptorReceived} once per received
        file descriptor. Scenario: unsupported CMSGs.
        """
        # Given that we can't just send random/invalid ancillary data via the
        # packer for it to be sent via sendmsg -- the kernel would not accept
        # it -- we'll temporarily replace recvmsg with a fake one that produces
        # a non-supported ancillary message level/type. This being said, from
        # the perspective of the ancillaryPacker, all that is required is to
        # let the test driver know that 0 file descriptors are expected.
        from twisted.python import sendmsg

        def ancillaryPacker(fdsToSend):
            ancillary = []
            expectedCount = 0
            return ancillary, expectedCount

        def fakeRecvmsgUnsupportedAncillary(skt, *args, **kwargs):
            data = b"some data"
            ancillary = [(None, None, b"")]
            flags = 0
            return sendmsg.ReceivedMessage(data, ancillary, flags)

        events = []
        addObserver(events.append)
        self.addCleanup(removeObserver, events.append)

        self.patch(sendmsg, "recvmsg", fakeRecvmsgUnsupportedAncillary)
        self._sendmsgMixinFileDescriptorReceivedDriver(ancillaryPacker)

        # Verify the expected message was logged.
        expectedMessage = "received unsupported ancillary data"
        found = any(expectedMessage in e["format"] for e in events)
        self.assertTrue(found, "Expected message not found in logged events")

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_avoidLeakingFileDescriptors(self):
        """
        If associated with a protocol which does not provide
        L{IFileDescriptorReceiver}, file descriptors received by the
        L{IUNIXTransport} implementation are closed and a warning is emitted.
        """
        # To verify this, establish a connection.  Send one end of the
        # connection over the IUNIXTransport implementation.  After the copy
        # should no longer exist, close the original.  If the opposite end of
        # the connection decides the connection is closed, the copy does not
        # exist.
        from socket import socketpair

        probeClient, probeServer = socketpair()

        events = []
        addObserver(events.append)
        self.addCleanup(removeObserver, events.append)

        class RecordEndpointAddresses(SendFileDescriptor):
            def connectionMade(self):
                self.hostAddress = self.transport.getHost()
                self.peerAddress = self.transport.getPeer()
                SendFileDescriptor.connectionMade(self)

        server = RecordEndpointAddresses(probeClient.fileno(), b"junk")
        client = ConnectableProtocol()

        runProtocolsWithReactor(self, server, client, self.endpoints)

        # Get rid of the original reference to the socket.
        probeClient.close()

        # A non-blocking recv will return "" if the connection is closed, as
        # desired.  If the connection has not been closed, because the
        # duplicate file descriptor is still open, it will fail with EAGAIN
        # instead.
        probeServer.setblocking(False)
        self.assertEqual(b"", probeServer.recv(1024))

        # This is a surprising circumstance, so it should be logged.
        format = (
            "%(protocolName)s (on %(hostAddress)r) does not "
            "provide IFileDescriptorReceiver; closing file "
            "descriptor received (from %(peerAddress)r)."
        )
        clsName = "ConnectableProtocol"

        # Reverse host and peer, since the log event is from the client
        # perspective.
        expectedEvent = dict(
            hostAddress=server.peerAddress,
            peerAddress=server.hostAddress,
            protocolName=clsName,
            format=format,
        )

        for logEvent in events:
            for k, v in expectedEvent.items():
                if v != logEvent.get(k):
                    break
            else:
                # No mismatches were found, stop looking at events
                break
        else:
            # No fully matching events were found, fail the test.
            self.fail(
                "Expected event (%s) not found in logged events (%s)"
                % (
                    expectedEvent,
                    pformat(
                        events,
                    ),
                )
            )

    @skipIf(not sendmsg, sendmsgSkipReason)
    def test_descriptorDeliveredBeforeBytes(self):
        """
        L{IUNIXTransport.sendFileDescriptor} sends file descriptors before
        L{ITransport.write} sends normal bytes.
        """

        @implementer(IFileDescriptorReceiver)
        class RecordEvents(ConnectableProtocol):
            def connectionMade(self):
                ConnectableProtocol.connectionMade(self)
                self.events = []

            def fileDescriptorReceived(innerSelf, descriptor):
                self.addCleanup(close, descriptor)
                innerSelf.events.append(type(descriptor))

            def dataReceived(self, data):
                self.events.extend(data)

        cargo = socket()
        server = SendFileDescriptor(cargo.fileno(), b"junk")
        client = RecordEvents()

        runProtocolsWithReactor(self, server, client, self.endpoints)

        self.assertEqual(int, client.events[0])
        self.assertEqual(b"junk", bytes(client.events[1:]))


class UNIXDatagramTestsBuilder(UNIXFamilyMixin, ReactorBuilder):
    """
    Builder defining tests relating to L{IReactorUNIXDatagram}.
    """

    requiredInterfaces = (interfaces.IReactorUNIXDatagram,)

    # There's no corresponding test_connectMode because the mode parameter to
    # connectUNIXDatagram has been completely ignored since that API was first
    # introduced.
    def test_listenMode(self):
        """
        The UNIX socket created by L{IReactorUNIXDatagram.listenUNIXDatagram}
        is created with the mode specified.
        """
        self._modeTest("listenUNIXDatagram", self.mktemp(), DatagramProtocol())

    @skipIf(
        not platform.isLinux(),
        "Abstract namespace UNIX sockets only " "supported on Linux.",
    )
    def test_listenOnLinuxAbstractNamespace(self):
        """
        On Linux, a UNIX socket path may begin with C{'\0'} to indicate a
        socket in the abstract namespace.  L{IReactorUNIX.listenUNIXDatagram}
        accepts such a path.
        """
        path = _abstractPath(self)
        reactor = self.buildReactor()
        port = reactor.listenUNIXDatagram("\0" + path, DatagramProtocol())
        self.assertEqual(port.getHost(), UNIXAddress("\0" + path))


class SocketUNIXMixin:
    """
    Mixin which uses L{IReactorSocket.adoptStreamPort} to hand out listening
    UNIX ports.
    """

    requiredInterfaces = (
        IReactorUNIX,
        IReactorSocket,
    )  # type: Optional[Sequence[Type[Interface]]]

    def getListeningPort(self, reactor, factory):
        """
        Get a UNIX port from a reactor, wrapping an already-initialized file
        descriptor.
        """
        portSock = socket(AF_UNIX)
        # self.mktemp() often returns a path which is too long to be used.
        path = mktemp(suffix=".sock", dir=".")
        portSock.bind(path)
        portSock.listen(3)
        portSock.setblocking(False)
        try:
            return reactor.adoptStreamPort(portSock.fileno(), portSock.family, factory)
        finally:
            portSock.close()

    def connectToListener(self, reactor, address, factory):
        """
        Connect to a listening UNIX socket.

        @param reactor: The reactor under test.
        @type reactor: L{IReactorUNIX}

        @param address: The listening's address.
        @type address: L{UNIXAddress}

        @param factory: The client factory.
        @type factory: L{ClientFactory}

        @return: The connector
        """
        return reactor.connectUNIX(address.name, factory)


class ListenUNIXMixin:
    """
    Mixin which uses L{IReactorTCP.listenUNIX} to hand out listening UNIX
    ports.
    """

    def getListeningPort(self, reactor, factory):
        """
        Get a UNIX port from a reactor
        """
        # self.mktemp() often returns a path which is too long to be used.
        path = mktemp(suffix=".sock", dir=".")
        return reactor.listenUNIX(path, factory)

    def connectToListener(self, reactor, address, factory):
        """
        Connect to a listening UNIX socket.

        @param reactor: The reactor under test.
        @type reactor: L{IReactorUNIX}

        @param address: The listening's address.
        @type address: L{UNIXAddress}

        @param factory: The client factory.
        @type factory: L{ClientFactory}

        @return: The connector
        """
        return reactor.connectUNIX(address.name, factory)


class UNIXPortTestsMixin:
    requiredInterfaces = (IReactorUNIX,)  # type: Optional[Sequence[Type[Interface]]]

    def getExpectedStartListeningLogMessage(self, port, factory):
        """
        Get the message expected to be logged when a UNIX port starts listening.
        """
        return "{} starting on {!r}".format(factory, nativeString(port.getHost().name))

    def getExpectedConnectionLostLogMsg(self, port):
        """
        Get the expected connection lost message for a UNIX port
        """
        return "(UNIX Port {} Closed)".format(nativeString(port.getHost().name))


class UNIXPortTestsBuilder(
    ListenUNIXMixin,
    UNIXPortTestsMixin,
    ReactorBuilder,
    ObjectModelIntegrationMixin,
    StreamTransportTestsMixin,
):
    """
    Tests for L{IReactorUNIX.listenUnix}
    """


class UNIXFDPortTestsBuilder(
    SocketUNIXMixin,
    UNIXPortTestsMixin,
    ReactorBuilder,
    ObjectModelIntegrationMixin,
    StreamTransportTestsMixin,
):
    """
    Tests for L{IReactorUNIX.adoptStreamPort}
    """


class UNIXAdoptStreamConnectionTestsBuilder(WriteSequenceTestsMixin, ReactorBuilder):
    requiredInterfaces = (
        IReactorFDSet,
        IReactorSocket,
        IReactorUNIX,
    )

    def test_buildProtocolReturnsNone(self):
        """
        {IReactorSocket.adoptStreamConnection} returns None if the given
        factory's buildProtocol returns None.
        """

        # Build reactor before anything else: allow self.buildReactor()
        # to skip the test if any of the self.requiredInterfaces isn't
        # provided by the reactor (example: Windows), preventing later
        # failures unrelated to the test itself.
        reactor = self.buildReactor()

        from socket import socketpair

        class NoneFactory(ServerFactory):
            def buildProtocol(self, address):
                return None

        s1, s2 = socketpair(AF_UNIX, SOCK_STREAM)
        s1.setblocking(False)
        self.addCleanup(s1.close)
        self.addCleanup(s2.close)

        s1FD = s1.fileno()
        factory = NoneFactory()
        result = reactor.adoptStreamConnection(s1FD, AF_UNIX, factory)
        self.assertIsNone(result)

    def test_ServerAddressUNIX(self):
        """
        Helper method to test UNIX server addresses.
        """

        def connected(protocols):
            client, server, port = protocols
            try:
                portPath = _coerceToFilesystemEncoding("", port.getHost().name)
                self.assertEqual(
                    "<AccumulatingProtocol #%s on %s>"
                    % (server.transport.sessionno, portPath),
                    str(server.transport),
                )

                self.assertEqual(
                    "AccumulatingProtocol,%s,%s"
                    % (server.transport.sessionno, portPath),
                    server.transport.logstr,
                )

                peerAddress = server.factory.peerAddresses[0]
                self.assertIsInstance(peerAddress, UNIXAddress)
            finally:
                # Be certain to drop the connection so the test completes.
                server.transport.loseConnection()

        reactor = self.buildReactor()
        d = self.getConnectedClientAndServer(
            reactor, interface=None, addressFamily=None
        )
        d.addCallback(connected)
        self.runReactor(reactor)

    def getConnectedClientAndServer(self, reactor, interface, addressFamily):
        """
        Return a L{Deferred} firing with a L{MyClientFactory} and
        L{MyServerFactory} connected pair, and the listening C{Port}. The
        particularity is that the server protocol has been obtained after doing
        a C{adoptStreamConnection} against the original server connection.
        """
        firstServer = MyServerFactory()
        firstServer.protocolConnectionMade = Deferred()

        server = MyServerFactory()
        server.protocolConnectionMade = Deferred()
        server.protocolConnectionLost = Deferred()

        client = MyClientFactory()
        client.protocolConnectionMade = Deferred()
        client.protocolConnectionLost = Deferred()

        # self.mktemp() often returns a path which is too long to be used.
        path = mktemp(suffix=".sock", dir=".")
        port = reactor.listenUNIX(path, firstServer)

        def firstServerConnected(proto):
            reactor.removeReader(proto.transport)
            reactor.removeWriter(proto.transport)
            reactor.adoptStreamConnection(proto.transport.fileno(), AF_UNIX, server)

        firstServer.protocolConnectionMade.addCallback(firstServerConnected)

        lostDeferred = gatherResults(
            [client.protocolConnectionLost, server.protocolConnectionLost]
        )

        def stop(result):
            if reactor.running:
                reactor.stop()
            return result

        lostDeferred.addBoth(stop)

        deferred = Deferred()
        deferred.addErrback(stop)

        startDeferred = gatherResults(
            [client.protocolConnectionMade, server.protocolConnectionMade]
        )

        def start(protocols):
            client, server = protocols
            deferred.callback((client, server, port))

        startDeferred.addCallback(start)

        reactor.connectUNIX(port.getHost().name, client)
        return deferred


globals().update(UNIXTestsBuilder.makeTestCaseClasses())
globals().update(UNIXDatagramTestsBuilder.makeTestCaseClasses())
globals().update(UNIXPortTestsBuilder.makeTestCaseClasses())
globals().update(UNIXFDPortTestsBuilder.makeTestCaseClasses())
globals().update(UNIXAdoptStreamConnectionTestsBuilder.makeTestCaseClasses())


class UnixClientTestsBuilder(ReactorBuilder, StreamClientTestsMixin):
    """
    Define tests for L{IReactorUNIX.connectUNIX}.
    """

    requiredInterfaces = (IReactorUNIX,)

    _path = None

    @property
    def path(self):
        """
        Return a path usable by C{connectUNIX} and C{listenUNIX}.

        @return: A path instance, built with C{_abstractPath}.
        """
        if self._path is None:
            self._path = _abstractPath(self)
        return self._path

    def listen(self, reactor, factory):
        """
        Start an UNIX server with the given C{factory}.

        @param reactor: The reactor to create the UNIX port in.

        @param factory: The server factory.

        @return: A UNIX port instance.
        """
        return reactor.listenUNIX(self.path, factory)

    def connect(self, reactor, factory):
        """
        Start an UNIX client with the given C{factory}.

        @param reactor: The reactor to create the connection in.

        @param factory: The client factory.

        @return: A UNIX connector instance.
        """
        return reactor.connectUNIX(self.path, factory)


globals().update(UnixClientTestsBuilder.makeTestCaseClasses())
