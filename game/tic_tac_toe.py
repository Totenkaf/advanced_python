# Copyright 2022 by Artem Ustsov
import sys


class TicTacGame:
    def __init__(self, input_fd=sys.stdin):
        '''Initialize basic game settings'''
        self.board_size = 3
        self.input_fd = input_fd
        self.board_cells_num = self.board_size * self.board_size
        self.board_field = list(range(1, self.board_cells_num + 1))

    def show_board(self) -> None:
        '''Draw the game board as pseudo graph in stdout'''
        print("\n")
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board_field[0], self.board_field[1], self.board_field[2]))
        print('\t_____|_____|_____')

        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board_field[3], self.board_field[4], self.board_field[5]))
        print('\t_____|_____|_____')

        print("\t     |     |")

        print("\t  {}  |  {}  |  {}".format(self.board_field[6], self.board_field[7], self.board_field[8]))
        print("\t     |     |")
        print("\n")

    def validate_input(self, current_player) -> tuple:
        '''
        Gives a current_player (X or O), check the input, return a tuple
        with validation status and chosen position by current_player
        '''
        while True:
            try:
                print(f"Player {current_player} turn. Choose your pos: ")
                player_chosen_pos = self.input_fd.readline()
                print(f"{current_player} choose {player_chosen_pos}")
                if player_chosen_pos == '':
                    return False, -1
                else:
                    player_chosen_pos = int(player_chosen_pos)
            except ValueError:
                print("Wrong input. Enter the number position from 1 to 9\n")
                continue

            if player_chosen_pos < 1 or player_chosen_pos > 9:
                print("Wrong input. Enter the number position from 1 to 9\n")
                continue

            if str(self.board_field[player_chosen_pos - 1]) not in "XO":
                break
            else:
                print("The cell is occupied. Try again!\n")
                continue

        return True, player_chosen_pos

    def make_player_step(self, step_counter) -> str:
        '''
        Takes a step_counter, return current_player
        '''
        if step_counter % 2 == 0:
            current_player = "X"
            is_validated, player_chosen_pos = self.validate_input(current_player)
            if is_validated:
                self.board_field[player_chosen_pos - 1] = current_player
            else:
                return "STOP"
        else:
            current_player = "O"
            is_validated, player_chosen_pos = self.validate_input(current_player)
            if is_validated:
                self.board_field[player_chosen_pos - 1] = current_player
            else:
                return "STOP"
        return current_player

    def start_pair_game(self) -> None:
        '''
        Initialize the game. Return None
        '''
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
        print("Game Over")

    def check_winner(self, current_player) -> bool:
        '''
        Takes a current_player and checks the current board_field status
        with win combinations, return True, otherwise False
        '''
        win_cords = (
                      (0, 1, 2), (3, 4, 5),
                      (6, 7, 8), (0, 3, 6),
                      (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)
                     )
        for win_cord in win_cords:
            if self.board_field[win_cord[0]] == self.board_field[win_cord[1]] == self.board_field[win_cord[2]]:
                print(current_player, "Wins!")
                return True
        return False

    def check_tie(self, step_counter):
        '''
        Takes a step_counter, returns True if step_counter = 9, otherwise False
        '''
        if step_counter == self.board_cells_num:
            print("Tie!")
            return True
        return False
