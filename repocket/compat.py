# -*- coding: utf-8 -*-
from six import string_types
from six import binary_type
from six import text_type

basestring = string_types
bytes = binary_type
unicode = text_type


def safe_repr(s):
    if isinstance(s, binary_type):
        s = s.decode('utf-8')

    return repr(s)


def cast_bytes(s, encoding='utf-8'):
    if isinstance(s, binary_type):
        return s
    elif isinstance(s, text_type):
        return s.encode(encoding)

    return cast_bytes(text_type(s))


def cast_string(s, encoding='utf-8'):
    if isinstance(s, text_type):
        return s
    elif isinstance(s, binary_type):
        return s.decode(encoding)

    return text_type(s)
