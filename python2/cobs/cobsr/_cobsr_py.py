"""
Consistent Overhead Byte Stuffing/Reduced (COBS/R)

This version is for Python 2.x.
"""


def encode(in_bytes):
    """Encode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).
    
    Input is any byte string. Output is also a byte string.
    
    Encoding guarantees no zero bytes in the output. The output
    string may be expanded slightly, by a predictable amount.
    
    An empty string is encoded to '\\x01'"""
    out_bytes = []
    idx = 0
    search_start_idx = 0
    for in_char in in_bytes:
        if idx - search_start_idx == 0xFE:
            out_bytes.append('\xFF')
            out_bytes.append(in_bytes[search_start_idx:idx])
            search_start_idx = idx
        if in_char == '\x00':
            out_bytes.append(chr(idx - search_start_idx + 1))
            out_bytes.append(in_bytes[search_start_idx:idx])
            search_start_idx = idx + 1
        idx += 1
    try:
        final_byte = in_bytes[-1]
    except IndexError:
        final_byte = '\x00'
    length_value = idx - search_start_idx + 1
    if ord(final_byte) < length_value:
        # Encoding same as plain COBS
        out_bytes.append(chr(length_value))
        out_bytes.append(in_bytes[search_start_idx:idx])
    else:
        # Special COBS/R encoding: length code is final byte,
        # and final byte is removed from data sequence.
        out_bytes.append(final_byte)
        out_bytes.append(in_bytes[search_start_idx:idx - 1])
    return ''.join(out_bytes)


def decode(in_bytes):
    """Decode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).
    
    Input should be a byte string that has been COBS/R encoded. Output
    is also a byte string.
    
    A ValueError exception will be raised if the encoded data
    is invalid. That is, if the encoded data contains zeros."""
    out_bytes = []
    idx = 0

    if len(in_bytes) > 0:
        while True:
            length = ord(in_bytes[idx])
            if length == 0:
                raise ValueError("zero byte found in input")
            idx += 1
            end = idx + length - 1
            copy_bytes = in_bytes[idx:end]
            if '\x00' in copy_bytes:
                raise ValueError("zero byte found in input")
            out_bytes.append(copy_bytes)
            idx = end
            if idx > len(in_bytes):
                out_bytes.append(chr(length))
                break
            elif idx < len(in_bytes):
                if length < 0xFF:
                    out_bytes.append('\x00')
            else:
                break
    return ''.join(out_bytes)
