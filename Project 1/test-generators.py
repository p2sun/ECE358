from app import exponential_rv_generator, uniform_rv_generator

total = 0
for i in range(0,1000000):
    test = uniform_rv_generator()
    total += test

print total/1000000