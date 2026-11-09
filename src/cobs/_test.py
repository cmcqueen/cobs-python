"""
Consistent Overhead Byte Stuffing/Reduced (COBS/R)

Common Unit Test methods used by both COBS and COBS/R.
"""

from array import array
import random


def infinite_non_zero_generator():
    while True:
        for i in range(1, 50):
            for j in range(1, 256, i):
                yield j


def non_zero_generator(length):
    non_zeros = infinite_non_zero_generator()
    for _ in range(length):
        yield next(non_zeros)


def non_zero_bytes(length):
    return b''.join(bytes([i]) for i in non_zero_generator(length))


class CodecTestConfig:
    codec = None
    predefined_encodings = []
    decode_error_test_strings = []
    NUM_TESTS = 5000
    MAX_LENGTH = 2000

    def simple_encode_non_zeros_only(self, in_bytes):
        out_list = []
        for i in range(0, len(in_bytes), 254):
            data_block = in_bytes[i: i + 254]
            out_list.append(bytes([len(data_block) + 1]))
            out_list.append(data_block)
        return b''.join(out_list)

    def expected_non_zero_encoding(self, in_bytes):
        return self.simple_encode_non_zeros_only(in_bytes)


class PredefinedEncodingsTestMixin(CodecTestConfig):
    def test_predefined_encodings(self):
        for test_string, expected_encoded_string in self.predefined_encodings:
            encoded = self.codec.encode(test_string)
            self.assertEqual(encoded, expected_encoded_string)

    def test_decode_predefined_encodings(self):
        for test_string, expected_encoded_string in self.predefined_encodings:
            decoded = self.codec.decode(expected_encoded_string)
            self.assertEqual(test_string, decoded)

class PredefinedDecodeErrorTestMixin(CodecTestConfig):
    def test_predefined_decode_error(self):
        for test_encoded in self.decode_error_test_strings:
            with self.assertRaises(self.codec.DecodeError):
                self.codec.decode(test_encoded)

class ZerosTestMixin(CodecTestConfig):
    def test_zeros(self):
        for length in range(520):
            test_string = b'\x00' * length
            encoded = self.codec.encode(test_string)
            expected_encoded = b'\x01' * (length + 1)
            self.assertEqual(encoded, expected_encoded, "encoding zeros failed for length %d" % length)
            decoded = self.codec.decode(encoded)
            self.assertEqual(decoded, test_string, "decoding zeros failed for length %d" % length)

class NonZerosTestMixin(CodecTestConfig):
    def test_non_zeros(self):
        for length in range(1, 1000):
            test_string = non_zero_bytes(length)
            encoded = self.codec.encode(test_string)
            expected_encoded = self.expected_non_zero_encoding(test_string)
            self.assertEqual(encoded, expected_encoded,
                             "encoded != expected_encoded for length %d\nencoded: %s\nexpected_encoded: %s" %
                             (length, repr(encoded), repr(expected_encoded)))

    def test_non_zeros_and_trailing_zero(self):
        for length in range(1, 1000):
            non_zeros_string = non_zero_bytes(length)
            test_string = non_zeros_string + b'\x00'
            encoded = self.codec.encode(test_string)
            if (len(non_zeros_string) % 254) == 0:
                expected_encoded = self.simple_encode_non_zeros_only(non_zeros_string) + b'\x01\x01'
            else:
                expected_encoded = self.simple_encode_non_zeros_only(non_zeros_string) + b'\x01'
            self.assertEqual(encoded, expected_encoded,
                             "encoded != expected_encoded for length %d\nencoded: %s\nexpected_encoded: %s" %
                             (length, repr(encoded), repr(expected_encoded)))

class RandomDataTestMixin(CodecTestConfig):
    def test_random(self):
        try:
            for _test_num in range(self.NUM_TESTS):
                length = random.randint(0, self.MAX_LENGTH)
                test_string = bytes(random.randint(0, 255) for x in range(length))
                encoded = self.codec.encode(test_string)
                self.assertTrue(b'\x00' not in encoded,
                                "encoding contains zero byte(s):\noriginal: %s\nencoded: %s" %
                                (repr(test_string), repr(encoded)))
                self.assertTrue(len(encoded) <= len(test_string) + 1 + (len(test_string) // 254),
                                "encoding too big:\noriginal: %s\nencoded: %s" %
                                (repr(test_string), repr(encoded)))
                decoded = self.codec.decode(encoded)
                self.assertEqual(decoded, test_string,
                                 "encoding and decoding random data failed:\noriginal: %s\ndecoded: %s" %
                                 (repr(test_string), repr(decoded)))
        except KeyboardInterrupt:
            pass

class InputTypesTestMixin(CodecTestConfig):
    def test_unicode_string(self):
        for test_string, expected_encoded_string in self.predefined_encodings:
            unicode_test_string = test_string.decode('latin')
            with self.assertRaises(TypeError):
                self.codec.encode(unicode_test_string)
            unicode_encoded_string = expected_encoded_string.decode('latin')
            with self.assertRaises(TypeError):
                self.codec.decode(unicode_encoded_string)

    def test_bytearray(self):
        for test_string, expected_encoded_string in self.predefined_encodings:
            bytearray_test_string = bytearray(test_string)
            encoded = self.codec.encode(bytearray_test_string)
            self.assertEqual(encoded, expected_encoded_string)
            bytearray_encoded_string = bytearray(expected_encoded_string)
            decoded = self.codec.decode(bytearray_encoded_string)
            self.assertEqual(decoded, test_string)

    def test_array_of_bytes(self):
        for test_string, expected_encoded_string in self.predefined_encodings:
            array_test_string = array('B', test_string)
            encoded = self.codec.encode(array_test_string)
            self.assertEqual(encoded, expected_encoded_string)
            array_encoded_string = array('B', expected_encoded_string)
            decoded = self.codec.decode(array_encoded_string)
            self.assertEqual(decoded, test_string)

    def test_memoryview(self):
        for test_string, expected_encoded_string in self.predefined_encodings:
            encoded = self.codec.encode(memoryview(test_string))
            self.assertEqual(encoded, expected_encoded_string)
            decoded = self.codec.decode(memoryview(expected_encoded_string))
            self.assertEqual(decoded, test_string)

    def test_array_of_half_words(self):
        typecodes = ['H', 'h', 'i', 'I', 'l', 'L', 'f', 'd']
        for typecode in typecodes:
            array_test_string = array(typecode, [49, 50, 51, 52, 53])
            with self.assertRaises(BufferError):
                self.codec.encode(array_test_string)
            array_encoded_string = array(typecode, [6, 49, 50, 51, 52, 53])
            with self.assertRaises(BufferError):
                self.codec.decode(array_encoded_string)

class UtilTestsMixin(CodecTestConfig):
    def test_encoded_len_calc(self):
        self.assertEqual(self.codec.encoding_overhead(5), 1)
        self.assertEqual(self.codec.max_encoded_length(5), 6)

    def test_encoded_len_calc_empty_packet(self):
        self.assertEqual(self.codec.encoding_overhead(0), 1)
        self.assertEqual(self.codec.max_encoded_length(0), 1)

    def test_encoded_len_calc_still_one_byte_overhead(self):
        self.assertEqual(self.codec.encoding_overhead(254), 1)
        self.assertEqual(self.codec.max_encoded_length(254), 255)

    def test_encoded_len_calc_two_byte_overhead(self):
        self.assertEqual(self.codec.encoding_overhead(255), 2)
        self.assertEqual(self.codec.max_encoded_length(255), 257)
