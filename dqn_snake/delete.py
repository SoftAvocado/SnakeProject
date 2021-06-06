"""
import numpy as np
import random
arr = np.array([0,0,0,0],[])
arr[0] = 1

new_pop = [[]]
row = [1,2,4,5]
new_pop[0].append(np.array(row))
new_pop[0].append(np.array(row))
print(new_pop)

pop = [[np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]]), np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])],[np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]]), np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])],[np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]]), np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])]]

c_len = 3
l_len = 3
row_len = 3
col_len = 4

new_pop = []
for c in range(c_len):
	new_pop.append([])
	for l in range(l_len):
		new_pop[c].append(np.array([[0.0 for _ in range(col_len)] for _ in range(row_len)]))
		for i in range(row_len):
			for j in range(col_len):
				new_pop[c][l][i][j] = random.random()%100

print(pop)
"""

print(-4.29848676e-01)
