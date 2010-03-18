
# Which to test:
# Default
import cobs
# C extension
#import cobs._cobsext as cobs
# Pure Python
#import cobs._cobspy as cobs

test_strings = [
    b"",
    b"1",
    b"12345",
    b"12345\x006789",
    b"\x0012345\x006789",
    b"12345\x006789\x00",
    b"\x00",
    b"\x00\x00",
    b"\x00\x00\x00",
    bytes(bytearray(range(1, 254))),
    bytes(bytearray(range(1, 255))),
    bytes(bytearray(range(1, 256))),
    bytes(bytearray(range(0, 256))),
]

decode_error_test_strings = [
    b"\x00",
    b"\x05123",
]

def test():
    # Basic unit testing
    for test_string in test_strings:
        encoded = cobs.encode(test_string)
#        print(repr(encoded))
        if 1:
            try:
                decoded = cobs.decode(encoded)
            except Exception:
                print("Original:\n    %s\nEncoded:\n    %s" % (repr(test_string), repr(encoded)))
                raise
            if decoded != test_string:
                raise Exception("Original doesn't match with decoded. Original:\n    %s\nDecoded:\n    %s" % (repr(test_string), repr(decoded)))

    # Test decode errors
    for test_string in decode_error_test_strings:
        try:
            cobs.decode(test_string)
        except cobs.DecodeError:
            pass
        else:
            raise Exception("Didn't raise a DecodeError exception for string:\n    %s" % repr(test_string))

    print("All tests passed")

if __name__ == "__main__":
    test()
