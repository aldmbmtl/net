API Reference
=============

Decorators
++++++++++

.. currentmodule:: net

.. autofunction:: connect

.. autofunction:: flag

Flags
+++++

.. autofunction:: null_response

.. autofunction:: invalid_connection

Connections
+++++++++++

.. autofunction:: info

.. autofunction:: pass_through

.. autofunction:: null

Peer
++++

.. autofunction:: Peer

.. autoclass:: net.peer._Peer
    :members: host, id, port, friendly_id, decode_id, generate_id, get_flag, encode, decode

    .. autoattribute:: net.peer._Peer.CONNECTIONS
    .. autoattribute:: net.peer._Peer.FLAGS
