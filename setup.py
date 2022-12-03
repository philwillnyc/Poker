#to rebuild, run:
#python setup.py build_ext --inplace
from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Hold-em algorithms',
    ext_modules=cythonize("algorithms.pyx"),
    zip_safe=False,
)