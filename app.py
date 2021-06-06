import os
from algorithms.BFS.BFS_algorithm import *
from algorithms.DQN.DQN_algorithm import *
from algorithms.GEN.genetic_algorithm import *

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def DISPLAY_menu():
	clearConsole()
	print("DISPLAY")
	print("Do you wish to use the graphical interface? It allows you to watch the agent play, but slows down the algorithm.\n")
	print("[1] for yes - use the GUI")
	print("[2] for no - don't use the GUI")

def SPEED_menu():
	print("SPEED")
	print("Enter the speed of the game or press Enter for default speed.\n")

def speed_is_ok(speed):
	numbers=list("0123456789")
	for i in range(len(speed)):
		if speed[i] not in numbers:
			return False
	return True

def get_PARAMS_menu():
	display = True
	speed = 50
	check_speed = True

	DISPLAY_menu()
	com = input("\nEnter command: ")
	if com == '1':
		display = True
	elif com == '2':
		display = False
	if display:
		clearConsole()
		while check_speed:
			SPEED_menu()
			com = input("\nEnter the speed: ")
			if com == '':
				speed = 50
				check_speed = False
			elif speed_is_ok(com):
				speed = int(com)
				check_speed = False
			else:
				clearConsole()
				print("Speed should be a positive integer number!\n")


	else:
		speed = 0
	return display, speed

def CLOSE_menu():
	clearConsole()
	print("EXIT")
	print("Are you sure you want to close the program?\n")
	print("[1] for yes")
	print("[2] for no")

def GEN_menu():
	clearConsole()
	print("GEN")
	print("Genetic algorithm is teaching the snake to play the game with neural network. For more settings use\n"
	      "environment/parametrs.py\n")
	print("[1] to run GEN in training mode")
	print("[2] to run GEN in game mode (using the standard weights)")
	print("[3] to go back")

def DQN_menu():
	clearConsole()
	print("DQN")
	print("Deep Q neural network algorithm is teaching the snake to play the game with Q-learning.\n"
	      "For more settings use environment/parametrs.py\n")
	print("[1] to run DQN in training mode")
	print("[2] to run DQN in game mode (using the standard weights)")
	print("[3] to go back")

def BFS_menu():
	clearConsole()
	print("BFS")
	print("Breadth-first search algorithm is calculating the shortest path from the head of the snake to an apple.\n"
	      "For more settings use environment/parametrs.py\n")
	print("[1] to run BSF algorithm")
	print("[2] to go back")

def menu():
	clearConsole()
	print("MENU\n")
	print("[1] to choose BFS algorithm")
	print("[2] to choose DQN algorithm")
	print("[3] to choose GEN algorithm")
	print("[4] to close the program")

if __name__ == '__main__':
	closed = False
	while not closed:
		menu()
		com = input("\nEnter command: ")
		if com == '1':
			BFS_menu()
			com = input("\nEnter command: ")
			if com == '1':
				display, speed = get_PARAMS_menu()
				BFS_run(display, speed)
			elif com == '2':
				continue
		elif com == '2':
			DQN_menu()
			com = input("\nEnter command: ")
			if com == '1':
				display, speed = get_PARAMS_menu()
				DQN_run(display = display, speed = speed, train = True)
			elif com == '2':
				display, speed = get_PARAMS_menu()
				DQN_run(display = display, speed = speed, train = False)
			elif com == '3':
				continue
		elif com == '3':
			GEN_menu()
			com = input("\nEnter command: ")
			if com == '1':
				display, speed = get_PARAMS_menu()
				GEN_run(display = display, speed = speed, train = True)
			elif com == '2':
				display, speed = get_PARAMS_menu()
				GEN_run(display = display, speed = speed, train = False)
			elif com == '3':
				continue
		elif com == '4':
			CLOSE_menu()
			com = input("\nEnter command: ")
			if com == '1':
				break
			elif com == '2':
				continue
