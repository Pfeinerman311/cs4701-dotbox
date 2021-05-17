
import math
import dotbox


def value(x):
    return 0, "New State"


def minimax(gameState,
            maxTurn,
            player):

    # Presetting depth to check
    if (gameState.is_over()):
        return gameState.term_val(player)

    # Maximizer's Turn
    if (maxTurn):
        vals = []
        for move in gameState.get_valid_moves():
            vals.append(minimax(gameState.test_move(move), False, NEXT PLAYER))
        return max(vals)

    # Minimizer's Turn
    else:
        return min(minimax(gameState,
                           True,  player),
                   minimax(gameState,
                           True,  player))


def getMove(player, game_state, stop_search):

    minimax(game_state, True,  player)
