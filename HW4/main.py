#imports
import copy
from time import process_time

#global variables
nodes_created = 0
total_nodes_created = 0


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
    node_number = 0

    # reset_board
    # sets the game board zero
    def reset_board(self):
        self.board = []
        for i in range(self.number_of_rows):
            row = []
            for j in range(self.number_of_columns):
                row.append('-')
            self.board.append(row)

    # make move
    # has the current player make a move. Mark the requested space and then swap player
    def make_move(self, row, column):
        # self.print_board()
        # print("*Player " + str(self.current_player) + "is making the move [" + str(row+1) + "," + str(column+1) + "]")
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

    # get_value_at
    # returns value of requested position on board
    def get_value_at(self, row, column):
        return self.board[row][column]

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
                pass
                print(f"| {space} ", end='')
            print(f"| ")
            c += 1

    def available_moves(self):
        list_moves = []
        rows = -1
        cols = -1
        for row_list in self.board:
          rows += 1
          cols = -1
          for space in row_list:
            cols += 1
            if space == 'X' or space == 'O':
                if cols-1 >= 0:
                    if self.board[rows][cols-1] == '-':
                        move_string = str(rows)+","+str(cols-1)
                        if move_string not in list_moves:
                            list_moves.append(move_string)

                if rows+1 <= self.number_of_rows-1:
                    if cols-1 >= 0:
                        if self.board[rows+1][cols-1] == '-':
                            move_string = str(rows+1)+","+str(cols-1)
                            if move_string not in list_moves:
                                list_moves.append(move_string)
                
                if rows+1 <= self.number_of_rows-1:
                  if self.board[rows+1][cols] == '-':
                    move_string = str(rows+1)+","+str(cols)
                    if move_string not in list_moves:
                      list_moves.append(move_string)
                
                if rows+1 <= self.number_of_rows-1:
                  if cols+1 <= self.number_of_columns-1:
                    if self.board[rows+1][cols+1] == '-':
                      move_string = str(rows+1)+","+str(cols+1)
                      if move_string not in list_moves:
                        list_moves.append(move_string)

                if cols+1 <= self.number_of_columns-1:
                  if self.board[rows][cols+1] == '-':
                    move_string = str(rows)+","+str(cols+1)
                    if move_string not in list_moves:
                      list_moves.append(move_string)

                if rows-1 >= 0:
                  if cols+1 <= self.number_of_columns-1:
                    if self.board[rows-1][cols+1] == '-':
                      move_string = str(rows-1)+","+str(cols+1)
                      if move_string not in list_moves:
                        list_moves.append(move_string)

                if rows-1 >= 0:
                  if self.board[rows-1][cols] == '-':
                    move_string = str(rows-1)+","+str(cols)
                    if move_string not in list_moves:
                      list_moves.append(move_string)
                      
                if rows-1 >= 0:
                  if cols-1 >= 0:
                    if self.board[rows-1][cols-1] == '-':
                      move_string = str(rows-1)+","+str(cols-1)
                      if move_string not in list_moves:
                        list_moves.append(move_string)
                
        return list_moves

    def initMinMax(self, max_depth, depth, active_turn):
        best_move = "-1,-1"
        score = -100000
        depth += 1
        current_player = self.current_player
        # populate score
        for m in self.available_moves():
            # print(" --------- " + m.split(",")[1])
            # create possible game state``
            possible_board = copy.deepcopy(self)
            # make m move on possible game state
            possible_board.make_move(int(m.split(",")[0]), int(m.split(",")[1]))
            passed_turn = possible_board.current_player
            if possible_board.current_player == 'X':
                possible_board.current_player = 'O'
            else:
                possible_board.current_player = 'X'
            if max_depth >= depth:
                candidate_score = possible_board.minmax(max_depth, depth, passed_turn)
            # print(score)
            if score < candidate_score:
                score = candidate_score
                # print(score)
                best_move = m
        # print(score)
        # print("best move: ", best_move)
        # print()
        return best_move
              

    def minmax(self, max_depth, depth, active_turn):
        global nodes_created
        nodes_created += 1
        moves = []
        scores = []
        depth += 1
        current_player = self.current_player
        # print("Current heuristic value of the possible board: " + str(evaluate_state(self, active_turn)))
        heuristic_value = evaluate_state(self, active_turn)
        # player
        passed_turn = self.current_player
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
        # populate score
        if heuristic_value > 900:
            return heuristic_value
        if max_depth >= depth and heuristic_value < 1000:
            for m in self.available_moves():
                # print(" --------- " + m.split(",")[1])
                # create possible game state``
                possible_board = copy.deepcopy(self)
                # make m move on possible game state
                possible_board.make_move(int(m.split(",")[0]), int(m.split(",")[1]))
                # print("we are adding to heuristic values here\n adding : "
                # + str(evaluate_state(possible_board, active_turn))
                # + "\n recursive depth iss: " + str(depth) + "Nodes generated: " + str(possible_board.node_number))
                scores.append(possible_board.minmax(max_depth, depth, passed_turn))
            # get score of possible game state and push it to move
        else:
            return heuristic_value
        # moves.append(m)

        # print("list of heurisic values calculated TTTT: ", scores,  "\n recursive depth iss: " + str(depth))
        # push move to move
        if active_turn == passed_turn:
            # max score
            # heuristic value has all values of possible board states of all possible moves`
            return max(scores)
        else:
            return min(scores)
              # min scores

            # if possible_board.current_player == current_player:

        # print("moves: ", moves)
        # print("available moves: ", self.available_moves())
        # print("scores: ", scores)

        # do min max calculation


