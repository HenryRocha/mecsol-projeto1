import numpy as np

# Starting variables.
E = 0.02
L = 2
A = 200E9
P = 50000
nElementos = 3

# Starting conditions
start_u = [0, 1, 1, 1]

# Forces
F = np.array([[0], [0], [0], [P]])

# Creating K matrix
Kbase = [[1, -1], [-1, 1]]
Kzeros = np.zeros((nElementos + 1, nElementos + 1))

for n in range(nElementos):
    Kzeros[n][n] += 1
    Kzeros[n][n+1] += -1
    Kzeros[n+1][n] += -1
    Kzeros[n+1][n+1] += 1

print(Kzeros)

# for n in range(nElementos):
#     for i in range(nElementos + 1):
#         for j in range(nElementos + 1):
#             if n + 1 >= i >= n and n + 1 >= j >= n:
#                 if i == j:
#                     Kzeros[i][j] = Kzeros[i][j] + 1
#                 else:
#                     Kzeros[i][j] = Kzeros[i][j] - 1

K = np.multiply(E * A / (L / nElementos), Kzeros)

# Deleting lines and columns
for i in start_u:
    if i == 0:
        F = np.delete(F, i, 0)

        K = np.delete(K, i, 0)
        K = np.delete(K, i, 1)


print(F)
print(K)
u = np.dot(np.linalg.inv(K), F)

print(u)
