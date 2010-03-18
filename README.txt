========================================
Consistent Overhead Byte Stuffing (COBS)
========================================

Python functions for encoding and decoding COBS.

-----
Intro
-----

Functions are provided for encoding and decoding according to
the basic COBS method.  The COBS variant "Zero Pair Elimination" (ZPE)
is not implemented.

A pure Python implementation and a C extension implementation
are provided. If the C extension is not available for some reason,
the pure Python version will be used.

This is fully implemented for Python 2.6. It is partially
implemented for Python 3.1--the C extension is working, but the
pure Python code is not.


References
``````````

    http://www.stuartcheshire.org/papers/COBSforSIGCOMM/

    http://www.stuartcheshire.org/papers/COBSforToN.pdf


------------
Installation
------------

The cobs package is installed using ``distutils``.  If you have the tools
installed to build a Python extension module, run the following command::

    python setup.py install


------------
Unit Testing
------------

Basic unit testing is in the ``test`` subdirectory. To run it::

    python test_cobs.py

-------
License
-------

See LICENSE.txt.
