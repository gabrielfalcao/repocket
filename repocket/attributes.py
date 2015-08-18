# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from uuid import uuid1, UUID


class Attribute(object):
    """Repocket treats its models and attributes as fully serializable.
    Every attribute contains a ``to_python`` method that knows how to
    serialize the type safely.

    """
    __base_type__ = bytes

    def __init__(self, null=False):
        self.can_be_null = null

    def to_string(self, value):
        """Utility method that knows how to safely convert the value into a string"""
        return str(self.cast(value))

    def from_string(self, value):
        return self.cast(value)

    def cast(self, value):
        """Casts the attribute value as the defined __base_type__."""
        return self.__base_type__(value)

    def to_python(self, value):
        """
        Returns a json-safe, serialiazed version of the attribute
        """
        return {
            'type': '.'.join([
                __name__,
                self.__class__.__name__
            ]),
            'value': self.to_string(value)
        }

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


class Bytes(Attribute):
    """Handles raw byte strings
    ``__base_type__ = bytes``
    """
    __base_type__ = bytes


class JSON(Unicode):
    """This special attribute automatically stores python data as JSON
    string inside of redis. ANd automatically deserializes it when
    retrieving.
    ``__base_type__ = unicode``
    """
