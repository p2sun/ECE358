from app import exponential_rv_generator, uniform_rv_generator

total = 0
for i in range(0,1000000):
    total += uniform_rv_generator()

print total/1000000