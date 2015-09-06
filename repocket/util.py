def is_null(value):
    if value is None:
        return True

    if isinstance(value, basestring) and value.lower() in ['null', 'none']:
        return True

    return False
