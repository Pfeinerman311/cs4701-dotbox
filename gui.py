import pygame
from pygame.locals import *
from pygame import gfxdraw
from collections import namedtuple
from time import sleep
from random import choice
from builtins import input

BOARDSIZE = 4

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

OWNER_NONE = 0
OWNER_USER = 1
OWNER_COMPUTER = 2

Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 50)
score_font = pygame.font.SysFont('Arial', 30)
dot_font = pygame.font.SysFont('Arial', 15)

BOX_USER = myfont.render('U', True, BLUE)
BOX_COMPUTER = myfont.render('C', True, RED)
spoke1 = [(2, 6), (10, 11), (9, 13), (4, 5)]
spoke2 = [(1, 5), (6, 7), (10, 14), (8, 9)]

size = BOARDSIZE * 100 + 100
SURF = pygame.display.set_mode((size, size))
pygame.display.set_caption("Dots and  Boxes")

clock = pygame.time.Clock()


board = []
for i in range(BOARDSIZE):
    for i2 in range(BOARDSIZE):
        # print(BOARDSIZE * i + i2)
        board.append(
            Point(BOARDSIZE * i + i2, i2 * 100 + 100, i * 100 + 100, []))
moves_done = []
moves_done_persons = []
boxes = [[i, i+1, i+BOARDSIZE, i+BOARDSIZE+1, OWNER_NONE] for i in range(0, 3)]
boxes.extend([[i, i+1, i+BOARDSIZE, i+BOARDSIZE+1, OWNER_NONE]
              for i in range(4, 7)])
boxes.extend([[i, i+1, i+BOARDSIZE, i+BOARDSIZE+1, OWNER_NONE]
              for i in range(8, 11)])
score = [0, 0]  # user, computer
is_user_turn = True


def id_to_index(_id):
    for i in range(len(board)):
        if board[i].id == _id:
            return i
    return -1


