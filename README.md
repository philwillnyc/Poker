

The goal of this project was to create a Texas Hold-em probabilities calculator from scratch: given information on all of the hands, and possibly community cards, compute the probability of each hand winning or tying. Initially written in python, the calculations were too slow in the most general case (no community cards yet shown), taking 60 seconds or so on a local machine. Caching seemed like a promising way to resolve this, but did not significantly reduce computation. Certainly some pruning techniques could be used to reduce the number of comparisons, but it seems that, especially in cases of more than 2 hands, the logic becomes too complex. At least, I do not see any strategies that would yield 60 fold or so reduction, which is what I was shooting for (so that calculations take at most one second). 

Instead, I decided to explore cython to speed up the brute force probability calculation. This reduced the computation time to less than half a second for 2 hand calculations, and a bit longer for larger numbers of hands, but always under 1 second. Further speed-ups could be accomplished by enabling multi-processing, but to do so would require restructuring the iteration in the main cython algorithm so that it can be done in parallel. This is quite do-able. Another potential speed up involves restructuring the cython algorithm to do hand rankings in parallel, so that, when one hand is the clear winner, the algorithm can move on to the next possibility.

The calculator is available [here](https://phillipwilliams.onrender.com/poker)


