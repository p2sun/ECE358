import math
from numpy import random

def exponential_rv_generator(lambda_factor):
    # get a random number between the range of 0 and 1
    #U is our random number between 0 and 1
    u = random.randrange(0,1)
    x = (-1 * lambda_factor) * math.log(1 - u)

    return x

def uniform_rv_generator():
    return random.randrange(0,1)


