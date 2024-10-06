import pickle
import socket
import sys
from protocol import Message
from protocol import Server_res

if len(sys.argv)!=4 and len(sys.argv)!=3:
    print(f"Usage: python3 {sys.argv[0]} <port> <player> <coordinate> or python3 {sys.argv[0]} <port> restart/close")

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = int(sys.argv[1])
server_addr = ('localhost', port)
client_socket.connect(server_addr)

params={"side":"client"}
if len(sys.argv)==4:
    params["player"]=sys.argv[2]
    params["coordinate"]=tuple([int(sys.argv[3][1:-1].split(',')[0]),int(sys.argv[3][1:-1].split(',')[1])])
    co=params["coordinate"]
    params["management"]=None

if len(sys.argv)==3:
    params["management"]=sys.argv[2]

client_msg=Message(params)
client_msg=pickle.dumps(client_msg)
client_socket.sendall(client_msg)

data=client_socket.recv(256)
server_res = pickle.loads(data)

if server_res.result==Server_res.ERROR_MOV:
    print(server_res.prompt)
    board=server_res.board
    for row in board:
        print("|",end="")
        for col in row:
            print(col, end="|")
        print("\n")
    

if server_res.result==Server_res.RESTART_ACK:
    print(server_res.prompt)
    board=server_res.board
    for row in board:
        print("|",end="")
        for col in row:
            print(col, end="|")
        print("\n")

if server_res.result==Server_res.VALID_MOVE_RES:
    board=server_res.board
    for row in board:
        print("|",end="")
        for col in row:
            print(col, end="|")
        print("\n")

if server_res.result==Server_res.WINNER_DETECTED:
    print(server_res.prompt)
    board=server_res.board
    for row in board:
        print("|",end="")
        for col in row:
            print(col, end="|")
        print("\n")
    print("please restart the game !")

if server_res.result==Server_res.CLOSE_SERVER:
    print(server_res.prompt)
