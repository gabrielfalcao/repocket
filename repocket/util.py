from six import string_types


def is_null(value):
    if value is None:
        return True

    if isinstance(value, string_types) and value.lower() in ['null', 'none']:
        return True

    return False
