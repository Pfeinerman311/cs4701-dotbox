import pygame
from pygame.locals import *
from pygame import gfxdraw
from time import sleep
from random import choice
from builtins import input
from collections import namedtuple

# Gui code inspired by https://github.com/coderkalyan/dots-boxes-py/blob/master/dots_boxes.py


class Ui:
    # Init of user interface
    def __init__(self, Boardsize, Grid, ai_game):
        self.Grid = Grid
        self.boards = Boardsize
        self.Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])
        pygame.init()
        pygame.font.init()
        self.is_ai = ai_game
        self.font = pygame.font.SysFont('timesnewroman', 50)
        self.score_font = pygame.font.SysFont('timesnewroman', 30)
        self.dot_font = pygame.font.SysFont('timesnewroman', 15)
        self.size = self.boards * 100 + 100
        self.w = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Dots and  Boxes")
        if self.is_ai:
            self.boxu = self.font.render('C1', True, (0, 0, 255))
            self.boxc = self.font.render('C2', True, (255, 0, 0))
        else:
            self.boxu = self.font.render('U', True, (0, 0, 255))
            self.boxc = self.font.render('C', True, (255, 0, 0))
        self.clock = pygame.time.Clock()
        self.board = []

        for i in range(self.boards):
            for i2 in range(self.boards):

                self.board.append(
                    self.Point(self.boards * i + i2, i2 * 100 + 100, i * 100 + 100, []))
        self.moves_completed = []
        self.score = [0, 0]
        self.is_user_turn = True
        self.boxes = []
        self.moves_completed_persons = []
        for row in range(self.boards-1):
            for col in range(self.boards-1):
                self.boxes.append([row*self.boards + col, 0])

    def id_to_index(self, _id):
        for i in range(len(self.board)):
            if self.board[i].id == _id:
                return i
        return -1

    def disp_board(self):
        if self.is_ai:
            self.score_user = self.score_font.render(
                "GAI: {}".format(self.score[0]), True, (0, 0, 255))

            w, h = self.score_font.size("GAI: {}".format(self.score[0]))
            self.w.blit(self.score_user, (self.size // 2 - w - 10, 10))
        else:

            self.score_user = self.score_font.render(
                "USER: {}".format(self.score[0]), True, (0, 0, 255))

            w, h = self.score_font.size("USER: {}".format(self.score[0]))
            self.w.blit(self.score_user, (self.size // 2 - w - 10, 10))

        score_comp = self.score_font.render(
            "AI: {}".format(self.score[1]), True, (255, 0, 0))
        w2, h2 = self.score_font.size("AI: {}".format(self.score[1]))
        self.w.blit(score_comp, (self.size // 2 + 10, 10))

        if self.is_user_turn:

            gfxdraw.filled_circle(self.w, self.size // 2 - w -
                                  20, 10 + h // 2, 7, (0, 0, 255))
            gfxdraw.aacircle(self.w, self.size // 2 - w - 20,
                             10 + h // 2, 7, (0, 0, 255))
        else:

            gfxdraw.filled_circle(self.w, self.size // 2 + w2 +
                                  20, 10 + h2 // 2, 7, (255, 0, 0))
            gfxdraw.aacircle(self.w, self.size // 2 +
                             w2 + 20, 10 + h2 // 2, 7, (255, 0, 0))

        for i, move in enumerate(self.moves_completed):
            p1 = self.board[self.id_to_index(move[0])]
            p2 = self.board[self.id_to_index(move[1])]
            thickness = 3 if move == self.moves_completed[-1] else 1
            if self.moves_completed_persons[i]:
                pygame.draw.line(self.w, (0, 0, 255), (p1.x, p1.y),
                                 (p2.x, p2.y), thickness)
            else:
                pygame.draw.line(self.w, (255, 0, 0), (p1.x, p1.y),
                                 (p2.x, p2.y), thickness)

        for i, point in enumerate(self.board):

            gfxdraw.filled_circle(self.w, point.x,
                                  point.y, 5, (0, 0, 0))
            gfxdraw.aacircle(self.w, point.x,
                             point.y, 5, (0, 0, 0))
            dot_num = self.dot_font.render(str(i), True, (0, 0, 0))
            self.w.blit(dot_num, (point.x + 10, point.y - 20))

        for box in self.boxes:

            x1 = self.board[self.id_to_index(box[0])].x
            y1 = self.board[self.id_to_index(box[0])].y
            # User
            if box[1] == 1:
                if self.is_ai:
                    text_width, text_height = self.font.size("C1")
                    self.w.blit(self.boxu, (x1 + 50 - text_width /
                                            2, y1 + 50 - text_height / 2))
                else:
                    text_width, text_height = self.font.size("U")
                    self.w.blit(self.boxu, (x1 + 50 - text_width /
                                            2, y1 + 50 - text_height / 2))
            # Comp
            elif box[1] == 2:
                if self.is_ai:
                    text_width, text_height = self.font.size("C2")
                    self.w.blit(self.boxc, (x1 + 50 - text_width /
                                            2, y1 + 50 - text_height / 2))

                text_width, text_height = self.font.size("C")
                self.w.blit(self.boxc, (x1 + 50 - text_width /
                                        2, y1 + 50 - text_height / 2))

    def move(self, is_user, id1, id2):
        self.is_user_turn = is_user
        self.board[self.id_to_index(id1)].partners.append(id2)
        self.board[self.id_to_index(id2)].partners.append(id1)
        self.moves_completed.append((id1, id2))
        self.moves_completed_persons.append(is_user)

    def start(self):
        self.w.fill((255, 255, 255))
        self.disp_board()
        pygame.display.update()

    def fill_box(self, boxe, player):
        index = int(list(boxe)[0])
        tmp = index//self.boards
        n_index = index-tmp

        for i, box in enumerate(self.boxes[n_index:n_index+1]):
            if player == 1:
                self.score[1] += 1
            else:
                self.score[0] += 1
            self.boxes[i+n_index][1] = player+1
            self.is_box = True

    def rerun(self):
        self.w.fill((255, 255, 255))
        self.disp_board()
        pygame.display.update()

    def update_pygame(self):
        pygame.display.update()
