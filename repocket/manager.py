# -*- coding: utf-8 -*-

import logging

from repocket.connections import configure
from repocket.attributes import Attribute

logger = logging.getLogger('repocket.manager')


class ActiveRecordManager(object):
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        return self.model.create(**kwargs)

    def get(self, id):
        instance = self.model()
        instance.set(instance.__primary_key__, id)

        prefix = instance._static_key_prefix()
        redis_key = ':'.join([prefix, str(id)])
        return self.get_item_from_redis_key(redis_key)

    def filter(self, **kw):
        all_results = self.all()
        results = [i for i in all_results if i is not None and i.matches(kw)]
        return results

    def all(self, connection=None):
        """Lists all items in redis, returns instances of the adopted model.
        ::

            class BlogPost(ActiveRecord):
                created_at = attributes.DateTime(auto_now=True)
                title = attributes.Unicode()
                text = attributes.Unicode()

           BlogPost.objects.all()

        """
        conn = connection or configure.get_connection()
        prefix = self.model._static_key_prefix()
        search_pattern = ':'.join([prefix, '*'])

        keys = conn.keys(search_pattern)
        items = [self.get_item_from_redis_key(k) for k in filter(lambda x: ':field:' not in x, keys)]
        return items

    def get_raw_dict_from_redis(self, key, connection=None):
        conn = connection or configure.get_connection()
        try:
            return conn.hgetall(key)
        except Exception as e:
            logger.warning('Failed to retrieve key {0}: {1}'.format(key, e))

    def get_item_from_redis_key(self, key, connection=None):
        conn = connection or configure.get_connection()
        raw = self.get_raw_dict_from_redis(key)
        if not raw:
            return

        data = self.deserialize_raw_item(raw)
        instance = self.model(**data)
        for field_name, field in self.model.__string_fields__.items():
            string_key = instance._calculate_key_for_field(field_name)
            value = conn.get(string_key)
            instance.set(field_name, value)

        return instance

    def deserialize_raw_item(self, raw_item):
        data = {}
        for key, raw_value in raw_item.iteritems():
            try:
                value = Attribute.from_json(raw_value)
            except TypeError as e:
                logger.error('Failed to deserialize field {0}.{1} because: {2}'.format(
                    self.model.__class__.__name__,
                    key,
                    str(e)
                ))
                raise

            data[key] = value

        return data
