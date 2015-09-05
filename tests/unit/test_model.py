# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from repocket.model import ActiveRecord
from repocket.attributes import ByteStream


class UnitModelOne(ActiveRecord):
    contents = ByteStream()


def test_active_record_calculate_key_prefix():
    ('ActiveRecord#_calculate_key_prefix should return a prefix based on the module name')

    item = UnitModelOne(id='059f3270-9e73-4d53-9970-443f83e412a0')
    result = item._calculate_key_prefix()
    result.should.equal('repocket:tests.unit.test_model:UnitModelOne:059f3270-9e73-4d53-9970-443f83e412a0')


def test_active_record_calculate_key_for_field():
    ('ActiveRecord#_calculate_key_for_field should return a prefix based on the module name')

    item = UnitModelOne(id='059f3270-9e73-4d53-9970-443f83e412a0')
    result = item._calculate_key_for_field('contents')
    result.should.equal('repocket:tests.unit.test_model:UnitModelOne:059f3270-9e73-4d53-9970-443f83e412a0:field:contents')

    repr(item).should.equal(b'tests.unit.test_model.UnitModelOne(hash={u\'id\': \'{"type": "AutoUUID", "value": "059f3270-9e73-4d53-9970-443f83e412a0", "module": "repocket.attributes"}\'}, strings={\'contents\': \'\'})')


def test_equality_ok():
    ('ActiveRecord should be comparable')

    item1 = UnitModelOne(id='059f3270-9e73-4d53-9970-443f83e412a0', contents=b'123')
    item2 = UnitModelOne(id='059f3270-9e73-4d53-9970-443f83e412a0', contents=b'123')

    item1.should.equal(item2)


def test_equality_failed():
    ('ActiveRecord should raise TypeError when failed to compare')

    item = UnitModelOne(id='059f3270-9e73-4d53-9970-443f83e412a0', contents=b'123')

    (lambda: item == 'foobar').when.called.should.have.raised(
        TypeError,
        'Cannot compare tests.unit.test_model.UnitModelOne'
        '(hash={u\'id\': \'{"type": "AutoUUID", "value": '
        '"059f3270-9e73-4d53-9970-443f83e412a0", "module":'
        ' "repocket.attributes"}\'}, '
        'strings={\'contents\': \'123\'})'
    )


def test_getitem():
    ('ActiveRecord should behave like a dict by letting you retrieve values using [] notation')

    item1 = UnitModelOne(id='059f3270-9e73-4d53-9970-443f83e412a0', contents=b'123')
    item1['id'].should.equal('059f3270-9e73-4d53-9970-443f83e412a0')
    item1['contents'].should.equal('123')
