/*
 * Consistent Overhead Byte Stuffing (COBS)
 *
 * Python C extension for COBS encoding and decoding functions.
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


#define GETSTATE(M) ((struct module_state *) PyModule_GetState(M))


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


#define COBS_ENCODE_DST_BUF_LEN_MAX(SRC_LEN)            ((SRC_LEN) + ((SRC_LEN)/254u) + 1)
#define COBS_DECODE_DST_BUF_LEN_MAX(SRC_LEN)            (((SRC_LEN) <= 1) ? 1 : ((SRC_LEN) - 1))


/*****************************************************************************
 * Types
 ****************************************************************************/

struct module_state
{
    /* cobs.DecodeError exception class. */
    PyObject * CobsDecodeError;
};


/*****************************************************************************
 * Functions
 ****************************************************************************/

static int cobs_traverse(PyObject *m, visitproc visit, void *arg)
{
    Py_VISIT(GETSTATE(m)->CobsDecodeError);
    return 0;
}


static int cobs_clear(PyObject *m)
{
    Py_CLEAR(GETSTATE(m)->CobsDecodeError);
    return 0;
}


/*
 * cobs.encode
 */
PyDoc_STRVAR(cobsencode__doc__,
"Encode a string using Consistent Overhead Byte Stuffing (COBS).\n"
"\n"
"Input is any byte string. Output is also a byte string.\n"
"\n"
"Encoding guarantees no zero bytes in the output. The output\n"
"string will be expanded slightly, by a predictable amount.\n"
"\n"
"An empty string is encoded to '\\x01'.");

/*
 * This Python C extension function uses arguments method METH_O,
 * meaning the arg parameter contains the single parameter
 * to the function.
 */
static PyObject*
cobsencode(PyObject* module, PyObject* arg)
{
    Py_buffer       src_py_buffer;
    const char *    src_ptr;
    Py_ssize_t      src_len;
    const char *    src_end_ptr;
    char *          dst_buf_ptr;
    char *          dst_code_write_ptr;
    char *          dst_write_ptr;
    char            src_byte;
    unsigned char   search_len;
    char            final_zero;
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
    dst_py_obj_ptr = PyBytes_FromStringAndSize(NULL, COBS_ENCODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        return NULL;
    }
    dst_buf_ptr = PyBytes_AsString(dst_py_obj_ptr);

    /* Encode */
    dst_code_write_ptr  = dst_buf_ptr;
    dst_write_ptr = dst_code_write_ptr + 1;
    search_len = 1;
    final_zero = TRUE;

    /* Iterate over the source bytes */
    while (src_ptr < src_end_ptr)
    {
        src_byte = *src_ptr++;
        if (src_byte == 0)
        {
            /* We found a zero byte */
            *dst_code_write_ptr = (char) search_len;
            dst_code_write_ptr = dst_write_ptr++;
            search_len = 1;
            final_zero = TRUE;
        }
        else
        {
            /* Copy the non-zero byte to the destination buffer */
            *dst_write_ptr++ = src_byte;
            search_len++;
            if (search_len == 0xFF)
            {
                /* We have a long string of non-zero bytes */
                *dst_code_write_ptr = (char) search_len;
                dst_code_write_ptr = dst_write_ptr++;
                search_len = 1;
                final_zero = FALSE;
            }
        }
    }

    /* We're done with the input buffer now, so we have to release the PyBuffer. */
    PyBuffer_Release(&src_py_buffer);

    /* We've reached the end of the source data (or possibly run out of output buffer)
     * Finalise the remaining output. In particular, write the code (length) byte.
     * Update the pointer to calculate the final output length.
     */
    if ((search_len > 1) || (final_zero != FALSE))
    {
        *dst_code_write_ptr = (char) search_len;
        dst_code_write_ptr = dst_write_ptr;
    }

    /* Calculate the output length, from the value of dst_code_write_ptr */
    _PyBytes_Resize(&dst_py_obj_ptr, dst_code_write_ptr - dst_buf_ptr);

    return dst_py_obj_ptr;
}


/*
 * cobs.decode
 */
PyDoc_STRVAR(cobsdecode__doc__,
"Decode a string using Consistent Overhead Byte Stuffing (COBS).\n"
"\n"
"Input should be a byte string that has been COBS encoded. Output\n"
"is also a byte string.\n"
"\n"
"A cobs.DecodeError exception may be raised if the encoded data\n"
"is invalid.");

/*
 * This Python C extension function uses arguments method METH_O,
 * meaning the arg parameter contains the single parameter
 * to the function.
 */
static PyObject*
cobsdecode(PyObject* module, PyObject* arg)
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
    dst_py_obj_ptr = PyBytes_FromStringAndSize(NULL, COBS_DECODE_DST_BUF_LEN_MAX(src_len));
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
                PyErr_SetString(GETSTATE(module)->CobsDecodeError, "zero byte found in input");
                return NULL;
            }
            len_code--;

            remaining_bytes = src_end_ptr - src_ptr;
            if (len_code > remaining_bytes)
            {
                PyBuffer_Release(&src_py_buffer);
                Py_DECREF(dst_py_obj_ptr);
                PyErr_SetString(GETSTATE(module)->CobsDecodeError, "not enough input bytes for length code");
                return NULL;
            }

            for (i = len_code; i != 0; i--)
            {
                src_byte = *src_ptr++;
                if (src_byte == 0)
                {
                    PyBuffer_Release(&src_py_buffer);
                    Py_DECREF(dst_py_obj_ptr);
                    PyErr_SetString(GETSTATE(module)->CobsDecodeError, "zero byte found in input");
                    return NULL;
                }
                *dst_write_ptr++ = src_byte;
            }

            if (src_ptr >= src_end_ptr)
            {
                break;
            }

            /* Add a zero to the end */
            if (len_code != 0xFE)
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
"Consistent Overhead Byte Stuffing (COBS)"
);

static PyMethodDef methodTable[] =
{
    { "encode", cobsencode, METH_O, cobsencode__doc__ },
    { "decode", cobsdecode, METH_O, cobsdecode__doc__ },
    { NULL, NULL, 0, NULL }
};


static struct PyModuleDef moduleDef =
{
    PyModuleDef_HEAD_INIT,
    "_cobsext",                     // name of module
    module__doc__,                  // module documentation
    sizeof(struct module_state),    // size of per-interpreter state of the module,
    methodTable,
    NULL,
    cobs_traverse,
    cobs_clear,
    NULL
};


/*****************************************************************************
 * Module initialisation
 ****************************************************************************/

PyMODINIT_FUNC
PyInit__cobsext(void)
{
    PyObject *              module;
    struct module_state *   st;


    /* Initialise cobs module C extension cobs._cobsext */
    module = PyModule_Create(&moduleDef);
    if (module == NULL)
    {
        return NULL;
    }

    st = GETSTATE(module);

    /* Initialise cobs.DecodeError exception class. */
    st->CobsDecodeError = PyErr_NewException("cobs.DecodeError", NULL, NULL);
    if (st->CobsDecodeError == NULL)
    {
        Py_DECREF(module);
        return NULL;
    }
    PyModule_AddObject(module, "DecodeError", st->CobsDecodeError);

    return module;
}

