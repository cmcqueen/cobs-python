"""
Consistent Overhead Byte Stuffing/Reduced (COBS/R)

This version is for Python 3.x.
"""


class DecodeError(Exception):
    pass


def _get_buffer_view(in_bytes):
    mv = memoryview(in_bytes)
    if mv.ndim > 1 or mv.itemsize > 1:
        raise BufferError('object must be a single-dimension buffer of bytes.')
    return mv

def encode(in_bytes):
    """Encode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).
    
    Input is any byte string. Output is also a byte string.
    
    Encoding guarantees no zero bytes in the output. The output
    string may be expanded slightly, by a predictable amount.
    
    An empty string is encoded to '\\x01'"""
    if isinstance(in_bytes, str):
        raise TypeError('Unicode-objects must be encoded as bytes first')
    in_bytes_mv = _get_buffer_view(in_bytes)
    out_bytes = bytearray()
    idx = 0
    search_start_idx = 0
    for in_char in in_bytes_mv:
        if idx - search_start_idx == 0xFE:
            out_bytes.append(0xFF)
            out_bytes += in_bytes_mv[search_start_idx:idx]
            search_start_idx = idx
        if in_char == b'\x00':
            out_bytes.append(idx - search_start_idx + 1)
            out_bytes += in_bytes_mv[search_start_idx:idx]
            search_start_idx = idx + 1
        idx += 1
    try:
        final_byte_value = ord(in_bytes_mv[-1])
    except IndexError:
        final_byte_value = 0
    length_value = idx - search_start_idx + 1
    if final_byte_value < length_value:
        # Encoding same as plain COBS
        out_bytes.append(length_value)
        out_bytes += in_bytes_mv[search_start_idx:idx]
    else:
        # Special COBS/R encoding: length code is final byte,
        # and final byte is removed from data sequence.
        out_bytes.append(final_byte_value)
        out_bytes += in_bytes_mv[search_start_idx:idx - 1]
    return bytes(out_bytes)


def decode(in_bytes):
    """Decode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).
    
    Input should be a byte string that has been COBS/R encoded. Output
    is also a byte string.
    
    A cobsr.DecodeError exception will be raised if the encoded data
    is invalid. That is, if the encoded data contains zeros."""
    if isinstance(in_bytes, str):
        raise TypeError('Unicode-objects are not supported; byte buffer objects only')
    in_bytes_mv = _get_buffer_view(in_bytes)
    out_bytes = bytearray()
    idx = 0

    if len(in_bytes_mv) > 0:
        while True:
            length = ord(in_bytes_mv[idx])
            if length == 0:
                raise DecodeError("zero byte found in input")
            idx += 1
            end = idx + length - 1
            copy_mv = in_bytes_mv[idx:end]
            if b'\x00' in copy_mv:
                raise DecodeError("zero byte found in input")
            out_bytes += copy_mv
            idx = end
            if idx > len(in_bytes_mv):
                out_bytes.append(length)
                break
            elif idx < len(in_bytes_mv):
                if length < 0xFF:
                    out_bytes.append(0)
            else:
                break
    return bytes(out_bytes)
