# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect
from collections import OrderedDict
from repocket.attributes import Attribute, AutoUUID
from repocket.errors import RepocketActiveRecordDefinitionError
from repocket.manager import ActiveRecordManager
MODELS = OrderedDict()


class ActiveRecordRegistry(type):
    def __init__(ActiveRecordClass, name, bases, members):
        module_name = ActiveRecordClass.__module__
        model_name = ActiveRecordClass.__name__

        if model_name == 'ActiveRecord' and module_name == 'repocket.model':
            super(ActiveRecordRegistry, ActiveRecordClass).__init__(name, bases, members)
            return

        attrs = ActiveRecordClass.configure_fields(members)
        super(ActiveRecordRegistry, ActiveRecordClass).__init__(name, bases, attrs)
        ActiveRecordClass.objects = ActiveRecordManager(ActiveRecordClass)
        MODELS[name] = ActiveRecordClass

    def configure_fields(ActiveRecordClass, members):
        fields = OrderedDict()
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
                fields[attribute] = value

            elif isinstance(value, Attribute):
                fields[attribute] = value

            members.pop(attribute)
            delattr(ActiveRecordClass, attribute)

        if primary_key_attribute is None:
            primary_key_attribute = 'id'
            fields['id'] = AutoUUID()

        ActiveRecordClass.__fields__ = fields
        ActiveRecordClass.__primary_key__ = primary_key_attribute

        return members
