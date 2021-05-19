import dotbox


# def max_alpha_beta(alpha, beta):
#     maxv = -2
#     px = None
#     py = None

#     result = is_end()

#     if result == 'X':
#         return (-1, 0, 0)
#     elif result == 'O':
#         return (1, 0, 0)
#     elif result == '.':
#         return (0, 0, 0)

#     for i in range(0, 3):
#         for j in range(0, 3):
#             if self.current_state[i][j] == '.':
#                 self.current_state[i][j] = 'O'
#                 (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
#                 if m > maxv:
#                     maxv = m
#                     px = i
#                     py = j
#                 self.current_state[i][j] = '.'

#                 # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
#                 if maxv >= beta:
#                     return (maxv, px, py)

#                 if maxv > alpha:
#                     alpha = maxv

#     return (maxv, px, py)


def maximize(gameState, players, alpha, beta):
    max_value = -2
    best_move = None

    if (gameState.is_over()):
        return gameState.term_val(players.get_players()[players.get_current_player])

    else:
        for m in gameState.get_valid_moves():
            line = dotbox.Line(m, players.get_players()[
                               players.get_current_player])
            ngameState = gameState.test_move(line)

            (x, y, z, v, min_move) = minimize(
                ngameState,  players, alpha, beta)

            if v > max_value:
                max_value = v
                best_move = m

            if max_value >= beta:
                players.switch_player()
                return (ngameState,  players, max_value, best_move)

            if max_value > alpha:
                alpha = max_value
            players.switch_player()
            return (ngameState, players, max_value, best_move)


#  def min_alpha_beta(self, alpha, beta):

#         minv = 2

#         qx = None
#         qy = None

#         result = self.is_end()

#         if result == 'X':
#             return (-1, 0, 0)
#         elif result == 'O':
#             return (1, 0, 0)
#         elif result == '.':
#             return (0, 0, 0)

#         for i in range(0, 3):
#             for j in range(0, 3):
#                 if self.current_state[i][j] == '.':
#                     self.current_state[i][j] = 'X'
#                     (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
#                     if m < minv:
#                         minv = m
#                         qx = i
#                         qy = j
#                     self.current_state[i][j] = '.'

#                     if minv <= alpha:
#                         return (minv, qx, qy)

#                     if minv < beta:
#                         beta = minv

#         return (minv, qx, qy)

def minimize(gameState,
             players, alpha, beta):
    min_value = 2
    best_move = None

    for m in gameState.get_valid_moves():

        line = dotbox.Line(m, players.get_players()[
                           players.get_current_player()])
        ngameState = gameState.test_move(
            line)
        (x, x, x, v, max_move) = maximize(
            ngameState,  players, alpha, beta)
        if m < min_value:
            min_value = v
            best_move = m

        if min_value <= alpha:
            players.switch_player()
            return (ngameState,  players, min_value, best_move)

        if min_value < beta:
            beta = min_value

        players.switch_player()
        return (ngameState, players, min_value, best_move)


def getMove(game_state, players):

    return maximize(game_state, players, 2, -2)
