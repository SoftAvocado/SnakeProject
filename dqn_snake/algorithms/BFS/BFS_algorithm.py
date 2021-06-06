from environment.parametrs import *
from environment.game import *
from environment.plot import *
from algorithms.BFS.shortest_path_bfs import shortest_path_bfs
import argparse
import distutils.util

path_log_games = 'environment/logs/log_games.txt'
log = open(path_log_games, 'w+')

def initialize_game(player, game, food):
    action = [1, 0, 0]
    player.do_move(action, player.x, player.y, game, food)


def run(params):
    pygame.init()
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
        initialize_game(player1, game, food1)
        if params['display']:
            display(player1, food1, game, record, counter_games, step)

        log.write("\n\n\t\t\t\tGAME: " + str(counter_games) + "\n")
        while not game.crash:
            log.write("Food location: (" + str(food1.x_food) + ", " + str(food1.y_food) + ")\n")
            log.write("Snake location: (" + str(player1.x) + ", " + str(player1.y) + ")\n")

            shortest_path = shortest_path_bfs((player1.x, player1.y),(food1.x_food, food1.y_food), (400,400),  player1.x_change,  player1.y_change, cell)
            log.write("Shortest path: " + str(shortest_path) + "\n")
            log.write("\n\t\t\t\tLOOKING FOR FOOD:\n")

            for i in range(len(shortest_path)):
                final_move = shortest_path[i]
                log.write("Snake location: (" + str(player1.x) + ", " + str(player1.y) + ")\n")
                log.write(str(step)+") Move: " + str(final_move) + "\n")
                player1.do_move(final_move, player1.x, player1.y, game, food1)
                record = get_record(game.score, record)
                step +=1
                if player1.eaten:
                    step =0
                if game.crash:
                    break
                if params['display']:
                    display(player1, food1, game, record, counter_games, step)
                    pygame.time.wait(params['speed'])
        counter_games += 1
        step = 0
        total_score += game.score
        print(f'Game {counter_games}      Score: {game.score}')
        log.write("\t\t\t\tGAME OVER\n")
        log.write("Score: " +str(game.score)+" \n")
        log.write("---------------------------------------------------------------------------------\n\n")
        score_plot.append(game.score)
        counter_plot.append(counter_games)
    mean, stdev = get_mean_stdev(score_plot)
    plot_seaborn(counter_plot, score_plot, False)
    return total_score, mean, stdev

def BFS_run(display, speed):
    pygame.font.init()
    parser = argparse.ArgumentParser()
    params = define_parameters()
    parser.add_argument("--display", nargs='?', type=distutils.util.strtobool, default=True)
    parser.add_argument("--speed", nargs='?', type=int, default=50)
    args = parser.parse_args()
    print("Args", args)
    params['display'] = display
    params['speed'] = speed
    run(params)
    log.close()