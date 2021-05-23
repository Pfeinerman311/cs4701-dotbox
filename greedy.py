import dotbox
import numpy as np


def box_move(gameState, players):
    moves = gameState.get_valid_moves()
    best_move = None
    s = False
    for m in moves:
        line = dotbox.Line(m, players.get_current_player())
        scored, new_game_state = gameState.test_move(line)
        if scored or s:
            if np.random.choice([True, False]):
                best_move = m
    if best_move != None:
        return best_move
    else:
        return moves[np.random.choice(len(moves))]


def getGreedyMove(game_state, players):

    return box_move(game_state, players)
