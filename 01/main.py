"""
TicTacToe game project. Main file
Copyright 2022 by Artem Ustsov
"""
import argparse
import sys

from tic_tac_toe import TicTacGame

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="stdin")
    parser.add_argument("-o", "--output", default="stdout")
    args = parser.parse_args()
    print(args)

    with open(
        args.input,
        "r",
        encoding="utf-8",
    ) if args.input != "stdin" else sys.stdin as input_file:
        with open(
            args.output,
            "w",
            encoding="utf-8",
        ) if args.output != "stdout" else sys.stdout as output_file:
            game = TicTacGame(input_fd=input_file, output_fd=output_file)
            game.start_pair_game()
