from environment.game import *
from environment.parametrs import *
from environment.plot import *
import math
import numpy as np
import random as rand

MOVES = [[0,0,1],[0,1,0],[1,0,0]]

DEVICE = 'cpu'  # 'cuda' if torch.cuda.is_available() else 'cpu'

def initialize_game(player, game, food):
	action = [1, 0, 0]
	player.do_move(action, player.x, player.y, game, food)

class GeneticAgent():
	def __init__(self, params):
		self.population_size = params['population_size']
		self.num_generations = params['num_generations']
		self.games_amount = params['episodes']
		self.input_size = params['input_size']
		self.h1_size = params['first_layer_size']
		self.h2_size = params['second_layer_size']
		self.h3_size = params['third_layer_size']
		self.output_size = params['output_size']
		self.mutation_chance = params['mutation_chance']
		self.mutation_size = params['mutation_size']
		self.weights = params['weights_gen_path']
		self.load_weights = params['load_weights']
		self.current_chromosome = None
		self.population = [self.generate_chromosome(self.input_size, self.h1_size, self.h2_size, self.h3_size,
		                                            self.output_size) for _ in range(self.population_size)]
		if params['test']:
			print("weights loaded")
			self.load_chromosome()
			self.population_size = 1
			self.num_generations = 1
		if params['train']:
			self.games_amount = 1

	def save_population(self):
		with open(self.weights, 'w') as f:
			for c in range(len(self.population)):
				f.write("Chromosome %d\n" % c)
				for l in range(len(self.population[c])):
					f.write("Layer %d\n" % l)
					for i in range(len(self.population[c][l])):
						for j in range(len(self.population[c][l][i])):
							f.write("%s ," % str(self.population[c][l][i][j]))
						f.write("\n")

	def save_chromosome(self, best_c):
		with open(self.weights, 'w') as f:
			for l in range(len(best_c)):
				f.write("Layer %d\n" % l)
				for i in range(len(best_c[l])):
					for j in range(len(best_c[l][i])):
						f.write("%s ," % str(best_c[l][i][j]))
					f.write("\n")

	def count_chromosomes(self):
		count = 0
		with open(self.weights, 'r') as f:
			for line in f:
				if "Chromosome" in line:
					count+=1
		return count

	def get_weight1(self, layer_num, row_num, weight_num):
		numbers = ["0","1","2","3","4","5","6","7","8","9"]
		with open(self.weights, 'r') as f:
			line_id = 0
			row_id = 0
			num = []
			start_collecting_number = False
			row_switch=False
			for line in f:
				if "Layer "+str(layer_num) in line:
					row_switch = True
				elif row_switch:
					if row_id == row_num:
						row_switch = False
						weights_line = line
						i_num=0
						for c in weights_line:
							if weight_num - i_num == 1 and c == "-":
								num.append("-")
							elif i_num == weight_num and c == ".":
								num.append(".")
							elif c in numbers:
								if i_num == weight_num:
									start_collecting_number = True
									num.append(c)
								else:
									i_num += 1
							if c ==" " and start_collecting_number:
								return(float(''.join(num)))
					row_id += 1
				line_id += 1
		return None

	def get_weight(self, line, weight_num):
		numbers = ["0","1","2","3","4","5","6","7","8","9"]
		num_count = 0
		start_collecting_number = False
		num = []
		for i in range(len(line)):
			if line[i] in numbers or line[i]=='-' or line[i]=='.' or line[i]=='e':
				if num_count == weight_num:
					start_collecting_number = True
					num.append(line[i])
			elif line[i] == ',':
				if start_collecting_number == True:
					return (float(''.join(num)))
				else:
					num_count += 1
		return None

	def load_population(self):
		new_population = []
		with open(self.weights, 'r') as f:
			print(self.count_chromosomes())
			c_len = self.count_chromosomes()
			l_len = len(self.population[0])
			for c in range(c_len):
				new_population.append([])
				for l in range(l_len):
					print(new_population)
					row = [0.0 for _ in range(len(self.population[c][l][0]))]
					new_population[c].append(np.array([row for _ in range(len((self.population[c][l])))]))
					for i in range(len((self.population[c][l]))):
						for j in range(len(self.population[c][l][i])):
							weight = self.get_weight(l, i, j)
							new_population[c][l][i][j] = weight
		self.population = new_population

	def load_chromosome(self):
		new_chromosome = []
		rows_in_layer = []
		l_count = -1
		row_count = 0
		with open(self.weights, 'r') as f:
			for line in f:
				if "Layer" not in line:
					row = []
					for i in range(len(self.population[0][l_count][0])):
						row.append(self.get_weight(line, i))
					row_count+=1
					rows_in_layer.append(row)
				else:
					if l_count != -1:
						new_chromosome.append(np.array(rows_in_layer))
						rows_in_layer = []
						row_count = 0
					l_count+=1
			new_chromosome.append(np.array(rows_in_layer))
		self.current_chromosome = new_chromosome

	def generate_chromosome(self, input_size, h1_size, h2_size, h3_size, output_size):
		hidden_layer1 = np.array([[rand.uniform(-1, 1) for _ in range(input_size)] for _ in range(h1_size)])
		hidden_layer2 = np.array([[rand.uniform(-1, 1) for _ in range(h1_size)] for _ in range(h2_size)])
		hidden_layer3 = np.array([[rand.uniform(-1, 1) for _ in range(h2_size)] for _ in range(h3_size)])
		output_layer = np.array([[rand.uniform(-1, 1) for _ in range(h3_size)] for _ in range(output_size)])
		return [hidden_layer1, hidden_layer2, hidden_layer3, output_layer]

	def get_move(self, game, player, food):
		input_vector = get_state(game, player, food)
		hidden_layer1 = self.current_chromosome[0]
		hidden_layer2 = self.current_chromosome[1]
		hidden_layer3 = self.current_chromosome[2]
		output_layer = self.current_chromosome[3]

		# Forward pass
		hidden_result1 = np.array([math.tanh(np.dot(input_vector, hidden_layer1[i])) for i in range(hidden_layer1.shape[0])])
		hidden_result2 = np.array([math.tanh(np.dot(hidden_result1, hidden_layer2[i])) for i in range(hidden_layer2.shape[0])])
		hidden_result3 = np.array([math.tanh(np.dot(hidden_result2, hidden_layer3[i])) for i in range(hidden_layer3.shape[0])])
		output_result = np.array([np.dot(hidden_result3, output_layer[i]) for i in range(output_layer.shape[0])])

		max_index = np.argmax(output_result)
		return MOVES[int(max_index)]

	def reproduce(self, top_25):
		new_population = []
		for chromosome in top_25:
			new_population.append(chromosome)
		for chromosome in top_25:
			new_chromosome = self.mutate(chromosome)
			new_population.append(new_chromosome)
		for _ in range(self.population_size // 2):
			new_chromosome = self.generate_chromosome(self.input_size, self.h1_size, self.h2_size, self.h3_size,
			                                               self.output_size)
			new_population.append(new_chromosome)
		return new_population

	def mutate(self, chromosome,c=1,s=1):
		new_chromosome = []
		for layer in chromosome:
			new_layer = np.copy(layer)
			for i in range(new_layer.shape[0]):
				for j in range(new_layer.shape[1]):
					if rand.uniform(0,1) < self.mutation_chance*c:
						new_layer[i][j] += rand.uniform(-1,1)*self.mutation_size*s
			new_chromosome.append(new_layer)
		return new_chromosome

	def one_generation(self, params, f):
		pygame.init()
		scores = [0 for _ in range(self.population_size)]
		max_score = 0
		counter_games = 0
		score_plot = []
		counter_plot = []
		record = 0
		total_score = 0
		step = 0
		for snake_i in range(self.population_size):
			for game_i in range(self.games_amount):
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						quit()
				if params['train']:
					self.current_chromosome = self.population[snake_i]
				game = Game(440, 440)
				player1 = game.player
				food1 = game.food

				initialize_game(player1, game, food1)
				if params['display']:
					display(player1, food1, game, record, counter_games, step)

				while not game.crash:
					final_move = self.get_move(game, player1, food1)
					player1.do_move(final_move, player1.x, player1.y, game, food1)
					step += 1
					if player1.eaten:
						step = 0
					record = get_record(game.score, record)
					if params['display']:
						display(player1, food1, game, record, counter_games, step)
						pygame.time.wait(params['speed'])
					if step > 200:
						game.crash = True

				counter_games += 1
				step = 0
				total_score += game.score
				# print(f'Game {counter_games}      Score: {game.score}')
				score_plot.append(game.score)
				counter_plot.append(counter_games)
				scores[snake_i] += game.score

				if game.score > max_score:
					max_score = get_record(game.score, max_score)
					print(max_score, "at ID", snake_i + 1)

		if params['train']:
			f.write('GENERATION RESULTS\n')
			f.write('Scores: ')
			for i in (np.argsort(scores)):
				print(scores[i], sep=" ", end="")
				f.write('{:3d}'.format(scores[i]))
			print()
			top_25_indexes = list(np.argsort(scores))[3 * (self.population_size // 4):self.population_size]

			f.write('\nTop 25: ')
			for i in (top_25_indexes):
				f.write('{:3d}'.format(scores[i]))
				print(scores[i], sep=" ", end="")
			print()
			top_25 = [self.population[i] for i in top_25_indexes][::-1]
			self.population = self.reproduce(top_25)
		else:
			top_25 =[]
			top_25.append(None)
		mean, stdev = get_mean_stdev(score_plot)
		return score_plot, max_score, mean, stdev, top_25[0]