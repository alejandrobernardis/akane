Akane
=====

An asynchronous Redis_ client for Tornado_.

This client is not finished and still under development. And I'm going to
try various thing with it before it reaches a stable release. Like stuff
that doesn't make sense. :D

.. _Redis: http://redis.io/
.. _Tornado: http://www.tornadoweb.org/


Roadmap
-------

* C-based reply parser. (in progress)
* Implement commands and unit tests. (in progress)
* Implement pipelining.

I haven't looked into pub/sub, Lua scripting and transactions, but those will be
included too. It just needs some more research.

I'll first support Python 2 and then add support for Python 3 to avoid version
checks everywhere in the code. There are some differences in the C-APIs of Python 2 
and 3.


License
-------

Akane is licensed under the MIT license. ``akane/buffer.c`` is from Sundown.
``akane/utils.c`` contains a function, ``intlen``, from Hiredis. That function
is under the BSD license. ``reverse`` and ``itoa`` are from K&R.


Installation
------------

Manually::

    python setup.py install
