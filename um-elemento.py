import numpy as np

# Starting variables.
E = 0.02
L = 2
A = 200E9
P = 50000

# Starting condicions, 0 if u is 0, 1 if it is not 0.
start_u = [0, 1]
K = np.multiply(E * A / L, [[1, -1], [-1, 1]])
F = [0, 50000]

for i in start_u:
    if i == 0:
        F = np.delete(F, i, 0)

        K = np.delete(K, i, 0)
        K = np.delete(K, i, 1)

# Calculate u's
u = np.linalg.inv(K) * F

print(u)