# evaluation function
# determines heuristic value of the given state based on the function given in the project documentation
# takes a board state, and returns the heuristic value of that state
def evaluate_state(board_state, current_player):
    # variable to hold heuristic value
    state_value = 0
    # check functions will evaluate based on [x,y] position of current space, track these values to pass to functions
    row_number = 0
    column_number = 0
    # go through each space till we find a marked space
    for row in board_state.board:
        for space in row:
            if space != '-':
                # print("================================\n running checks on ["
                # + str(row_number+1) + "," + str(column_number+1) + "]")
                # check horizontals
                # print("------------------------\nStart of horizontal")
                state_value += check_horizontal(board_state, row_number, column_number, current_player)
                # print("After running horizontal check: " + str(state_value))
                # check verticals
                # print("------------------------\nStart of vertical")
                state_value += check_verticals(board_state, row_number, column_number, current_player)
                # print("After running verticals check: " + str(state_value))
                # check diagonals
                # need to check both left and right diagonals
                # check right
                # print("------------------------\nStart of right diag")
                state_value += check_diagonals_right(board_state, row_number, column_number, current_player)
                # print("After running right diagonals check: " + str(state_value))
                # check left
                # print("------------------------\nStart of left diag")
                state_value += check_diagonals_left(board_state, row_number, column_number, current_player)
                # print("After running left diagonals check: " + str(state_value))
            # column number update
            column_number += 1
        # increment row number
        row_number += 1
        # set column number back to 0
        column_number = 0
    return state_value


# determine heuristic value of current row u
# used by check_horizontals check_verticals check_diagonals in order to avoid repeating it each time
def check_return_heuristic( number_in_row, open_status, same_player_status):
    # print("Values we are getting in check return are:\nnumber_in_rows: " + str(number_in_row) + "\nopen_status: "
    # + str(open_status) + "\n same_player_status: "+str(same_player_status))
    # if we have 4 in a row then this is a winning state, and we return 1000 to indicate this
    # (-1000 if winning state for opponent)
    if number_in_row == 4:
        if same_player_status == 0:
            return 1000
        else:
            return -1000
    elif 4 > number_in_row >= 2:
        if same_player_status == 0:
            if number_in_row == 3 and open_status == 2:
                return 200
            elif number_in_row == 3 and open_status == 1:
                return 150
            elif number_in_row == 2 and open_status == 2:
                return 20
            elif number_in_row == 2 and open_status == 1:
                return 5
            else:
                return 0
        else:
            if number_in_row == 3 and open_status == 2:
                return -80
            elif number_in_row == 3 and open_status == 1:
                return -40
            elif number_in_row == 2 and open_status == 2:
                return -15
            elif number_in_row == 2 and open_status == 1:
                return -2
            else:
                return 0
    # if there is less than 2 in a row (single mark) we do not take it into account
    else:
        return 0


