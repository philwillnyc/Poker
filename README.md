Dependencies:


-Cython
-Flask

To run, first complile the cython code with:

python setup.py build_ext --inplace

Then run:

python interface.py

This launches the development flask server and then you can access the interface through a web browser. 

The goal of this project was to create a Texas Hold-em probabilities calculator from scratch: given information on all of the hands, and possibly community cards, compute the probability of each hand winning or tying. Initially written in python, the calculations were too slow in the most general case (no community cards yet shown), taking 60 seconds or so on my local machine. Caching seemed like a promising way to resolve this, but did not prove very effective. Certainly some pruning techniques could be used to reduce the number of comparisons, but it seems that, especially in cases of more than 2 hands, the logic becomes too complex. At least, I did not see any strategies that would yield 60 fold or so reduction, which is what I was shooting for (so that calculations take at most one second). 

Instead, I decided to explore cython. This reduced the computation time to less than half a second for 2 hand calculations, and a bit longer for larger numbers of hands, but always under 1 second. Further speedups could be accomplished by enabling multi-processing, but to do so would require restructuring the iteration in the main cython algorithm so that it can be done in parallel. This is quite do-able. 