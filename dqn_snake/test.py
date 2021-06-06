import random
from environment.plot import *

def games_plot():
	counter_games = 250
	score_plot = []
	counter_plot = []
	for i in range(counter_games - 1):
		rand = random.uniform(0, 1)
		if rand <= 0.2:
			num = int(random.uniform(0, 5))
		elif rand >= 0.2 and rand < 0.4:
			num = int(random.uniform(5, 15))
		elif rand >= 0.4 and rand < 0.6:
			num = int(random.uniform(15, 22))
		elif rand >= 0.6 and rand < 0.99:
			num = int(random.uniform(22, 50))
		else:
			print(rand)
			num = int(random.uniform(50, 70))
		score_plot.append(num)
	for i in range(counter_games - 1):
		counter_plot.append(i)
	print(score_plot)

	mean, stdev = get_mean_stdev(score_plot)
	plot_seaborn(counter_plot, score_plot, False)

def learning_plot():
	counter_games = 250
	score_plot = []
	counter_plot = []
	for i in range(counter_games - 1):
		if i <= counter_games*0.1:
			num = int(random.uniform(0, 2))
		elif i >= counter_games*0.1 and i < counter_games*0.2:
			num = int(random.uniform(0, 3))
		elif i >= counter_games*0.2 and i < counter_games*0.3:
			num = int(random.uniform(0, 5))
		elif i >= counter_games*0.3 and i < counter_games*0.5:
			num = int(random.uniform(0, 8))
		elif i >= counter_games*0.5 and i < counter_games * 0.6:
			num = int(random.uniform(0, 15))
		elif i >= counter_games*0.6 and i < counter_games * 0.7:
			num = int(random.uniform(0, 22))
		elif i >= counter_games*0.7 and i < counter_games * 0.8:
			num = int(random.uniform(0, 40))
		else:
			num = int(random.uniform(0, 50))
		score_plot.append(num)
	for i in range(counter_games - 1):
		counter_plot.append(i)
	print(score_plot)

	mean, stdev = get_mean_stdev(score_plot)
	plot_seaborn(counter_plot, score_plot, True)

def learning_plot2():
	counter_games = 250
	max_score_plot = []
	counter_gen_plot = []
	for i in range(counter_games - 1):
		if i <= counter_games*0.1:
			num = int(random.uniform(1, 3))
		elif i >= counter_games*0.1 and i < counter_games*0.2:
			num = int(random.uniform(2, 4))
		elif i >= counter_games*0.2 and i < counter_games*0.3:
			num = int(random.uniform(2, 5))
		elif i >= counter_games*0.3 and i < counter_games*0.5:
			num = int(random.uniform(3, 7))
		elif i >= counter_games*0.5 and i < counter_games * 0.6:
			num = int(random.uniform(4, 12))
		elif i >= counter_games*0.6 and i < counter_games * 0.7:
			num = int(random.uniform(5, 20))
		elif i >= counter_games*0.7 and i < counter_games * 0.8:
			num = int(random.uniform(6, 24))
		else:
			num = int(random.uniform(7, 30))
		max_score_plot.append(num)
	for i in range(counter_games - 1):
		counter_gen_plot.append(i)
	print(max_score_plot)

	mean, stdev = get_mean_stdev(max_score_plot)
	plot_seaborn(counter_gen_plot, max_score_plot, True, '# generation', 'max score')

def games_plot2():
	counter_games = 250
	score_plot = []
	counter_plot = []
	for i in range(counter_games - 1):
		rand = random.uniform(0, 1)
		if rand <= 0.2:
			num = int(random.uniform(0, 5))
		elif rand >= 0.2 and rand < 0.4:
			num = int(random.uniform(7, 14))
		elif rand >= 0.4 and rand < 0.6:
			num = int(random.uniform(14, 18))
		elif rand >= 0.6 and rand < 0.99:
			num = int(random.uniform(18, 26))
		else:
			print(rand)
			num = int(random.uniform(26, 32))
		score_plot.append(num)
	for i in range(counter_games - 1):
		counter_plot.append(i)
	print(score_plot)

	mean, stdev = get_mean_stdev(score_plot)
	plot_seaborn(counter_plot, score_plot, False,'# chromosome', 'score')


games_plot2()