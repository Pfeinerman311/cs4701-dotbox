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
        tmp = []
        for i in n:
            tmp.append(Player(i))
        return tmp

    def number_of_players(self, self.players):
        return len(self.players)

    def get_players(self):
        return self.players
