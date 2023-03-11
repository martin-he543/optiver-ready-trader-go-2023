Module ready_trader_go.util
===========================

Functions
---------

    
`create_datagram_endpoint(loop: asyncio.events.AbstractEventLoop, protocol_factory: Callable[[], asyncio.protocols.DatagramProtocol], local_addr: Optional[Tuple[str, int]] = None, remote_addr: Optional[Tuple[str, int]] = None, *, family: int = 0, proto: int = 0, flags: int = 0, reuse_port: Optional[bool] = None, allow_broadcast: Optional[bool] = None, sock: Optional[socket.socket] = None, interface: Optional[str] = None) ‑> Tuple[asyncio.transports.BaseTransport, asyncio.protocols.BaseProtocol]`
:   Return a datagram endpoint.
    
    In the case that a multicast address is supplied, this function creates the
    socket manually.