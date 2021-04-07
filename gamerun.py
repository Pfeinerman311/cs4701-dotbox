# A module to run the lines and dots game
import dotbox
import players


def play_game(n):
    players = players.Players(n)
    game_state = dotbox.Grid(9)  # init 9 - might change
    while game_state.full():
        for p in n:
            print("Player "+string(p.get_id()) + "choose your line:")
            line = input()
            game_state.turn(p.get_id(), line)

    print("Congrats! The game is over")


# Start of game:
def main():
    print("Welcome to Dots and Boxes.")
    print("How many players are playing?")
    n = input()
    play_game(n)


if __name__ == "__main__":
    main()
