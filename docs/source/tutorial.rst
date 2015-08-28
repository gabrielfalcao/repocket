.. _tutorial:

Tutorial
========

Here you will learn how to become fluent inrepocket in just a couple
of minutes.


Installing
^^^^^^^^^^

.. highlight:: bash

::

   pip install repocket


Configuring the connection
^^^^^^^^^^^^^^^^^^^^^^^^^^

Repocket uses a global connection pool where all the connections will
be shared when possible.

In your application code you will have to configure how repocket
connects, but you will do it only once, to show you how, imagine that
this is your own application code:


.. highlight:: python

::

   from repocket.connections import configure


   configure.connection_pool(hostname='myredis.cooldomain.com', port=6379, db=0)
   # at this point you're ready to use your declared models



Declaring Models
^^^^^^^^^^^^^^^^

Repocket provides a model interface that looks just like Django, but
the field types are super simplified.

Here is how you declare a model:


::

   from repocket import attributes
   from repocket import ActiveRecord


   class User(ActiveRecord):
       name = attributes.Unicode()
       email = attributes.Bytes()
       password = attributes.Bytes()


If you were in Django you would then need to run ``syncdb`` to have a
SQL table called ``User`` with the declared fields. But *this ain't
Django, ight?*

At this point you are ready to start saving user data in redis.

By default the attributes of the your model are actively saved in a
``hash`` redis datastructure.

Repocket *currenty* also supports another attribute called
``ByteStream`` that will seamlessly store the value in a string, so
that you can ``APPEND`` more bytes to it with a single call.
