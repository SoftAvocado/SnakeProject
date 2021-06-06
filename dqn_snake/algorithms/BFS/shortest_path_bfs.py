import numpy as np
import queue


def log_filled_grid(filled_grid):
	path = 'algorithms/BFS/logs/log_filled_grid.txt'
	with open(path) as f:
		np.savetxt(path, filled_grid, fmt='%6d', delimiter=' ')
		np.savetxt(path, filled_grid, fmt='%6d', delimiter=' ')

def get_filled_grid(grid_size):
	# filling the grid with a corresponding number

	filled_grid = np.empty(grid_size)
	count = 0
	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			filled_grid[i][j] = count
			count +=1
	return filled_grid.astype(int)

def get_adjacency_list(grid_size, filled_grid):
	# creating unfilled adjacency list (dictionary)

	adj_list = {}
	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			adj_list[filled_grid[i][j]] = []

	# filling adjacency list (dictionary)
	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			if ((i-1)>=0):                                          # neighbour up (i-1, j)
				adj_list[filled_grid[i][j]].append(filled_grid[i-1][j])
			if ((i+1)<grid_size[0]):                               # neighbour down (i+1, j)
				adj_list[filled_grid[i][j]].append(filled_grid[i+1][j])
			if ((j+1)<grid_size[1]):                               # neighbour right (i, j+1)
				adj_list[filled_grid[i][j]].append(filled_grid[i][j+1])
			if ((j-1)>=0):                                          # neighbour left (i, j-1)
				adj_list[filled_grid[i][j]].append(filled_grid[i][j-1])
			#adj_list[filled_grid[i][j]].sort()
	return adj_list


def log_prev(prev):
	# в клетку i пришли из *
	# все, что не None - числа, по которым мы прошли во время поиска
	# но при этом не все числа принадлежат кратчайшему пути
	path = 'algorithms/BFS/logs/log_prev.txt'
	f = open(path, 'w')
	for i in range(len(prev)):
		f.write('i={:6d}    {:s}\n'.format(i, str(prev[i])))
	f.close()
def solve(start, end, adj_list, n):
	# creating a prev list to reconstruct path.
	# in prev list every node is represented as an i key.
	# prev[i] keeps the number of an i parent.

	q = queue.Queue()
	q.put(start)

	visited = []
	for i in range(n):
		visited.append(False)
	visited[start] = True

	prev = []
	for i in range(n):
		prev.append(None)

	while not q.empty():
		node = q.get()
		neighbours = adj_list[node]

		for neighbour in neighbours:
			if visited[neighbour] == False:
				q.put(neighbour)
				visited[neighbour] = True
				prev[neighbour] = node
				if neighbour == end:
					return prev
	return prev

def reconstructPath(start, end, prev):
	# creating a shortest path from start to end using id numbers

	path = []
	i=end
	while (i != None):
		path.append(i)
		i = prev[i]
	path.reverse()
	if path[0] == start:
		return path
	return []

def snake_direction(path, i, cell, change):
	# direction in witch the snake is looking
	if change != (0, 0):
		if change == (20, 0):
			return "right"
		if change == (-20, 0):
			return "left"
		if change == (0, -20):
			return "up"
		if change == (0, 20):
			return "down"

	if path[i-1] == (path[i] + cell):
		return "up"
	if path[i-1] == (path[i]-cell):
		return "down"
	if (path[i-1]+1) == path[i]:
		return "right"
	else:
		return "left"

def modify_path(path, cell, grid_size, filled_grid, start, end, change):
	snake_dir = snake_direction(path, 0, cell, change)
	path_dir = snake_direction(path, 1, cell, (0,0))
	new_path=[]

	if (snake_dir == "up" and path_dir == "down") or (snake_dir == "down" and path_dir == "up"):
		if (abs(path[0] - path[-1]) <= grid_size[1]) or (((path[0] - path[-1]) % 20 == 0) and (
			(path[0] - path[-1]) < (grid_size[0] * grid_size[1] - cell))):                    # in the same row or col

			new_path.append(path[0])
			if (path[0] - (path[0]-(path[0]%grid_size[1])))!=0:       # left col exists
				for i in range(len(path)):
					new_path.append(path[i] - 1)
			else:                                                     # right col exists
				for i in range(len(path)):
					new_path.append(path[i] + 1)
			new_path.append(path[-1])
		else:
			new_path = alternative_path(filled_grid, grid_size, start, end)
		return new_path

	elif (snake_dir == "right" and path_dir == "left") or (snake_dir == "left" and path_dir == "right"):
		if (path[0] - path[-1] <= grid_size[1]) or (((path[0] - path[-1]) % 20 == 0) and (
			(path[0] - path[-1]) < grid_size[0] * grid_size[1] - cell)):                    # in the same row or col
			new_path.append(path[0])
			if (path[0]-cell)>=0:       # row above exists
				for i in range(len(path)):
					new_path.append(path[i] - cell)
			else:                       # row beneath exists
				for i in range(len(path)):
					new_path.append(path[i] + cell)
			new_path.append(path[-1])
		else:
			new_path = alternative_path(filled_grid, grid_size, start, end)
		return new_path
	return []             # don't require modification

