/*
 * Consistent Overhead Byte Stuffing/Reduced (COBS/R)
 *
 * Python C extension for COBS/R encoding and decoding functions.
 *
 * Copyright (c) 2010 Craig McQueen
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */


/*****************************************************************************
 * Includes
 ****************************************************************************/

// Force Py_ssize_t to be used for s# conversions.
#define PY_SSIZE_T_CLEAN
#include <Python.h>


/*****************************************************************************
 * Defines
 ****************************************************************************/

#ifndef FALSE
#define FALSE       (0)
#endif

#ifndef TRUE
#define TRUE        (!FALSE)
#endif

#ifndef MIN
#define MIN(X,Y)    ((X) < (Y) ? (X) : (Y))
#endif


/*
 * Given a PyObject* obj, fill in the Py_buffer* viewp with the result
 * of PyObject_GetBuffer.  Sets and exception and issues a return NULL
 * on any errors.
 */
#define GET_BUFFER_VIEW_OR_ERROUT(obj, viewp) do { \
        if (!PyObject_CheckBuffer((obj))) { \
            PyErr_SetString(PyExc_TypeError, \
                            "object supporting the buffer API is required"); \
            return NULL; \
        } \
        if (PyObject_GetBuffer((obj), (viewp), PyBUF_FORMAT) == -1) { \
            return NULL; \
        } \
        if (((viewp)->ndim > 1) || ((viewp)->itemsize > 1)) { \
            PyErr_SetString(PyExc_BufferError, \
                            "object must be a single-dimension buffer of bytes"); \
            PyBuffer_Release((viewp)); \
            return NULL; \
        } \
    } while(0);


#define COBSR_ENCODE_DST_BUF_LEN_MAX(SRC_LEN)           ((SRC_LEN) + ((SRC_LEN)/254u) + 1)
#define COBSR_DECODE_DST_BUF_LEN_MAX(SRC_LEN)           (((SRC_LEN) <= 1) ? 1 : (SRC_LEN))


/*****************************************************************************
 * Functions
 ****************************************************************************/

/*
 * cobsr.encode
 */
PyDoc_STRVAR(cobsr_encode__doc__,
    "Encode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).\n"
    "\n"
    "Input is any byte string. Output is also a byte string.\n"
    "\n"
    "Encoding guarantees no zero bytes in the output. The output\n"
    "string may be expanded slightly, by a predictable amount.\n"
    "\n"
    "An empty string is encoded to '\\x01'."
);

/*
 * This Python C extension function uses arguments method METH_O,
 * meaning the arg parameter contains the single parameter
 * to the function.
 */
static PyObject*
cobsr_encode(PyObject* module, PyObject* arg)
{
    Py_buffer       src_py_buffer;
    const char *    src_ptr;
    Py_ssize_t      src_len;
    const char *    src_end_ptr;
    char *          dst_buf_ptr;
    char *          dst_code_write_ptr;
    char *          dst_write_ptr;
    unsigned char   src_byte;
    unsigned char   search_len;
    PyObject *      dst_py_obj_ptr;


    if (PyUnicode_Check((arg)))
    {
        PyErr_SetString(PyExc_TypeError,
                        "Unicode-objects must be encoded as bytes first");
        return NULL;
    }
    GET_BUFFER_VIEW_OR_ERROUT(arg, &src_py_buffer);
    src_ptr = src_py_buffer.buf;
    src_len = src_py_buffer.len;

    src_end_ptr = src_ptr + src_len;

    /* Make an output string */
    dst_py_obj_ptr = PyBytes_FromStringAndSize(NULL, COBSR_ENCODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        return NULL;
    }
    dst_buf_ptr = PyBytes_AsString(dst_py_obj_ptr);

    /* Encode */
    dst_code_write_ptr  = dst_buf_ptr;
    dst_write_ptr = dst_code_write_ptr + 1;
    search_len = 1;
    src_byte = 0;

    /* Iterate over the source bytes */
    if (src_ptr < src_end_ptr)
    {
        for (;;)
        {
            src_byte = *src_ptr++;
            if (src_byte == 0)
            {
                /* We found a zero byte */
                *dst_code_write_ptr = (char) search_len;
                dst_code_write_ptr = dst_write_ptr++;
                search_len = 1;
                if (src_ptr >= src_end_ptr)
                {
                    break;
                }
            }
            else
            {
                /* Copy the non-zero byte to the destination buffer */
                *dst_write_ptr++ = src_byte;
                search_len++;
                if (src_ptr >= src_end_ptr)
                {
                    break;
                }
                if (search_len == 0xFF)
                {
                    /* We have a long string of non-zero bytes */
                    *dst_code_write_ptr = (char) search_len;
                    dst_code_write_ptr = dst_write_ptr++;
                    search_len = 1;
                }
            }
        }
    }

    /* We're done with the input buffer now, so we have to release the PyBuffer. */
    PyBuffer_Release(&src_py_buffer);

    /* We've reached the end of the source data.
     * Finalise the remaining output. In particular, write the code (length) byte.
     *
     * For COBS/R, the final code (length) byte is special: if the final data byte is
     * greater than or equal to what would normally be the final code (length) byte,
     * then replace the final code byte with the final data byte, and remove the final
     * data byte from the end of the sequence. This saves one byte in the output.
     *
     * Update the pointer to calculate the final output length.
     */
    if (src_byte < search_len)
    {
        /* Encoding same as plain COBS */
        *dst_code_write_ptr = (char) search_len;
        dst_code_write_ptr = dst_write_ptr;
    }
    else
    {
        /* Special COBS/R encoding: length code is final byte,
         * and final byte is removed from data sequence. */
        *dst_code_write_ptr = (char) src_byte;
        dst_code_write_ptr = dst_write_ptr - 1;
    }

    /* Calculate the output length, from the value of dst_code_write_ptr */
    _PyBytes_Resize(&dst_py_obj_ptr, dst_code_write_ptr - dst_buf_ptr);

    return dst_py_obj_ptr;
}


