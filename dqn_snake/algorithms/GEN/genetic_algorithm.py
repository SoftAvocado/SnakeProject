from algorithms.GEN.genetic_evolution import *
import argparse

def test(params):
	score_plot, max_score, mean, stdev = all_generations(params)
	return score_plot, max_score, mean, stdev

def all_generations(params):
	agent = GeneticAgent(params)
	score_plot = []
	counter_gen = []
	max_plot = []
	max_score=0
	mean=0
	stdev =0
	f = open(params['log_gen_path'], 'w+')
	best_c = None
	for gen in range(agent.num_generations):
		f.write('GENERATION {:3d}\n'.format(gen))
		score_plot, max_score, mean, stdev, best_c = agent.one_generation(params, f)
		max_plot.append(max_score)
		counter_gen.append(gen)
		f.write('\nMax score in generation {:3d} = {:3d}\n'.format(gen, max_score))
		print("gen", gen)
	if params['train']:
		print("weights saved")
		agent.save_chromosome(best_c)
	if params['plot_score']:
		if params['train']:
			plot_seaborn(counter_gen, max_plot, params['train'])
		if params['test']:
			counter_games=[i for i in range(params['episodes'])]
			plot_seaborn(counter_games,score_plot, params['train'])
	f.close()
	return score_plot, max_score, mean, stdev

def GEN_run(display, speed, train):
	pygame.font.init()
	parser = argparse.ArgumentParser()
	params = define_parameters()
	if train:
		params['train'] = True
		params['test'] = False
	else:
		params['train'] = False
		params['test'] = True
	parser.add_argument("--display", nargs='?', type=distutils.util.strtobool, default=True)
	parser.add_argument("--speed", nargs='?', type=int, default=50)
	args = parser.parse_args()
	print("Args", args)
	params['display'] = display
	params['speed'] = speed
	if params['train']:
		params['load_weights'] = False
		all_generations(params)
	if params['test']:
		params['load_weights'] = True
		test(params)
