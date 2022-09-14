class TicTacGame:
    def __init__(self, board_size=3, board_border_size=13):
        self.board_size = board_size
        self.board_border_size = board_border_size
        self.board_field = list(range(1, self.board_size * self.board_size + 1))

    def show_board(self) -> None:
        print("-" * self.board_border_size)
        for row in range(self.board_size):
            print(
                    "|", self.board_field[0 + row * self.board_size],
                    "|", self.board_field[1 + row * self.board_size],
                    "|", self.board_field[2 + row * self.board_size], 
                    "|"
                )
            print("-" * self.board_border_size)

    def validate_input(self, player_token) -> None:
        valid = False
        while not valid:
            player_answer = input("Turn Token " + player_token + "?" + " ")
            try:
                player_answer = int(player_answer)
            except ValueError:
                print("Wrong input. Enter the number position from 1 to 9")
                continue

            if 1 <= player_answer <= 9:
                if str(self.board_field[player_answer - 1]) not in "XO":
                    self.board_field[player_answer - 1] = player_token
                    valid = True
                else:
                    print("The cell is occupied. Try again!")
            else:  # fool check should be deleted
                print("Wrong input. Enter the number position from 1 to 9")

    def start_single_game(self) -> None:
        counter = 0
        win = False
        while not win:
            self.show_board()
            if counter % 2 == 0:
                self.validate_input("X")  # add possibility to choose who turns first
            else:
                self.validate_input("O")
            counter += 1
            if counter > 4:  # magic number needs to be removed
                tmp = self.check_winner()
                if tmp:
                    print(tmp, "Wins!")
                    win = True  # unusable variable. why?
                    break
            if counter == 9:
                print("Tie!")
                break
        self.show_board()

    def check_winner(self) -> bool:
        win_cords = (
                      (0, 1, 2), (3, 4, 5),
                      (6, 7, 8), (0, 3, 6),
                      (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)
                     )
        for win_cord in win_cords:
            if self.board_field[win_cord[0]] == self.board_field[win_cord[1]] == self.board_field[win_cord[2]]:
                return self.board_field[win_cord[0]]
        return False
