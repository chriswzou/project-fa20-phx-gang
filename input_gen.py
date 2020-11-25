import random

N_STUDENTS = 50
OUTPUT = [] # list of lists
FIND_OPTIMAL_NAIVE = True

# Generate S_max
S_MAX_SCALE = 100
HAPPY_SCALE = 100
S_MAX = round(S_MAX_SCALE * random.random(), ndigits=3)
STRESS_SCALE = S_MAX / 4

# Generate happiness and stress values for all the edges
print(S_MAX)
for i in range(N_STUDENTS): 
    for j in range(N_STUDENTS):
        if i < j:
            s_ij = round(STRESS_SCALE * random.random(), ndigits=3)
            h_ij = round(random.uniform(0.9 * s_ij, 1.1 * s_ij), ndigits=3)
            print(i, j, h_ij, s_ij)

