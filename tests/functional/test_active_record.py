# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid
from repocket.model import ActiveRecord
from repocket import attributes

from .helpers import clean_slate


class User(ActiveRecord):
    id = attributes.AutoUUID()
    access_token = attributes.Bytes()
    email = attributes.Unicode()
    github_metadata = attributes.JSON()


class BlogPost(ActiveRecord):
    id = attributes.AutoUUID()
    author = attributes.Pointer(User)
    created_at = attributes.DateTime(auto_now=True)
    title = attributes.Unicode()
    body = attributes.Unicode()


@clean_slate
def test_save_user(context):
    ('ActiveRecord.save() should store the the fields successfully in a hash')

    # Given that I instantiate a user
    obj1 = User(
        access_token=b'sometoken',
        email='foo@bar.com',
        github_metadata={
            'yay': 'this is json baby!'
        }
    )

    key = obj1.save()

    result = context.connection.hgetall(key)
    result.should.be.a(dict)
    result.should.have.length_of(4)
    result.should.have.key('email').being.equal(
        '{"type": "Unicode", "value": "foo@bar.com", "module": "repocket.attributes"}')
    result.should.have.key('github_metadata').being.equal(
        '{"type": "JSON", "value": "{u\'yay\': u\'this is json baby!\'}", "module": "repocket.attributes"}')
    result.should.have.key('id').being.a(str)


@clean_slate
def test_object_manager_all(context):
    ('ActiveRecord.objects.all() should return all the saved items of the same kind')

    # Given 3 users
    User(email='1@test.com').save()
    User(email='2@test.com').save()
    User(email='3@test.com').save()

    # When I call objects.all()
    results = User.objects.all()

    # Then it should have 3 items
    results.should.have.length_of(3)

    # And the items should be models
    u1, u2, u3 = list(sorted(results, key=lambda item: item.email))
    u1.should.be.a(User)
    u2.should.be.a(User)
    u3.should.be.a(User)

    # And the data should be deserialized
    u1.email.should.equal('1@test.com')
    u2.email.should.equal('2@test.com')
    u3.email.should.equal('3@test.com')


@clean_slate
def test_object_manager_filter(context):
    ('ActiveRecord.objects.filter() should return a list of filtered items')

    # Given 3 users
    User(email='one@test.com').save()
    User(email='one@test.com').save()
    User(email='two@test.com').save()

    # When I call objects.all()
    results = User.objects.filter(email='one@test.com')

    # Then it should have 2 items
    results.should.have.length_of(2)

    # And the items should be models
    u1, u2 = results
    u1.should.be.a(User)
    u2.should.be.a(User)

    # And the data should be deserialized
    u1.email.should.contain('one@test.com')
    u2.email.should.equal('one@test.com')


@clean_slate
def test_object_manager_get(context):
    ('ActiveRecord.objects.get() should return an item')

    # Given a user
    user1_uuid = uuid.uuid1()
    u1 = User(
        id=str(user1_uuid),
        email='one@test.com'
    )
    u1.save()

    # When I call objects.get()
    result = User.objects.get(id=user1_uuid)

    # Then it should return a user
    result.should.be.a(User)
