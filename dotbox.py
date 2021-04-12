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

    def get_dir(self):
        if self.pts[0][0] == self.pts[1][0]:
            return 0
        else:
            return 1

    def is_same(self, line):
        return (self.pts == line.get_pts())


class Box:
    def __init__(self, index, owner=None):
        self.index = index
        self.owner = None

    def get_index(self):
        return self.index

    def get_corners(self):
        r, c = self.index[0], self.index[1]
        return [(r, c), (r, c+1), (r+1, c), (r+1, c+1)]

    def get_owner(self):
        return self.owner

    def is_edge(self, line):
        p1, p2 = line.get_pts()[0], line.get_pts()[1]
        return (p1 in self.get_corners()) and (p2 in self.get_corners())


class Grid:
    def __init__(self, dim):
        self.dim = dim
        self.lines = []
        self.boxes = np.zeros((dim[0]-1, dim[1]-1))
        for row in range(dim[0]):
            for col in range(dim[1]):
                if row < dim[0]-2:
                    self.lines.append(Line([(row, col), (row+1, col)]))
                if col < dim[1]-2:
                    self.lines.append(Line([(row, col), (row, col+1)]))
        for row in range(dim[0]-1):
            for col in range(dim[1]-1):
                self.boxes[row, col] = Box((row, col))

    def is_full(self):
        #rows, cols = self.dim[0], self.dim[1]
        #max = 2*rows*cols - rows - cols
        # return (len(self.lines) == max)
        count = len(np.where(Line.get_owner(self.lines) == None))
        return (count == 0)

    def draw_line(self, line):
        assert not self.is_full()
        index = np.where(self.lines)
