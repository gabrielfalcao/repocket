import json
import uuid
import logging

from repocket import attributes
from repocket.connections import configure
from repocket.registry import ActiveRecordRegistry


logger = logging.getLogger("repocket.model")


class ActiveRecord(object):
    """base model class, this is how you declare your active record.

    ::

        class User(ActiveRecord):
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

    __metaclass__ = ActiveRecordRegistry

    def __init__(self, *args, **kw):
        for attribute, field in self.__fields__.items():
            default = field.get_empty_value()
            raw_value = kw.get(attribute, default)
            if raw_value:
                value = field.cast(raw_value)
            else:
                value = default

            self.set(attribute, value)

    def __repr__(self):
        attributes = ', '.join(['{0}={1}'.format(k, repr(v)) for k, v in self.to_dict(simple=True).items() if v])
        return '{0}({1})'.format(self.__compound_name__, attributes)

    def __getitem__(self, name):
        options = self.__fields__.keys()
        if name not in options:
            raise KeyError("{0} is not a valid field in {1}, options are {2}".format(name, self, options))

        return getattr(self, name)

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, self.__class__):
            raise TypeError('Cannot compare {0} with {1}'.format(self, other))

        return self.to_dict() == other.to_dict()

    @classmethod
    def create(cls, **kwargs):
        """Takes all the valid attributes of an active record, saves it
        immediately and returns the instance, ready for further manipulation.
        """
        item = cls(**kwargs)
        item.save()
        return item

    @classmethod
    def _static_key_prefix(cls):
        return b'repocket:{0}:{1}'.format(
            cls.__namespace__,
            cls.__name__,
        )

    def get_id(self):
        return getattr(self, self.__primary_key__, None)

    def _calculate_key_for_field(self, name):
        return b':'.join([
            self._calculate_hash_key(),
            'field',
            name,
        ])

    def _calculate_hash_key(self):
        return b':'.join([
            bytes(self._key_prefix),
            bytes(self._primary_key),
        ])

    def _set_primary_key(self, value=None):
        if self._get_primary_key():
            # already set, carry on
            return

        value = uuid.uuid1()
        self.set(self.__primary_key__, value)

    def _get_primary_key(self):
        return self.get(self.__primary_key__)

    @property
    def _key_prefix(self):
        """returns the key prefix for the given model class.
        this property is used for calculating a new redis key.

        It forms the keys based on the following pattern:

        ::

            repocket:python_module_contaning_your_model:YourActiveRecordClassName
        """

        return self._static_key_prefix()

    @property
    def _primary_key(self):
        """
        Repocket automatically assigns a UUID1 as the ``id`` of your model, after set, the id itself is used to compose the redis key.

        For example, let's say that your model has the uuid: ``c5bb91d4-45e6-11e5-b77b-6c4008a70392``
        and that your Person model is defined at ``yourapp.models.Person``
        the redis key will become:

        ::

            repocket:yourapp.models:Person:c5bb91d4-45e6-11e5-b77b-6c4008a70392
        """
        return self.get(self.__primary_key__)

    def append_to_bytestream(self, field_name, value):
        redis_key = self._calculate_key_for_field(field_name)
        conn = configure.get_connection()
        conn.append(redis_key, value)

        old_value = getattr(self, field_name) or ''
        new_value = bytes(old_value) + bytes(value)
        setattr(self, field_name, new_value)
        return redis_key

    def get(self, attribute, fallback=None):
        return getattr(self, attribute, fallback)

    def set(self, field_name, value):
        field = self.__fields__.get(field_name)
        if not field:
            tmpl = 'attempt to set unexisting field "{0}" in the model {1}.{2}'
            msg = tmpl.format(field_name, self.__class__.__module__, self.__class__.__name__)
            raise AttributeError(msg)

        if isinstance(field, attributes.ByteStream):
            old_value = getattr(self, field_name, bytes()) or bytes()
            value = bytes(old_value) + bytes(value)

        setattr(self, field_name, value)

    def to_dict(self, simple=False):
        data = {
            # the "hash" key contains the main attributes, but special
            # attributes like ByteStream get translated into other
            # redis data types, which also require special keys,
            # that's why the data is separated before serialized
            'hash': {},
            # the "strings" key contains all the attributes that are
            # of the type "string"
            'strings': {},
        }
        simple_version = {}
        for name, field in self.__fields__.items():
            value = getattr(self, name, field.get_empty_value())

            try:
                serialized_value = field.to_json(value)

            except Exception as e:
                logger.error('Failed to serialize field {0}.{1} of type {2} with value: {3} - {4}'.format(
                    self.__class__.__name__,
                    name,
                    type(value),
                    value,
                    e
                ))
                serialized_value = field.get_empty_value()

            if isinstance(field, attributes.ByteStream):
                if not simple:
                    data['strings'][name] = value
                else:
                    simple_version[name] = value

            elif isinstance(field, attributes.Pointer):
                if not simple:
                    data['hash'][name] = serialized_value
                else:
                    simple_version[name] = value and value.to_dict(simple=True) or value

            elif isinstance(field, (attributes.UUID, attributes.AutoUUID)):
                if not simple:
                    data['hash'][name] = serialized_value
                else:
                    simple_version[name] = str(value)

            else:
                if not simple:
                    data['hash'][name] = serialized_value
                else:
                    simple_version[name] = value

        if simple:
            return simple_version

        return data

    def save(self):
        """Persists the model in redis.
        Automatically generates a primary key value if one was not provided
        """
        self._set_primary_key()
        redis_hash_key = self._calculate_hash_key()

        conn = configure.get_connection()
        data = self.to_dict()
        pipeline = conn.pipeline()
        pipeline = pipeline.hmset(redis_hash_key, data['hash'])
        redis_keys = {
            'hash': redis_hash_key,
            'strings': {}
        }
        for name, value in data['strings'].items():
            redis_string_key = self._calculate_key_for_field(name)
            redis_keys['strings'][name] = redis_string_key
            pipeline = pipeline.set(redis_string_key, value)

        pipeline.execute()
        return redis_keys

    def delete(self):
        """Deletes all the redis keys used by this model"""
        keys = [self._calculate_hash_key()]
        keys.extend([self._calculate_key_for_field(k) for k in self.__string_fields__.keys()])

        conn = configure.get_connection()
        results = conn.delete(*keys)
        return results

    def matches(self, kw):
        """Takes a dictionary with keyword args and returns true if all the
        args match the model field values"""
        matched = False
        for k, v in kw.items():
            field = self.__fields__[k]
            comp = field.cast(v)

            if self.get(k) == comp:
                matched = True
            else:
                matched = False

        return matched
