# Word segmentation in a Bayesian framework
In this project, we implement the algorithm for word segmentation as proposed in:

Goldwater, S., Griffiths, T. L., & Johnson, M. (2009). A Bayesian framework for word segmentation: Exploring the effects of context. Cognition, 112(1), 21–54. doi:10.1016/j.cognition.2009.03.008

# Software
* Python 3.4
* Numpy / scipy
* ...

# Plan
The project consists of three big steps

1. **Initialization** (Valentin is working on that)
  * Insert random boundaries 
2. **Gibbs-sampling** (Bas is trying to make sense of that)
  *  for every iteration
    * for every line
      * for every possible boundary
        Compute $P(h_1 | h^-)$ and  $P(h_2 | h^-)$ and draw one of $h_1$ and $h_2$ according to their probabilities.
3. **Experiment**
  We have to think about this.

