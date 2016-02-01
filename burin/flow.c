#include <Python.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>


static PyObject *py_flow_lic(PyObject *self, PyObject *args) {
  PyArrayObject *vectors_array = NULL;
  double *vectors;
  npy_intp *shape;
  PyArray_Descr *dtype;

  if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &vectors_array)) return NULL;

  // check type and shape of observations array
  dtype = PyArray_DTYPE(vectors_array);
  if (dtype->type != 'd') {
    PyErr_SetString(PyExc_ValueError, "wrong type");
    return NULL;
  }

  if (PyArray_NDIM(vectors_array) != 2) {
    PyErr_SetString(PyExc_ValueError, "wrong number of dimensions");
    return NULL;
  }

  shape = PyArray_SHAPE(vectors_array);
//   if (shape[0] != 6) {
//     PyErr_SetString(PyExc_ValueError, "wrong number of filters");
//     return NULL;
//   }
//   if (shape[1] != 4) {
//     PyErr_SetString(PyExc_ValueError, "wrong number of polarization states");
//     return NULL;
//   }

  vectors = (double *) PyArray_DATA(vectors_array);

  return Py_BuildValue("i", 0);
}

static PyMethodDef flow_methods[] = {
  {"lic", py_flow_lic, METH_VARARGS, "Line-integral convolution implementation"},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initflow(void) {
  PyObject *m = Py_InitModule3("flow", flow_methods, "Flow routines.");
  if (m == NULL) return;
  import_array();
}
