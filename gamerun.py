# A module to run the lines and dots game
import dotbox
import users
import interface
import pygame
import ai
import sys
import greedy
import time


def player_move(players, game_state, gui, ai_game):

    if (players.get_current_player().get_id() == 1):
        move = ai.getMove(game_state, players)[3]
        try:
            players.set_ai_player()

            line = dotbox.Line(move, players.get_current_player())
            attempt = game_state.draw_line(line)
            att = attempt[0]
            box = attempt[2].keys()
            print("The AI drew a line from " +
                  str(move[0])+" to "+str(move[1]))
        except AssertionError:
            print("Invalid move - Assertion Error")
        else:
            gui.move(False, move[0], move[1])
            if att:
                print(players.get_current_player().get_id())
                gui.fill_box(box, players.get_current_player().get_id())
            else:
                players.set_user_player()

    elif (ai_game):
        move = greedy.getGreedyMove(game_state, players)
        try:
            line = dotbox.Line(move, players.get_current_player())
            attempt = game_state.draw_line(line)
            att = attempt[0]
            box = attempt[2].keys()
            print("The Greedy AI drew a line from " +
                  str(move[0])+" to "+str(move[1]))
        except AssertionError:
            print("Invalid move - Assertion Error")
        else:
            gui.move(True, move[0], move[1])
            if att:
                gui.fill_box(box, players.get_current_player().get_id())
            else:
                players.switch_player()

    else:

        try:
            p1, p2 = map(int, input(
                "What move do you want to make?").split(","))
        except ValueError:
            print("Invalid move - not provided two numbers with a comma inbetween")
        else:

            line = dotbox.Line((p1, p2), players.get_current_player())
            try:
                attempt = game_state.draw_line(line)
                att = attempt[0]
                box = attempt[2].keys()
            except AssertionError:
                print("Invalid move - Assertion Error")
            else:
                gui.move(True, p1, p2)
                if att:
                    print("You scored!")
                    gui.fill_box(box, players.get_current_player().get_id())
                else:
                    players.switch_player()


def play_game(n, size, ai_game):
    players = users.Players(n)
    game_state = dotbox.Grid((size, size), players.get_players())
    gui = interface.Ui(size, size)
    gui.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gui.w.fill((255, 255, 255))
        gui.is_user_turn = True
        gui.disp_board()
        gui.update_pygame()
        player_move(players, game_state, gui, ai_game)
        if game_state.game_over():
            print("The game is over.")
            print("Player "+str(game_state.get_winner()
                                [0].get_id())+" won the game.")
            break
        gui.disp_board()
        gui.update_pygame()

    gui.disp_board()
    time.sleep(10)
    gui.update_pygame()


# Start of game:
def main():
    print("Welcome to Dots and Boxes.")
    print("How many players are playing?")
    n = input()
    print("What size game would you like to play?")
    print("Type 2 for a 2x2, 3 for a 3x3 or 4 for a 4x4 grid!")
    size = input()
    print("Would you like to test the AI? Type Yes or No!")
    ai_game = input()
    if ai_game == "Yes":
        play_game(n, int(size), True)
    else:
        play_game(n, int(size), False)


if __name__ == "__main__":
    main()
