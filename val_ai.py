import dotbox
import numpy as np


def maximize(game_state, players, alpha, beta, move):
    if (game_state.is_over()):
        v = game_state.state_val(players.get_current_player())
        print("MAX")
        print(move)
        print(v)
        return (game_state, players,  v, move)

    max_value = -(game_state.total_boxes() + 1)
    best_move = None
    state = None

    for m in game_state.get_valid_moves():
        line = dotbox.Line(m, players.get_current_player())
        scored, new_state = game_state.test_move(line)

        if scored:
            (x, y, v, min_move) = maximize(
                new_state, players, alpha, beta, m)

            # if v > max_value:
            #     max_value = v
            #     best_move = m
            #     state = new_state

        else:
            players.switch_player()
            (x, y, v, min_move) = minimize(
                new_state, players, alpha, beta, m)

        # if v == max_value:
        #   swap = np.random.choice([True, False])
        #   if swap:
        #     max_value = v
        #     best_move = m
        #     state = new_state

        # elif v > max_value:
        #     max_value = v
        #     best_move = m
        #     state = new_state

        if (v > max_value) or (v == max_value and np.random.choice([True, False])):
            max_value = v
            best_move = m
            state = new_state

        alpha = max(alpha, max_value)

        if beta <= alpha:
            # players.switch_player()
            print("MAXIMIZER PRUNE")
        # return (new_state,  players, max_value, best_move)
            break

        # players.switch_player()
    return (state, players, max_value, best_move)


def minimize(game_state, players, alpha, beta, move):
    if (game_state.is_over()):
        v = game_state.state_val(players.get_current_player())
        print("MIN")
        print(move)
        print(v)
        return (game_state, players,  v, move)

    min_value = game_state.total_boxes() + 1
    best_move = None
    state = None

    for m in game_state.get_valid_moves():

        line = dotbox.Line(m, players.get_current_player())
        scored, new_state = game_state.test_move(line)

        if scored:
            (x, x,  v, max_move) = minimize(
                new_state,  players, alpha, beta, m)

            # if v < min_value:
            #     min_value = v
            #     best_move = m
            #     state = new_state

        else:
            players.switch_player()
            (x, x,  v, max_move) = maximize(
                new_state,  players, alpha, beta, m)

        if (v < min_value) or (v == min_value and np.random.choice([True, False])):
            min_value = v
            best_move = m
            state = new_state

        beta = min(beta, min_value)

        if beta <= alpha:
            print("MINIMIZER PRUNE")
        # players.switch_player()
        # return (new_state,  players, min_value, best_move)
            break

        # players.switch_player()
    return (state, players, min_value, best_move)


def getMove(game_state, players):
    boxes = game_state.total_boxes()
    print(game_state.get_valid_moves())
    return maximize(game_state, players, -(boxes+1), boxes + 1, game_state.get_valid_moves()[0])
