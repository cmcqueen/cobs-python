
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

--------
Examples
--------

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


---------------------------
Encoding Sizes Using COBS/R
---------------------------

Given an input data packet of size *n*, COBS/R encoding may or may not add a
+1 byte overhead, depending on the contents of the input data.

Example for :math:`n=3`:

==============  ==============  ==============  ==============  ======================  ======================
:math:`x_0`     :math:`x_1`     :math:`x_2`     :math:`x_3`     Probability of Pattern  Probability of +1 byte
==============  ==============  ==============  ==============  ======================  ======================
any             any             any             :math:`=0`      |fp0|                   :math:`1`
any             any             :math:`=0`      :math:`≠0`      |fp1|                   :math:`P(x_3 < 2|x_3≠0)`
any             :math:`=0`      :math:`≠0`      :math:`≠0`      |fp2|                   :math:`P(x_3 < 3|x_3≠0)`
:math:`=0`      :math:`≠0`      :math:`≠0`      :math:`≠0`      |fp3|                   :math:`P(x_3 < 4|x_3≠0)`
:math:`≠0`      :math:`≠0`      :math:`≠0`      :math:`≠0`      |fp4|                   :math:`P(x_3 < 5|x_3≠0)`
==============  ==============  ==============  ==============  ======================  ======================

..  |fp0|   replace::   :math:`P(x_3=0)`
..  |fp1|   replace::   :math:`P(x_2=0) \times P(x_3≠0)`
..  |fp2|   replace::   :math:`P(x_1=0) \times P(x_2≠0) \times P(x_3≠0)`
..  |fp3|   replace::   :math:`P(x_0=0) \times P(x_1≠0) \times P(x_2≠0) \times P(x_3≠0)`
..  |fp4|   replace::   :math:`P(x_0≠0) \times P(x_1≠0) \times P(x_2≠0) \times P(x_3≠0)`

For byte probabilities that are evenly distributed, this simplifies to:

==============  ==============  ==============  ==============  ======================  ==========================
:math:`x_0`     :math:`x_1`     :math:`x_2`     :math:`x_3`     Probability of Pattern  Probability of +1 byte
==============  ==============  ==============  ==============  ======================  ==========================
any             any             any             :math:`=0`      |f2p0|                  :math:`1`
any             any             :math:`=0`      :math:`≠0`      |f2p1|                  :math:`\frac{1}{255}`
any             :math:`=0`      :math:`≠0`      :math:`≠0`      |f2p2|                  :math:`\frac{2}{255}`
:math:`=0`      :math:`≠0`      :math:`≠0`      :math:`≠0`      |f2p3|                  :math:`\frac{3}{255}`
:math:`≠0`      :math:`≠0`      :math:`≠0`      :math:`≠0`      |f2p4|                  :math:`\frac{4}{255}`
==============  ==============  ==============  ==============  ======================  ==========================

..  |f2p0|  replace::   :math:`\frac{1}{256}`
..  |f2p1|  replace::   :math:`\frac{1}{256}\left(\frac{255}{256}\right)^1`
..  |f2p2|  replace::   :math:`\frac{1}{256}\left(\frac{255}{256}\right)^2`
..  |f2p3|  replace::   :math:`\frac{1}{256}\left(\frac{255}{256}\right)^3`
..  |f2p4|  replace::   :math:`\left(\frac{255}{256}\right)^4`
