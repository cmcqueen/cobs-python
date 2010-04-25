
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

The :mod:`cobs` package is provided, which contains modules containing functions
for encoding and decoding according to COBS methods.


What Is COBS?
`````````````

COBS is a method of encoding a packet of bytes into a form that contains no
bytes with value zero (0x00). The input packet of bytes can contain bytes
in the full range of 0x00 to 0xFF. The COBS encoded packet is guaranteed to
generate packets with bytes only in the range 0x01 to 0xFF. Thus, in a
communication protocol, packet boundaries can be reliably delimited with 0x00
bytes.

The COBS encoding does have to increase the packet size to achieve this
encoding. However, compared to other byte-stuffing methods, the packet size
increase is reasonable and predictable. COBS always adds 1 byte to the
message length. Additionally, for longer packets of length *n*, it *may* add
:math:`\left\lfloor\frac{n}{254}\right\rfloor`
additional bytes to the encoded packet size.

For example, compare to the PPP protocol, which uses 0x7E bytes to delimit
PPP packets. The PPP protocol uses an "escape" style of byte stuffing,
replacing all occurences of 0x7E bytes in the packet with 0x7D 0x5E. But that
byte-stuffing method can potentially double the size of the packet in the
worst case. COBS uses a different method for byte-stuffing, which has a much
more reasonable worst-case overhead.

For more details about COBS, see the references [COBS]_ [COBSPPP]_.

I have included a variant on COBS, :ref:`COBS/R <COBS/R>`, which slightly
modifies COBS to often avoid the +1 byte overhead of COBS. So in many cases,
especially for smaller packets, the size of a COBS/R encoded packet is the
same size as the original packet. For more details about COBS/R see the
:ref:`documentation for Consistent Overhead Byte Stuffing—Reduced <COBS/R>`.


References
``````````

.. [COBS]       | `Consistent Overhead Byte Stuffing <http://www.stuartcheshire.org/papers/COBSforToN.pdf>`_
                | Stuart Cheshire and Mary Baker
                | IEEE/ACM Transations on Networking, Vol. 7, No. 2, April 1999

.. [COBSPPP]    | `PPP Consistent Overhead Byte Stuffing (COBS) <http://tools.ietf.org/html/draft-ietf-pppext-cobs-00>`_
                | PPP Working Group Internet Draft
                | James Carlson, IronBridge Networks
                | Stuart Cheshire and Mary Baker, Stanford University
                | November 1997


----------------
Modules Provided
----------------

==================  ======================  ===============================================================
Module              Short Name              Long Name
==================  ======================  ===============================================================
:mod:`cobs.cobs`    COBS                    Consistent Overhead Byte Stuffing (basic method) [COBS]_
:mod:`cobs.cobsr`   :ref:`COBS/R <COBS/R>`  :ref:`Consistent Overhead Byte Stuffing—Reduced <COBS/R>`
==================  ======================  ===============================================================

"Consistent Overhead Byte Stuffing—Reduced" (COBS/R) is my own invention, a
modification of basic COBS encoding, and is described in more detail in the
:ref:`documentation for Consistent Overhead Byte Stuffing—Reduced <COBS/R>`.

The following are not implemented:

==================  ======================================================================
Short Name          Long Name
==================  ======================================================================
COBS/ZPE            Consistent Overhead Byte Stuffing—Zero Pair Elimination [COBS]_
COBS/ZRE            Consistent Overhead Byte Stuffing—Zero Run Elimination [COBSPPP]_
==================  ======================================================================

A pure Python implementation and a C extension implementation are provided. If
the C extension is not available for some reason, the pure Python version will
be used.


-----
Usage
-----

The modules provide an :func:`encode` and a :func:`decode` function.

In Python 2.x, the input should be a byte string. Basic usage (example in
Python 2.x)::

    >>> from cobs import cobs
    >>> encoded = cobs.encode('Hello world\x00This is a test')
    >>> encoded
    '\x0cHello world\x0fThis is a test'
    >>> cobs.decode(encoded)
    'Hello world\x00This is a test'

:ref:`COBS/R <COBS/R>` usage is almost identical::

    >>> from cobs import cobsr
    >>> encoded = cobsr.encode('Hello world\x00This is a test')
    >>> encoded
    '\x0cHello worldtThis is a tes'
    >>> cobsr.decode(encoded)
    'Hello world\x00This is a test'

For Python 3.x, input cannot be Unicode strings. Byte strings are acceptable
input. Any type that implements the buffer protocol, providing a single
block of bytes, is also acceptable as input::

    >>> from cobs import cobs
    >>> encoded = cobs.encode(bytearray(b'Hello world\x00This is a test'))
    >>> encoded
    b'\x0cHello world\x0fThis is a test'
    >>> cobs.decode(encoded)
    b'Hello world\x00This is a test'


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

The cobs package is installed using :mod:`distutils`.  If you have the tools
installed to build a Python extension module, run the following command::

    python setup.py install


------------
Unit Testing
------------

Basic unit testing is in the :mod:`test` sub-module, e.g. :mod:`cobs.cobs.test`.
To run it on Python >=2.5::

    python -m cobs.cobs.test
    python -m cobs.cobsr.test

Alternatively, in the :file:`test` directory run::

    python test_cobs.py
    python test_cobsr.py


-------
License
-------

The code is released under the MIT license.

    Copyright (c) 2010 Craig McQueen
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

