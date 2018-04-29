import codecs
import datetime
import collections
import json as pyjson

from copy import deepcopy
from decimal import Decimal
# from flask_restplus.utils import merge


class OrderedDict(collections.OrderedDict):
    """A drop-in replacement for :py:class:`collections.OrderedDict` with 2 extra features:

    - Hashable: can be used in a :py:class:`set`
    - A method for creating a safe deep copy
    - Can serialize :py:mod:`datetime` objects and :py:class:`decimal.Decimal`
    """
    def __hash__(self):
        return int(codecs.encode(json.dumps(self).encode('utf-8'), 'hex'), 16)

    def deepcopy(self):
        """
        :returns: a safe :py:func:`copy.deepcopy` of itself
        """
        return OrderedDict(deepcopy(list(self.items())))


def pre_serialize(o):
    if isinstance(o, bytes):
        return o.decode('utf-8')

    elif isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
        return o.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    elif isinstance(o, Decimal):
        return float(o)

    return json.encoder.default(o)


class json(object):
    """drop-in replacement for python module :py:mod:`json` with extra
    features:

    - can serialize:
      - :py:class:`bytes`
      - :py:class:`datetime.datetime`
      - :py:class:`datetime.date`
      - :py:class:`datetime.time`
    """
    encoder = pyjson.JSONEncoder()

    @classmethod
    def load(cls, *args, **kw):
        """.. seealso::  :py:meth:`json.load`"""
        return pyjson.load(*args, **kw)

    @classmethod
    def dump(cls, *args, **kw):
        """.. seealso::  :py:meth:`json.dump`"""
        kw['sort_keys'] = kw.pop('sort_keys', True)
        kw['default'] = pre_serialize
        return pyjson.dump(*args, **kw)

    @classmethod
    def dumps(cls, *args, **kw):
        """.. seealso::  :py:meth:`json.dumps`"""
        kw['default'] = pre_serialize
        kw['sort_keys'] = kw.pop('sort_keys', True)

        return pyjson.dumps(*args, **kw)

    @classmethod
    def loads(cls, *args, **kw):
        """.. seealso::  :py:meth:`json.loads`"""
        return pyjson.loads(*args, **kw)
