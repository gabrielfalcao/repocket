# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid
from pendulum import Pendulum
from datetime import datetime
from repocket.model import ActiveRecord
from repocket import attributes
from repocket.compat import binary_type

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
    body = attributes.ByteStream()


@clean_slate
def test_save_user(context):
    ('ActiveRecord.save() should store the the fields successfully in a hash')

    # Given that I instantiate a user
    obj1 = User(
        id='295decfd-deb5-11e5-88db-6c4008a70392',
        access_token=b'sometoken',
        email='foo@bar.com',
        github_metadata={
            'yay': 'this is json baby!'
        }
    )

    keys = obj1.save()
    key = keys['hash']

    result = context.connection.hgetall(key)
    result.should.be.a(dict)
    result.should.have.length_of(4)
    result.should.have.key(b'email').being.equal(
        b'{"module": "repocket.attributes", "type": "Unicode", "value": "foo@bar.com"}'
    )
    result.should.have.key(b'github_metadata').being.equal(
        b'{"module": "repocket.attributes", "type": "JSON", "value": "{\'yay\': \'this is json baby!\'}"}'
    )
    result.should.have.key(b'id').being.a(binary_type)
    obj1.to_dict(simple=True).should.equal({
        'access_token': b'sometoken',
        'email': 'foo@bar.com',
        'github_metadata': {
            'yay': 'this is json baby!'
        },
        'id': '295decfd-deb5-11e5-88db-6c4008a70392'
    })


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


@clean_slate
def test_bytestream(context):
    ('A model that contains a ByteStream should '
     'store the attribute value in a separate '
     'redis key that contains a string')

    post = BlogPost(
        body='the initial content\n'
    )

    keys = post.save()

    body_key = keys['strings']['body']
    body_key.should.equal('repocket:tests.functional.test_active_record:BlogPost:{0}:field:body'.format(post.id))
    context.connection.get(body_key).should.equal(
        b'the initial content\n'
    )
    post.body.should.equal(
        b'the initial content\n'
    )


@clean_slate
def test_bytestream_append(context):
    ('A model should provide a `field_append()` method where `field` is a ByteStream')

    post = BlogPost(
        body='the initial content\n'
    )
    post.save()
    post.should.have.property('append_body').being.a('types.MethodType')

    body_key = post.append_body("more content\n")

    body_key.should.equal('repocket:tests.functional.test_active_record:BlogPost:{0}:field:body'.format(post.id))
    context.connection.get(body_key).should.equal(
        b'the initial content\nmore content\n'
    )
    post.body.should.equal(
        b'the initial content\nmore content\n'
    )

    result = BlogPost.objects.get(id=post.id)
    result.should.be.a(BlogPost)
    result.body.should.equal(
        b'the initial content\nmore content\n'
    )


@clean_slate
def test_pointer_saves_reference(context):
    ('Saving a Pointer attribute should store a reference to the model')

    author = User(
        id='b9c9bf17-ef60-45bf-8217-4daabc6bc483',
        email='foo@bar.com',
    )
    author.save()
    post = BlogPost(
        body='the initial content\n',
        author=author
    )
    keys = post.save()

    key = keys['hash']
    result = context.connection.hgetall(key)

    result.should.have.key(b'author').being.equal(
        b'{"module": "repocket.attributes", "type": "Pointer", "value": "repocket:tests.functional.test_active_record:User:b9c9bf17-ef60-45bf-8217-4daabc6bc483"}'
    )

    post.author.should.equal(author)


@clean_slate
def test_comparing_two_models(context):
    ('Two models should be comparable from by their json output')

    author1 = User(
        id='b9c9bf17-ef60-45bf-8217-4daabc6bc483',
        email='foo@bar.com',
    )
    post1 = BlogPost(
        body='the initial content\n',
        author=author1,
        created_at=datetime(2015, 2, 25),
    )

    author2 = User(
        id='b9c9bf17-ef60-45bf-8217-4daabc6bc483',
        email='foo@bar.com',
    )
    post2 = BlogPost(
        body='the initial content\n',
        author=author2,
        created_at=datetime(2015, 2, 25),
    )

    author1.should.equal(author2)
    post1.should.equal(post2)


@clean_slate
def test_get_retrieving_reference(context):
    ('Retrieving an object through manager.get() should also retrieve the references')
    import os

    os.environ['DEBUG'] = 'true'
    author = User(
        id='b9c9bf17-ef60-45bf-8217-4daabc6bc483',
        email='foo@bar.com',
    )
    author.save()
    post = BlogPost(
        body='the initial content\n',
        author=author,
        created_at=Pendulum(2015, 2, 25),
    )

    post.save()
    post.author.should.equal(author)

    result = BlogPost.objects.get(id=post.id)
    result.should.equal(post)


@clean_slate
def test_create_user(context):
    ('ActiveRecord.create() should store the the fields successfully in a hash')

    # Given that I instantiate create a user
    result = User.create(
        access_token=b'sometoken',
        email='foo@bar.com',
        github_metadata={
            'yay': 'this is json baby!'
        }
    )

    result.should.be.a(User)

    found = User.objects.get(id=result.id)
    found.should.equal(result)


@clean_slate
def test_to_simple_dict(context):
    ('Model#to_dict(simple=True) will return a simple key-value dict with the model contents')

    author = User(
        id='b9c9bf17-ef60-45bf-8217-4daabc6bc483',
        email='foo@bar.com',
    )
    result = author.to_dict(simple=True)

    result.should.equal({
        'access_token': b'',
        'email': u'foo@bar.com',
        'github_metadata': u'',
        'id': u'b9c9bf17-ef60-45bf-8217-4daabc6bc483'
    })


@clean_slate
def test_delete_user(context):
    ('ActiveRecord.delete() should remove all the redis keys')

    # Given that I create a user
    usr1 = User.objects.create(
        access_token=b'sometoken',
        email='foo@bar.com',
        github_metadata={
            'yay': 'this is json baby!'
        }
    )

    User.objects.all().should_not.be.empty

    deleted_keys = usr1.delete()
    deleted_keys.should.equal(1)

    User.objects.all().should.be.empty
