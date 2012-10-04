/* Copyright 2012 Peter Williams
 * Licensed under the GNU General Public License version 3 or higher. 
 */

#include <Python.h>

static PyObject *
py_thingie (PyObject *self, PyObject *args)
{
    int foo;

    if (!PyArg_ParseTuple (args, "i", &foo))
	return NULL;

    return Py_BuildValue ("i", foo);
}

static PyMethodDef methods[] = {
#define DEF(name, signature) { #name, py_##name, METH_VARARGS, #name " " signature }
    DEF(thingie, "(int i) => int"),
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
__attribute__ ((visibility ("default")))
initprecastro (void)
{
    Py_InitModule("precastro", methods);

    /*
      PyObject *mod, *dict;
      mod = Py_InitModule("precastro", methods);
      dict = PyModule_GetDict (mod);
      PyDict_SetItemString (dict, "MiriadError", mts_exc_miriad_err);
    */
}
