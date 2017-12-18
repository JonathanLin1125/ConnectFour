import connectfourinterface
import collections

GameState = collections.namedtuple('GameState', ['board', 'turn'])

#Function prompts the user for a move and checks if it is valid before moving
def try_move(game_state:GameState) ->GameState:
    while True:
        try:
            move = connectfourinterface.get_move()
            column = connectfourinterface.get_column() - 1
            game_state = connectfourinterface.drop_or_pop(move, column, game_state)
            return game_state
        except:
            print("Invalid move")

#Keeps looping in a while loop until there is a winner       
def play_game(game_state:GameState):
    while(connectfourinterface.check_winner(game_state) == connectfourinterface.get_None()):
        connectfourinterface.print_board(game_state)
        connectfourinterface.print_turn(game_state)
        game_state = try_move(game_state)
    connectfourinterface.print_board(game_state)
    connectfourinterface.print_winner(game_state)

#Starts game by calling the starting_board function in the interface
def begin_game():
    game_state = connectfourinterface.starting_board()
    play_game(game_state)
    
if __name__ == "__main__":
    begin_game()
