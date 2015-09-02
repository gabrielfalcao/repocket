# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from repocket.attributes import Attribute, AutoUUID, ByteStream
from repocket.errors import RepocketActiveRecordDefinitionError
from repocket.manager import ActiveRecordManager
from repocket._cache import MODELS


class ActiveRecordRegistry(type):
    def __init__(ActiveRecordClass, name, bases, members):
        module_name = ActiveRecordClass.__module__
        compound_name = '.'.join([module_name, name])

        if name not in ('ActiveRecordRegistry', 'ActiveRecord'):
            ActiveRecordRegistry.configure_fields(ActiveRecordClass, members)
            ActiveRecordClass.objects = ActiveRecordManager(ActiveRecordClass)
            ActiveRecordClass.__namespace__ = str(module_name)
            ActiveRecordClass.__compound_name__ = compound_name
            MODELS[compound_name] = ActiveRecordClass

        super(ActiveRecordRegistry, ActiveRecordClass).__init__(name, bases, members)

    @staticmethod
    def configure_fields(ActiveRecordClass, members):
        hash_fields = OrderedDict()
        string_fields = OrderedDict()
        primary_key_attribute = None

        for attribute, value in members.items():
            if isinstance(value, AutoUUID):
                if primary_key_attribute is not None:
                    msg = '{0} already defined the primary key: {1}, but you also defined {2}'
                    raise RepocketActiveRecordDefinitionError(msg.format(
                        ActiveRecordClass,
                        primary_key_attribute,
                        attribute,
                    ))

                primary_key_attribute = attribute

            elif isinstance(value, ByteStream):
                field_name = str(attribute)
                string_fields[field_name] = value
                append_method_name = 'append_{0}'.format(attribute)
                setattr(ActiveRecordClass, append_method_name, lambda self, string_value: ActiveRecordClass.append_to_bytestream(self, field_name, string_value))

            if isinstance(value, Attribute):
                hash_fields[str(attribute)] = value
                members.pop(attribute, None)
                try:
                    delattr(ActiveRecordClass, attribute)
                except AttributeError:
                    pass

        if primary_key_attribute is None:
            primary_key_attribute = 'id'
            hash_fields['id'] = AutoUUID()

        ActiveRecordClass.__fields__ = hash_fields
        ActiveRecordClass.__string_fields__ = string_fields
        ActiveRecordClass.__primary_key__ = primary_key_attribute

        return members
