
import math
import dotbox


def minimax(gameState,
            maxTurn,
            player, players):

    print("----------------")

    # Base Case
    if (gameState.is_over()):
        print("in case")
        return gameState.term_val(players.get_players()[player])
    print(gameState.is_over())
    # Maximizer's Turn
    elif (maxTurn):
        vals = [0]
        if player == 1:
            player = 0
        else:
            player = 1

        # print(gameState.get_valid_moves())

        for m1, m2 in gameState.get_valid_moves():

            line = dotbox.Line((m1, m2), players.get_players()[player])
            vals.append(minimax(gameState.test_move(
                line), False, player, players))
        return max(vals)

    # Minimizer's Turn
    else:
        vals = []
        if player == 1:
            player = 0
        else:
            player = 1

        for m1, m2 in gameState.get_valid_moves():
            print(m1)
            print(m2)
            print("is over")
            print(gameState.is_over())
            # print(dotbox.Line((m1, m2), players.get_players()[player]))

            line = dotbox.Line((m1, m2), players.get_players()[player])
            vals.append(minimax(gameState.test_move(
                line), True, player, players))
        return min(vals)


def getMove(player, game_state, players):

    return minimax(game_state, True,  player, players)