=====
Usage
=====

How to use in your project:

.. code-block:: python

    import net


Basic usage of defining connected net function.

.. code-block:: python

    # application code
    @net.connect
    def multiply_values(peer, request, val1, val2):
        return val1 * val2

Running the function locally

.. code-block:: python

    >>> multiply_values(5, 10)
    50

Running the function remotely

.. code-block:: python

    >>> import net
    >>>
    >>> # get all net peers reachable on local host and the local area network.
    >>> for peer_id in net.get_peers():
    >>>     #
    >>>     print(multiply_values(5, 10, peer=peer_id))
    50
    ...