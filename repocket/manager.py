import logging

from repocket.connections import configure
from repocket.attributes import Attribute

logger = logging.getLogger('repocket.manager')


class ModelManager(object):
    def __init__(self, model):
        self.model = model

    def get(self, id):
        prefix = self.model()._calculate_key_prefix()
        redis_key = ':'.join([prefix, str(id)])
        return self.get_item_from_redis_key(redis_key)

    def filter(self, **kw):
        all_results = self.all()
        results = [i for i in all_results if i.matches(kw)]
        return results

    def all(self, connection=None):
        """Lists all items in redis, returns instances of the adopted model.
        ::

            class BlogPost(Model):
                created_at = attributes.DateTime(auto_now=True)
                title = attributes.Unicode()
                text = attributes.Unicode()

           BlogPost.objects.all()

        """
        conn = connection or configure.get_connection()
        prefix = self.model()._calculate_key_prefix()
        search_pattern = ':'.join([prefix, '*'])
        keys = conn.keys(search_pattern)
        items = [self.get_item_from_redis_key(k) for k in keys]
        return items

    def get_raw_dict_from_redis(self, key, connection=None):
        conn = connection or configure.get_connection()
        try:
            return conn.hgetall(key)
        except Exception:
            logger.exception('Failed to retrieve key')

    def get_item_from_redis_key(self, key):
        raw = self.get_raw_dict_from_redis(key)
        if raw is None:
            return

        data = self.deserialize_raw_item(raw)
        return self.model(**data)

    def deserialize_raw_item(self, raw_item):
        data = {}
        for key, raw_value in raw_item.iteritems():
            value = Attribute.from_json(raw_value)
            data[key] = value

        return data
