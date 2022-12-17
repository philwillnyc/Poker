Dependencies:
-Cython
-Flask

To run, first complile the cython code with:

python setup.py build_ext --inplace

Then run:

python interface.py

This launches the development flask server from which you can access the interface. 