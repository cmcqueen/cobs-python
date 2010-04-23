========================================
Consistent Overhead Byte Stuffing (COBS)
========================================

:Author: Craig McQueen
:Contact: http://craig.mcqueen.id.au/
:Copyright: 2010 Craig McQueen


Python functions for encoding and decoding COBS.

-----
Intro
-----

The ``cobs`` package is provided, which contains modules containing functions
for encoding and decoding according to COBS methods.

==================  ==================  ===============================================================
Module              Short Name          Long Name
==================  ==================  ===============================================================
``cobs.cobs``       COBS                Consistent Overhead Byte Stuffing (basic method) [#ieeeton]_
``cobs.cobsr``      COBS/R              `Consistent Overhead Byte Stuffing/Reduced`_
==================  ==================  ===============================================================

"`Consistent Overhead Byte Stuffing/Reduced`_" (COBS/R) is my own invention,
a modification of basic COBS encoding, and is described in more detail below.

The following are not implemented:

==================  ======================================================================
Short Name          Long Name
==================  ======================================================================
COBS/ZPE            Consistent Overhead Byte Stuffing--Zero Pair Elimination [#ieeeton]_
COBS/ZRE            Consistent Overhead Byte Stuffing--Zero Run Elimination [#ppp]_
==================  ======================================================================

A pure Python implementation and a C extension implementation are provided. If
the C extension is not available for some reason, the pure Python version will
be used.

References
``````````

.. [#ieeeton]   | `Consistent Overhead Byte Stuffing`__
                | Stuart Cheshire and Mary Baker
                | IEEE/ACM Transations on Networking, Vol. 7, No. 2, April 1999

.. __:
.. _Consistent Overhead Byte Stuffing (for IEEE):
    http://www.stuartcheshire.org/papers/COBSforToN.pdf

.. [#ppp]       | `PPP Consistent Overhead Byte Stuffing (COBS)`_
                | PPP Working Group Internet Draft
                | James Carlson, IronBridge Networks
                | Stuart Cheshire and Mary Baker, Stanford University
                | November 1997

.. _PPP Consistent Overhead Byte Stuffing (COBS):
    http://tools.ietf.org/html/draft-ietf-pppext-cobs-00


-----
Usage
-----

The modules provide an ``encode`` and a ``decode`` function.

In Python 2.x, the input should be a byte string. Basic usage (example in
Python 2.x)::

    >>> from cobs import cobs
    >>> encoded = cobs.encode('Hello world\x00This is a test')
    >>> encoded
    '\x0cHello world\x0fThis is a test'
    >>> cobs.decode(encoded)
    'Hello world\x00This is a test'

`COBS/R`_ usage is almost identical:

    >>> from cobs import cobsr
    >>> encoded = cobsr.encode('Hello world\x00This is a test')
    >>> encoded
    '\x0cHello worldtThis is a tes'
    >>> cobsr.decode(encoded)
    'Hello world\x00This is a test'

For Python 3.x, input cannot be Unicode strings. Byte strings are acceptable
input. Any input that implements the buffer protocol, providing a single
block of bytes, is also acceptable as input.


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

Basic unit testing is in the ``test`` sub-module, e.g. ``cobs.cobs.test``. To run it on Python >=2.5::

    python -m cobs.cobs.test

Alternatively, in the ``test`` directory run::

    python test_cobs.py


-------
License
-------

The code is released under the MIT license. See LICENSE.txt for details.


..  _COBS/R:
..  _Consistent Overhead Byte Stuffing/Reduced:

--------------------------------------------------
Consistent Overhead Byte Stuffing/Reduced (COBS/R)
--------------------------------------------------

A modification of COBS, which I'm calling "Consistent Overhead Byte
Stuffing/Reduced" (COBS/R), is provided in the ``cobs.cobsr`` module. Its
purpose is to save one byte from the encoded form in some cases. Plain COBS
encoding always has a +1 byte encoding overhead. COBS/R can often avoid the +1
byte, which can be a useful savings if it is mostly small messages that are
being encoded.

In plain COBS, the last length code byte in the message has some inherent
redundancy: if it is greater than the number of remaining bytes, this is
detected as an error.

In COBS/R, instead we opportunistically replace the final length code byte with
the final data byte, whenever the value of the final data byte is greater than
or equal to what the final length value would normally be. This variation can be
unambiguously decoded: the decoder notices that the length code is greater than
the number of remaining bytes.

Examples
````````

The byte values in the examples are in hex.

First example:

Input:

======  ======  ======  ======  ======  ======
2F      A2      00      92      73      02
======  ======  ======  ======  ======  ======

This example is encoded the same in COBS and COBS/R. Encoded (length code bytes
are bold):

======  ======  ======  ======  ======  ======  ======
**03**  2F      A2      **04**  92      73      02
======  ======  ======  ======  ======  ======  ======

Second example:

The second example is almost the same, except the final data byte value is
greater than what the length byte would be.

Input:

======  ======  ======  ======  ======  ======
2F      A2      00      92      73      26
======  ======  ======  ======  ======  ======

Encoded in plain COBS (length code bytes are bold):

======  ======  ======  ======  ======  ======  ======
**03**  2F      A2      **04**  92      73      26
======  ======  ======  ======  ======  ======  ======

Encoded in COBS/R:

======  ======  ======  ======  ======  ======
**03**  2F      A2      **26**  92      73    
======  ======  ======  ======  ======  ======

Because the last data byte (**26**) is greater than the usual length code
(**04**), the last data byte can be inserted in place of the length code, and
removed from the end of the sequence. This avoids the usual +1 byte overhead of
the COBS encoding.

The decoder detects this variation on the encoding simply by detecting that the
length code is greater than the number of remaining bytes. That situation would
be a decoding error in regular COBS, but in COBS/R it is used to save one byte
in the encoded message.
