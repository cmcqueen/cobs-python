
..  _COBS/R:
..  _Consistent Overhead Byte Stuffing—Reduced:

===================================================
Consistent Overhead Byte Stuffing—Reduced (COBS/R)
===================================================

This describes a modification of COBS, which I'm calling "Consistent Overhead
Byte Stuffing—Reduced" (COBS/R), is provided in the :mod:`cobs.cobsr` module.
Its purpose is to save one byte from the encoded form in some cases. Plain
COBS encoding always has a +1 byte encoding overhead [COBS]_. COBS/R can often
avoid the +1 byte, which can be a useful savings if it is mostly small
messages that are being encoded.

In plain COBS, the last length code byte in the message has some inherent
redundancy: if it is greater than the number of remaining bytes, this is
detected as an error.

In COBS/R, instead we opportunistically replace the final length code byte
with the final data byte, whenever the value of the final data byte is greater
than or equal to what the final length value would normally be. This variation
can be unambiguously decoded: the decoder notices that the length code is
greater than the number of remaining bytes.

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

