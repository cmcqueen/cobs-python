
:mod:`cobs.cobsr`—COBS/R Encoding and Decoding
==============================================

.. module:: cobs.cobsr
   :synopsis: Consistent Overhead Byte Stuffing—Reduced (COBS/R)
.. moduleauthor:: Craig McQueen
.. sectionauthor:: Craig McQueen

This module provides functions for encoding and decoding byte strings using
the COBS/R encoding method.

.. note:: This documentation is for Python 2.x usage. Python 3.x usage is very similar,
    with the main difference that input strings must be explicitly defined as
    :keyword:`bytes` type. E.g.::

       encoded = cobsr.encode(b'Hello world\x00This is a test')


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


Examples
^^^^^^^^

    >>> from cobs import cobsr
    
    >>> encoded = cobsr.encode('Hello world\x00This is a test')
    >>> encoded
    '\x0cHello worldtThis is a tes'
    
    >>> cobsr.decode(encoded)
    'Hello world\x00This is a test'
