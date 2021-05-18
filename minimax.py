
import math
import dotbox


def minimax(gameState,
            maxTurn,
            player, players):

    # Presetting depth to check
    if (gameState.is_over()):
        return gameState.term_val(player)

    # Maximizer's Turn
    if (maxTurn):
        vals = []
        for move in gameState.get_valid_moves():
            vals.append(minimax(gameState.test_move(
                move), False, players-player))
        return max(vals)

    # Minimizer's Turn
    else:
        vals = []
        for move in gameState.get_valid_moves():
            vals.append(minimax(gameState.test_move(move), True, NEXT PLAYER))
        return min(vals)


def getMove(player, game_state, players):

    minimax(game_state, True,  player, players)