def get_move_list(path, cell, x_change, y_change):
	# changing path list with id numbers into move list with actions
	# action - [S, R, L]
	x_start_dir = x_change
	y_start_dir = y_change
	move_list = []
	for i in range(len(path)-1):
		snake_dir = snake_direction(path, i, cell, (x_start_dir, y_start_dir))
		if snake_dir == "up":                               # snake looks up
			if path[i+1]==(path[i]-1):
				move_list.append([0, 0, 1])  # go left
			elif path[i+1]==(path[i]+1):
				move_list.append([0, 1, 0])  # go right
			else:
				move_list.append([1, 0, 0])  # go straight

		elif snake_dir == "down":                           # snake looks down
			if path[i+1]==(path[i]+1):
				move_list.append([0, 0, 1])  # go left
			elif path[i+1]==(path[i]-1):
				move_list.append([0, 1, 0])  # go right
			else:
				move_list.append([1, 0, 0])  # go straight

		elif snake_dir == "right":                          # snake looks right
			if path[i+1]==(path[i]-cell):
				move_list.append([0, 0, 1])  # go left
			elif path[i+1]==(path[i]+cell):
				move_list.append([0, 1, 0])  # go right
			else:
				move_list.append([1, 0, 0])  # go straight
		else:                                               # snake looks left
			if path[i+1]==(path[i]+cell):
				move_list.append([0, 0, 1])  # go left
			elif path[i+1]==(path[i]-cell):
				move_list.append([0, 1, 0])  # go right
			else:
				move_list.append([1, 0, 0])  # go straight
		x_start_dir = 0
		y_start_dir = 0
	return move_list

def alternative_path(filled_grid, grid_size, start, end):
	# creating unfilled adjacency list (dictionary)

	adj_list = {}
	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			adj_list[filled_grid[i][j]] = []

	# filling adjacency list (dictionary)
	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			if ((j+1)<grid_size[1]):                               # neighbour right (i, j+1)
				adj_list[filled_grid[i][j]].append(filled_grid[i][j+1])
			if ((j-1)>=0):                                          # neighbour left (i, j-1)
				adj_list[filled_grid[i][j]].append(filled_grid[i][j-1])
			if ((i-1)>=0):                                          # neighbour up (i-1, j)
				adj_list[filled_grid[i][j]].append(filled_grid[i-1][j])
			if ((i+1)<grid_size[0]):                               # neighbour down (i+1, j)
				adj_list[filled_grid[i][j]].append(filled_grid[i+1][j])

	n = grid_size[0] * grid_size[1]
	prev = solve(start, end, adj_list, n)
	log_prev(prev)

	path = reconstructPath(start, end, prev)
	return path

def shortest_path_bfs(s, e, g_s, x_channge, y_change, cell):
	start = (int(s[0]/cell), int(s[1]/cell))
	end = (int(e[0]/cell), int(e[1]/cell))
	grid_size = (int(g_s[0]/cell), int(g_s[1]/cell))

	start = start[1]*grid_size[0]+start[0]
	end = end[1]*grid_size[1]+end[0]

	filled_grid = get_filled_grid(grid_size)
	log_filled_grid(filled_grid)

	adj_list = get_adjacency_list(grid_size, filled_grid)
	n = grid_size[0] * grid_size[1]
	prev = solve(start, end, adj_list, n)
	log_prev(prev)

	path = reconstructPath(start, end, prev)

	new_path = modify_path(path, cell,  grid_size, filled_grid, start, end, (x_channge, y_change))
	if new_path != []:
		path = new_path

	move_list = get_move_list(path, cell, x_channge, y_change)
	return move_list

def translate_moves(shortest_path):
	shortest_path_new = []
	for move in shortest_path:
		if move == [0, 0, 1]:
			shortest_path_new.append("left")
		elif move == [0, 1, 0]:
			shortest_path_new.append("right")
		elif move == [1, 0, 0]:
			shortest_path_new.append("straight")
	return shortest_path_new
