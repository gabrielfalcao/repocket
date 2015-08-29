.. _serialization:

Serialization Rules
===================

Repocket stores your data consistently with its original field
type. Under the hood repocket stores everything as json, in a way or
another.

Here you will the rules followed by repocket so that your data content
is pristine.


How it gets stored in redis
"""""""""""""""""""""""""""

Later in this documentation you will learn the rules that repocket
follows to generate redis keys, for now know that the ``.save()``
method returns a dictionary containing all the redis keys used to
store that one model instance's data.

Because we don't have any ``ByteStream`` fields in the ``User`` model
definition, all the data will be declared in a single *hash* in redis.
So lets check what its redis key looks like:

::

   >>> harrys_keys
   {
       "hash": "repocket:tests.functional.test_active_record:User:970773fa-4de1-11e5-86f4-6c4008a70392",
       "strings": {}
   }


The guts of the data
""""""""""""""""""""

Now you know that the redis key for the *hash* is
``repocket:tests.functional.test_active_record:User:970773fa-4de1-11e5-86f4-6c4008a70392``,
so now you can check what is in redis:

.. highlight:: bash

::

   $ redis-cli --raw HGETALL repocket:tests.functional.test_active_record:User:970773fa-4de1-11e5-86f4-6c4008a70392
    email
    {"type": "Bytes", "value": "harry@hogwards.uk", "module": "repocket.attributes"}
    name
    {"type": "Unicode", "value": "Harry Potter", "module": "repocket.attributes"}
    password
    {"type": "Bytes", "value": "somethingsecret", "module": "repocket.attributes"}
    id
    {"type": "AutoUUID", "value": "970773fa-4de1-11e5-86f4-6c4008a70392", "module": "repocket.attributes"}
    metadata
    {"type": "JSON", "value": "{'known_tricks': ['Protego', 'Expelliarmus', 'Wingardium Leviosa', 'Expecto Patronum']}", "module": "repocket.attributes"}


Awesome! You can see your data in redis, you can notice how repocket
stores the data in a json object with metadata that describes the
stored type. You can learn more in the :ref:`serialization` chapter


.. note:: the metadata field is an ``attributes.JSON()`` field, so it
          can store any builtin python type, and automatically
          serializes it. It's a great example of how flexible you can
          be with repocket.
