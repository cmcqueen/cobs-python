
:mod:`cobs`—COBS Encoding and Decoding
======================================

.. module:: cobs.cobs
   :synopsis: Consistent Overhead Byte Stuffing (COBS)
.. moduleauthor:: Craig McQueen
.. sectionauthor:: Craig McQueen

This module provides functions for encoding and decoding byte strings using
the COBS encoding method.

.. note:: This documentation is for Python 2.x usage. Python 3.x usage is very similar,
    with the main difference that input strings must be explicitly defined as
    :keyword:`bytes` type. E.g.::

       encoded = cobs.encode(b'Hello world\x00This is a test')


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


Examples
^^^^^^^^

    >>> from cobs import cobs
    
    >>> encoded = cobs.encode('Hello world\x00This is a test')
    >>> encoded
    '\x0cHello world\x0fThis is a test'
    
    >>> cobs.decode(encoded)
    'Hello world\x00This is a test'
