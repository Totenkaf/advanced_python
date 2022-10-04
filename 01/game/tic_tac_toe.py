"""
TicTacToe game project.
Copyright 2022 by Artem Ustsov
"""
import sys


class TicTacGame:
    """Main TicTacToe game Object"""

    def __init__(self, input_fd=sys.stdin, output_fd=sys.stdout):
        """Initialize basic game settings"""
        self.board_size = 3
        self.input_fd = input_fd
        self.output_fd = output_fd
        self.board_cells_num = self.board_size * self.board_size
        self.board_field = list(range(1, self.board_cells_num + 1))

    def show_board(self) -> None:
        """Draw the game board as pseudo graph in stdout"""

        print("\n", file=self.output_fd)

        print("\t     |     |", file=self.output_fd)
        print(
            f"\t  {self.board_field[0]}  |  "
            f"{self.board_field[1]}  |  "
            f"{self.board_field[2]}",
            file=self.output_fd,
        )
        print("\t_____|_____|_____", file=self.output_fd)

        print("\t     |     |", file=self.output_fd)
        print(
            f"\t  {self.board_field[3]}  |  "
            f"{self.board_field[4]}  |  "
            f"{self.board_field[5]}",
            file=self.output_fd,
        )
        print("\t_____|_____|_____", file=self.output_fd)

        print("\t     |     |", file=self.output_fd)
        print(
            f"\t  {self.board_field[6]}  |  "
            f"{self.board_field[7]}  |  "
            f"{self.board_field[8]}",
            file=self.output_fd,
        )
        print("\t     |     |", file=self.output_fd)

        print("\n", file=self.output_fd)

    def validate_input(self, current_player) -> tuple:
        """
        Gives a current_player (X or O), check the input, return a tuple
        with validation status and chosen position by current_player
        """
        while True:
            try:
                print(
                    f"Player {current_player} turn. Choose your pos: ",
                    file=self.output_fd,
                )
                player_chosen_pos = self.input_fd.readline()
                print(
                    f"{current_player} choose {player_chosen_pos}",
                    file=self.output_fd,
                )
                if player_chosen_pos == "":
                    return False, -1
                player_chosen_pos = int(player_chosen_pos)
            except ValueError:
                print(
                    "Wrong input. Enter the number position from 1 to 9\n",
                    file=self.output_fd,
                )
                continue

            if player_chosen_pos < 1 or player_chosen_pos > 9:
                print(
                    "Wrong input. Enter the number position from 1 to 9\n",
                    file=self.output_fd,
                )
                continue

            if str(self.board_field[player_chosen_pos - 1]) not in "XO":
                break
            print("The cell is occupied. Try again!\n", file=self.output_fd)
            continue

        return True, player_chosen_pos

    def make_player_step(self, step_counter) -> str:
        """
        Takes a step_counter, return current_player
        """
        if step_counter % 2 == 0:
            current_player = "X"
            is_valid, player_chosen_pos = self.validate_input(current_player)
            if is_valid:
                self.board_field[player_chosen_pos - 1] = current_player
            else:
                return "STOP"
        else:
            current_player = "O"
            is_valid, player_chosen_pos = self.validate_input(current_player)
            if is_valid:
                self.board_field[player_chosen_pos - 1] = current_player
            else:
                return "STOP"
        return current_player

    def start_pair_game(self) -> None:
        """
        Initialize the game. Return None
        """
        step_counter = 0
        game_over = False
        while not game_over:
            self.show_board()
            current_player = self.make_player_step(step_counter)
            if current_player != "STOP":
                step_counter += 1
                if self.check_winner(current_player):
                    game_over = True
                elif self.check_tie(step_counter):
                    game_over = True
            else:
                break
        self.show_board()
        print("Game Over", file=self.output_fd)

    def check_winner(self, current_player) -> bool:
        """
        Takes a current_player and checks the current board_field status
        with win combinations, return True, otherwise False
        """
        win_cords = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        )
        for win_cord in win_cords:
            if (
                self.board_field[win_cord[0]]
                == self.board_field[win_cord[1]]
                == self.board_field[win_cord[2]]
            ):
                print(current_player, "Wins!", file=self.output_fd)
                return True
        return False

    def check_tie(self, step_counter):
        """
        Takes a step_counter, returns True if step_counter = 9, otherwise False
        """
        if step_counter == self.board_cells_num:
            print("Tie!", file=self.output_fd)
            return True
        return False