/*
 * cobsr.decode
 */
PyDoc_STRVAR(cobsr_decode__doc__,
    "Decode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).\n"
    "\n"
    "Input should be a byte string that has been COBS/R encoded. Output\n"
    "is also a byte string.\n"
    "\n"
    "A ValueError exception will be raised if the encoded data\n"
    "is invalid. That is, if the encoded data contains zeros."
);

/*
 * This Python C extension function uses arguments method METH_O,
 * meaning the arg parameter contains the single parameter
 * to the function.
 */
static PyObject*
cobsr_decode(PyObject* module, PyObject* arg)
{
    Py_buffer               src_py_buffer;
    const char *            src_ptr;
    Py_ssize_t              src_len;
    const char *            src_end_ptr;
    char *                  dst_buf_ptr;
    char *                  dst_write_ptr;
    Py_ssize_t              remaining_bytes;
    unsigned char           len_code;
    unsigned char           src_byte;
    unsigned char           i;
    PyObject *              dst_py_obj_ptr;


    if (PyUnicode_Check((arg)))
    {
        PyErr_SetString(PyExc_TypeError,
                        "Unicode-objects are not supported; byte buffer objects only");
        return NULL;
    }
    GET_BUFFER_VIEW_OR_ERROUT(arg, &src_py_buffer);
    src_ptr = src_py_buffer.buf;
    src_len = src_py_buffer.len;

    src_end_ptr = src_ptr + src_len;

    /* Make an output string */
    dst_py_obj_ptr = PyBytes_FromStringAndSize(NULL, COBSR_DECODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        PyBuffer_Release(&src_py_buffer);
        return NULL;
    }
    dst_buf_ptr = PyBytes_AsString(dst_py_obj_ptr);

    /* Decode */
    dst_write_ptr = dst_buf_ptr;

    if (src_len != 0)
    {
        for (;;)
        {
            len_code = (unsigned char) *src_ptr++;
            if (len_code == 0)
            {
                PyBuffer_Release(&src_py_buffer);
                Py_DECREF(dst_py_obj_ptr);
                PyErr_SetString(PyExc_ValueError, "zero byte found in input");
                return NULL;
            }

            remaining_bytes = src_end_ptr - src_ptr;

            for (i = MIN(len_code - 1, remaining_bytes); i != 0; i--)
            {
                src_byte = *src_ptr++;
                if (src_byte == 0)
                {
                    PyBuffer_Release(&src_py_buffer);
                    Py_DECREF(dst_py_obj_ptr);
                    PyErr_SetString(PyExc_ValueError, "zero byte found in input");
                    return NULL;
                }
                *dst_write_ptr++ = src_byte;
            }

            if (len_code - 1 > remaining_bytes)
            {
                *dst_write_ptr++ = len_code;
            }

            if (src_ptr >= src_end_ptr)
            {
                break;
            }

            /* Add a zero to the end */
            if (len_code != 0xFF)
            {
                *dst_write_ptr++ = 0;
            }
        }
    }

    /* We're done with the input buffer now, so we have to release the PyBuffer. */
    PyBuffer_Release(&src_py_buffer);

    /* Calculate the output length, from the value of dst_code_write_ptr */
    _PyBytes_Resize(&dst_py_obj_ptr, dst_write_ptr - dst_buf_ptr);

    return dst_py_obj_ptr;
}


/*****************************************************************************
 * Module definitions
 ****************************************************************************/

PyDoc_STRVAR(module__doc__,
    "Consistent Overhead Byte Stuffing/Reduced (COBS/R)"
);

static PyMethodDef methodTable[] =
{
    { "encode", cobsr_encode, METH_O, cobsr_encode__doc__ },
    { "decode", cobsr_decode, METH_O, cobsr_decode__doc__ },
    { NULL, NULL, 0, NULL }
};


static struct PyModuleDef moduleDef =
{
    PyModuleDef_HEAD_INIT,
    "_cobsr_ext",                   // name of module
    module__doc__,                  // module documentation
    -1,                             // size of per-interpreter state of the module,
                                    // or -1 if the module keeps state in global variables.
    methodTable,
    NULL,
    NULL,
    NULL,
    NULL
};


/*****************************************************************************
 * Module initialisation
 ****************************************************************************/

PyMODINIT_FUNC
PyInit__cobsr_ext(void)
{
    PyObject * module;


    /* Initialise cobsr module C extension cobsr._cobsr_ext */
    module = PyModule_Create(&moduleDef);

    return module;
}

