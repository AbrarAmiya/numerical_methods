# -*- coding: utf-8 -*-
"""Hermite_and_Newtons_Divided_Difference_Interpolation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1js5raG6II8u1GfgA_zu1JP_N9WnT8IqS

Make sure you remove `raise NotImplementedError()` and fill in any place that says `# YOUR CODE HERE`, as well as your `NAME`, `ID`, and `SECTION` below:
"""

NAME = "Md. Abrar-ud-doula Amiya"
ID = "21301567"
SECTION = "07"

"""---

# Part 1: Hermite Interpolation
---
Hermite Interpolation is an example of a variant of the interpolation problem, where the interpolant matches one or more **derivatives of $f$**  at each of the nodes, in addition to the function values.

## Importing the necessary libraries
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from numpy.polynomial import Polynomial

P=Polynomial([1,2,3,4])

print(P.deriv(1))

"""## Creating the components for Hermite interpolation

For the case of Hermite Interpolation, we look for a polynomial that matches both $f'(x_i)$ and $f(x_i)$ at the nodes $x_i = x_0,\dots,x_n$. Say you have $n+1$ data points, $(x_0, y_0), (x_1, y_1), x_2, y_2), \dots, (x_n, y_n)$ and you happen to know the first-order derivative at all of these points, namely, $(x_0, y_0 ^\prime ), (x_1, y_1 ^\prime ), x_2, y_2 ^\prime ), \dots ,(x_n, y_n ^\prime )$. According to hermite interpolation, since there are $2n + 2$ conditions; $n+1$ for $f(x_i)$ plus $n+1$ for $f'(x_i)$; you can fit a polynomial of order $2n+1$.

General form of a $2n+1$ degree Hermite polynomial:

