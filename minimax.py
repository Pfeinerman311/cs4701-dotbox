
import math
import dotbox


def value(x):
    return 0, "New State"


def minimax(gameState,
            maxTurn,
            player):

    # Presetting depth to check
    if (gameState.isOver()):
        return gameState.termval(player)

    # Maximizer's Turn
    if (maxTurn):
        level_value, gameState = value()
        return max(minimax(checkDepth + 1, gameState,
                           False,  Depth),
                   minimax(curDepth + 1, gameState,
                           False, Depth))
    # Minimizer's Turn
    else:
        return min(minimax(checkDepth + 1, gameState,
                           True,  Depth),
                   minimax(checkDepth + 1, gameState,
                           True,  Depth))


def getMove(player, game_state, stop_search):

    minimax(game_state, True,  player)
