Module ready_trader_go.pubsub
=============================

Classes
-------

`MmapPublisher(fileno: int, mm: mmap.mmap, protocol: asyncio.protocols.BaseProtocol)`
:   A publisher based on a memory mapped file.

    ### Ancestors (in MRO)

    * ready_trader_go.pubsub.Publisher
    * asyncio.transports.WriteTransport
    * asyncio.transports.BaseTransport

`MmapSubscriber(fileno: int, buffer: mmap.mmap, from_addr: Tuple[str, int], protocol: Optional[asyncio.protocols.DatagramProtocol] = None)`
:   A subscriber based on a memory mapped file.

    ### Ancestors (in MRO)

    * ready_trader_go.pubsub.Subscriber
    * asyncio.transports.DatagramTransport
    * asyncio.transports.BaseTransport

`Publisher(buffer: Union[mmap.mmap, memoryview], protocol: asyncio.protocols.BaseProtocol)`
:   Publisher side of a datagram transport based on shared memory.
    
    Transport is achieved through the use of memory mapped files or shared
    memory blocks. There must be an interval between writes to permit
    subscribers to read the data before it is overwritten.

    ### Ancestors (in MRO)

    * asyncio.transports.WriteTransport
    * asyncio.transports.BaseTransport

    ### Descendants

    * ready_trader_go.pubsub.MmapPublisher

    ### Methods

    `abort(self) ‑> None`
    :   Close the publisher immediately.

    `can_write_eof(self) ‑> bool`
    :   Return False. Publisher's don't support writing EOF.

    `close(self) ‑> None`
    :   Close the publisher.

    `write(self, data: Union[bytearray, bytes, memoryview]) ‑> None`
    :   Publish the provided data.

`PublisherFactory(typ: str, name: str)`
:   A factory class for Publisher instances.

    ### Instance variables

    `name`
    :   Return the name for this publisher factory.

    `typ`
    :   Return the type for this publisher factory.

    ### Methods

    `create(self, protocol: asyncio.protocols.BaseProtocol) ‑> ready_trader_go.pubsub.Publisher`
    :   Create a new Publisher instance.

`Subscriber(buffer: Union[mmap.mmap, memoryview], from_addr: Tuple[str, int], protocol: asyncio.protocols.DatagramProtocol)`
:   Subscriber side of a datagram transport based on shared memory.
    
    Transport is achieved through the use of memory mapped files or shared
    memory blocks. An interval between writes gives subscribers time to read
    the data before it is overwritten and the subscriber polls the shared
    memory in order to pick up changes as soon as possible.

    ### Ancestors (in MRO)

    * asyncio.transports.DatagramTransport
    * asyncio.transports.BaseTransport

    ### Descendants

    * ready_trader_go.pubsub.MmapSubscriber

    ### Methods

    `abort(self) ‑> None`
    :   Close the transport immediately.

    `close(self) ‑> None`
    :   Close the subscriber.

    `get_protocol(self) ‑> asyncio.protocols.DatagramProtocol`
    :   Return the current protocol.

    `is_closing(self)`
    :   Return True if the subscriber is closing or is closed.

    `sendto(self, data: Union[bytearray, bytes, memoryview], addr: Optional[Tuple[str, int]] = None) ‑> None`
    :   Send data to the transport.

`SubscriberFactory(typ: str, name: str)`
:   A factory class for Subscribers.

    ### Instance variables

    `name`
    :   Return the name for this subscriber factory.

    `typ`
    :   Return the type for this subscriber factory.

    ### Methods

    `create(self, protocol: Optional[asyncio.protocols.DatagramProtocol] = None) ‑> ready_trader_go.pubsub.Subscriber`
    :   Return a new Subscriber instance.