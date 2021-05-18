# A module to run the lines and dots game
import dotbox
import users
import interface
import pygame
import minimax


def player_move(players, game_state, gui, player):
    #0 is player and 1 is AI

    player = (player + 1) % 1
    print("player is")
    print(str(player))
    player_ob = players[player]
    # player = 0
    if (player == 1):
        values = minimax(player_ob, game_state, players)
        print("values are:")
        print(values)

    else:
        try:
            p1, p2 = map(int, input(
                "What move do you want to make?").split(","))
        except ValueError:
            print("Invalid move - not provided two numbers with a comma inbetween")
        else:
            line = dotbox.Line((p1, p2), players.get_players()[player])
            try:
                attempt = game_state.draw_line(line)
                att = attempt[0]
                box = attempt[2].keys()
            except AssertionError:
                print("Invalid move - Assertion Error")
            else:
                gui.move(True, p1, p2)

                if att:
                    print("You scored!.")
                    # print("box in gamerun is "+str(type(box)))
                    gui.fill_box(box)


def play_game(n):
    players = users.Players(n)
    # init 9 - might change
    game_state = dotbox.Grid((4, 4), players.get_players())
    gui = interface.Ui(4, 4)
    gui.start()
    player = 1
    tmp = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gui.SURF.fill((255, 255, 255))
        gui.is_user_turn = True
        gui.disp_board()
        gui.update_pygame()
        player_move(players, game_state, gui, player)
        # wait(6)

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
