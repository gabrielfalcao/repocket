# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class RepocketActiveRecordDefinitionError(Exception):
    """Exception raised when a model has more than one AutoUUID or any
    other kind of inconsistency in the model declaration.
    """
