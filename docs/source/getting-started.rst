.. _getting-started:

Getting Started
===============

Repocket is an active record that let's you use redis as main data
store.

Redis is commonly seen as a ephemeral, cache-purposed in-memory database.

But the reality is that redis is a data structure server.

In the same way that python has the ``int``, ``float``, ``unicode``,
``list``, ``set`` and ``dict`` builtin types, redis has equivalent
datastructures, and some really cool functions to manipulate them in
an optimized way.

Repocket lets you declare your models in a Django-fashioned way.


.. highlight: python

::

    class Project(ActiveRecord):
        name = attributes.Unicode()
        git_uri = attributes.Bytes()


    class Build(ActiveRecord):
        id = attributes.AutoUUID()
        project = attributes.Pointer(Project)
        started_at = attributes.DateTime()
        ended_at = attributes.DateTime()
        stdout = attributes.ByteStream()
        stderr = attributes.ByteStream()
