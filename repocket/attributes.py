# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import importlib

from datetime import datetime
from uuid import uuid1, UUID


class Attribute(object):
    """Repocket treats its models and attributes as fully serializable.
    Every attribute contains a ``to_python`` method that knows how to
    serialize the type safely.

    """
    __base_type__ = bytes
    __empty_value__ = b''

    def __init__(self, null=False):
        self.can_be_null = null

    def to_string(self, value):
        """Utility method that knows how to safely convert the value into a string"""
        return str(self.cast(value))

    def from_string(self, value):
        return self.cast(value)

    @classmethod
    def get_base_type(cls, value):
        """Returns the __base_type__"""
        return cls.__base_type__

    def get_empty_value(cls):
        return cls.__empty_value__

    @classmethod
    def cast(cls, value):
        """Casts the attribute value as the defined __base_type__."""
        return cls.__base_type__(value)

    def to_python(self, value):
        """
        Returns a json-safe, serialiazed version of the attribute
        """
        return {
            'module': self.__class__.__module__,
            'type': self.__class__.__name__,
            'value': self.to_string(value)
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
        value = json.loads(raw_value)
        return cls.from_python(value)

    def to_json(self, value):
        return json.dumps(self.to_python(value))


class AutoUUID(Attribute):
    """Automatically assigns a uuid1 as the value.
    ``__base_type__ = uuid.UUID``
    """
    __base_type__ = UUID

    def generate(self):
        return uuid1()


class Unicode(Attribute):
    """Handles unicode-safe values
    ``__base_type__ = unicode``
    """
    __base_type__ = unicode
    __empty_value__ = u''


class Bytes(Attribute):
    """Handles raw byte strings
    ``__base_type__ = bytes``
    """
    __base_type__ = bytes
    __empty_value__ = b''


class JSON(Unicode):
    """This special attribute automatically stores python data as JSON
    string inside of redis. ANd automatically deserializes it when
    retrieving.
    ``__base_type__ = unicode``
    """


class DateTime(Attribute):
    """Repocket treats its models and attributes as fully serializable.
    Every attribute contains a ``to_python`` method that knows how to
    serialize the type safely.

    """
    __base_type__ = bytes
    __empty_value__ = datetime.utcnow


    def __init__(self, auto_now=False, null=False):
        super(DateTime, self).__init__(null=null)
        self.auto_now = False

    def generate(self):
        return datetime.utcnow().isoformat()


class Pointer(Attribute):
    """Think of it as a soft foreign key.

    This will automatically store the unique id of the target model
    and automatically retrieves it for you.
    """
    __base_type__ = None
    __empty_value__ = None

    def __init__(self, to_model, null=False):
        super(Pointer, self).__init__(null=null)
        self.__base_type__ = to_model


class ByteStream(Attribute):
    """Handles bytes that will be stored as a string in redis
    ``__base_type__ = bytes``
    """
    __base_type__ = bytes
    __empty_value__ = b''
