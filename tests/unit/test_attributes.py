# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
from uuid import UUID
from datetime import datetime
from repocket.attributes import Attribute
from repocket.attributes import AutoUUID
from repocket.attributes import Unicode
from repocket.attributes import Bytes
from repocket.attributes import JSON
from repocket.attributes import DateTime
from repocket.attributes import Pointer
from repocket.attributes import ByteStream

test_uuid = UUID('3112edba-4b5d-11e5-b02e-6c4008a70392')


def test_attribute_to_string():
    ('Attribute#to_string() should have cast the value as string')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call to_string
    result = attribute.to_string(100)

    # Then the result should be a string
    result.should.be.a(bytes)


def test_attribute_from_string():
    ('Attribute#from_string() should have cast the value as string')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call from_string
    result = attribute.from_string('100')

    # Then the result should be a string
    result.should.be.a(bytes)


def test_attribute_get_base_type():
    ('Attribute#get_base_type() should return the __base_type__')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call get_base_type
    result = attribute.get_base_type()

    # Then the result should be bytes
    result.should.equal(bytes)


def test_attribute_to_python():
    ('Attribute#to_python() should prepare data to be serialized')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call to_python
    result = attribute.to_python('the value')

    # Then the result should be a dictionary with metadata
    result.should.equal({
        'module': 'repocket.attributes',
        'type': 'Attribute',
        'value': 'the value',
    })


def test_attribute_from_python():
    ('Attribute.from_python() should deserialize the given dict into a value')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call from_python
    result = attribute.from_python({
        b'module': b'repocket.attributes',
        b'type': b'Attribute',
        b'value': b'foobar',
    })

    # Then the result should be a value
    result.should.equal(
        b'foobar'
    )


def test_attribute_from_json():
    ('Attribute.from_json() should deserialize the given dict into a value')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call from_json
    result = attribute.from_json(json.dumps({
        b'module': b'repocket.attributes',
        b'type': b'Attribute',
        b'value': b'foobar',
    }))

    # Then the result should be a value
    result.should.equal(
        b'foobar'
    )


def test_attribute_to_json():
    ('Attribute.to_json() should deserialize the given dict into a value')

    # Given an instance of attribute
    attribute = Attribute()

    # When I call to_json
    result = attribute.to_json('chucknorris')

    # Then the result should be a value
    result.should.equal(
        '{"type": "Attribute", "value": "chucknorris", "module": "repocket.attributes"}'
    )


def test_autouuid_to_string():
    ('AutoUUID#to_string() should have cast the value as string')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call to_string
    result = autouuid.to_string(str(test_uuid))

    # Then the result should be a string
    result.should.be.a(bytes)


def test_autouuid_from_string():
    ('AutoUUID#from_string() should have cast the value as string')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call from_string
    result = autouuid.from_string('3112edba-4b5d-11e5-b02e-6c4008a70392')

    # Then the result should be a UUID
    result.should.be.a(UUID)


def test_autouuid_get_base_type():
    ('AutoUUID#get_base_type() should return the __base_type__')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call get_base_type
    result = autouuid.get_base_type()

    # Then the result should be bytes
    result.should.equal(UUID)


def test_autouuid_to_python():
    ('AutoUUID#to_python() should prepare data to be serialized')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call to_python
    result = autouuid.to_python('3112edba-4b5d-11e5-b02e-6c4008a70392')

    # Then the result should be a dictionary with metadata
    result.should.equal({
        'module': 'repocket.attributes',
        'type': 'AutoUUID',
        'value': '3112edba-4b5d-11e5-b02e-6c4008a70392',
    })


def test_autouuid_from_python():
    ('AutoUUID.from_python() should deserialize the given dict into a value')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call from_python
    result = autouuid.from_python({
        b'module': b'repocket.attributes',
        b'type': b'AutoUUID',
        b'value': b'3112edba-4b5d-11e5-b02e-6c4008a70392',
    })

    # Then the result should be a value
    result.should.equal(
        test_uuid
    )


def test_autouuid_from_json():
    ('AutoUUID.from_json() should deserialize the given dict into a value')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call from_json
    result = autouuid.from_json(json.dumps({
        b'module': b'repocket.attributes',
        b'type': b'AutoUUID',
        b'value': b'3112edba-4b5d-11e5-b02e-6c4008a70392',
    }))

    # Then the result should be a value
    result.should.equal(test_uuid)


def test_autouuid_to_json():
    ('AutoUUID.to_json() should deserialize the given dict into a value')

    # Given an instance of autouuid
    autouuid = AutoUUID()

    # When I call to_json
    result = autouuid.to_json('3112edba-4b5d-11e5-b02e-6c4008a70392')

    # Then the result should be a value
    result.should.equal(
        '{"type": "AutoUUID", "value": "3112edba-4b5d-11e5-b02e-6c4008a70392", "module": "repocket.attributes"}'
    )


def test_unicode_to_string():
    ('Unicode#to_string() should have cast the value as string')

    # Given an instance of unicode
    instance = Unicode()

    # When I call to_string
    result = instance.to_string(str(test_uuid))

    # Then the result should be a string
    result.should.be.a(bytes)


