import numpy as np


class Line:
    def __init__(self, pts, owner=None):
        self.pts = tuple(sorted(pts))
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
        if self.pts[0] - self.pts[1] == 1:
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

    def get_corners(self, dim):
        i = self.index
        return [i, i+1, i+dim[1], i+dim[1]+1]

    def get_owner(self):
        return self.owner

    def get_lines(self):
        return self.lines

    def get_line_count(self):
        return len(self.lines)

    def is_edge(self, line, dim):
        p1, p2 = line.get_pts()[0], line.get_pts()[1]
        return (p1 in self.get_corners(dim)) and (p2 in self.get_corners(dim))

    def add_line(self, line, dim):
        assert self.is_edge(line, dim)
        assert self.get_line_count() < 4
        exists = False
        for l in self.lines:
            exists = line.is_same(l)
        assert not exists
        self.lines = np.append(self.lines, line)
        if self.get_line_count() == 4:
            self.owner = line.get_owner()
            return True
        else:
            return False


class Grid:
    def __init__(self, dim, players):
        self.dim = dim
        self.players = players
        self.lines = {}
        self.boxes = {}
        for row in range(dim[0]):
            for col in range(dim[1]):
                if row < dim[0]-1:
                    self.lines[(row*dim[1]+col, (row+1)*dim[1]+col)] = Line(
                        (row*dim[1]+col, (row+1)*dim[1]+col))
                if col < dim[1]-1:
                    self.lines[(row*dim[1]+col, row*dim[1]+col+1)] = Line(
                        (row*dim[1]+col, row*dim[1]+col+1))
        for row in range(dim[0]-1):
            for col in range(dim[1]-1):
                self.boxes[row*dim[1]+col] = Box(row*dim[1]+col)

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
        score = 0
        if self.boxes[p1].add_line(line, self.dim):
            score += 1
        if (line.get_dir() == 0) and (p1/self.dim[1] >= 1):
            if self.boxes[p1-self.dim[1]].add_line(line, self.dim):
                score += 1
        elif (line.get_dir() == 1) and (p1 % self.dim[1] > 0):
            if self.boxes[p1-1].add_line(line, self.dim):
                score += 1
        return score

    def is_valid(self, line):
        valid = True
        p1, p2 = line.get_pts()[0], line.get_pts()[1]
        valid = valid and ((p2-p1 == 1) or (p2-p1 == self.dim[1]))
        valid = valid and ((p1 >= 0) and (p1 < self.dim[0]*self.dim[1]))
        valid = valid and ((p2 >= 0) and (p2 < self.dim[0]*self.dim[1]))
        current = self.lines[line.get_pts()]
        valid = valid and (current.get_owner() == None)
        valid = valid and (line.get_owner() in self.players)
        return valid

    def draw_line(self, line):
        scored = False
        assert not self.game_over()
        key = line.get_pts()
        current = self.lines[key]
        assert current.get_owner() == None
        self.lines[key] = line
        if self.upd_boxes(line) > 0:
            scored = True
        return scored, line.get_pts()

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
