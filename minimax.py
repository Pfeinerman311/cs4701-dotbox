
import math


def value(x):
    return 0, "New State"


def minimax(checkDepth, gameState,
            maxTurn,
            Depth):

    # Presetting depth to check
    if (checkDepth == Depth):
        return value(nodeIndex)

    # Maximizer's Turn
    if (maxTurn):
        level_value, gameState = value()
        return max(minimax(checkDepth + 1, gameState,
                           False,  Depth),
                   minimax(curDepth + 1, gameState,
                           False, Depth))
    # Minimizer's Turn
    else:
        return min(minimax(checkDepth + 1, gameState
                           True,  Depth),
                   minimax(checkDepth + 1, gameState,
                           True,  Depth))


treeDepth = 2

print(minimax(0, 0, True, treeDepth))
