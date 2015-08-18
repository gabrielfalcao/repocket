Repocket
########

Simple active record for redis.


Collaborating
=============


1. Get the code
'''''''''''''''

::

   $ cd ~/Work
   $ git clone git@github.com:gabrielfalcao/repocket.git
   $ cd repocket


2. Ensure that you have virtualenvwrapper installed
'''''''''''''''''''''''''''''''''''''''''''''''''''

::

   $ pip install virtualenvwrapper


3. Create a virtual env for repocket
''''''''''''''''''''''''''''''''''''

For the first time:

::

   $ mkvirtualenv repocket

After this, every time you want to run repocket again, just run the
command:

::

   $ workon repocket


4. Install python dependencies
''''''''''''''''''''''''''''''

::

   $ pip install -r requirements.txt


5. Run the tests
''''''''''''''''

::

   -$ make test
