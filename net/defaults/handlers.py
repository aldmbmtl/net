# -*- coding: utf-8 -*-
"""
Default Connected Handlers
--------------------------

Prebuilt connected handlers for net. Do not modify.
"""
# package imports
import net

__all__ = [
    'info',
    'pass_through',
    'null',
    'subscription_handler',
    'connections'
]


# basic descriptor
@net.connect()
def info(*args, **kwargs):
    """
    Return information about the peer requested.

    .. code-block:: python

        friendly_information = net.info(peer='somepeer')

    :return: peer.friendly_id
    """
    return net.Peer().friendly_id


# basic connection descriptor
@net.connect()
def connections(*args, **kwargs):
    """
    Return the connections registered with the peer.

    .. code-block:: python

        friendly_information = net.connections(peer='somepeer')

    :return: peer.CONNECTIONS
    """
    connections = net.Peer().CONNECTIONS

    return 'Connections on {1}:\n\t{0}'.format(
        '\n\n\t'.join(
            [
                '{0}\n\t\t{1}'.format(key, connections[key]) for key in connections.keys()
            ]
        ),
        net.Peer().friendly_id
    )


# utilities
@net.connect()
def pass_through(*args, **kwargs):
    """
    Used for testing, takes your arguments and passes them back for type
    testing.

    .. code-block:: python

        variable = "Test this comes back the way I sent it."

        response = net.pass_through(variable, peer='somepeer')

    :return: *args, **kwargs
    """
    if len(args) == 1:
        return args[0]
    return args, kwargs


@net.connect()
def null(*args, **kwargs):
    """
    Return a null response flag

    :return: NULL Flag
    """
    return net.Peer().get_flag("NULL")


@net.connect()
def subscription_handler(event, peer, connection):
    """
    Will register the incoming peer and connection with the local peers
    subscription of the event passed. This is for internal use only.

    :param event: event id
    :param peer: foreign peer id
    :param connection: connection id
    """
    # handles strings with b'' wrapping them.
    try:
        peer = str(peer.split("'")[1]).encode('ascii')
        connection = str(connection.split("'")[1]).encode('ascii')
    except IndexError:
        pass

    net.Peer().register_subscriber(event, peer, connection)