
:mod:`cobs.cobs`—COBS Encoding and Decoding
============================================

.. module:: cobs.cobs
   :synopsis: Consistent Overhead Byte Stuffing (COBS)
.. moduleauthor:: Craig McQueen
.. sectionauthor:: Craig McQueen

This module provides functions for encoding and decoding byte strings using
the COBS encoding method.

In Python 2.x, the input type to the functions must be a byte string. Unicode
strings may *appear* to work at first, but only if they can be automatically
encoded to bytes using the ``ascii`` encoding. So Unicode strings should not be
used.

In Python 3.x, byte strings are acceptable input. Types that implement the
buffer protocol, providing a simple buffer of bytes, are also acceptable. Thus
types such as ``bytearray`` and ``array('B',...)`` are accepted input. The
output type is always a byte array.


:func:`encode` -- COBS encode
-----------------------------

The function encodes a byte string according to the COBS encoding method.

.. function:: encode(data)

    :param data:    Data to encode.
    :type data:     byte string

    :return:        Encoded data.
    :rtype:         byte string

:func:`decode` -- COBS decode
-----------------------------

The function decodes a byte string according to the COBS method.

.. function:: decode(data)

    :param data:    Data to decode.
    :type data:     byte string

    :return:        Decoded data.
    :rtype:         byte string


..  _cobs-examples:

Examples
^^^^^^^^

Basic usage example, in Python 2.x using byte string inputs::

    >>> from cobs import cobs
    
    >>> encoded = cobs.encode(b'Hello world\x00This is a test')
    >>> encoded
    '\x0cHello world\x0fThis is a test'
    
    >>> cobs.decode(encoded)
    'Hello world\x00This is a test'


For Python 3.x, input cannot be Unicode strings. Byte strings are acceptable
input. Also, any type that implements the buffer protocol, providing a single
block of bytes, is also acceptable as input::

    >>> from cobs import cobs
    >>> encoded = cobs.encode(bytearray(b'Hello world\x00This is a test'))
    >>> encoded
    b'\x0cHello world\x0fThis is a test'
    >>> cobs.decode(encoded)
    b'Hello world\x00This is a test'

