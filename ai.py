
import math
import dotbox


def minimax(gameState,
            maxTurn,
            player, players):

    # Base Case
    if (gameState.is_over()):
        return gameState.term_val(players.get_players()[player])

    # Maximizer's Turn
    if (maxTurn):
        vals = []
        if player == 1:
            player = 0
        else:
            player = 1
        for move in gameState.get_valid_moves():
            vals.append(minimax(gameState.test_move(
                move), False, player, players))
        return max(vals)

    # Minimizer's Turn
    else:
        vals = []
        if player == 1:
            player = 0
        else:
            player = 1
        for move in gameState.get_valid_moves():
            vals.append(minimax(gameState.test_move(
                move), True, player, players))
        return min(vals)


def getMove(player, game_state, players):

    return minimax(game_state, True,  player, players)
