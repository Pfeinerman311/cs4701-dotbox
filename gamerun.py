# A module to run the lines and dots game
import dotbox
import users
import interface
import pygame


def play_game(n):
    players = users.Players(n)
    game_state = dotbox.Grid((4, 4), players)  # init 9 - might change
    gui = interface.Ui(4, 4)
    gui.start()
    player = 1
    while True:
        player = player+1 % 1
        try:
            p1, p2 = map(int, input(
                "What move do you want to make?").split(","))
        except ValueError:
            print("Invalid move")
        else:
            line = game_state.Line(p1, p2), players[player])
            try:
                attempt=game_state.draw_line(line)
            except AssertionError
                print("Invalid move")
            else
                gui.move(True, p1, p2)


                if is_box:
                    print("You scored! Have another turn.")
                    gui.rerun()


# Start of game:
def main():
    print("Welcome to Dots and Boxes.")
    print("How many players are playing?")
    n=input()

    play_game(n)


if __name__ == "__main__":
    main()
