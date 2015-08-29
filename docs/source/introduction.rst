.. _introduction:

Introduction
============

Repocket is an active record that let's you use redis as main data
store.

Redis is commonly seen as a ephemeral, cache-purposed in-memory database.

But the reality is that redis is a data structure server.

In the same way that python has the ``int``, ``float``, ``unicode``,
``list``, ``set`` and ``dict`` builtin types, redis has equivalent
datastructures, and some really cool functions to manipulate them in
an optimized way.

Repocket lets you declare your models in a Django-fashioned way,
automatically validate your fields, store in redis and retrieve them
in a very elegant way.

Also Repocket is ready for application needs like "foreign key".

Nobody likes foreign keys, relational databases get slow and complex
because of relationships and constraints. In fact, the reason that all
the logic of validation, contraints and consistency checks was built
in SQL databases is that back in the day we didn't have great
application frameworks and thousands of open source tools to help us
write great, reliable software.

But that changed, now you can use database servers just to store your
data, and all the consistency checks and validations can live in your
application code.

Repocket supports *"pointers"* which are references from one active
record to another, also it will automatically retrieve the
directly-related objects for you when you retrieve data from redis.


Here is a full example with all the supported field types of repocket:

.. highlight: python

::

    from repocket import attributes
    from repocket import ActiveRecord

     class Project(ActiveRecord):
         name = attributes.Unicode()
         git_uri = attributes.Bytes()
         metadata = attributes.JSON()

     class Build(ActiveRecord):
         id = attributes.AutoUUID()
         project = attributes.Pointer(Project)
         started_at = attributes.DateTime()
         ended_at = attributes.DateTime()
         stdout = attributes.ByteStream()
         stderr = attributes.ByteStream()
