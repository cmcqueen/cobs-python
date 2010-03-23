"""
Consistent Overhead Byte Stuffing (COBS)

Unit Tests

This version is for Python 2.6.
"""

import cobs
import unittest


decode_error_test_strings = [
    b"\x00",
    b"\x05123",
    b"\x051234\x00",
    b"\x0512\x004",
]

def infinite_non_zero_generator():
    while True:
        for i in xrange(1,50):
            for j in xrange(1,256, i):
                yield j

def non_zero_generator(length):
    non_zeros = infinite_non_zero_generator()
    for i in xrange(length):
        yield non_zeros.next()

def non_zero_bytes(length):
    return b''.join(chr(i) for i in non_zero_generator(length))


class PredefinedEncodingsTests(unittest.TestCase):
    predefined_encodings = [
        [ b"",                                          b"\x01"                                                     ],
        [ b"1",                                         b"\x021"                                                    ],
        [ b"12345",                                     b"\x0612345"                                                ],
        [ b"12345\x006789",                             b"\x0612345\x056789"                                        ],
        [ b"\x0012345\x006789",                         b"\x01\x0612345\x056789"                                    ],
        [ b"12345\x006789\x00",                         b"\x0612345\x056789\x01"                                    ],
        [ b"\x00",                                      b"\x01\x01"                                                 ],
        [ b"\x00\x00",                                  b"\x01\x01\x01"                                             ],
        [ b"\x00\x00\x00",                              b"\x01\x01\x01\x01"                                         ],
        [ bytes(bytearray(range(1, 254))),              bytes(b"\xfe" + bytearray(range(1, 254)))                   ],
        [ bytes(bytearray(range(1, 255))),              bytes(b"\xff" + bytearray(range(1, 255)))                   ],
        [ bytes(bytearray(range(1, 256))),              bytes(b"\xff" + bytearray(range(1, 255)) + b"\x02\xff")     ],
        [ bytes(bytearray(range(0, 256))),              bytes(b"\x01\xff" + bytearray(range(1, 255)) + b"\x02\xff") ],
    ]

    def test_predefined_encodings(self):
        for (test_string, expected_encoded_string) in self.predefined_encodings:
            encoded = cobs.encode(test_string)
            self.assertEqual(encoded, expected_encoded_string)

    def test_decode_predefined_encodings(self):
        for (test_string, expected_encoded_string) in self.predefined_encodings:
            decoded = cobs.decode(expected_encoded_string)
            self.assertEqual(test_string, decoded)


class PredefinedDecodeErrorTests(unittest.TestCase):
    def test_predefined_decode_error(self):
        for test_encoded in decode_error_test_strings:
            self.assertRaises(cobs.DecodeError, cobs.decode, test_encoded)


class ZerosTest(unittest.TestCase):
    def test_zeros(self):
        for length in xrange(520):
            test_string = b'\x00' * length
            encoded = cobs.encode(test_string)
            expected_encoded = b'\x01' * (length + 1)
            self.assertEqual(encoded, expected_encoded)


class NonZerosTest(unittest.TestCase):
    def test_non_zeros(self):
        for length in xrange(520):
            test_string = non_zero_bytes(length)
            encoded = cobs.encode(test_string)
            expected_encoded = b'\x01' * (length + 1)
            self.assertEqual(encoded, expected_encoded)


def runtests():
    unittest.main()


if __name__ == '__main__':
    runtests()