$$p_{2n+1} = \sum_{k=0}^{n} \left(f(x_k)h_k(x) + f'(x_k)\hat{h}_k(x)\right), \tag{1}$$

where $h_k$ and $\hat{h}_k$ are defined using Lagrange basis functions by the following equations:

$$h_k(x) = (1-2(x-x_k)l^\prime_k(x_k))l^2_k(x_k), \tag{2}$$

and

$$\hat{h}_k(x) = (x-x_k)l^2_k(x), \tag{3}$$

where the Lagrange basis function being:

$$l_k(x) = \prod_{j=0, j\neq k}^{n} \frac{x-x_j}{x_k-x_j}. \tag{4}$$

**Note** that, we can rewrite Equation $(2)$ in this way,

\begin{align}
h_k(x) &= \left(1-2(x-x_k)l^\prime_k(x_k) \right)l^2_k(x) \\
&= \left(1 - 2xl^\prime_k(x_k) + 2x_kl^\prime_k(x_k) \right)l^2_k(x) \\
&= \left(1 + 2x_kl^\prime_k(x_k) - 2l'_k(x_k)x \right) l^2_k(x) \tag{5}
\end{align}
Replacing $l^\prime_k(x_k)$ with $m$, we get:
$$h_k(x) = (1 - 2xm + 2x_km)l^2_k(x). \tag{6}$$

# Tasks:

* The functions: `l(k, x)`, `h(k, x)` and `h_hat(k, x)` calculate the corresponding $l_k$, $h_k$, and $\hat{h}_k$, respectively.

* Function `l(k, x)` has already been defined for you. Your task is to complete the `h(k, x)`, `h_hat(k, x)`, and `hermit(x, y, y_prime)` functions.

* Later we will draw some plots to check if the code is working.

---

### Part 1: Calculate $l_k$
This function uses the following equation to calculate $l_k(x)$ and returns a polynomial:

$$l_k(x) = \prod_{j=0, j\neq k}^{n} \frac{x-x_j}{x_k-x_j}.$$
"""

# Already written for you.

def l(k, x):
    n = len(x)
    assert (k < len(x))

    x_k = x[k]
    x_copy = np.delete(x, k)

    denominator = np.prod(x_copy - x_k)

    coeff = []

    for i in range(n):
        coeff.append(sum([np.prod(x) for x in combinations(x_copy, i)]) * (-1)**(i) / denominator)

    coeff.reverse()

    return Polynomial(coeff)

"""### Part 2: Calculate $h_k$
This function calculates $h_k(x)$ using the following equation:
$$h_k(x) = \left(1 + 2x_kl^\prime_k(x_k) - 2l'_k(x_k)x \right) l^2_k(x_k).$$

This equation is basically a multiplication of two polynomials.

First polynomial: $1 + 2x_kl^\prime_k(x_k) - 2l'_k(x_k)x$.

Second polynomial: $l^2_k(x_k)$.

The `coeff` variable should contain a python list of coefficient values for the **first** polynomial of the equation. These coefficient values are used to create a polynomial `p`.
"""

def h(k, x):
    # initialize with None. Replace with appropriate values/function calls
    l_k = l(k,x)
    l_k_sqr = l_k**2
    l_k_prime = l_k.deriv(1)
    coeff = [1+2*x[k]*(l_k_prime(x[k])),-2*(l_k_prime(x[k]))]
    p = Polynomial(coeff)

    # --------------------------------------------
    # # YOUR CODE HERE
    # raise NotImplementedError()
    # --------------------------------------------

    return p * l_k_sqr

# Test case for the h(k, x) function
x = [3, 5, 7, 9]
k = 2
h_test = h(k, [3, 5, 7, 9])
h_result = Polynomial([-2.5, 0.5]) * (l(k, x) ** 2)

assert Polynomial.has_samecoef(h_result, h_test)
assert h_result == h_test

"""### Part 3: Calculate $\hat{h}_k$
This function calculates $\hat{h}_k(x)$ using the following equation:

$$\hat{h}_k(x) = (x-x_k)l^2_k(x_k).$$

This equation is also a multiplication of two polynomials.

First polynomial: $x-x_k$.

Second polynomial:  $l^2_k(x_k)$.

The `coeff` variable should contain a python list of coefficient values for the **first** polynomial of the equation. These coefficient values are used to create a polynomial `p`.
"""

def h_hat(k, x):
    # Initialize with none
    l_k = l(k,x)
    l_k_sqr = l_k*l_k
    coeff = [-x[k],1]
    p = Polynomial(coeff)

    # --------------------------------------------
    # YOUR CODE HERE
    # raise NotImplementedError()
    # --------------------------------------------

    return p * l_k_sqr

x = [3, 5, 7, 9]
k = 2
h_test = h_hat(k, [3, 5, 7, 9])
h_result = Polynomial([-7, 1]) * (l(k, x) ** 2)

assert Polynomial.has_samecoef(h_result, h_test)
assert h_result == h_test

"""### Part 4: The Hermite Polynomial
This function uses the following equation:

$$p_{2n+1} = \sum_{k=0}^{n} \left(f(x_k)h_k(x) + f'(x_k)\hat{h}_k(x)\right).$$

The polynomial denoted by the equation is calculated by the variable `f`.
"""

def hermit(x, y, y_prime):
    assert len(x) == len(y)
    assert len(y) == len(y_prime)

    f = None
    # --------------------------------------------
    # YOUR CODE HERE
    f = Polynomial([0.0])
    for i in range(len(x)):
      f +=((y[i]*h(i,x)) + (y_prime[i] * h_hat(i,x)))

    # --------------------------------------------
    return f

"""## Testing our methods by plotting graphs.

**Note:**

* For each of the 5 plots, there will be 2 curves plotted: one being the original function, and the other being the interpolated curve.

* The original functions are displayed in orange color, while the hermite interpolated curves are in blue.

* `x`, `y`, and `y_prime` contain $x_i$, $f(x_i)$, and $f'(x_i)$ of the given nodes of the original function $f$.

Upon calling the `hermit()` function, it returns a polynomial `f`. For example, for plot 1, it is called `f3`.

In general, a polynomial may look like the following: $f = 1 + 2x + 3x^2$. Next, we pass in a number of $x$ values to the polynomial by calling the `.linspace()` function on the polynomial object using `f.linspace()`. This function outputs a tuple, which is stored in a variable called `data`. First element of `data` contains a 1D numpy array of $x_i$ values generated by `linspace()`, and the second element of `data` contains a 1D numpy array of the corresponding $y_i$ values outputted by our example polynomial:
$f = 1 + 2x + 3x^2$.

Using `test_x`, we generate a range of $x_i$ values to plot the original function, and `test_y` contains the corresponding $y_i$ values of the original function. For the first plot, our original function is the *sine curve*.

For all the plots:

`plt.plot(test_x, test_y)` plots the original function.

`plt.plot(data[0], data[1])` plots the interpolated polynomial.
"""

pi      = np.pi
x       = np.array([0.0, pi/8.0,  pi, 4.0*pi/2.0])
y       = np.array([0.0,    1.0, 0.0,       -1.0])
y_prime = np.array([1.0,    0.0, 1.0,        0.0])

"""**Plot 1:** trying to interpolate a sine curve (`np.sin()`) using first 2 nodes in `x` and `y`, and their corresponding derivative in `y_prime`."""

n      = 1
f3     = hermit(x[:(n+1)], y[:(n+1)], y_prime[:(n+1)])
data   = f3.linspace(n=50, domain=[-3, 3])
test_x = np.linspace(-10, 10, 50, endpoint=True)
test_y = np.sin(test_x)

plt.plot(data[0], data[1])
plt.plot(test_x, test_y)
plt.show()

"""**Plot 2:** trying to interpolate a sine curve (`np.sin()`) using first 3 nodes in `x` and `y` and their corresponding derivative in `y_prime`."""

n      = 2
f5     = hermit(x[:(n+1)], y[:(n+1)], y_prime[:(n+1)])
data   = f5.linspace(n=100, domain=[-0.85, 2.5])
test_x = np.linspace(-5*pi, 5*pi, 100, endpoint=True)
test_y = np.sin(test_x)

plt.plot(test_x, test_y) # 25-
plt.plot(data[0], data[1]) # 10-33
plt.show()

"""**Plot 3:** trying to interpolate a sine curve (`np.sin()`) using first 4 nodes in `x` and `y` and their corresponding derivative in `y_prime`."""

n      = 3
f7     = hermit(x[:(n+1)], y[:(n+1)], y_prime[:(n+1)])
data   = f7.linspace(n=50, domain=[-0.45, 3.3])
test_x = np.linspace(-6*pi, 6*pi, 50, endpoint=True)
test_y = np.sin(test_x)

plt.plot(data[0], data[1])
plt.plot(test_x, test_y)
plt.show()

"""**Plot 4:** trying to interpolate an exponential curve (`np.exp()`) using all nodes in `x` and `y` and their corresponding derivatives in `y_prime`."""

#defining new set of given node information: x, y and y'
x       = np.array([0.0, 1.0,          2.0       ])
y       = np.array([1.0, 2.71828183,  54.59815003])
y_prime = np.array([0.0, 5.43656366, 218.39260013])


f7      = hermit( x, y, y_prime)
data    = f7.linspace(n=50, domain=[-0.7, 2.45])
test_x  = np.linspace(-0.5, 2.2, 50, endpoint=True)
test_y  = np.exp(test_x**2)

plt.plot(data[0], data[1])
plt.plot(test_x, test_y)
plt.show()

"""**Plot 5:** trying to interpolate $y = (x-3)^2 + 1$ using all nodes in `x` and `y` and their corresponding derivatives in `y_prime`.

For this plot you might be able to see only one curve due to the two curves overlapping. This means that our polynomial is accurately interpolating the original function.

"""

#defining new set of given node information: x, y and y'
x       = np.array([1.0, 3.0, 5.0])
y       = np.array([5.0, 1.0, 5.0])
y_prime = np.array([-4.0, 0.0, 4.0])

f7      = hermit( x, y, y_prime)
data    = f7.linspace(n=50, domain=[-11, 10.5])
test_x  = np.linspace(-10, 10, 50, endpoint=True)
test_y  = (test_x-3)**2 + 1

plt.plot(data[0], data[1])
plt.plot(test_x, test_y)
plt.show()

"""## Part 2: Polynomial Interpolation Using Newton's Divided Difference Form
---

### Newton's Divided Difference Form

Newton form of a $n$ degree polynomial:

$$p_n(x) = \sum_{k=0}^{n} a_kn_k(x),$$
where the basis is:
$$n_k(x) = \prod_{j=0}^{k-1}(x-x_j),$$
$$ n_0(x)=1,$$

and the coefficients are: $$a_k = f[x_0, x_1, ..., x_k],$$

where the notation $f[x_0, x_1,\dots,x_k]$ denotes the divided difference.

By expanding the Newton form, we get:

$$p(x) = f [x_0] + (x-x_0) f[x_0,x_1] + (x-x_0) (x-x_1) f[x_0,x_1,x_2] + \dots + (x-x_0) (x-x_1) \dots (x-x_{k-1}) f[x_0, x_1, \dots, x_k]$$

### Tasks:
1. Complete the `calc_div_diff(x,y)` function which takes input `x` and `y`, and calculates all the divided differences. You may use the lambda function `difference()` inside the `calc_div_diff(x,y)` function to calculate the divided differences.

2. Complete the `__call__()` function which takes an input `x`, and calculates `y` using all the difference coefficients. `x` can be a single value or a numpy. In this case, it is a numpy array.

`res` variable must contain all results (corresponding y for x).
"""

class Newtons_Divided_Differences:

    def __init__(self, differences):
        self.differences = differences

    def __call__(self, x):
        '''
        this function is for calculating y from given x using all the difference coefficients
        x can be a single value or a numpy
        the formula being used:
        f(x) = f [x0] + (x-x0) f[x0,x1] + (x-x0) (x-x1) f[x0,x1,x2] + . . . + (x-x0) (x-x1) . . . (x-xk-1) f[x0, x1, . . ., xk]

        work on this after implementing 'calc_div_diff'. Then you should have
        f[x0], f[x0,x1]. . . . . ., f[x0, x1, . . ., xk] stored in self.differences

        'res' variable must return all the results (corresponding y for x)
        '''

        res = np.zeros(len(x)) #Initialization to avoid runtime error. You can change this line if you wish

        #----------------------------------------------
        # YOUR CODE HERE
        def minterm(limit, value, control):
          n = 1
          for i in range(0, limit):
            n = n * (value - control[i])
          return n


        def calculate(value):
          t1 = differences[0]
          for i in range(1, len(data_x)):
            t1 = t1 + (minterm(i, value, data_x) * differences[i])
          grand = t1
          return grand

        k = 0
        res = np.zeros(len(x))
        for i in x:
          res[k] = calculate(i)
          k+=1
        return res
        #----------------------------------------------



# basic rule for calculating the difference, implanted in the lambda function.
# You may use it if you wish
difference = lambda y2, y1, x2, x1: (y2-y1)/(x2-x1)

def calc_div_diff(x,y):
    assert(len(x)==len(y))
    #write this function to calculate all the divided differences in the list 'b'
    b = []  #initializing
    #----------------------------------------------
    # YOUR CODE HERE
    k = len(x)

    x = np.copy(x)
    b = np.copy(y)
    for i in range (1, k):
      b[i:k] = (b[i:k] - b[i-1])/(x[i:k] - x[i-1])
    return b
    #----------------------------------------------

data_x = [-3.,-2.,-1.,0.,1.,3.,4.]
data_y = [-60.,-80.,6.,1.,45.,30.,16.]

test = calc_div_diff(data_x, data_y)

assert len(test) == len(data_x)

"""### Plotting the polynomial
* `data_x` and `data_y` are the coordinates of the given nodes.

* `differences` is a list which contains the divided differences as each of its elements: $f[x_0], f[x_0,x_1], f[x_0,x_1,x_2], \dots$

* `obj` is an object of type `Newtons_Divided_Differences`. Creating the object runs the constructor of the class where the `difference` are stored in `self.differences`.

* `X` contains $x_i$ values through which we want to plot our polynomial.

* Calling the object using `obj(X)` executes the `__call__()` function of the class, which returns a numpy array containing the corresponding $y_i$ values, and storing them in variable `F`.

* Using `plt.plot(X,F)`, we plot the $(x_i, y_i)$ pairs of the polynomial.
"""

import numpy as np
import matplotlib.pyplot as plt

data_x = np.array([-5.,-1,-0.5,0.5,3.5,7.,9])
data_y = np.array([-30., -50., 36., 31., 75., 60., 46.])
differences = calc_div_diff(list(data_x), list(data_y))
p = Newtons_Divided_Differences(list(differences))
test_x = np.linspace(-7, 10, 50, endpoint=True)
test_y = p(test_x)

#generating 50 points from -3 to 4 in order to create a smooth line
plt.plot(test_x, test_y)
plt.plot(data_x, data_y, 'ro')
plt.show()

"""**Problem related Newton's Divided Difference interpolation**

Suppose, you have three nodes (-0.5, 1.87), (0, 2.20), (0.5, 2.44). Using Newton's Divided Difference method, print out the value of the interpolating polynomial at x = 6.

You have to solve the problem using Newtons_Divided_Differences class.
"""

data_x = np.array([-0.5, 0, 0.5])
data_y = np.array([1.87, 2.20, 2.44])
differences = calc_div_diff(list(data_x), list(data_y))
p = Newtons_Divided_Differences(list(differences))

test_x = np.array([6])
test_y = p(test_x)
print(test_y)

"""**Problem related Hermite interpolation**

Suppose, consider the following data set:

![Capture.JPG](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAeAB4AAD/4RDaRXhpZgAATU0AKgAAAAgABAE7AAIAAAAFAAAISodpAAQAAAABAAAIUJydAAEAAAAKAAAQyOocAAcAAAgMAAAAPgAAAAAc6gAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAERlbGwAAAAFkAMAAgAAABQAABCekAQAAgAAABQAABCykpEAAgAAAAMxOAAAkpIAAgAAAAMxOAAA6hwABwAACAwAAAiSAAAAABzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAyMjoxMDoxNCAxOTozNjoyNQAyMDIyOjEwOjE0IDE5OjM2OjI1AAAARABlAGwAbAAAAP/hCxdodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvADw/eHBhY2tldCBiZWdpbj0n77u/JyBpZD0nVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkJz8+DQo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIj48cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPjxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSJ1dWlkOmZhZjViZGQ1LWJhM2QtMTFkYS1hZDMxLWQzM2Q3NTE4MmYxYiIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIi8+PHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9InV1aWQ6ZmFmNWJkZDUtYmEzZC0xMWRhLWFkMzEtZDMzZDc1MTgyZjFiIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iPjx4bXA6Q3JlYXRlRGF0ZT4yMDIyLTEwLTE0VDE5OjM2OjI1LjE4MDwveG1wOkNyZWF0ZURhdGU+PC9yZGY6RGVzY3JpcHRpb24+PHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9InV1aWQ6ZmFmNWJkZDUtYmEzZC0xMWRhLWFkMzEtZDMzZDc1MTgyZjFiIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iPjxkYzpjcmVhdG9yPjxyZGY6U2VxIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+PHJkZjpsaT5EZWxsPC9yZGY6bGk+PC9yZGY6U2VxPg0KCQkJPC9kYzpjcmVhdG9yPjwvcmRmOkRlc2NyaXB0aW9uPjwvcmRmOlJERj48L3g6eG1wbWV0YT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgPD94cGFja2V0IGVuZD0ndyc/Pv/bAEMABwUFBgUEBwYFBggHBwgKEQsK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)

Using Hermit basis, print out the interpolating polynomial and find the value at x = [0.15,0.30,0.50].

You have to solve this problem using hermit function.
"""

x       = np.array([1.0, 0.2])
y       = np.array([-0.620, -0.283])
y_prime = np.array([3.585, 3.140])

p      = hermit( x, y, y_prime)
display(p)

x_arr = np.array([0.15, .3, .5])
p(x_arr)