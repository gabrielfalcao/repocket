.. _getting-started:

Getting Started
===============

No more tease; here is a full example of how to declare 2 active
records with a pointer from one to the other.


.. highlight: python

::

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
