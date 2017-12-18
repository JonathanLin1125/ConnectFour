import connectfour
import collections

#Define the variable GameState
GameState = collections.namedtuple('GameState', ['board', 'turn'])

#Getter method for the value of RED in connectfour.py
def get_Red()->int:
    return connectfour.RED

#Getter method for the value of YELLOW in connectfour.py
def get_Yellow()->int:
    return connectfour.YELLOW

#Getter method for the value of NONE in connectfour.py
def get_None()->int:
    return connectfour.NONE

#Returns the GameState after either dropping or popping in a given column
#Input choice should be either "D" or "P"
def drop_or_pop(choice:str, column_number:int, game_state:GameState):
    if choice == "D":
        return connectfour.drop(game_state, column_number)
    elif choice == "P":
        return connectfour.pop(game_state, column_number)

#Getter method for checking if there is a winner in connectfour.py
def check_winner(game_state:GameState) ->int:
    return connectfour.winner(game_state)

#Prompts user for move, reprompts unless user inputs either d or p, case-insensitive
#Returns the move
def get_move()->str:
    move = input("Drop(D) or Pop(P)? ").strip().upper()
    while( move != "D" and move != "P"):
        print("Invalid Input")
        move = input("Drop(D) or Pop(P)? ").strip().upper()
    return move

#Gets the column number, which has to be between 1 and 7, inclusive
#Checks that input is also an integer, and returns the column number if valid
def get_column()->int:
    while True:
        column = input("Enter the Column(1-7): ").strip()
        try:
            int_column = int(column)
            if(int_column > 0 and int_column < 8):
                return int_column
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")

#Prints winner based off the current state of game_state
def print_winner(game_state:GameState):
    if GameState != None:
        if check_winner(game_state) == connectfour.RED:
            print("Red wins!")
        elif check_winner(game_state) == connectfour.YELLOW:
            print("Yellow wins!")
    else:
        print("No Winner")

#Prints if it's Red's or Yellow's turn
def print_turn(game_state:GameState):
    if game_state.turn == connectfour.RED:
        print("It is Red's turn to move")
    elif game_state.turn == connectfour.YELLOW:
        print("It is Yellow's turn to move")

#Prints the board by iterating through the 2D array
def print_board(game_state:GameState):
    print()
    print("1 2 3 4 5 6 7")
    for y in range(connectfour.BOARD_ROWS):
        for x in range(connectfour.BOARD_COLUMNS):
            entry = game_state.board[x][y]
            if entry == connectfour.NONE:
                print(".", end="")
            elif entry == connectfour.RED:
                print("R", end="")
            elif entry == connectfour.YELLOW:
                print("Y", end="")
            if x < (connectfour.BOARD_COLUMNS - 1):
               print(" ", end="")
        print()
    print()

#Starts the board by calling the new_game() method in connectfour.py
#Returns the GameState that will be used
def starting_board() ->GameState:
    return connectfour.new_game()
