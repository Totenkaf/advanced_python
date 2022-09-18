'''
TicTacToe game project. Unit tests
Copyright 2022 by Artem Ustsov
'''
import os
import sys
import unittest
from unittest.mock import patch

from game.tic_tac_toe import TicTacGame


class TestTicTacGame(unittest.TestCase):
    '''
    Main testclass of TicTacGame Object
    '''
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=consider-using-with
    def setUp(self) -> None:
        self.steps_with_mistakes = [5, 'x', -10, 12, '*']
        self.x_wins_steps = [5, 1, 2, 3, 8]
        self.o_wins_steps = [1, 9, 2, 3, 4, 6]
        self.tie_steps = [5, 1, 8, 2, 3, 7, 4, 6, 9]

        with open("x_wins.txt", "w", encoding="utf-8") as self.file_1:
            for step in self.x_wins_steps:
                self.file_1.write(str(step))
                self.file_1.write('\n')

        with open("o_wins.txt", "w", encoding="utf-8") as self.file_2:
            for step in self.o_wins_steps:
                self.file_2.write(str(step))
                self.file_2.write('\n')

        with open("tie.txt", "w", encoding="utf-8") as self.file_3:
            for step in self.tie_steps:
                self.file_3.write(str(step))
                self.file_3.write('\n')

        with open("input_with_mistakes.txt", "w", encoding="utf-8") \
                as self.file_4:
            for step in self.steps_with_mistakes:
                self.file_4.write(str(step))
                self.file_4.write('\n')

        self.file_1 = open(self.file_1.name, 'r', encoding="utf-8")
        self.game_1 = TicTacGame(input_fd=self.file_1)

        self.file_2 = open(self.file_2.name, 'r', encoding="utf-8")
        self.game_2 = TicTacGame(input_fd=self.file_2)

        self.file_3 = open(self.file_3.name, 'r', encoding="utf-8")
        self.game_3 = TicTacGame(input_fd=self.file_3)

        self.file_4 = open(self.file_4.name, 'r', encoding="utf-8")
        self.game_4 = TicTacGame(input_fd=self.file_4)

        self.game = TicTacGame()

    def tearDown(self) -> None:
        self.file_1.close()
        self.file_2.close()
        self.file_3.close()
        self.file_4.close()
        try:
            os.remove(self.file_1.name)
            os.remove(self.file_2.name)
            os.remove(self.file_3.name)
            os.remove(self.file_4.name)
        except OSError as why:
            print(why)

    def test_object_init_stdin(self):
        '''Test default initialisations with standart input object'''
        self.assertEqual(self.game.input_fd, sys.stdin)
        self.assertEqual(self.game.board_size, 3)
        self.assertEqual(self.game.board_cells_num, 9)
        self.assertEqual(self.game.board_field, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_object_init_file(self):
        '''Test default initialisations with file input object'''
        self.assertEqual(self.game_1.input_fd, self.file_1)
        self.assertEqual(self.game_2.input_fd, self.file_2)
        self.assertEqual(self.game_3.input_fd, self.file_3)

    @patch.object(TicTacGame, "show_board")
    def test_show_board(self, show_board_mock):
        '''Test the show_board method via mocking'''
        show_board_mock.return_value = None
        self.assertEqual(self.game.show_board(), None)
        self.assertTrue(show_board_mock.called)

    def test_make_player_step(self):
        '''Test equivalence of returning current_player name'''
        step_counter = 0
        self.assertEqual(self.game_1.make_player_step(step_counter), "X")
        step_counter = 1
        self.assertEqual(self.game_1.make_player_step(step_counter), "O")

    def test_validate_correct_input(self):
        '''Test correct input through file input'''
        self.assertEqual(self.game_1.validate_input("X"), (True, 5))
        self.assertEqual(self.game_1.validate_input("O"), (True, 1))
        self.assertEqual(self.game_1.validate_input("X"), (True, 2))
        self.assertEqual(self.game_1.validate_input("O"), (True, 3))
        self.assertEqual(self.game_1.validate_input("X"), (True, 8))

    def test_validate_wrong_input(self):
        '''Test incorrect input through file input'''
        self.assertEqual(self.game_4.validate_input("X"), (True, 5))
        self.assertEqual(self.game_4.validate_input("O"), (False, -1))

    def test_check_x_winner(self):
        '''Сhecking the ability to return the correct X winner'''
        for i, step in enumerate(self.x_wins_steps):
            if i % 2 == 0:
                self.game_1.board_field[step - 1] = 'X'
            else:
                self.game_1.board_field[step - 1] = 'O'
        self.assertTrue(self.game_1.check_winner('X'))

    def test_check_o_winner(self):
        '''Сhecking the ability to return the correct O winner'''
        for i, step in enumerate(self.o_wins_steps):
            if i % 2 == 0:
                self.game_2.board_field[step - 1] = 'X'
            else:
                self.game_2.board_field[step - 1] = 'O'
        self.assertTrue(self.game_2.check_winner('O'))

    def test_check_tie(self):
        '''Сhecking the ability to return the correct tie situation'''
        self.assertTrue(self.game_1.check_tie(9))
        self.assertFalse(self.game_1.check_tie(6))

    @patch.object(TicTacGame, "start_pair_game")
    def test_start_pair_game(self, start_pair_game_mock):
        '''Test the start_pair_game method via mocking'''
        start_pair_game_mock.return_value = None
        self.assertEqual(self.game_1.start_pair_game(), None)
        self.assertTrue(start_pair_game_mock.called)

    @patch.object(TicTacGame, "check_tie")
    def test_tie_game(self, check_tie_mock):
        '''Test the check_tie method via mocking'''
        check_tie_mock.return_value = False
        self.game_3.start_pair_game()
        self.assertEqual(check_tie_mock.call_count, 9)
        self.assertEqual(self.game_3.board_field, ['O', 'O', 'X',
                                                   'X', 'X', 'O',
                                                   'O', 'X', 'X'])
