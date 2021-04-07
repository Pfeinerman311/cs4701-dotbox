import numpy as np


class Line:
    def __init__(self, pts, owner=None):
        self.pts = pts
        self.owner = owner

    def own(self, owner):
        self.owner = owner

    def get_pts(self):
        return self.pts

    def get_owner(self):
        return self.owner


class Box:
    def __init__(self, corners, owner=None):
        self.corners = corners
        self.lines = []
        self.owner = None

    def get_corners(self):
        return self.corners

    def get_lines(self):
        return self.lines

    def get_owner(self):
        return self.owner

    def is_edge(self, line):
        p1, p2 = Line.get_pts(line)[0], Line.get_pts(line)[1]
        return (p1 in self.corners) and (p2 in self.corners)

    def add_line(self, line):
        assert len(self.lines) == 4
        assert not (line in self.lines)
        assert self.is_edge(line)
        self.lines.append(line)
        if len(self.lines) == 4:
            self.owner = Line.get_owner(line)
            return self.owner
        else:
            return None


class Grid:
    def __init__(self, dim):
        self.dim = dim
        self.lines = []
        self.boxes = np.zeros((dim[0]-1, dim[1]-1))
        for row in range(dim[0]-1):
            for col in range(dim[1]-1):
                self.boxes[row, col] = Box([(row, col), (row, col+1),
                                            (row+1, col), (row+1, col+1)])

    def is_full(self):
        rows, cols = self.dim[0], self.dim[1]
        max = 2*rows*col - row - col
        return (len(self.lines) == max)
