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

// Make compatible with previous Python versions
#if PY_VERSION_HEX < 0x02050000
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif


#ifndef FALSE
#define FALSE       (0)
#endif

#ifndef TRUE
#define TRUE        (!FALSE)
#endif

#ifndef MIN
#define MIN(X,Y)    ((X) < (Y) ? (X) : (Y))
#endif


#define COBSR_ENCODE_DST_BUF_LEN_MAX(SRC_LEN)           ((SRC_LEN) + ((SRC_LEN)/254u) + 1)
#define COBSR_DECODE_DST_BUF_LEN_MAX(SRC_LEN)           (((SRC_LEN) <= 1) ? 1 : (SRC_LEN))


/*****************************************************************************
 * Variables
 ****************************************************************************/

/*
 * cobsr.DecodeError exception class.
 */
static PyObject *CobsrDecodeError;


/*****************************************************************************
 * Functions
 ****************************************************************************/

/*
 * Encode
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

static PyObject*
cobsr_encode(PyObject* self, PyObject* args)
{
    const char *    src_ptr;
    Py_ssize_t      src_len;
    const char *    src_end_ptr;
    char *          dst_buf_ptr;
    char *          dst_code_write_ptr;
    char *          dst_write_ptr;
    unsigned char   src_byte;
    unsigned char   search_len;
    PyObject *      dst_py_obj_ptr;


    if (!PyArg_ParseTuple(args, "s#:in_bytes", &src_ptr, &src_len))
    {
        return NULL;
    }
    src_end_ptr = src_ptr + src_len;

    /* Make an output string */
    dst_py_obj_ptr = PyString_FromStringAndSize(NULL, COBSR_ENCODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        return NULL;
    }
    dst_buf_ptr = PyString_AsString(dst_py_obj_ptr);

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
    _PyString_Resize(&dst_py_obj_ptr, dst_code_write_ptr - dst_buf_ptr);

    return dst_py_obj_ptr;
}


/*
 * Decode
 */
PyDoc_STRVAR(cobsr_decode__doc__,
    "Decode a string using Consistent Overhead Byte Stuffing/Reduced (COBS/R).\n"
    "\n"
    "Input should be a byte string that has been COBS/R encoded. Output\n"
    "is also a byte string.\n"
    "\n"
    "A cobsr.DecodeError exception will be raised if the encoded data\n"
    "is invalid. That is, if the encoded data contains zeros."
);

static PyObject*
cobsr_decode(PyObject* self, PyObject* args)
{
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


    if (!PyArg_ParseTuple(args, "s#:in_bytes", &src_ptr, &src_len))
    {
        return NULL;
    }
    src_end_ptr = src_ptr + src_len;

    /* Make an output string */
    dst_py_obj_ptr = PyString_FromStringAndSize(NULL, COBSR_DECODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        return NULL;
    }
    dst_buf_ptr = PyString_AsString(dst_py_obj_ptr);

    /* Decode */
    dst_write_ptr = dst_buf_ptr;

    if (src_len != 0)
    {
        for (;;)
        {
            len_code = (unsigned char) *src_ptr++;
            if (len_code == 0)
            {
                Py_DECREF(dst_py_obj_ptr);
                PyErr_SetString(CobsrDecodeError, "zero byte found in input");
                return NULL;
            }

            remaining_bytes = src_end_ptr - src_ptr;

            for (i = MIN(len_code - 1, remaining_bytes); i != 0; i--)
            {
                src_byte = *src_ptr++;
                if (src_byte == 0)
                {
                    Py_DECREF(dst_py_obj_ptr);
                    PyErr_SetString(CobsrDecodeError, "zero byte found in input");
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

    /* Calculate the output length, from the value of dst_code_write_ptr */
    _PyString_Resize(&dst_py_obj_ptr, dst_write_ptr - dst_buf_ptr);

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
    { "encode", cobsr_encode, METH_VARARGS, cobsr_encode__doc__ },
    { "decode", cobsr_decode, METH_VARARGS, cobsr_decode__doc__ },
    { NULL, NULL, 0, NULL }
};


/*****************************************************************************
 * Module initialisation
 ****************************************************************************/

PyMODINIT_FUNC
init_cobsr_ext(void)
{
    PyObject * module;

    /* Initialise cobsr module C extension cobsr._cobsr_ext */
    module = Py_InitModule3("_cobsr_ext", methodTable, module__doc__);
    if (module == NULL)
        return;

    /* Initialise cobsr.DecodeError exception class. */
    CobsrDecodeError = PyErr_NewException("_cobsr_ext.DecodeError", NULL, NULL);
    if (CobsrDecodeError == NULL)
    {
        Py_DECREF(module);
        return;
    }
    Py_INCREF(CobsrDecodeError);
    PyModule_AddObject(module, "DecodeError", CobsrDecodeError);
}

