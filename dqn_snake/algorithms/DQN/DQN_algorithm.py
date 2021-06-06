from environment.parametrs import *
from environment.game import *
from environment.plot import *
from algorithms.DQN.DQN import DQNAgent
import argparse
import random
import torch.optim as optim
import torch
from algorithms.DQN.bayesOpt import *
import distutils.util


def initialize_game(player, game, food, agent, batch_size):
	state_init1 = get_state(game, player, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
	action = [1, 0, 0]
	player.do_move(action, player.x, player.y, game, food)
	state_init2 = get_state(game, player, food)
	reward1 = agent.set_reward(player, game.crash)
	agent.remember(state_init1, action, reward1, state_init2, game.crash)
	agent.replay_new(agent.memory, batch_size)


def test(params):
	params['load_weights'] = True
	params['train'] = False
	params["test"] = False
	score, mean, stdev = run(params)
	return score, mean, stdev


def run(params):
	"""
	Run the DQN algorithm, based on the parameters previously set.
	"""
	pygame.init()
	agent = DQNAgent(params)
	agent = agent.to(DEVICE)
	agent.optimizer = optim.Adam(agent.parameters(), weight_decay=0, lr=params['learning_rate'])
	counter_games = 0
	score_plot = []
	counter_plot = []
	record = 0
	total_score = 0
	step = 0

	while counter_games < params['episodes']:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		# Initialize classes
		game = Game(440, 440)
		player1 = game.player
		food1 = game.food

		# Perform first move
		initialize_game(player1, game, food1, agent, params['batch_size'])
		if params['display']:
			display(player1, food1, game, record, counter_games, step)

		while not game.crash:
			if not params['train']:
				agent.epsilon = 0.01
			else:
				# agent.epsilon is set to give randomness to actions
				agent.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])

			# get old state
			state_old = get_state(game, player1, food1)

			# perform random actions based on agent.epsilon, or choose the action
			if random.uniform(0, 1) < agent.epsilon:
				final_move = np.eye(3)[randint(0, 2)]
			else:
				# predict action based on the old state
				with torch.no_grad():
					state_old_tensor = torch.tensor(state_old.reshape((1, 11)), dtype=torch.float32).to(DEVICE)
					prediction = agent(state_old_tensor)
					final_move = np.eye(3)[np.argmax(prediction.detach().cpu().numpy()[0])]

			# perform new move and get new state
			player1.do_move(final_move, player1.x, player1.y, game, food1)
			step += 1
			if player1.eaten:
				step = 0
			state_new = get_state(game, player1, food1)

			# set reward for the new state
			reward = agent.set_reward(player1, game.crash)

			if params['train']:
				# train short memory base on the new action and state
				# store the new data into a long term memory
				# agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
				agent.remember(state_old, final_move, reward, state_new, game.crash)
				agent.replay_new(agent.memory, params['batch_size'])

			record = get_record(game.score, record)
			if params['display']:
				display(player1, food1, game, record, counter_games, step)
				pygame.time.wait(params['speed'])
			if step > 100:
				game.crash = True
		#if params['train']:
			#agent.replay_new(agent.memory, params['batch_size'])
		counter_games += 1
		step = 0
		total_score += game.score
		print(f'Game {counter_games}      Score: {game.score}')
		score_plot.append(game.score)
		counter_plot.append(counter_games)
	mean, stdev = get_mean_stdev(score_plot)
	if params['train']:
		model_weights = agent.state_dict()
		torch.save(model_weights, params["weights_dqn_path"])
	if params['plot_score']:
		plot_seaborn(counter_plot, score_plot, params['train'])
	return total_score, mean, stdev


def DQN_run(display, speed, train):
	print(__name__)
	# Set options to activate or deactivate the game view, and its speed
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
	parser.add_argument("--bayesianopt", nargs='?', type=distutils.util.strtobool, default=False)
	args = parser.parse_args()
	print("Args", args)
	params['display'] = display
	params['speed'] = speed
	#params['display'] = args.display
	#params['speed'] = args.speed
	if args.bayesianopt:
		bayesOpt = BayesianOptimizer(params)
		bayesOpt.optimize_RL()
	if params['train']:
		params['load_weights'] = False
		run(params)
	if params['test']:
		params['train'] = False
		params['load_weights'] = True
		test(params)