def test_unicode_from_string():
    ('Unicode#from_string() should have cast the value as string')

    # Given an instance of unicode
    instance = Unicode()

    # When I call from_string
    result = instance.from_string('unsafestring')

    # Then the result should be a UUID
    result.should.be.an(unicode)


def test_unicode_get_base_type():
    ('Unicode#get_base_type() should return the __base_type__')

    # Given an instance of unicode
    instance = Unicode()

    # When I call get_base_type
    result = instance.get_base_type()

    # Then the result should be bytes
    result.should.equal(unicode)


def test_unicode_to_python():
    ('Unicode#to_python() should prepare data to be serialized')

    # Given an instance of unicode
    instance = Unicode()

    # When I call to_python
    result = instance.to_python(u'unsafestring')

    # Then the result should be a dictionary with metadata
    result.should.equal({
        'module': 'repocket.attributes',
        'type': 'Unicode',
        'value': 'unsafestring',
    })


def test_unicode_from_python():
    ('Unicode.from_python() should deserialize the given dict into a value')

    # Given an instance of unicode
    instance = Unicode()

    # When I call from_python
    result = instance.from_python({
        b'module': b'repocket.attributes',
        b'type': b'Unicode',
        b'value': u'unsafestring',
    })

    # Then the result should be a value
    result.should.equal('unsafestring')


def test_unicode_from_json():
    ('Unicode.from_json() should deserialize the given dict into a value')

    # Given an instance of unicode
    instance = Unicode()

    # When I call from_json
    result = instance.from_json(json.dumps({
        b'module': b'repocket.attributes',
        b'type': b'Unicode',
        b'value': b'unsafestring',
    }))

    # Then the result should be a value
    result.should.equal(u'unsafestring')


def test_unicode_to_json():
    ('Unicode.to_json() should deserialize the given dict into a value')

    # Given an instance of unicode
    instance = Unicode()

    # When I call to_json
    result = instance.to_json(u'unsafestring')

    # Then the result should be a value
    result.should.equal(
        '{"type": "Unicode", "value": "unsafestring", "module": "repocket.attributes"}'
    )


def test_datetime_to_string():
    ('DateTime#to_string() should have cast the value as string')

    # Given an instance of datetime
    instance = DateTime()

    # When I call to_string
    result = instance.to_string('2015-08-25 15:57:37-04:00')

    # Then the result should be a string
    result.should.be.a(bytes)


def test_datetime_from_string():
    ('DateTime#from_string() should have cast the value as string')

    # Given an instance of datetime
    instance = DateTime()

    # When I call from_string
    result = instance.from_string('2015-08-25 15:57:37-04:00')

    # Then the result should be a UUID
    result.should.be.an(datetime)


def test_datetime_get_base_type():
    ('DateTime#get_base_type() should return the __base_type__')

    # Given an instance of datetime
    instance = DateTime()

    # When I call get_base_type
    result = instance.get_base_type()

    # Then the result should be bytes
    result.should.equal(datetime)


def test_datetime_to_python():
    ('DateTime#to_python() should prepare data to be serialized')

    # Given an instance of datetime
    instance = DateTime()

    # When I call to_python
    result = instance.to_python('Tue Aug 25 15:57:37 EDT 2015')

    # Then the result should be a dictionary with metadata
    result.should.equal({
        'module': 'repocket.attributes',
        'type': 'DateTime',
        'value': '2015-08-25T15:57:37-04:00',
    })


def test_datetime_from_python():
    ('DateTime.from_python() should deserialize the given dict into a value')

    # Given an instance of datetime
    instance = DateTime()

    # When I call from_python
    result = instance.from_python({
        b'module': b'repocket.attributes',
        b'type': b'DateTime',
        b'value': u'Tue Aug 25 15:57:37 EDT 2015',
    })

    # Then the result should be a value
    result.should.be.a(datetime)
    result.replace(tzinfo=None).should.equal(datetime(2015, 8, 25, 15, 57, 37))


def test_datetime_from_json():
    ('DateTime.from_json() should deserialize the given dict into a value')

    # Given an instance of datetime
    instance = DateTime()

    # When I call from_json
    result = instance.from_json(json.dumps({
        b'module': b'repocket.attributes',
        b'type': b'DateTime',
        b'value': b'Tue Aug 25 15:57:37 EDT 2015',
    }))

    # Then the result should be a value
    result.should.be.a(datetime)
    result.replace(tzinfo=None).should.equal(datetime(2015, 8, 25, 15, 57, 37))


def test_datetime_to_json():
    ('DateTime.to_json() should deserialize the given dict into a value')

    # Given an instance of datetime
    instance = DateTime()

    # When I call to_json
    result = instance.to_json(u'Tue Aug 25 15:57:37 EDT 2015')

    # Then the result should be a value
    result.should.equal(
        '{"type": "DateTime", "value": "2015-08-25T15:57:37-04:00", "module": "repocket.attributes"}'
    )
