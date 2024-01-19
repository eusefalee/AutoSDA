# This file defins a function that iteratively fits a series of data points with multiple straight lines.
# Originally taken from the following website:
# https://datascience.stackexchange.com/questions/8457/python-library-for-segmented-regression-a-k-a-piecewise-regression
# Reference:
# Muggeo, V. M. (2003). Estimating regression models with unknown breakpoints. Statistics in medicine, 22(19), 3055-3071.
# Adapted by GUAN, XINGQUAN in Sept. 2019 @ UCLA.

# Import necessary packages (make sure those packages are pre-installed on your PC)
import numpy as np
from numpy.linalg import lstsq

# Two predefined functions which will be used later
ramp = lambda u: np.maximum( u, 0 )
step = lambda u: ( u > 0 ).astype(float)

def segmented_linear_regression( X, Y, breakpoints, maximum_iteration=5000 ):
    """
    This function uses multiple straight lines to fit a series of data points.
    :param X: a list to denote the X coordinate of data points.
    :param Y: a list to denote the Y coordinate of data points.
              Note that X and Y should have the same length.
    :param breakpoints: a list which denote the X coordinates for initial breakpoints.
                                Suppose the user wants to use three straight lines to fit the data, then this list should have two element.
                                The first element is the X coordinate which separates the first stragight line and second line.
                                The second element is the X coordinate which separates the second straight line with the last line segment.
    :param maximum_iteration: an integer to denote the maximum iteration times. After this number, the function stops iterations.
    :return X_solution, Y_solution, breakpoints:
    X_solution: X coordinates for starting and ending points of fitted straight lines.
    Y_solution: Y coordinates for starting and ending points of fitted straight lines.
    """
    # Sort the initialized breakpoints (if they are not input as a sorted array/list).
    breakpoints = np.sort( np.array(breakpoints) )

    dt = np.min( np.diff(X) )
    ones = np.ones_like(X)

    for i in range( 0, maximum_iteration ):
        # Linear regression:  solve A*p = Y
        Rk = [ramp( X - xk ) for xk in breakpoints ]
        Sk = [step( X - xk ) for xk in breakpoints ]
        A = np.array([ ones, X ] + Rk + Sk )
        p =  lstsq(A.transpose(), Y, rcond=None)[0] 

        # Parameters identification:
        a, b = p[0:2]
        ck = p[ 2:2+len(breakpoints) ]
        dk = p[ 2+len(breakpoints): ]

        # Estimation of the next break-points:
        newBreakpoints = breakpoints - dk/ck 

        # Stop condition
        if np.max(np.abs(newBreakpoints - breakpoints)) < dt/5:
            break

        breakpoints = newBreakpoints
    else:
        print( 'maximum iteration reached' )

    # Compute the final segmented fit:
    Xsolution = np.insert( np.append( breakpoints, max(X) ), 0, min(X) )
    ones =  np.ones_like(Xsolution) 
    Rk = [ c*ramp( Xsolution - x0 ) for x0, c in zip(breakpoints, ck) ]

    Ysolution = a*ones + b*Xsolution + np.sum( Rk, axis=0 )
    
    return Xsolution, Ysolution