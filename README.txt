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

Python >= 2.6 and 3.x are supported, and have both a C extension and a pure
Python implementation.

However the installer is not smart enough to install the pure Python
implementation when the C extension cannot be compiled.

The C extension seems to work in Python 2.4 and 2.5. However, it has not been
tested much. There is no pure Python implementation for these versions. The unit
test file in the ``test`` directory also does not run under Python 2.4 and 2.5.
I don't know how much interest there is for these older Python versions. Please
let me know if you would like support for these older Python versions to be
improved.

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
