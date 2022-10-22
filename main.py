# board class
class Board:
    # constructor
    def __init__(self):
        # instance variables
        self.board = []
        # set board to start state
        self.reset_board()

    # class variables
    current_player = 'x'
    number_of_rows = 5
    number_of_columns = 6

    # reset_board
    # sets the game board to its starting state described in the project document
    def reset_board(self):
        for i in range(self.number_of_rows):
            row = []
            for j in range(self.number_of_columns):
                row.append('-')
            self.board.append(row)
        # make the first move as specified in the project document
        self.make_move(3, 4)
        self.make_move(3, 3)

    # make move
    # has the current player make a move. Mark the requested space and then swap player
    def make_move(self, row, column):
        self.board[row][column] = self.current_player
        self.swap_player_turn()

    # swap player turn
    # change current player turn
    # make move will auto swap after marking, so this should not be called outside of make_move
    def swap_player_turn(self):
        if self.current_player == 'x':
            return self.current_player == 'o'
        else:
            return self.current_player == 'x'

    # is_board_filled
    # check if there is a legal move that can be made
    def is_board_filled(self):
        # for every row in the board
        for row in self.board:
            # check each space in the row
            for space in row:
                # if there is an unmarked space, then there is still a move to be made
                if space == '-':
                    return False
        # if there are no '-' spaces, then the board is filled and game is over
        return True

    # print_board
    # prints out the board, so we can see current game state
    def print_board(self):
        # used to count row number
        c = 0
        # print first row which are column headers
        print(f"| ", end='')
        for column in range(self.number_of_columns):
            print(f"| {column + 1}", end='')
        print("| ")

        for row in self.board:
            # print row header
            print(f"| {c + 1} ", end='')
            for space in row:
                print(f"|{space}", end='')
            print(f"| ")

# make move

# evaluation function

# minmax function
