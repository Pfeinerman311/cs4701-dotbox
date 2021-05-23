class Player:
    def __init__(self, id):
        self.id = id
        self.points = 0

    def get_id(self):
        return self.id

    def get_points(self):
        return self.points


class Players:
    def __init__(self, n):
        self.players = []
        self.init_players(n)
        self.current_player = self.players[0]

    def init_players(self, n):

        for i in range(int(n)):
            self.players.append(Player(i))

    def p_length(self):
        return len(self.players)

    def get_players(self):
        return self.players

    def get_current_player(self):
        return self.current_player

    def switch_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def set_user_player(self):
        self.current_player = self.players[0]

    def set_ai_player(self):
        self.current_player = self.players[1]

    def get_other_player(self):
        if self.current_player == self.players[0]:
            return self.players[1]
        else:
            return self.players[0]
