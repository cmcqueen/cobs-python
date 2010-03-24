"""
Consistent Overhead Byte Stuffing (COBS)

This version is for Python 2.x.
"""


class DecodeError(Exception):
    pass


def encode(in_bytes):
    """Encode a string using Consistent Overhead Byte Stuffing (COBS).
    
    Input is any byte string. Output is also a byte string.
    
    Encoding guarantees no zero bytes in the output. The output
    string will be expanded slightly, by a predictable amount.
    
    An empty string is encoded to '\\x01'"""
    final_zero = True
    out_bytes = []
    idx = 0
    search_start_idx = 0
    for in_char in in_bytes:
        if in_char == '\x00':
            final_zero = True
            out_bytes.append(chr(idx - search_start_idx + 1))
            out_bytes.append(in_bytes[search_start_idx:idx])
            search_start_idx = idx + 1
        else:
            if idx - search_start_idx == 0xFD:
                final_zero = False
                out_bytes.append('\xFF')
                out_bytes.append(in_bytes[search_start_idx:idx+1])
                search_start_idx = idx + 1
        idx += 1
    if idx != search_start_idx or final_zero:
        out_bytes.append(chr(idx - search_start_idx + 1))
        out_bytes.append(in_bytes[search_start_idx:idx])
    return ''.join(out_bytes)


def decode(in_bytes):
    """Decode a string using Consistent Overhead Byte Stuffing (COBS).
    
    Input should be a byte string that has been COBS encoded. Output
    is also a byte string.
    
    A cobs.DecodeError exception may be raised if the encoded data
    is invalid."""
    out_bytes = []
    idx = 0

    if len(in_bytes) > 0:
        while True:
            length = ord(in_bytes[idx])
            if length == 0:
                raise DecodeError("zero byte found in input")
            idx += 1
            end = idx + length - 1
            copy_bytes = in_bytes[idx:end]
            if '\x00' in copy_bytes:
                raise DecodeError("zero byte found in input")
            out_bytes.append(copy_bytes)
            idx = end
            if idx > len(in_bytes):
                raise DecodeError("not enough input bytes for length code")
            if idx < len(in_bytes):
                if length < 0xFF:
                    out_bytes.append('\x00')
            else:
                break
    return ''.join(out_bytes)
