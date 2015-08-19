import redis


class configure(object):
    """global redis connection manager.
    this class is intended to be used as a singleton:

    * the ``connection_pool`` method will set a global connection pool with the given ``hostname``, ``port`` and ``db``
    * the ``get_connection`` can be used safely at any time after ``connection_pool`` was already set.
    """
    pool = None

    @classmethod
    def connection_pool(cls, hostname='localhost', port=6379, db=0):
        """sets the global redis connection pool.

        **arguments**

        * ``hostname`` - a string pointing to a valid hostname, defaults to ``localhost``
        * ``port`` - an integer with the port to connect to, defaults to ``6379``
        * ``db`` - a positive integer with the redis db to connect to, defaults to ``0``
        """
        cls.pool = redis.ConnectionPool(host=hostname, port=port, db=db)
        return cls

    @classmethod
    def get_connection(cls):
        """returns a connection from the pool.
        this method should **only** be called after you already called ``connection_pool``
        """
        return redis.Redis(connection_pool=cls.pool)
