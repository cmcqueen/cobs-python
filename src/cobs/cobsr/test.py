"""
Consistent Overhead Byte Stuffing/Reduced (COBS/R)

Unit Tests

This version is for Python 3.x.
"""

import unittest

from .. import cobsr as cobsr
from .._test import (
    CodecTestConfig,
    InputTypesTestMixin,
    NonZerosTestMixin,
    PredefinedDecodeErrorTestMixin,
    PredefinedEncodingsTestMixin,
    RandomDataTestMixin,
    UtilTestsMixin,
    ZerosTestMixin,
)
#from ..cobsr import _cobsr_py as cobsr


class _CobsrTestConfig(CodecTestConfig):
    codec = cobsr
    predefined_encodings = [
        [ b"",                                  b"\x01"                                                         ],
        [ b"\x01",                              b"\x02\x01"                                                     ],
        [ b"\x02",                              b"\x02"                                                         ],
        [ b"\x03",                              b"\x03"                                                         ],
        [ b"\x7E",                              b"\x7E"                                                         ],
        [ b"\x7F",                              b"\x7F"                                                         ],
        [ b"\x80",                              b"\x80"                                                         ],
        [ b"\xD5",                              b"\xD5"                                                         ],
        [ b"\xFE",                              b"\xFE"                                                         ],
        [ b"\xFF",                              b"\xFF"                                                         ],
        [ b"a\x02",                             b"\x03a\x02"                                                    ],
        [ b"a\x03",                             b"\x03a"                                                        ],
        [ b"a\xFF",                             b"\xFFa"                                                        ],
        [ b"\x05\x04\x03\x02\x01",              b"\x06\x05\x04\x03\x02\x01"                                     ],
        [ b"12345",                             b"51234"                                                        ],
        [ b"12345\x00\x04\x03\x02\x01",         b"\x0612345\x05\x04\x03\x02\x01"                                ],
        [ b"12345\x006789",                     b"\x06123459678"                                                ],
        [ b"\x0012345\x006789",                 b"\x01\x06123459678"                                            ],
        [ b"12345\x006789\x00",                 b"\x0612345\x056789\x01"                                        ],
        [ b"\x00",                              b"\x01\x01"                                                     ],
        [ b"\x00\x00",                          b"\x01\x01\x01"                                                 ],
        [ b"\x00\x00\x00",                      b"\x01\x01\x01\x01"                                             ],
        [ bytes(bytearray(range(1, 254))),      bytes(b"\xfe" + bytearray(range(1, 254)))                       ],
        [ bytes(bytearray(range(1, 255))),      bytes(b"\xff" + bytearray(range(1, 255)))                       ],
        [ bytes(bytearray(range(1, 256))),      bytes(b"\xff" + bytearray(range(1, 255)) + b"\xff")             ],
        [ bytes(bytearray(range(0, 256))),      bytes(b"\x01\xff" + bytearray(range(1, 255)) + b"\xff")         ],
        [ bytes(bytearray(range(2, 256))),      bytes(b"\xff" + bytearray(range(2, 255)))                       ],
    ]

    decode_error_test_strings = [
        b"\x00",
        b"\x051234\x00",
        b"\x0512\x004",
    ]

    def expected_non_zero_encoding(self, in_bytes):
        out_list = []
        for i in range(0, len(in_bytes), 254):
            data_block = in_bytes[i: i + 254]
            out_list.append(bytes([len(data_block) + 1]))
            out_list.append(data_block)
        last_block = out_list[-1]
        last_char_value = last_block[-1]
        if last_char_value >= len(last_block) + 1:
            del out_list[-2:]
            out_list.append(bytes([last_char_value]))
            out_list.append(last_block[:-1])
        return b''.join(out_list)


class PredefinedEncodingsTests(_CobsrTestConfig, PredefinedEncodingsTestMixin, unittest.TestCase):
    pass


class PredefinedDecodeErrorTests(_CobsrTestConfig, PredefinedDecodeErrorTestMixin, unittest.TestCase):
    pass


class ZerosTest(_CobsrTestConfig, ZerosTestMixin, unittest.TestCase):
    pass


class NonZerosTest(_CobsrTestConfig, NonZerosTestMixin, unittest.TestCase):
    pass


class RandomDataTest(_CobsrTestConfig, RandomDataTestMixin, unittest.TestCase):
    pass


class InputTypesTest(_CobsrTestConfig, InputTypesTestMixin, unittest.TestCase):
    pass


class UtilTests(_CobsrTestConfig, UtilTestsMixin, unittest.TestCase):
    pass


def runtests():
    unittest.main()


if __name__ == '__main__':
    runtests()
