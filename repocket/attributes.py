# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import importlib
import logging
import dateutil.parser

from uuid import UUID as PythonsUUID
from datetime import datetime

from decimal import Decimal as PythonsDecimal

from repocket._cache import MODELS
from repocket.util import is_null

logger = logging.getLogger("repocket.attributes")


def get_current_time(field):
    return datetime.utcnow()


class Attribute(object):
    """Repocket treats its models and attributes as fully serializable.
    Every attribute contains a ``to_python`` method that knows how to
    serialize the type safely.

    """
    __base_type__ = bytes
    __empty_value__ = b''

    def __init__(self, null=False, default=None, encoding='utf-8'):
        self.can_be_null = null
        self.default = default
        self.encoding = encoding

    def to_string(self, value):
        """Utility method that knows how to safely convert the value into a string"""
        converted = self.cast(value)
        if isinstance(converted, unicode):
            converted = converted.encode(self.encoding)

        return bytes(converted)

    def from_string(self, value):
        return self.cast(value)

    @classmethod
    def get_base_type(cls):
        """Returns the __base_type__"""
        return cls.__base_type__

    def get_empty_value(cls):
        if callable(cls.__empty_value__):
            return cls.__empty_value__()

        # otherwise...
        return cls.__empty_value__

    @classmethod
    def cast(cls, value):
        """Casts the attribute value as the defined __base_type__."""
        return cls.__base_type__(value)

    def to_python(self, value, simple=False):
        """
        Returns a json-safe, serialiazed version of the attribute
        """
        cls = type(self)

        if simple:
            return value

        safe_value = self.to_string(value)

        return {
            'module': cls.__module__,
            'type': cls.__name__,
            'value': safe_value
        }

    @classmethod
    def from_python(cls, data):
        type_name = data['type']
        module_name = data['module']
        raw_value = data['value']
        module = importlib.import_module(module_name)
        attribute = getattr(module, type_name)
        return attribute.cast(raw_value)

    @classmethod
    def from_json(cls, raw_value):
        try:
            value = json.loads(raw_value)
        except Exception:
            logger.error('Failed to deserialize value: {0}'.format(repr(raw_value)))
            return

        return cls.from_python(value)

    def to_json(self, value, simple=False):
        data = self.to_python(value, simple=simple)
        return json.dumps(data, default=bytes)


class UUID(Attribute):
    """Automatically assigns a uuid1 as the value.
    ``__base_type__ = uuid.UUID``
    """
    __base_type__ = PythonsUUID

    @classmethod
    def cast(cls, value):
        if isinstance(value, PythonsUUID):
            return value

        if is_null(value):
            return

        try:
            return cls.__base_type__(value)
        except ValueError as e:
            raise ValueError(": ".join([str(e), repr(value)]))


class AutoUUID(UUID):
    """Automatically assigns a uuid1 as the value.
    ``__base_type__ = uuid.UUID``
    """
    __base_type__ = PythonsUUID


class Unicode(Attribute):
    """Handles unicode-safe values
    ``__base_type__ = unicode``
    """
    __base_type__ = unicode
    __empty_value__ = u''

    def to_string(self, value):
        return super(Unicode, self).to_string(unicode(value))


class Bytes(Attribute):
    """Handles raw byte strings
    ``__base_type__ = bytes``
    """
    __base_type__ = bytes
    __empty_value__ = b''


class Integer(Attribute):
    """Handles int
    ``__base_type__ = int``
    """
    __base_type__ = int
    __empty_value__ = 0


class Float(Attribute):
    """Handles float
    ``__base_type__ = float``
    """
    __base_type__ = float
    __empty_value__ = 0.0


class Decimal(Attribute):
    """Handles Decimal
    ``__base_type__ = Decimal``
    """
    __base_type__ = PythonsDecimal
    __empty_value__ = PythonsDecimal('0')


class JSON(Unicode):
    """This special attribute automatically stores python data as JSON
    string inside of redis. ANd automatically deserializes it when
    retrieving.
    ``__base_type__ = unicode``
    """
    __base_type__ = json.dumps

    @classmethod
    def cast(cls, value):
        if not isinstance(value, basestring):
            return value

        try:
            return json.loads(value)
        except ValueError:
            return value


class DateTime(Attribute):
    """Repocket treats its models and attributes as fully serializable.
    Every attribute contains a ``to_python`` method that knows how to
    serialize the type safely.

    """
    __base_type__ = datetime
    __empty_value__ = None

    def __init__(self, auto_now=False, null=False):
        super(DateTime, self).__init__(null=null)
        self.auto_now = False

    @classmethod
    def cast(cls, value):
        if is_null(value):
            return

        if isinstance(value, datetime):
            return value

        return dateutil.parser.parse(value)

    def to_string(self, value):
        if not value:
            return json.dumps(None)

        return self.cast(value).isoformat()


class Pointer(Attribute):
    """Think of it as a soft foreign key.

    This will automatically store the unique id of the target model
    and automatically retrieves it for you.
    """
    __base_type__ = None
    __empty_value__ = None

    def __init__(self, to_model, null=False):
        self.model = to_model
        super(Pointer, self).__init__(null=null)

    def to_string(self, value):
        if not value:
            return json.dumps(None)

        if not value.get_id():
            raise ReferenceError('The model {0} must be saved before serialized as a pointer in another model'.format(value))

        return value._calculate_hash_key()

    @classmethod
    def cast(cls, value):
        """this method uses a redis connection to retrieve the referenced item"""
        if is_null(value):
            return

        if type(value) in MODELS.values():
            # the value is already a valid model instance
            return value

        try:
            _, module_name, model_name, model_uuid = value.split(':')
        except ValueError:
            raise ValueError('the given value is not a valid repocket reference: {0}'.format(value))

        compound_name = '.'.join([module_name, model_name])
        Model = MODELS.get(compound_name, None)
        if not Model:
            raise ReferenceError('The model {0} is not available in repocket. Make sure that you imported it'.format(compound_name))

        result = Model.objects.get(**{Model.__primary_key__: model_uuid})
        return result


class ByteStream(Attribute):
    """Handles bytes that will be stored as a string in redis
    ``__base_type__ = bytes``
    """
    __base_type__ = bytes
    __empty_value__ = b''
