# A module to run the lines and dots game
import dotbox
import users
import interface
import pygame


def play_game(n):
    players = users.Players(n)
    # game_state = dotbox.Grid([4, 4], players)  # init 9 - might change
    gui = interface.Ui(4, 4)
    gui.start()
    while True:
        try:
            p1, p2 = map(int, input(
                "What move do you want to make?").split(","))
        except ValueError:
            print("Invalid move")
        else:
            if gui.is_connection(p1, p2):
                print("Sorry, this move is already taken.")

            elif not gui.is_valid(p1, p2):
                print("Invalid move.")

            else:
                is_box = gui.move(True, p1, p2)
                gui.check_complete()

                if is_box:
                    print("You scored! Have another turn.")
                    gui.SURF.fill((255, 255, 255))
                    gui.disp_board()
                    pygame.display.update()
                    gui.check_complete()


# Start of game:
def main():
    print("Welcome to Dots and Boxes.")
    print("How many players are playing?")
    n = input()

    play_game(n)


if __name__ == "__main__":
    main()
