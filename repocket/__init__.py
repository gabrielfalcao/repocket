# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
import redis

from repocket import attributes
from repocket.registry import ModelRegistry

__all__ = [
    'attributes',
    'configure',
    'Model',
]


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


class Model(object):
    """base model class, this is how you declare your active record.

    ::

        class User(Model):
            id = attributes.AutoUUID()
            github_access_token = attributes.Bytes()
            name = attributes.Unicode()
            email = attributes.Unicode()
            carpentry_token = attributes.Bytes()
            github_metadata = attributes.JSON()

        obj1 = User(
            github_access_token=b'sometoken',
            email='foo@bar.com',
            carpentry_token=b'1234',
            github_metadata={
                'yay': 'this is json baby!'
            }
        )

        key = obj1.save()
        connection = configure.get_connection()
        raw_results = connection.hgetall(key)
    """

    __metaclass__ = ModelRegistry
    def __init__(self, **kw):
        for attribute, value in kw.iteritems():
            self.set(attribute, value)

    def _calculate_key_prefix(self):
        return b'repocket:{0}:{1}'.format(
            self.__class__.__module__,
            self.__class__.__name__,
        )

    def _set_primary_key(self):
        if self.get(self.__primary_key__):
            # already set, carry on
            return

        value = str(uuid.uuid1())
        self.set(self.__primary_key__, value)

    @property
    def _key_prefix(self):
        """returns the key prefix for the given model class.
        this property is used for calculating a new redis key.

        It forms the keys based on the following pattern:

        ::

            repocket:python_module_contaning_your_model:YourModelClassName

        Repocket automatically assigns a UUID1 as the ``id`` of your model, after set, the id itself is used to compose the redis key.

        For example, let's say that your model has the uuid: ``c5bb91d4-45e6-11e5-b77b-6c4008a70392``
        and that your Person model is defined at ``yourapp.models.Person``
        the redis key will become:

        ::

            repocket:yourapp.models:Person:c5bb91d4-45e6-11e5-b77b-6c4008a70392

        """

        return self._calculate_key_prefix()

    @property
    def _primary_key(self):
        return self.get(self.__primary_key__)

    def get(self, attribute, fallback=None):
        return getattr(self, attribute, fallback)

    def set(self, attribute, value):
        if attribute not in self.__fields__:
            msg = 'attempt to set unexisting field {0} in the model {1}'
            raise AttributeError(msg.format(attribute, self))

        setattr(self, attribute, value)

    def to_dict(self):
        data = {}
        for name, field in self.__fields__.items():
            value = getattr(self, name, None)
            if not value:
                continue

            serialized_value = field.to_json(value)
            data[name] = serialized_value

        return data

    def save(self):
        self._set_primary_key()
        redis_hash_key = b':'.join([
            self._key_prefix,
            self._primary_key,
        ])
        conn = configure.get_connection()
        data = self.to_dict()
        conn.hmset(redis_hash_key, data)
        return redis_hash_key
