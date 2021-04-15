import pygame
from pygame.locals import *
from pygame import gfxdraw
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input


class Ui:

    def __init__(self, Boardsize, Grid):
        self.Grid = Grid
        self.Boardsize = Boardsize

        self.BOARDSIZE = 4
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        self.OWNER_NONE = 0
        self.OWNER_USER = 1
        self.OWNER_COMPUTER = 2

        self.Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 50)
        self.score_font = pygame.font.SysFont('Arial', 30)
        self.dot_font = pygame.font.SysFont('Arial', 15)

        self.BOX_USER = self.font.render('U', True, self.BLUE)
        self.BOX_COMPUTER = self.font.render('C', True, self.RED)
        self.spoke1 = [(2, 6), (10, 11), (9, 13), (4, 5)]
        self.spoke2 = [(1, 5), (6, 7), (10, 14), (8, 9)]

        self.size = self.BOARDSIZE * 100 + 100
        self.SURF = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Dots and  Boxes")

        self.clock = pygame.time.Clock()

        self.board = []
        for i in range(self.BOARDSIZE):
            for i2 in range(self.BOARDSIZE):

                self.board.append(
                    self.Point(self.BOARDSIZE * i + i2, i2 * 100 + 100, i * 100 + 100, []))
        self.moves_done = []
        self.moves_done_persons = []
        self.boxes = [[i, i+1, i+self.BOARDSIZE, i+self.BOARDSIZE+1, self.OWNER_NONE]
                      for i in range(0, 3)]
        self.boxes.extend([[i, i+1, i+self.BOARDSIZE, i+self.BOARDSIZE+1, self.OWNER_NONE]
                           for i in range(4, 7)])
        self.boxes.extend([[i, i+1, i+self.BOARDSIZE, i+self.BOARDSIZE+1, self.OWNER_NONE]
                           for i in range(8, 11)])
        self.score = [0, 0]
        self.is_user_turn = True

    def id_to_index(self, _id):
        for i in range(len(self.board)):
            if self.board[i].id == _id:
                return i
        return -1

    def disp_board(self):
        self.score_user = self.score_font.render(
            "USER: {}".format(self.score[0]), True, self.BLUE)
        w, h = self.score_font.size("USER: {}".format(self.score[0]))
        self.SURF.blit(self.score_user, (self.size // 2 - w - 10, 10))
        score_comp = self.score_font.render(
            "AI: {}".format(self.score[1]), True, self.RED)
        w2, h2 = self.score_font.size("AI: {}".format(self.score[1]))
        self.SURF.blit(score_comp, (self.size // 2 + 10, 10))
        if self.is_user_turn:

            gfxdraw.filled_circle(self.SURF, self.size // 2 - w -
                                  20, 10 + h // 2, 7, self.BLUE)
            gfxdraw.aacircle(self.SURF, self.size // 2 - w - 20,
                             10 + h // 2, 7, self.BLUE)
        else:

            gfxdraw.filled_circle(self.SURF, self.size // 2 + w2 +
                                  20, 10 + h2 // 2, 7, self.RED)
            gfxdraw.aacircle(self.SURF, self.size // 2 +
                             w2 + 20, 10 + h2 // 2, 7, self.RED)
        for i, move in enumerate(self.moves_done):
            p1 = self.board[id_to_index(move[0])]
            p2 = self.board[id_to_index(move[1])]
            thickness = 3 if move == self.moves_done[-1] else 1
            if self.moves_done_persons[i]:
                pygame.draw.line(self.SURF, self.BLUE, (p1.x, p1.y),
                                 (p2.x, p2.y), thickness)
            else:
                pygame.draw.line(self.SURF, self.RED, (p1.x, p1.y),
                                 (p2.x, p2.y), thickness)

        for i, point in enumerate(self.board):

            gfxdraw.filled_circle(self.SURF, point.x,
                                  point.y, 5, self.BLACK)
            gfxdraw.aacircle(self.SURF, point.x,
                             point.y, 5, self.BLACK)
            dot_num = self.dot_font.render(str(i), True, self.BLACK)
            self.SURF.blit(dot_num, (point.x + 10, point.y - 20))
        for box in self.boxes:
            x1 = self.board[self.id_to_index(box[0])].x
            y1 = self.board[self.id_to_index(box[0])].y
            if box[4] == self.OWNER_USER:
                text_width, text_height = self.font.size("U")
                self.SURF.blit(self.BOX_USER, (x1 + 50 - text_width /
                                               2, y1 + 50 - text_height / 2))
            elif box[4] == self.OWNER_COMPUTER:
                text_width, text_height = self.font.size("C")
                self.SURF.blit(self.BOX_COMPUTER, (x1 + 50 - text_width /
                                                   2, y1 + 50 - text_height / 2))

    def is_connection(self, id1, id2):
        if (id1, id2) in self.moves_done:
            return True
        if (id2, id1) in self.moves_done:
            return True
        return False

    def is_valid(self, id1, id2):
        if is_connection(id1, id2):
            return False
        p1 = self.board[id_to_index(id1)]
        p2 = self.board[id_to_index(id2)]
        if (p1.x == p2.x + 100 or p1.x == p2.x - 100) and p1.y == p2.y:
            return True
        if p1.x == p2.x and (p1.y == p2.y + 100 or p1.y == p2.y - 100):
            return True
        return False

    def move(self, is_user, id1, id2):

        self.board[id_to_index(id1)].partners.append(id2)
        self.board[id_to_index(id2)].partners.append(id1)
        self.moves_done.append((id1, id2))
        self.moves_done_persons.append(is_user)
        return check_move_made_box(is_user, id1, id2)

    def possible_moves(self):
        possible = []
        for a in range(1, len(board)):
            for b in list(range(1, len(self.board))):
                if b == a:
                    continue
                if not is_valid(a, b):
                    continue
                possible.append((a, b))
        return possible

    def count_connections_box(self, box):

        count = 0
        not_connections = []
        if is_connection(box[0], box[1]):
            count += 1
        else:
            not_connections.append((box[0], box[1]))
            not_connections.append((box[1], box[0]))
        if is_connection(box[1], box[3]):
            count += 1
        else:
            not_connections.append((box[1], box[3]))
            not_connections.append((box[3], box[1]))
        if is_connection(box[2], box[3]):
            count += 1
        else:
            not_connections.append((box[2], box[3]))
            not_connections.append((box[3], box[2]))
        if is_connection(box[2], box[0]):
            count += 1
        else:
            not_connections.append((box[2], box[0]))
            not_connections.append((box[0], box[2]))

        return (count, not_connections)

    def check_complete(self):
        possible = possible_moves()
        if len(possible) == 0:

            print("Game over")
            if score[0] > score[1]:
                print("You won! Score: {} to {}".format(score[0], score[1]))
            elif score[1] > score[0]:
                print(
                    "Computer won :( Score: {} to {}".format(score[0], score[1]))
            else:
                print("Tie game. Score: {} to {}".format(score[0], score[1]))
            input("Press enter to end game:")
            pygame.quit()
            sys.exit()

    def move_makes_box(self, id1, id2):
        is_box = False

        for i, box in enumerate(boxes):
            temp = list(box[:-1])

            if id1 not in temp or id2 not in temp:
                continue

            temp.remove(id1)
            temp.remove(id2)

            if is_connection(temp[0], temp[1]):
                if (is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or (is_connection(id1, temp[1]) and is_connection(id2, temp[0])):
                    is_box = True

        return is_box

    def check_move_made_box(self, is_user, id1, id2):
        is_box = False
        for i, box in enumerate(boxes):
            temp = list(box[:-1])
            if id1 not in temp or id2 not in temp:
                continue
            temp.remove(id1)
            temp.remove(id2)
            if is_connection(temp[0], temp[1]) and ((is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or
                                                    (is_connection(id1, temp[1]) and is_connection(id2, temp[0]))):

                if is_user:
                    score[0] += 1
                    boxes[i][4] = OWNER_USER
                else:
                    score[1] + 1
                    boxes[i][4] = OWNER_COMPUTER
                is_box = True

        return is_box

    # def user_move(self,):
    #     try:
    #         p1, p2 = map(int, input(
    #             "What move do you want to make?").split(","))
    #     except ValueError:
    #         print("Invalid move.")
    #         user_move()
    #     else:
    #         if is_connection(p1, p2):
    #             print("Sorry, this move is already taken.")
    #             user_move()
    #         elif not is_valid(p1, p2):
    #             print("Invalid move.")
    #             user_move()
    #         else:
    #             is_box = move(True, p1, p2)
    #             check_complete()

    #             if is_box:
    #                 print("You scored! Have another turn.")
    #                 SURF.fill((255, 255, 255))
    #                 disp_board()
    #                 pygame.display.update()
    #                 check_complete()
    #                 user_move()

    def start(self):
        self.SURF.fill((255, 255, 255))
        self.disp_board()
        pygame.display.update()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.SURF.fill((255, 255, 255))
            self.is_user_turn = True
            self.disp_board()
            pygame.display.update()
            # self.user_move()
            self.disp_board()
            pygame.display.update()

    def rerun(self):
        self.SURF.fill((255, 255, 255))
        self.disp_board()
        pygame.display.update()
        self.check_complete()
