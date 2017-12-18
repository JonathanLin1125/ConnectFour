import socket
from collections import namedtuple

connection = namedtuple("connection", ["socket", "socket_in", "socket_out"])

#Connects the server and uses the namedtuple, connection, to store the parts
#If host/port is invalid, None is returned to notify user that host/port is invalid
def connect_server(host:str, port:int)->connection:
    socket_connection = socket.socket()
    address = (host, port)
    try:
        socket_connection.connect(address)
        socket_connection_in = socket_connection.makefile("r")
        socket_connection_out = socket_connection.makefile("w")
        return connection(socket = socket_connection, socket_in = socket_connection_in, socket_out = socket_connection_out)
    except:
        print("Invalid Host/Port")
        return None

#Sends the message given in the paramter to the connection
def send_message(message:str, connection:connection):
    connection.socket_out.write(message + "\r\n")
    connection.socket_out.flush()

#Reads in a line from the server giventhe connection and returns the string
def receive_message(connection:connection)->str:
    return connection.socket_in.readline()

#Closes the connection
def close(connection:connection):
    print("Disconnecting...")
    connection.socket_in.close()
    connection.socket_out.close()
    connection.socket.close()
    print("Disconnected")

#Prompts user for host, which can not be an empty string
def get_host() ->str:
    while True:
        host = input("Host: ").strip()

        if host == "":
            print("Not a valid host, please try again")
        else:
            return host

#Prompts user for the port
def get_port() ->int:
    while True:
        try:
            port = int(input("Port: "))

            if port < 0 or port > 65535:
                print("Not a valid port; please try again")
            else:
                return port
        except ValueError:
            print("Not a valid port; please try agian")

#Prompts user for username, which can not contain a space
def get_username() ->str:
    username = input("Username: ")
    while( " " in username.strip() or len(username.strip()) == 0):
        print("Invalid username")
        username = input("Username: ")
    return username.strip()

    
