Repocket
########

Simple active record for redis. Drop-in replacement for CQLEngine

.. image:: https://readthedocs.org/projects/repocket/badge/?version=latest


Why
===

I needed an active record that worked almost as a drop-in replacement for CQLEngine.

Long-story-short I had a project where I originally wrote the db layer
usign cassandra, through CQLEngine. It became an overkill and I
decided to use redis instead.

There is a pretty good documentation available and more importantly
**I commited to 100% of unit and functional test coverage**. This code
is battle ready for production, if you find any bugs in it you can fix
within minutes.

That also means that collaboration is easy, just don't break anything,
don't delete tests and add as test coverage to you collaboration: when
fixing a bug, write at least one test to reproduce the problem in an
automated way.

If you want a new feature, please feel free to open a ticket and
request, someone might make your dreams come true. Better yet, submit
a pull request; just please **remember to write tests and
documentation** for your contributions.



Quick Usage
===========


::

   $ pip install repocket



Declare your models
^^^^^^^^^^^^^^^^^^^


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


Persist in redis
^^^^^^^^^^^^^^^^

::

    >>> import bcrypt

    >>> harry = User(
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
    >>> redis_keys_for_harry = harry.save()
    >>>
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


Query
^^^^^

::

    >>> harry = User.objects.get(id='970773fa-4de1-11e5-86f4-6c4008a70392')
    >>> harry.metadata

    >>> results = User.objects.filter(house_name='Griffindor')
    >>> len(results)
    >>> results[0] == harry
    True

    >>> results[1] == ron
    True
