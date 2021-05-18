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

    def init_players(self, n):
        print("in users init")
        tmp = []
        for i in range(int(n)):
            print("player " + str(i))
            self.players.append(Player(i))

    def p_length(self):
        return len(self.players)

    def get_players(self):
        return self.players
