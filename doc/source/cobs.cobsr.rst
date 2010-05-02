
:mod:`cobs.cobsr`—COBS/R Encoding and Decoding
==============================================

.. module:: cobs.cobsr
   :synopsis: Consistent Overhead Byte Stuffing—Reduced (COBS/R)
.. moduleauthor:: Craig McQueen
.. sectionauthor:: Craig McQueen

This module provides functions for encoding and decoding byte strings using
the :ref:`COBS/R <COBS/R>` encoding method.

In Python 2.x, the input type to the functions must be a byte string. Unicode
strings may *appear* to work at first, but only if they can be automatically
encoded to bytes using the ``ascii`` encoding. So Unicode strings should not be
used.

In Python 3.x, byte strings are acceptable input. Types that implement the
buffer protocol, providing a simple buffer of bytes, are also acceptable. Thus
types such as ``bytearray`` and ``array('B',...)`` are accepted input. The
output type is always a byte string.


:func:`encode` -- COBS/R encode
-------------------------------

The function encodes a byte string according to the COBS/R encoding method.

.. function:: encode(data)

    :param data:    Data to encode.
    :type data:     byte string

    :return:        Encoded data.
    :rtype:         byte string

:func:`decode` -- COBS/R decode
-------------------------------

The function decodes a byte string according to the COBS/R method.

.. function:: decode(data)

    :param data:    Data to decode.
    :type data:     byte string

    :return:        Decoded data.
    :rtype:         byte string


..  _cobsr-examples:

Examples
^^^^^^^^

Basic usage example, in Python 2.x using byte string inputs::


    >>> from cobs import cobsr
    
    >>> encoded = cobsr.encode(b'Hello world\x00This is a test')
    >>> encoded
    '\x0cHello worldtThis is a tes'
    
    >>> cobsr.decode(encoded)
    'Hello world\x00This is a test'


For Python 3.x, input cannot be Unicode strings. Byte strings are acceptable
input. Also, any type that implements the buffer protocol, providing a single
block of bytes, is also acceptable as input::

    >>> from cobs import cobsr
    >>> encoded = cobsr.encode(bytearray(b'Hello world\x00This is a test'))
    >>> encoded
    b'\x0cHello worldtThis is a tes'
    >>> cobsr.decode(encoded)
    b'Hello world\x00This is a test'

