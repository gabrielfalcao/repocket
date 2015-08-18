# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from repocket import Model, attributes

from .helpers import clean_slate


class User(Model):
    id = attributes.AutoUUID()
    github_access_token = attributes.Bytes()
    name = attributes.Unicode()
    email = attributes.Unicode()
    carpentry_token = attributes.Bytes()
    github_metadata = attributes.JSON()


@clean_slate
def test_save_user(context):
    ('Model.save() should store the the fields successfully in a hash')

    # Given that I instantiate a user
    obj1 = User(
        github_access_token=b'sometoken',
        email='foo@bar.com',
        carpentry_token=b'1234',
        github_metadata={
            'yay': 'this is json baby!'
        }
    )

    key = obj1.save()

    result = context.connection.hgetall(key)
    result.should.be.a(dict)
    result.should.have.length_of(5)
    result.should.have.key('email').being.equal(
        '{"type": "repocket.attributes.Unicode", "value": "foo@bar.com"}')
    result.should.have.key('carpentry_token').being.equal(
        '{"type": "repocket.attributes.Bytes", "value": "1234"}')
    result.should.have.key('github_metadata').being.equal(
        '{"type": "repocket.attributes.JSON", "value": "{u\'yay\': u\'this is json baby!\'}"}')
    result.should.have.key('id').being.a(str)
