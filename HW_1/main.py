"""
TicTacToe game project. Main file
Copyright 2022 by Artem Ustsov
"""
import sys

from game.tic_tac_toe import TicTacGame

if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding="utf-8") \
            if len(sys.argv) > 1 else sys.stdin as f:
        game = TicTacGame(input_fd=f)
        game.start_pair_game()
