import dotbox


def box_move(gameState, players):
    for i in gameState.get_valid_moves():
        line = dotbox.Line(i, players.get_current_player())
        scored, new_game_state = gameState.test_move(line)
        if scored:
            return i

    return gameState.get_valid_moves()[0]


def getGreedyMove(game_state, players):

    return box_move(game_state, players)
