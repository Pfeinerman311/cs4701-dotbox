import dotbox


def maximize(gameState, players, alpha, beta):
    max_value = -2
    best_move = None

    if (gameState.is_over()):
        v = gameState.term_val(players.get_current_player())
        return (0, 0,  v, 0)

    for m in gameState.get_valid_moves():
        line = dotbox.Line(m, players.get_current_player())
        scored, ngameState = gameState.test_move(line)

        if scored:
            (x, y, v, min_move) = maximize(
                ngameState, players, alpha, beta)
        else:
            players.switch_player()
            (x, y, v, min_move) = minimize(
                ngameState, players, alpha, beta)

        if v > max_value:
            max_value = v
            best_move = m

        if max_value >= beta:
            # players.switch_player()
            return (ngameState,  players, max_value, best_move)

        if max_value > alpha:
            alpha = max_value

        # players.switch_player()
        return (ngameState, players, max_value, best_move)


def minimize(gameState,
             players, alpha, beta):
    min_value = 2
    best_move = None
    if (gameState.is_over()):
        v = gameState.term_val(players.get_current_player())
        return (0, 0,  v, 0)

    for m in gameState.get_valid_moves():

        line = dotbox.Line(m, players.get_current_player())
        scored, ngameState = gameState.test_move(
            line)
        if scored:
            (x, x,  v, max_move) = minimize(
                ngameState,  players, alpha, beta)
        else:
            players.switch_player()
            (x, x,  v, max_move) = maximize(
                ngameState,  players, alpha, beta)

        if v < min_value:
            min_value = v
            best_move = m

        if min_value <= alpha:
            # players.switch_player()
            return (ngameState,  players, min_value, best_move)

        if min_value < beta:
            beta = min_value

        # players.switch_player()
        return (ngameState, players, min_value, best_move)


def getMove(game_state, players):

    return maximize(game_state, players, 2, -2)
