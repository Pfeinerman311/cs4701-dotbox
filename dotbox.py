import numpy as np


class Line:
    def __init__(self, pts, owner=None):
        self.pts = tuple(sorted(pts, key=lambda tup: [tup[0], tup[1]]))
        self.owner = owner

    def __eq__(self, line):
        return (self.pts == line.get_pts())

    def __repr__(self):
        return 'Line({!r}, {!r})'.format(self.pts, self.owner)

    def __str__(self):
        return 'Line conntecting points {}, Owner is {}'.format(self.pts, self.owner)

    def own(self, owner):
        self.owner = owner

    def get_pts(self):
        return self.pts

    def get_owner(self):
        return self.owner

    def get_dir(self):
        if self.pts[0][0] == self.pts[1][0]:
            return 0
        else:
            return 1


class Box:
    def __init__(self, index, owner=None):
        self.index = index
        self.owner = None
        self.lines = []

    def get_index(self):
        return self.index

    def get_corners(self):
        r, c = self.index[0], self.index[1]
        return [(r, c), (r, c+1), (r+1, c), (r+1, c+1)]

    def get_owner(self):
        return self.owner

    def get_lines(self):
        return self.lines

    def get_line_count(self):
        return len(self.lines)

    def is_edge(self, line):
        p1, p2 = line.get_pts()[0], line.get_pts()[1]
        return (p1 in self.get_corners()) and (p2 in self.get_corners())

    def add_line(self, line):
        assert self.is_edge(line)
        assert self.get_line_count() < 4
        exists = False
        for l in self.lines:
            exists = line.is_same(l)
        assert not exists
        self.lines = np.append(self.lines, line)


class Grid:
    def __init__(self, dim, players):
        self.dim = dim
        self.players = players
        self.lines = {}
        self.boxes = np.zeros((dim[0]-1, dim[1]-1))
        for row in range(dim[0]):
            for col in range(dim[1]):
                if row < dim[0]-1:
                    self.lines[(row, col), (row+1, col)] = Line(
                        ((row, col), (row+1, col)))
                if col < dim[1]-1:
                    self.lines[(row, col), (row, col+1)] = Line(
                        ((row, col), (row, col+1)))
        for row in range(dim[0]-1):
            for col in range(dim[1]-1):
                self.boxes[row, col] = Box((row, col))

    def game_over(self):
        # rows, cols = self.dim[0], self.dim[1]
        # max = 2*rows*cols - rows - cols
        # return (len(self.lines) == max)
        owners = [l.get_owner() for l in self.lines]
        return not (None in owners)

    def get_line_index(self, line):
        pts = [l.get_pts() for l in self.lines]
        return np.where(pts[0] == line.get_pts())[0]

    def upd_boxes(self, line):
        p1 = line.get_pts()[0]
        self.boxes[p1[0], p1[1]] = self.boxes[p1[0], p1[1]].add_line(line)
        if (line.get_dir() == 0) and (p1[0] != 0):
            self.boxes[p1[0]-1, p1[1]] = self.boxes[p1[0],
                                                    p1[1]].add_line(line)
        elif (line.get_dir() == 1) and (p1[1] != 0):
            self.boxes[p1[0], p1[1]-1] = self.boxes[p1[0],
                                                    p1[1]].add_line(line)

    def is_valid(self, line):
        valid = True
        p1, p2 = line.get_pts()[0], line.get_pts()[1]
        valid = valid and ((p1[0] >= 0) and (p1[1] >= 0))
        valid = valid and ((p2[0] >= 0) and (p2[1] >= 0))
        valid = valid and ((p1[0] < self.dim[0]) and (p1[1] < self.dim[1]))
        valid = valid and ((p2[0] < self.dim[0]) and (p2[1] < self.dim[1]))
        current = self.lines[line.get_pts()]
        valid = valid and (current.get_owner() == None)
        valid = valid and (line.get_owner() in self.players)
        return valid

    def draw_line(self, line):
        assert not self.game_over()
        key = line.get_pts()
        current = self.lines[key]
        assert current.get_owner() == None
        self.lines[key] = line
        self.upd_boxes(line)
        return line.get_pts()

    def get_scores(self):
        scores = {None: 0}
        for p in self.players:
            scores[p] = 0
        for box in self.boxes:
            scores[box.get_owner()] += 1
        del scores[None]
        return scores

    def get_winner(self):
        scores = self.get_scores()
        m = max(scores, key=lambda key: scores[key])
        winners = [k for k, v in scores.items() if v == scores[m]]
        return winners
