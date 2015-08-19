# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect
from collections import OrderedDict
from repocket.attributes import Attribute, AutoUUID
from repocket.errors import RepocketModelDefinitionError
from repocket.manager import ModelManager
MODELS = OrderedDict()


class ModelRegistry(type):
    def __init__(ModelClass, name, bases, members):
        module_name = ModelClass.__module__
        model_name = ModelClass.__name__

        if model_name == 'Model' and module_name == 'repocket.model':
            super(ModelRegistry, ModelClass).__init__(name, bases, members)
            return

        attrs = ModelClass.configure_fields(members)
        super(ModelRegistry, ModelClass).__init__(name, bases, attrs)
        ModelClass.objects = ModelManager(ModelClass)
        MODELS[name] = ModelClass

    def configure_fields(ModelClass, members):
        fields = OrderedDict()
        primary_key_attribute = None
        for attribute, value in members.items():
            if isinstance(value, AutoUUID):
                if primary_key_attribute is not None:
                    msg = '{0} already defined the primary key: {1}, but you also defined {2}'
                    raise RepocketModelDefinitionError(msg.format(
                        ModelClass,
                        primary_key_attribute,
                        attribute,
                    ))

                primary_key_attribute = attribute
                fields[attribute] = value

            elif isinstance(value, Attribute):
                fields[attribute] = value

            members.pop(attribute)
            delattr(ModelClass, attribute)

        if primary_key_attribute is None:
            primary_key_attribute = 'id'
            fields['id'] = AutoUUID()

        ModelClass.__fields__ = fields
        ModelClass.__primary_key__ = primary_key_attribute

        return members
