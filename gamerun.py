# A module to run the lines and dots game
import dotbox
import users
import interface
import pygame


def player_move(players, game_state, gui, player):
    # player = (player + 1) % 1
    player = 0

    try:
        p1, p2 = map(int, input(
            "What move do you want to make?").split(","))
    except ValueError:
        print("Invalid move - not provided two numbers with a comma inbetween")
    else:
        print(len(players.get_players()))
        line = dotbox.Line((p1, p2), players.get_players()[player])
        try:
            attempt = game_state.draw_line(line)[0]
        except AssertionError:
            print("Invalid move - Assertion Error")
        else:
            gui.move(True, p1, p2)

            if attempt:
                print("You scored!.")


def play_game(n):
    players = users.Players(n)
    game_state = dotbox.Grid((4, 4), players)  # init 9 - might change
    gui = interface.Ui(4, 4)
    gui.start()
    player = 1
    while True:
        gui.SURF.fill((255, 255, 255))
        gui.is_user_turn = True
        gui.disp_board()
        gui.update_pygame()
        player_move(players, game_state, gui, player)
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