def disp_board():
    score_user = score_font.render("USER: {}".format(score[0]), True, BLUE)
    w, h = score_font.size("USER: {}".format(score[0]))
    SURF.blit(score_user, (size // 2 - w - 10, 10))
    score_comp = score_font.render("AI: {}".format(score[1]), True, RED)
    w2, h2 = score_font.size("AI: {}".format(score[1]))
    SURF.blit(score_comp, (size // 2 + 10, 10))
    if is_user_turn:

        gfxdraw.filled_circle(SURF, size // 2 - w - 20, 10 + h // 2, 7, BLUE)
        gfxdraw.aacircle(SURF, size // 2 - w - 20, 10 + h // 2, 7, BLUE)
    else:

        gfxdraw.filled_circle(SURF, size // 2 + w2 + 20, 10 + h2 // 2, 7, RED)
        gfxdraw.aacircle(SURF, size // 2 + w2 + 20, 10 + h2 // 2, 7, RED)
    for i, move in enumerate(moves_done):
        p1 = board[id_to_index(move[0])]
        p2 = board[id_to_index(move[1])]
        thickness = 3 if move == moves_done[-1] else 1
        if moves_done_persons[i]:
            pygame.draw.line(SURF, BLUE, (p1.x, p1.y), (p2.x, p2.y), thickness)
        else:
            pygame.draw.line(SURF, RED, (p1.x, p1.y), (p2.x, p2.y), thickness)

    for i, point in enumerate(board):

        gfxdraw.filled_circle(SURF, point.x, point.y, 5, BLACK)
        gfxdraw.aacircle(SURF, point.x, point.y, 5, BLACK)
        dot_num = dot_font.render(str(i), True, BLACK)
        SURF.blit(dot_num, (point.x + 10, point.y - 20))
    for box in boxes:
        x1 = board[id_to_index(box[0])].x
        y1 = board[id_to_index(box[0])].y
        if box[4] == OWNER_USER:
            text_width, text_height = myfont.size("U")
            SURF.blit(BOX_USER, (x1 + 50 - text_width /
                                 2, y1 + 50 - text_height / 2))
        elif box[4] == OWNER_COMPUTER:
            text_width, text_height = myfont.size("C")
            SURF.blit(BOX_COMPUTER, (x1 + 50 - text_width /
                                     2, y1 + 50 - text_height / 2))


def is_connection(id1, id2):
    if (id1, id2) in moves_done:
        return True
    if (id2, id1) in moves_done:
        return True
    return False


def is_valid(id1, id2):
    if is_connection(id1, id2):
        return False
    p1 = board[id_to_index(id1)]
    p2 = board[id_to_index(id2)]
    if (p1.x == p2.x + 100 or p1.x == p2.x - 100) and p1.y == p2.y:
        return True
    if p1.x == p2.x and (p1.y == p2.y + 100 or p1.y == p2.y - 100):
        return True
    return False


def move(is_user, id1, id2):

    board[id_to_index(id1)].partners.append(id2)
    board[id_to_index(id2)].partners.append(id1)
    moves_done.append((id1, id2))
    moves_done_persons.append(is_user)
    return check_move_made_box(is_user, id1, id2)


def possible_moves():
    possible = []
    for a in range(1, len(board)):
        for b in list(range(1, len(board))):
            if b == a:
                continue
            if not is_valid(a, b):
                continue
            possible.append((a, b))
    return possible


def count_connections_box(box):

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


def get_best_move_v1(possible):
    # take random from possible moves
    return choice(possible)


def get_best_move_v2(possible):
    # check if there are any possible boxes
    for p_move in possible:
        if move_makes_box(*p_move):
            # this move can make a box - take it!
            return p_move

    return choice(possible)


def check_complete():
    possible = possible_moves()
    if len(possible) == 0:
        # game is finished!
        print("Game over")
        if score[0] > score[1]:
            print("You won! Score: {} to {}".format(score[0], score[1]))
        elif score[1] > score[0]:
            print("Computer won :( Score: {} to {}".format(score[0], score[1]))
        else:
            print("Tie game. Score: {} to {}".format(score[0], score[1]))
        input("Press enter to end game:")
        pygame.quit()
        sys.exit()


def move_makes_box(id1, id2):
    is_box = False
    # check if the connection just make from id1 to id2 made a box
    for i, box in enumerate(boxes):
        temp = list(box[:-1])
        # print(temp)
        if id1 not in temp or id2 not in temp:
            continue
        # temp = list(box[:])
        temp.remove(id1)
        temp.remove(id2)
        # print(temp)
        if is_connection(temp[0], temp[1]):
            if (is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or (is_connection(id1, temp[1]) and is_connection(id2, temp[0])):
                is_box = True

    return is_box


def check_move_made_box(is_user, id1, id2):
    is_box = False
    # check if the connection just make from id1 to id2 made a box
    for i, box in enumerate(boxes):
        temp = list(box[:-1])
        if id1 not in temp or id2 not in temp:
            continue
        temp.remove(id1)
        temp.remove(id2)
        if is_connection(temp[0], temp[1]) and ((is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or
                                                (is_connection(id1, temp[1]) and is_connection(id2, temp[0]))):
            # yup, we just made a box
            if is_user:
                score[0] += 1
                boxes[i][4] = OWNER_USER
            else:
                score[1] + 1
                boxes[i][4] = OWNER_COMPUTER
            is_box = True

    return is_box


def user_move():
    try:
        p1, p2 = map(int, input("What move do you want to make?").split(","))
    except ValueError:
        print("Invalid move.")
        user_move()
    else:
        if is_connection(p1, p2):
            print("Sorry, this move is already taken.")
            user_move()
        elif not is_valid(p1, p2):
            print("Invalid move.")
            user_move()
        else:
            is_box = move(True, p1, p2)
            check_complete()

            if is_box:
                print("You scored! Have another turn.")
                SURF.fill((255, 255, 255))
                disp_board()
                pygame.display.update()
                check_complete()
                user_move()


SURF.fill((255, 255, 255))
disp_board()
pygame.display.update()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SURF.fill((255, 255, 255))
    is_user_turn = True
    disp_board()
    pygame.display.update()
    user_move()
    disp_board()
    pygame.display.update()
