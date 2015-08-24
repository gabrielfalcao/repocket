# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from repocket.model import ActiveRecord
from repocket.attributes import ByteStream


class UnitModelOne(ActiveRecord):
    contents = ByteStream()


def test_active_record_calculate_key_prefix():
    ('ActiveRecord#_calculate_key_prefix should return a prefix based on the module name')

    item = UnitModelOne()
    result = item._calculate_key_prefix()
    result.should.equal('repocket:repocket.model:UnitModelOne')


def test_active_record_calculate_key_for_field():
    ('ActiveRecord#_calculate_key_for_field should return a prefix based on the module name')

    item = UnitModelOne(id='123456')
    result = item._calculate_key_for_field('contents')
    result.should.equal('repocket:repocket.model:UnitModelOne:123456:field:contents')
