import datetime

DEVICE = 'cpu'  # 'cuda' if torch.cuda.is_available() else 'cpu'

def define_parameters():
	params = dict()
	#General
	params['episodes'] = 100
	# Neural Network
	params['input_size'] = 11
	params['first_layer_size'] = 200  # neurons in the first layer
	params['second_layer_size'] = 20  # neurons in the second layer
	params['third_layer_size'] = 50  # neurons in the third layer
	params['output_size'] = 3
	# Q-learning Network
	params['epsilon_decay_linear'] = 1/400
	params['learning_rate'] = 0.00013629
	params['memory_size'] = 2000
	params['batch_size'] = 10
	# Genetic evolution
	params['population_size'] = 1000
	params['num_generations'] = 100
	params['mutation_chance'] = 0.1
	params['mutation_size'] = 0.1
	# Settings
	params['display'] = True
	params['speed'] = 50
	params['load_weights'] = False
	params['train'] = True
	params['test'] = False
	params['plot_score'] = True
	params['weights_dqn_path'] = 'algorithms/DQN/weights/weights_2.h5'
	params['weights_gen_path'] = 'algorithms/GEN/weights/weights.txt'
	params['log_dqn_path'] = 'algorithms/DQN/logs/scores_' + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.txt'
	params['log_gen_path'] = 'algorithms/GEN/logs/scores_' + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.txt'
	return params