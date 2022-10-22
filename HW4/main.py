# board class
class Board:
    # constructor
    def __init__(self):
        # instance variables
        self.board = []
        # set board to start state
        self.reset_board()

    # class variables
    current_player = 'X'
    number_of_rows = 5
    number_of_columns = 6
    turn_number = 1

    # reset_board
    # sets the game board to its starting state described in the project document
    def reset_board(self):
        self.board = []
        for i in range(self.number_of_rows):
            row = []
            for j in range(self.number_of_columns):
                row.append('-')
            self.board.append(row)
        # reset number of turns to 0
        self.turn_number = 1
        # make the first move as specified in the project document
        # project doc is indexed from 1, while we are indexing at 0 so subtract one
        self.make_move(3-1, 4-1)
        self.make_move(3-1, 3-1)

    # make move
    # has the current player make a move. Mark the requested space and then swap player
    def make_move(self, row, column):
        self.print_board()
        print("*Player " + self.current_player + " is making the move [" + str(row+1) + "," + str(column+1) + "]")
        self.board[row][column] = self.current_player
        self.swap_player_turn()
        self.turn_number += 1

    # swap player turn
    # change current player turn
    # make move will auto swap after marking, so this should not be called outside of make_move
    def swap_player_turn(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

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
        c = 1
        # print turn info
        print("\n===============================\nCurrent Turn Number is: " + str(self.turn_number) +
              "\nCurrent Player is: " + self.current_player + "\n===============================")
        # print first row which are column headers
        print(f"|  ", end='')
        for column in range(self.number_of_columns):
            print(f" | {column + 1}", end='')
        print(" | ")

        for row in self.board:
            # print row header
            print(f"| {c} ", end='')
            for space in row:
                print(f"| {space} ", end='')
            print(f"| ")
            c += 1


# evaluation function
# determines heuristic value of the given state based on the function given in the project documentation
# tates a board state, and reutrns the heuristic value of that state
def evaluate_state(board_state):
    # go through each space till we find a marked space
    for row in board_state.board:
        for space in row:
            if space != '-':
                # check horizontals
                check_horizontal(board_state,row,space)
                # check verticles
                # check diagnolas
    return 0


def check_horizontal(board_state, row, column):
    return


# evaluate all the horizontals of current board states
def check_horizontal_space(board_state, row, column):
    # check if open
    open_status = 0
    # if space before is - then it is open, and we track this
    # if column is zero and nothing is in front of it
    if column > 0 and board_state.board[row][column] == '-':
        open_status += 1
    # if space before is same as current space, then we have already accounted for it being in a row
    # and do not need to run this function again (check to make sure we arent checking out of bounds)
    if column > 0 and board_state.board[row][column-1] is board_state.board[row][column]:
        open_status += 1
    number_in_row = 1
    # count number of same in a row
    while True:
        # if we reach the end of the number of columns
        if  column+number_in_row > board_state.number_of_columns:
            break
        # if the next in row is same as current space then we have row of that value
        elif board_state.board[row][column] is board_state.board[row][column+number_in_row]:
            number_in_row += 1
        # if next space is open indicate that and break while as there is no more row
        elif board_state.board[row][column+number_in_row] == '-':
            open_status += 1
            break
        # only other condition is space is x
        else:
            break
    # need space value and the current player to finish evaluating, 0 means same as player, 1 is diffrent
    same_player_status=0
    if board_state.current_player is not board_state.board[row][column]:
        same_player_status = 1
    # if we have 4 in a row then this is a winning state, and we return 1000 to indicate this
    # (-1000 if winning state for opponent)
    if number_in_row == 4:
        if same_player_status == 0:
            return 1000
        else:
            return -1000
    elif 4 > number_in_row >= 2:
        if same_player_status == 0:
            if number_in_row == 2:
                return
        return
    # if there is less than 2 in a row (single mark) we do not take it into account
    else:
        return 0



# minmax function


# main
def main():
    game_board = Board()




if __name__ == "__main__":
    main()