# evaluate all the horizontals of current board states
def check_horizontal(board_state, row, column, current_player):
    # check if open
    open_status = 0
    # if space before is - then it is open, and we track this
    # if column is zero and nothing is in front of it
    if column > 0 and board_state.get_value_at(row, column-1) == '-':
        open_status += 1
    # if space before is same as current space, then we have already accounted for it being in a row
    # and do not need to run this function again (check to make sure we arent checking out of bounds)
    if column > 0 and board_state.board[row][column-1] == board_state.board[row][column]:
        return 0
    number_in_row = 1
    # count number of same in a row
    while True:
        # if we reach the end of possible members of this row (out for board bounds)
        if column+number_in_row > board_state.number_of_columns-1:
            break
        # if the next in row is same as current space then we have row of that value
        elif board_state.board[row][column] == board_state.board[row][column+number_in_row]:
            number_in_row += 1
        # if next space is open indicate that and break while as there is no more row
        elif board_state.board[row][column+number_in_row] == '-':
            open_status += 1
            break
        # only other condition is that the next space is other value so row is broken
        else:
            break
    # need space value and the current player to finish evaluating, 0 means same as player, 1 is different
    same_player_status=0
    if current_player != board_state.board[row][column]:
        same_player_status = 1
    # evaluate the row value and return it
    return check_return_heuristic(number_in_row, open_status, same_player_status)


# check vertical axis of space for rows, similar to check_horizontals
def check_verticals(board_state, row, column, current_player):
    # check if open
    open_status = 0
    # if space before is - then it is open, and we track this
    # if row is zero and nothing is in front of it
    if row > 0 and board_state.board[row-1][column] == '-':
        open_status += 1
    # print("open status at start is: " + str(open_status))
    # if space before is same as current space, then we have already accounted for it being in a row
    # and do not need to run this function again (check to make sure we arent checking out of bounds)
    if row > 0 and board_state.board[row-1][column] == board_state.board[row][column]:
        return 0
    number_in_row = 1
    # count number of same in a row
    while True:
        # if we reach the end of possible members of this row (out for board bounds)
        if row+number_in_row > board_state.number_of_rows-1:
            # print("we are entering out of bounds break")
            break
        # if the next in row is same as current space then we have row of that value
        elif board_state.board[row][column] == board_state.board[row+number_in_row][column]:
            # print("we are entering row is good break")
            number_in_row += 1
        # if next space is open indicate that and break while as there is no more row
        elif board_state.board[row+number_in_row][column] == '-':
            # print("we are entering end space is break")
            open_status += 1
            break
        # only other condition is that the next space is other value so row is broken
        else:
            # print("we are entering row broken break")
            break
    # need space value and the current player to finish evaluating, 0 means same as player, 1 is different
    same_player_status=0
    if current_player != board_state.board[row][column]:
        same_player_status = 1
    # evaluate the row value and return it
    return check_return_heuristic(number_in_row, open_status, same_player_status)


def check_diagonals_right(board_state, row, column, current_player):
    # check if open
    open_status = 0
    # if space before is - then it is open, and we track this
    # if row is zero and nothing is in front of it
    if row > 0 and column > 0:
        if board_state.board[row-1][column-1] == '-':
            open_status += 1
    # print("open status at start is: " + str(open_status))
    # if space before is same as current space, then we have already accounted for it being in a row
    # and do not need to run this function again (check to make sure we are not checking out of bounds)
    # print(board_state.board[row - 1][column - 1])
    # print(board_state.board[row][column])
    # print(board_state.board[row - 1][column - 1] == board_state.board[row][column])
    if row > 0 and column > 0:
        if board_state.board[row - 1][column - 1] == board_state.board[row][column]:
            # print("we are entering been there done that")
            return 0
    number_in_row = 1
    # count number of same in a row
    while True:
        # if we reach the end of possible members of this row (out for board bounds)
        if row + number_in_row > board_state.number_of_rows-1 or column + number_in_row > board_state.number_of_columns-1:
            # print("we are entering out of bounds break")
            break
        # if the next in row is same as current space then we have row of that value
        elif board_state.board[row][column] == board_state.board[row + number_in_row][column + number_in_row]:
            # print("we are entering row is good break")
            number_in_row += 1
        # if next space is open indicate that and break while as there is no more row
        elif board_state.board[row + number_in_row][column + number_in_row] == '-':
            # print("we are entering end space is break")
            open_status += 1
            break
        # only other condition is that the next space is other value so row is broken
        else:
            # print("we are entering row broken break")
            break
    # need space value and the current player to finish evaluating, 0 means same as player, 1 is different
    same_player_status = 0
    if current_player != board_state.board[row][column]:
        same_player_status = 1
    # evaluate the row value and return it
    return check_return_heuristic(number_in_row, open_status, same_player_status)


