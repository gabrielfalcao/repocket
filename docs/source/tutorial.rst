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

   >>> from repocket.connections import configure
   >>> configure.connection_pool(hostname='myredis.cooldomain.com', port=6379, db=0)

   # at this point you're ready to use your declared models



Declaring Models
^^^^^^^^^^^^^^^^

Repocket provides a model interface that looks just like Django, but
the field types are super simplified.

Here is how you declare a model:


::

    >>> from repocket import attributes
    >>> from repocket import ActiveRecord
    >>>
    >>>
    >>> class User(ActiveRecord):
    ...     name = attributes.Unicode()
    ...     house_name = attributes.Unicode()
    ...     email = attributes.Bytes()
    ...     password = attributes.Bytes()
    ...     metadata = attributes.JSON()


If you were in Django you would then need to run ``syncdb`` to have a
SQL table called ``User`` with the declared fields. But *this ain't
Django, ight?*

At this point you are ready to start saving user data in redis.

By default the attributes of the your model are actively saved in a
``hash`` redis datastructure.

Repocket *currenty* also supports another attribute called
``ByteStream`` that will seamlessly store the value in a string, so
that you can ``APPEND`` more bytes to it with a single call.

But we will get there soon enough, for now let's understand how to
save a new user and how it will be saved inside of redis.

Persisting Data
^^^^^^^^^^^^^^^

Let's save a ``User`` instance in redis:


.. highlight:: python

::

    >>> import bcrypt

    >>> harry = User.create(
    ...     id='970773fa-4de1-11e5-86f4-6c4008a70392',
    ...     name='Harry Potter',
    ...     email='harry@hogwards.uk',
    ...     house_name='Gryffindor',
    ...     password=bcrypt.hashpw(b'hermione42', bcrypt.gensalt(10)),
    ...     metadata={
    ...         'known_tricks': [
    ...             "Protego",
    ...             "Expelliarmus",
    ...             "Wingardium Leviosa",
    ...             "Expecto Patronum"
    ...         ]
    ...     }
    ... )
    >>> ron = User.create(
    ...     id='40997aa4-71fc-4ad3-b0d7-04c0fac6d6d8',
    ...     name='Ron Weasley',
    ...     house_name='Gryffindor',
    ...     email='ron@hogwards.uk',
    ...     password=bcrypt.hashpw(b'hermione42', bcrypt.gensalt(10)),
    ...     metadata={
    ...         'known_tricks': [
    ...             "Protego",
    ...             "Expelliarmus",
    ...         ]
    ...     }
    ... )


Retrieving an item by its id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> harry = User.objects.get(id='970773fa-4de1-11e5-86f4-6c4008a70392')
    >>> harry.metadata
    {
        'known_tricks': [
            "Protego",
            "Expelliarmus",
            "Wingardium Leviosa",
            "Expecto Patronum"
        ]
    }


Manipulating in-memory data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can get the valus of an instance with either ``.attribute``` notation or ``["attribute"]``.

::

    >>> harry = User.objects.get(id='970773fa-4de1-11e5-86f4-6c4008a70392')
    >>> harry.id
    UUID('970773fa-4de1-11e5-86f4-6c4008a70392')


::

    >>> harry['id']
    UUID('970773fa-4de1-11e5-86f4-6c4008a70392')



Deleting a record from redis
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``delete()`` method returns an integer corresponding to the number
of redis keys that were deleted as result.

::

    >>> harry = User.objects.get(id='970773fa-4de1-11e5-86f4-6c4008a70392')
    >>> harry.delete()
    1



Retrive multiple items with filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    >>> results = User.objects.filter(house_name='Griffindor')
    >>> len(results)
    2
    >>> results[0].name
    'Harry Potter'
    >>> results[1].name
    'Ron Weasley'



.. note:: The order in which the elements are returned by ``filter()``
          cannot be guaranteed because the id is a *uuid*.
          Use the ``.order_by()`` method

..

    Ordering results
    ^^^^^^^^^^^^^^^^

    The ``filter()`` method returns a ``ResultSet`` object, which is a
    list with superpowers. The main superpower is the ability to order the
    results.


        >>> results = User.objects.filter(house_name='Griffindor').order_by('-name')
        >>> len(results)
        2
        >>> results[0].name
        'Ron Weasley'
        >>> results[1].name
        'Harry Potter'
