========================================
Consistent Overhead Byte Stuffing (COBS)
========================================

Python functions for encoding and decoding COBS.

-----
Intro
-----

Functions are provided for encoding and decoding according to the basic COBS
method.  The COBS variant "Zero Pair Elimination" (ZPE) is not implemented.

A pure Python implementation and a C extension implementation are provided. If
the C extension is not available for some reason, the pure Python version will
be used.

References
``````````

    http://www.stuartcheshire.org/papers/COBSforSIGCOMM/

    http://www.stuartcheshire.org/papers/COBSforToN.pdf


-------------------------
Supported Python Versions
-------------------------

Python >= 2.4 and 3.x are supported, and have both a C extension and a pure
Python implementation.

Python versions < 2.4 might work, but have not been tested. Python 3.0 has
also not been tested.


------------
Installation
------------

The cobs package is installed using ``distutils``.  If you have the tools
installed to build a Python extension module, run the following command::

    python setup.py install


------------
Unit Testing
------------

Basic unit testing is in the module ``cobs.test``. To run it on Python >=2.5::

    python -m cobs.test

Alternatively, in the ``test`` directory run::

    python test_cobs.py


-------
License
-------

The code is released under the MIT license. See LICENSE.txt for details.
