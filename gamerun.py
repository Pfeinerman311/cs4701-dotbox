# A module to run the lines and dots game
import dotbox
import users
import interface
import pygame
import ai
import sys


def player_move(players, game_state, gui):
    print("Current player is:")
    print(players.get_current_player().get_id())
    if (players.get_current_player().get_id() == 1):
        print("in ai move")
        move = ai.getMove(game_state, players)[3]
        try:
            print("move is:")
            print(move)
            attempt = game_state.draw_line(move)
            att = attempt[0]
            box = attempt[2].keys()
        except AssertionError:
            print("Invalid move - Assertion Error")
        else:
            gui.move(True, move[0], move[1])
            if att:
                print("The AI scored!")
                gui.fill_box(box)
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
                    gui.fill_box(box)
        players.switch_player()


def play_game(n):
    players = users.Players(n)
    game_state = dotbox.Grid((2, 2), players.get_players())
    gui = interface.Ui(2, 2)
    gui.start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gui.SURF.fill((255, 255, 255))
        gui.is_user_turn = True
        gui.disp_board()
        gui.update_pygame()
        player_move(players, game_state, gui)
        gui.disp_board()
        gui.update_pygame()


# Start of game:
def main():
    print("Welcome to Dots and Boxes.")
    print("How many players are playing?")
    n = input()
    play_game(n)


if __name__ == "__main__":
    main()
