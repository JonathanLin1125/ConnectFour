import connectfourserverinterface
import connectfourinterface
from collections import namedtuple

connection = namedtuple("connection",  ["socket", "socket_in", "socket_out"])
GameState = namedtuple("GameState", ["board", "turn"])

#Sends move to the server and reads the next response
#If next response is "INVALID", then user will retry another move until a valid move is inputted 
def send_move(connection:connection, game_state:GameState) ->GameState:
    response = "INVALID"
    
    while response == "INVALID":
        move = connectfourinterface.get_move()
        column = connectfourinterface.get_column()
        if(move == "D"):
            connectfourserverinterface.send_message("DROP " + str(column), connection)
        elif(move == "P"):
            connectfourserverinterface.send_message("POP " + str(column), connection)
            
        #Server either replies with "INVALID" or "OKAY" or "WINNER_RED/WINNER_YELLOW"
        response = connectfourserverinterface.receive_message(connection).strip()
        if response == "INVALID":
            print("Invalid Move")
            message = connectfourserverinterface.receive_message(connection).strip()

    return connectfourinterface.drop_or_pop(move, column - 1, game_state)

#Receives move from server and attempts to move the board, if it is not possible, server has made an invalid move
def receive_move(connection:connection, game_state:GameState) ->GameState:
    move = connectfourserverinterface.receive_message(connection).split()

    try:
        if move[0] == "DROP":
            return connectfourinterface.drop_or_pop("D", int(move[1]) -1, game_state)
        elif move[0] == "POP":
            return connectfourinterface.drop_or_pop("P", int(move[1]) -1, game_state)
    except:
        print("Server has made an invalid move")
        return None

#Loops game in a while loop, checking for if there is a winner after a user move, or a winner after the server move
#If server makes an invalid move, connection ends and there is no winner
def play_game(connection:connection):
    message = None

    game_state = connectfourinterface.starting_board()
    connectfourinterface.print_board(game_state)

    while( message != "WINNER_RED" and message != "WINNER_YELLOW" and game_state != None):
        connectfourinterface.print_turn(game_state)
        game_state = send_move(connection, game_state)
        connectfourinterface.print_board(game_state)

        if connectfourinterface.check_winner(game_state) == connectfourinterface.get_Red():
            message = "WINNER_RED"
        elif connectfourinterface.check_winner(game_state) == connectfourinterface.get_Yellow():
            message = "WINNER_YELLOW"
        else:
            #Keeps playing if the response from send_move was "OKAY"
            connectfourinterface.print_turn(game_state)
            game_state = receive_move(connection, game_state)

            #If server made an invalid move, gaem_state should now be set to None
            if game_state != None:
                #Message == READY, or "WINNER_RED/WINNER_YELLOW"
                message = connectfourserverinterface.receive_message(connection).strip()
                connectfourinterface.print_board(game_state)
    connectfourinterface.print_winner(game_state)
    connectfourserverinterface.close(connection)
    
#Iniates game with server
def start_game(connection:connection):
    connectfourserverinterface.send_message("AI_GAME", connection)
    print("Server is " + connectfourserverinterface.receive_message(connection), end="")

#Sends username to server
#Server responds with Welcome + username, which is printed to the console
#Returns true if connection is valid, false if otherwise
def get_username(connection:connection)->bool:
    username = connectfourserverinterface.get_username()
    connectfourserverinterface.send_message("I32CFSP_HELLO " + username, connection)
    message = connectfourserverinterface.receive_message(connection).strip()
    if(message != ("WELCOME " + username)):
        print("Not a valid connection")
        return False
    else:
        print("\n" + message)
        return True

#Calls the functions in the interface to prompt user for host/port
#Connects to the host/port, if they are invalid, program will end
#After user is connected, user will input username and game will start
def connect():
    host = connectfourserverinterface.get_host()
    port = connectfourserverinterface.get_port()

    print(f"Connecting to {host} (port {port})...")

    connection = connectfourserverinterface.connect_server(host, port)
    if(connection != None):
        print("Connected!")
    
        if(get_username(connection)):
            start_game(connection)
            play_game(connection)
        else:
            connectfourserverinterface.close(connection)
            print("Quitting...")
    else:
        print("Quitting...")
     
if __name__ == "__main__":
    connect()
