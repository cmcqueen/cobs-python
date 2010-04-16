========================================
Consistent Overhead Byte Stuffing (COBS)
========================================

Python functions for encoding and decoding COBS.

-----
Intro
-----

Functions are provided for encoding and decoding according to the basic COBS
method.

A variant of COBS is also provided, which I'm calling "`Consistent Overhead
Byte Stuffing/Reduced`_" (COBS/R), in the ``cobsr`` module.

The COBS variant "Zero Pair Elimination" (ZPE) and "Zero Run Elimination" (ZRE)
is not implemented.

A pure Python implementation and a C extension implementation are provided. If
the C extension is not available for some reason, the pure Python version will
be used.

References
``````````

.. [#sigcomm]   | `Consistent Overhead Byte Stuffing`__
                | Stuart Cheshire and Mary Baker, Computer Science Department, Stanford University
                | SIGCOMM '97 - Cannes, France, September 1997

.. __:
.. _Consistent Overhead Byte Stuffing (for SigCOMM): http://www.stuartcheshire.org/papers/COBSforSIGCOMM/

.. [#ieeeton]   | `Consistent Overhead Byte Stuffing`__
                | Stuart Cheshire and Mary Baker
                | IEEE/ACM Transations on Networking, Vol. 7, No. 2, April 1999

.. __:
.. _Consistent Overhead Byte Stuffing (for IEEE): http://www.stuartcheshire.org/papers/COBSforToN.pdf

.. [#ppp]       | `PPP Consistent Overhead Byte Stuffing (COBS)`_
                | PPP Working Group Internet Draft
                | James Carlson, IronBridge Networks
                | Stuart Cheshire and Mary Baker, Stanford University
                | November 1997

.. _PPP Consistent Overhead Byte Stuffing (COBS): http://tools.ietf.org/html/draft-ietf-pppext-cobs-00


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


..  _Consistent Overhead Byte Stuffing/Reduced:

--------------------------------------------------
Consistent Overhead Byte Stuffing/Reduced (COBS/R)
--------------------------------------------------

A modification of COBS is also provided, which I'm calling "COBS/Reduced"
(COBS/R), in the ``cobsr`` module. Its purpose is to save one byte from
the encoded form in some cases. Plain COBS encoding always has a +1 byte
encoding overhead. COBS/R can sometimes avoid the +1 byte, which can be
a useful savings if it is mostly small messages that are being encoded.

In plain COBS, the last code (length) byte in the message has some
inherent redundancy: if it is greater than the number of remaining bytes,
this is detected as an error.

In COBS/R, instead we opportunistically replace the final length byte
with the final data byte, whenever the value of the final data byte is
greater than or equal to what the final length value would be. This can
be unambiguously decoded.

Examples:
`````````

All examples are in hex.

First example:

Input:

==  ==  ==  ==  ==  ==
2F  A2  00  92  73  02
==  ==  ==  ==  ==  ==

This example is encoded the same in COBS and COBS/R. Encoded (length bytes are bold):

======  ======  ======  ======  ======  ======  ======
**03**  2F      A2      **04**  92      73      02
======  ======  ======  ======  ======  ======  ======

Second example:

The second example is almost the same, except the final data byte value
is greater than what the length byte would be.

Input:

==  ==  ==  ==  ==  ==
2F  A2  00  92  73  26
==  ==  ==  ==  ==  ==

Encoded in COBS (length bytes are bold):

======  ======  ======  ======  ======  ======  ======
**03**  2F      A2      **04**  92      73      26
======  ======  ======  ======  ======  ======  ======

Encoded in COBS/R:

======  ======  ======  ======  ======  ======
**03**  2F      A2      **26**  92      73    
======  ======  ======  ======  ======  ======

Because the last data byte (**26**) is greater than the usual length code
(**04**), the last data byte can be inserted in place of the length code,
and removed from the end of the sequence. This avoids the usual +1 byte
overhead of the COBS encoding.

The decoder detects this variation on the encoding simply by detecting that
the length code is greater than the number of remaining bytes. That situation
would be a decoding error in regular COBS, but in COBS/R it is used to save
an encoded byte.
