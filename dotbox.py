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
        if self.pts[1] - self.pts[0] == 1:
            # Horizontal Line
            return 0
        else:
            # Vertical Line
            return 1

    def copy_line(self):
        return Line(self.pts, self.owner)


class Box:
    def __init__(self, index, owner=None):
        self.index = index
        self.owner = owner
        self.lines = []

    def get_index(self):
        return self.index

    def get_owner(self):
        return self.owner

    def own(self, player):
        assert self.owner == None
        self.owner = player

    def get_corners(self, dim):
        i = self.index
        return [i, i+1, i+dim[1], i+dim[1]+1]

    def get_edges(self, dim):
        c = self.get_corners(dim)
        return [(c[0], c[1]), (c[1], c[2]), (c[2], c[3]), (c[3], c[0])]

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
            exists = l == line
        assert not exists
        self.lines = np.append(self.lines, line)
        if self.get_line_count() == 4:
            self.owner = line.get_owner()
            return True
        else:
            return False

    def copy_box(self):
        return Box(self.index, self.owner)


class Grid:
    def __init__(self, dim, players):
        self.dim = dim
        self.players = players
        self.lines = {}
        self.boxes = {}
        for row in range(dim[0]):
            for col in range(dim[1]):
                if col < dim[1]-1:
                    self.lines[(row*dim[1]+col, row*dim[1]+col+1)] = Line(
                        (row*dim[1]+col, row*dim[1]+col+1))
                if row < dim[0]-1:
                    self.lines[(row*dim[1]+col, (row+1)*dim[1]+col)] = Line(
                        (row*dim[1]+col, (row+1)*dim[1]+col))
        for row in range(dim[0]-1):
            for col in range(dim[1]-1):
                self.boxes[row*dim[1]+col] = Box(row*dim[1]+col)

    def game_over(self):
        owners = [l.get_owner() for l in self.lines.values()]
        return not (None in owners)

    def get_line_index(self, line):
        pts = [l.get_pts() for l in self.lines]
        return np.where(pts[0] == line.get_pts())[0]

    def box_corners(self, index):
        return [index, index+1, index+self.dim[1]+1, index+self.dim[1]]

    def box_edges(self, index):
        c = self.box_corners(index)
        return [(c[0], c[1]), (c[1], c[2]), (c[3], c[2]), (c[0], c[3])]

    # def check_box(self, index):
    #     filled = 1
    #     edges = self.box_edges(index)
    #     for e in edges:
    #         if self.lines[e].get_owner() == None:
    #             filled = 0
    #     if self.boxes[index].get_owner() != None:
    #         filled = 2
    #     return filled

    def check_box(self, index):
        lines = 0
        edges = self.box_edges(index)
        for e in edges:
            if self.lines[e].get_owner() != None:
                lines += 1
        # if self.boxes[index].get_owner() != None:
        #     lines = -1
        return lines

    def upd_boxes(self, line):
        p1 = line.get_pts()[0]
        player = line.get_owner()
        filled = {}
        # self.print_boxes()
        if (p1 % self.dim[1] < self.dim[1]-1) and (p1 / self.dim[0] < self.dim[0]-1):
            # print("FIRST")
            # print(p1)
            if self.check_box(p1) == 4:
                self.boxes[p1].own(player)
                filled[p1] = self.boxes[p1]
        if (line.get_dir() == 0) and (p1/self.dim[1] >= 1):
            # print("SECOND")
            # print(p1-self.dim[1])
            if self.check_box(p1-self.dim[1]) == 4:
                self.boxes[p1 - self.dim[1]].own(player)
                filled[p1-self.dim[1]] = self.boxes[p1-self.dim[1]]
        if (line.get_dir() == 1) and (p1 % self.dim[1] > 0):
            # print("THIRD")
            # print(p1-1)
            if self.check_box(p1-1) == 4:
                self.boxes[p1-1].own(player)
                filled[p1-1] = self.boxes[p1-1]
        # self.print_boxes()
        return filled

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
        assert self.is_valid(line)
        key = line.get_pts()
        current = self.lines[key]
        assert current.get_owner() == None
        self.lines[key] = line
        filled = self.upd_boxes(line)
        if len(filled) > 0:
            scored = True
        # print("FILLED")
        # print(filled)
        # print("SCORE")
        # print(self.get_scores())
        return scored, line.get_pts(), filled

    def get_scores(self):
        # scores = {None: 0}
        # for p in self.players:
        #     scores[p] = 0
        # for box in self.boxes.values():
        #     scores[box.get_owner()] += 1
        # del scores[None]
        # return scores
        # self.print_boxes()
        scores = {}
        # print(self.players)
        for p in self.players:
            scores[p] = 0
        for box in self.boxes.values():
            if box.get_owner() != None:
                scores[box.get_owner()] = scores[box.get_owner()] + 1
        #del scores[None]
        # print(scores)
        return scores

    def get_winner(self):
        scores = self.get_scores()
        m = max(scores, key=lambda key: scores[key])
        winners = [k for k, v in scores.items() if v == scores[m]]
        return winners

    def get_valid_moves(self):
        # if self.is_over():
        #     return []
        # else:
        valid = [k for k, v in self.lines.items() if v.get_owner() == None]
        return valid

    def state_val(self, player):
        tot_boxes = self.total_boxes()
        # print(tot_boxes)
        to_win = tot_boxes/2
        # print(to_win)
        scores = self.get_scores()
        # print(scores)
        for w in self.get_winner():
            # print(w)
            if scores[w] > to_win:
                # print(scores[w])
                #print(w == player)
                if w == player:
                    return tot_boxes
                else:
                    return -tot_boxes
        threes = [k for k in self.boxes.keys() if self.check_box(k) == 3]
        num_threes = len(threes)
        opp = [v for k, v in scores.items() if k != player and k != None]
        # # if scores[player] + num_threes > to_win:
        # if opp[0] + num_threes > to_win:
        #     return -tot_boxes
        # else:
        #     return scores[player] - num_threes - opp[0]
        return scores[player] - opp[0]

    def val(self, move):
        assert self.is_valid(move)
        player = move.get_owner()
        tot_boxes = len(self.boxes)
        to_win = tot_boxes/2
        scores = self.get_scores()
        for w in self.get_winner():
            if scores[w] >= to_win:
                if w == player:
                    return tot_boxes
                else:
                    return -tot_boxes
        threes = [k for k in self.boxes.keys() if self.check_box(k) == 3]
        num_threes = len(threes)
        if scores[player] + num_threes > to_win:
            return tot_boxes
        else:
            opp = [v for k, v in scores.items() if k != player and k != None]
            return scores[player] - opp[0] - num_threes

    def is_over(self):
        if self.game_over():
            return True
        tot_boxes = len(self.boxes)
        to_win = tot_boxes//2
        scores = self.get_scores()
        for w in self.get_winner():
            if scores[w] > to_win:
                return True
        else:
            return False

    def term_val(self, player):
        assert self.game_over()
        winners = self.get_winner()
        if len(winners) != 1:
            return 0
        w = winners.pop()
        if w == player:
            return 1
        else:
            return -1

    def test_move(self, line):
        assert not self.game_over()
        assert self.is_valid(line)
        key = line.get_pts()
        current = self.lines[key]
        assert current.get_owner() == None
        new_grid = self.copy_grid()
        new_grid.lines[key] = line
        filled = new_grid.upd_boxes(line)
        scored = len(filled) > 0
        return scored, new_grid

    def print_lines(self):
        for l in self.lines.values():
            print(str(l) + ", ")

    def total_boxes(self):
        return len(self.boxes)

    def copy_grid(self):
        new_grid = Grid(self.dim, self.players)
        for k, v in self.lines.items():
            new_grid.lines[k] = v.copy_line()
        for k, v in self.boxes.items():
            new_grid.boxes[k] = v.copy_box()
        return new_grid

    def print_boxes(self):
        for k in self.boxes.keys():
            print(str(k) + ": " + str(self.boxes[k].get_owner()))

    def will_lose(self, player):
        tot_boxes = self.total_boxes()
        to_win = tot_boxes//2
        scores = self.get_scores()
        for w in self.get_winner():
            if scores[w] > to_win:
                if w != player:
                    return True
        threes = [k for k in self.boxes.keys() if self.check_box(k) == 3]
        num_threes = len(threes)
        opp = [v for k, v in scores.items() if k != player and k != None]
        if opp[0] + num_threes > to_win:
            return True
        return False
