/* Copyright 2012 Peter Williams
 * Licensed under the GNU General Public License version 3 or higher.
 */

#include <Python.h>

#include "novas.h"
#include "sofa.h"

static PyObject *novas_err = NULL;

static PyObject *
py_novas_astro_star (PyObject *self, PyObject *args)
{
    cat_entry star = {{0}};
    double jdtt, rares, decres;
    short int err;

    if (!PyArg_ParseTuple (args, "ddddddd", &jdtt, &star.ra, &star.dec,
			   &star.promora, &star.promodec,
			   &star.parallax, &star.radialvelocity))
	return NULL;

    if ((err = astro_star (jdtt, &star, 0, &rares, &decres))) {
	PyErr_Format (novas_err, "NOVAS error code %d", err);
	return NULL;
    }

    return Py_BuildValue ("dd", rares, decres);
}

static PyMethodDef methods[] = {
#define DEF(name, signature) { #name, py_##name, METH_VARARGS, #name " " signature }
    DEF(novas_astro_star, "(jdtt, ra, dec, promora, promodec, parallax, rv) => (ra, dec)"),
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
__attribute__ ((visibility ("default")))
initprecastro (void)
{
    PyObject *mod, *dict;

    novas_err = PyErr_NewException ("precastro.NovasError", NULL, NULL);
    mod = Py_InitModule("precastro", methods);
    dict = PyModule_GetDict (mod);
    PyDict_SetItemString (dict, "NovasError", novas_err);
}
