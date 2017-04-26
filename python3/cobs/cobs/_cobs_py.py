"""
Consistent Overhead Byte Stuffing (COBS)

This version is for Python 3.x.
"""


class DecodeError(Exception):
    pass


def _get_buffer_view(in_bytes):
    mv = memoryview(in_bytes)
    if mv.ndim > 1 or mv.itemsize > 1:
        raise BufferError('object must be a single-dimension buffer of bytes.')
    try:
        mv = mv.cast('c')
    except AttributeError:
        pass
    return mv

def encode(in_bytes):
    """Encode a string using Consistent Overhead Byte Stuffing (COBS).
    
    Input is any byte string. Output is also a byte string.
    
    Encoding guarantees no zero bytes in the output. The output
    string will be expanded slightly, by a predictable amount.
    
    An empty string is encoded to '\\x01'"""
    if isinstance(in_bytes, str):
        raise TypeError('Unicode-objects must be encoded as bytes first')
    in_bytes_mv = _get_buffer_view(in_bytes)
    final_zero = True
    out_bytes = bytearray()
    idx = 0
    search_start_idx = 0
    for in_char in in_bytes_mv:
        if in_char == b'\x00':
            final_zero = True
            out_bytes.append(idx - search_start_idx + 1)
            out_bytes += in_bytes_mv[search_start_idx:idx]
            search_start_idx = idx + 1
        else:
            if idx - search_start_idx == 0xFD:
                final_zero = False
                out_bytes.append(0xFF)
                out_bytes += in_bytes_mv[search_start_idx:idx+1]
                search_start_idx = idx + 1
        idx += 1
    if idx != search_start_idx or final_zero:
        out_bytes.append(idx - search_start_idx + 1)
        out_bytes += in_bytes_mv[search_start_idx:idx]
    return bytes(out_bytes)


def decode(in_bytes):
    """Decode a string using Consistent Overhead Byte Stuffing (COBS).
    
    Input should be a byte string that has been COBS encoded. Output
    is also a byte string.
    
    A cobs.DecodeError exception will be raised if the encoded data
    is invalid."""
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
                raise DecodeError("not enough input bytes for length code")
            if idx < len(in_bytes_mv):
                if length < 0xFF:
                    out_bytes.append(0)
            else:
                break
    return bytes(out_bytes)
