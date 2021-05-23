import dotbox
import numpy as np


def maximize(game_state, players, alpha, beta, move):
    if (game_state.game_over()):
        v = game_state.state_val(players.get_current_player())
        return (game_state, players,  v, move)

    max_value = -(game_state.total_boxes() + 1)
    best_move = None
    state = None

    moves = game_state.get_valid_moves()

    if (len(moves) > 12):
        mv = -(game_state.total_boxes() + 1)
        bm = -(game_state.total_boxes() + 1)
        coords = moves[np.random.choice(len(moves))]
        line = dotbox.Line(coords, players.get_current_player())
        scored, new_state = game_state.test_move(line)
        return (game_state, players, 0, coords)

    for m in moves:
        line = dotbox.Line(m, players.get_current_player())
        scored, new_state = game_state.test_move(line)

        if scored:
            (x, y, v, max_move) = maximize(
                new_state, players, alpha, beta, m)

        else:
            (x, y, v, min_move) = minimize(
                new_state, players, alpha, beta, m)

        if (v > max_value) or (v == max_value and np.random.choice([True, False])):
            max_value = v
            best_move = m
            state = new_state

        alpha = max(alpha, max_value)

        if beta <= alpha:
            break

    return (state, players, max_value, best_move)


def minimize(game_state, players, alpha, beta, move):
    if (game_state.game_over()):
        v = game_state.state_val(players.get_current_player())
        return (game_state, players,  v, move)

    min_value = game_state.total_boxes() + 1
    best_move = None
    state = None

    moves = game_state.get_valid_moves()

    for m in moves:
        line = dotbox.Line(m, players.get_other_player())
        scored, new_state = game_state.test_move(line)

        if scored:
            (x, x,  v, max_move) = minimize(
                new_state,  players, alpha, beta, m)

        else:
            (x, x,  v, max_move) = maximize(
                new_state,  players, alpha, beta, m)

        if (v < min_value) or (v == min_value and np.random.choice([True, False])):
            min_value = v
            best_move = m
            state = new_state

        beta = min(beta, min_value)

        if beta <= alpha:
            break

    return (state, players, min_value, best_move)


def getMove(game_state, players):
    boxes = game_state.total_boxes()
    return maximize(game_state, players, -(boxes+1), boxes + 1, game_state.get_valid_moves()[0])
