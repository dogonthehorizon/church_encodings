# λ
# TODO something something discovered languages; Philip Waddler

# Church Encodings are an interesting way of representing data in the lambda
# calculus. We'll see throughout this file how we can represent the Natural
# numbers and a few operations on them with surprsingly few constructs.

# At it's core, the lambda calculus is a way of mathematically representing
# computation. You may already be familiar with aspects of the lambda calculus
# if you've used any recent programming language that supports higher-order
# functions (we're using Python today).

# The lambda calculus is defined via the following three concepts:
#
#    - Variables
#    - Application
#    - Abstraction
# TODO define these better
# Also introduce lambda calculus syntax

# We can start by encoding booleans into lambda terms. We typically think of
# True and False as binary values, but we can also think about them in terms of
# choices. Think about the last time you wrote an if statement, it probably
# followed a pattern like this:

if True:  # Some boolean condition that evaluates to True or False
    1  # It's True, so we choose the first option
else:
    2  # False, so we choose the second option

# So looked at from a different perspective, True is the same as a function
# that takes two arguments and returns the first, and False is the same as a
# function that takes two arguments and returns the second. In other words:
# we can encode boolean values as lambda terms that choose between two options.

# Let's start by encoding booleans into the lambda calculus before we implement
# them in Python.
#
#   True is represented as  (λ x. (λ y. x))
#   False is represented as (λ x. (λ y. y))
#
# If we successively apply the lambda terms we can reduce true as follows:
#
#   (λ x. (λ y. x))
#   (λ x. x)
#   x
#
# Leaving us with the first choice. Go ahead and reduce False to prove to
# yourself that it will always return the second choice. Sometimes it helps
# write it out on pen and paper! Don't worry, I'm not going anywhere.

# Now that we've proven to ourselves that we can encode booleans in the lambda
# calculus, let's go ahead and apply this newfound knowledge in Python:

true = lambda x: lambda y: x
false = lambda x: lambda y: y

# So how do we prove that these two functions follow our intuitions about True
# and False? We could write out unit tests for these functions, but we would
# only be testing specific examples. 'true' should be true no matter if I pass
# in 1 and 2 as arguments or if I pass 'foo' and 'bar', or even 1 and 'foo';
# that is, 'true' should _always_ return the first argument. We can consider
# this to be a 'law' or 'property' about how 'true' should behave. Luckily,
# libraries exist in many modern languages that allow us to test such
# properties about our code without having to spell out every single example we
# want to test. These libraries are known as property-based or generative
# testing tools.

# One such Python library is called 'hypothesis', which provides us with a
# simple, straightforward interface for testing properties about our code.

# We start by importing the 'given' function, which is a way of providing our
# test functions with sample data, otherwise known as strategies.
from hypothesis import given

# We'll also import the 'integers' strategy which we'll use to generate random
# numbers for our test cases. There are many other strategies available, and
# you can even define your own, but for our purposes 'integers' will be
# sufficient to test Church encoded Natural numbers.
from hypothesis.strategies import integers

# Since we'll be using this strategy a lot let's assign it to a variable for
# readability's sake. CPython in particular doesn't optimize tail recursion, so
# we'll also need to be careful that we don't test any numbers that are too
# large for our computer to handle in memory.
import sys
naturals = integers(min_value=0, max_value=sys.getrecursionlimit()-100)

## TODO bookmark

@given(x=naturals, y=naturals)
def test_true_returns_first_arg(x, y):
    assert (true)(x)(y) == x
test_true_returns_first_arg()

@given(x=naturals,y=naturals)
def test_false_returns_second_arg(x, y):
    assert (false)(x)(y) == y
test_false_returns_second_arg()

zero = false
succ = lambda n: lambda f: lambda x: (f)((n)(f)(x))

one = succ(zero)
two = succ(one)
three = succ(two)
four = succ(three)
five = succ(four)
six = succ(five)
seven = succ(six)
eight = succ(seven)
nine = succ(eight)

plus_one = lambda x: x + 1
un_church = lambda x: (x)(plus_one)(0)
church = lambda x: zero if x == 0 else succ(church(x-1))


@given(naturals)
def test_church_encoding_fns_are_idempotent(x):
    assert un_church(church(x)) == x
test_church_encoding_fns_are_idempotent()

@given(naturals)
def test_succ_always_returns_plus_one(x):
    assert un_church((succ)(church(x))) == x + 1
test_succ_always_returns_plus_one()