def check_diagonals_left(board_state, row, column, current_player):
    # check if open
    open_status = 0
    # if space before is - then it is open, and we track this
    # if row is zero and nothing is in front of it
    if row > 0 and column < board_state.number_of_columns-1:
        if board_state.board[row-1][column+1] == '-':
            open_status += 1
    # print("open status at start is: " + str(open_status))
    # if space before is same as current space, then we have already accounted for it being in a row
    # and do not need to run this function again (check to make sure we are not checking out of bounds)
    if row > 0 and column < board_state.number_of_columns-1:
        if board_state.board[row - 1][column + 1] == board_state.board[row][column]:
            # print("we are entering been there done that")
            return 0
    number_in_row = 1
    # count number of same in a row
    while True:
        # if we reach the end of possible members of this row (out for board bounds)
        if row + number_in_row > board_state.number_of_rows-1 or column - number_in_row < 0:
            # print("we are entering out of bounds break")
            break
        # if the next in row is same as current space then we have row of that value
        elif board_state.board[row][column] == board_state.board[row + number_in_row][column - number_in_row]:
            # print("we are entering row is good break")
            number_in_row += 1
        # if next space is open indicate that and break while as there is no more row
        elif board_state.board[row + number_in_row][column - number_in_row] == '-':
            # print("we are entering end space is break")
            open_status += 1
            break
        # only other condition is that the next space is other value so row is broken
        else:
            # print("we are entering row broken break")
            break
    # need space value and the current player to finish evaluating, 0 means same as player, 1 is different
    same_player_status = 0
    if current_player != board_state.board[row][column]:
        same_player_status = 1
    # evaluate the row value and return it
    return check_return_heuristic(number_in_row, open_status, same_player_status)


def play_a_game(board):
    # start game timer
    t1_start = process_time()
    # import some globals
    global nodes_created
    global total_nodes_created
    i = 0
    winner = 'It is a Tie'
    while not board.is_board_filled():
        board.print_board()
        max_depth = 0
        if board.current_player == 'X':
            # print(evaluate_state(board, 'X'))
            if evaluate_state(board, 'X') > 700:
                winner = 'Player X'
                break
            elif evaluate_state(board, 'X') < -700:
                winner = 'Player O'
                break
            max_depth = 2
        else:
            # print(evaluate_state(board, 'O'))
            if evaluate_state(board, 'O') > 700:
                winner = 'Player O'
                break
            elif evaluate_state(board, 'O') < -700:
                winner = 'Player X'
                break
            max_depth = 4
        # determine best move using minimax
        t2_start = process_time()
        best_move = board.initMinMax(max_depth, 0, board.current_player)
        t2_stop = process_time()
        print("* Player " + str(board.current_player) + " is making the move [" + str(int(best_move.split(",")[0]))
              + "," + str(best_move.split(",")[1]) + "]\n*    Player " + str(board.current_player)
              + " is running minimax algorithm on a " + str(max_depth)
              + "-ply game tree\n*    total nodes created by minimax for this move: "
              + str(nodes_created) + "\n*    Elapse time: " + str(t2_stop - t2_start) + " seconds")
        # update node tracking globals
        total_nodes_created += nodes_created
        nodes_created = 0
        board.make_move(int(best_move.split(",")[0]), int(best_move.split(",")[1]))
    # stop game timer
    t1_stop = process_time()
    print("\n\n****************************\n  !!!!!!GAME IS OVER!!!!!!"
          "\n****************************\nThe winner of the game is:   "
          + winner + "\nTotal nodes created for minmax: " + str(total_nodes_created)
          + "\nTotal runtime of game: ", str(t1_stop - t1_start) + " seconds")
    # if someone wins


# main
def main():

    # Create Board
    game_board = Board()

    # SET UP STATES
    # ASSIGNMENT STATE
    game_board.make_move(3 - 1, 4 - 1)
    game_board.make_move(3 - 1, 3 - 1)
    game_board.current_player = 'X'

    # EXAMPLE #! (state from project file)
    # game_board.current_player = 'O'
    # game_board.make_move(1, 2)
    # game_board.make_move(1, 3)
    # game_board.make_move(2, 2)
    # game_board.make_move(3, 2)
    # game_board.make_move(3, 1)
    # game_board.make_move(3, 3)
    # game_board.make_move(3, 4)
    # game_board.make_move(4, 2)
    # game_board.make_move(2, 3)
    # game_board.make_move(2, 4)
    # game_board.current_player = 'X'

    # EXAMPLE #2

    # Play a Game
    play_a_game(game_board)


if __name__ == "__main__":
    main()
