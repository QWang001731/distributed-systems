import pickle
import socket
import sys
from protocol import Message
from protocol import Server_res

if len(sys.argv)!=2:
    print("Usage : python3 server.py <port>")


class Server:
    def __init__(self, port) -> None:
        self.port=port        
        self.board=[[" "," "," "],
                    [" "," "," "],
                    [" "," "," "]]
        
        self.server_addr = ('localhost', self.port)
        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind(self.server_addr)
        self.server_socket.listen(1)
        self.running=True
        print(f'''Game server is ready.\nPlease send me requests through port {self.port}.''')

    def run(self):
        while self.running:
            connection, client_address = self.server_socket.accept()
            data = connection.recv(128)
            if data:
                request_msg = pickle.loads(data)
                params = {"side": "server"}
                if request_msg.management=="restart":
                    for i in range(3):
                        for j in range(3):
                            self.board[i][j]=" "
                    params["result"]=Server_res.RESTART_ACK
                    params["prompt"]="Game has been restarted."
                    params["board"]=self.board
                    server_response = Message(params)
                    serialized_msg = pickle.dumps(server_response)
                    connection.sendall(serialized_msg)
                    print("game restarted")
                    continue

                if request_msg.management=="close":
                    self.running=False
                    params["result"]=Server_res.CLOSE_SERVER
                    params["prompt"] = "Server has been closed"
                    params["board"]=self.board
                    server_response=Message(params)
                    serialized_msg = pickle.dumps(server_response)
                    connection.sendall(serialized_msg)
                    continue

                if request_msg.player not in ['X', 'O']:
                    params["result"] = Server_res.ERROR_MOV
                    params["prompt"] = "The player you input is invalid"
                    params["board"]=self.board
                
                elif request_msg.coordinate[0] not in [0,1,2] or request_msg.coordinate[1] not in [0,1,2] or self.board[request_msg.coordinate[0]][request_msg.coordinate[1]]!=" ":
                    params["result"] = Server_res.ERROR_MOV
                    params["prompt"] = f"The position {request_msg.coordinate}you input is invalid"
                    params["board"]=self.board

                else:
                    self.board[request_msg.coordinate[0]][request_msg.coordinate[1]] = request_msg.player
                    params["board"]=self.board
                    has_winner, player = self.test_winner()
                    if has_winner:
                        params["result"] = Server_res.WINNER_DETECTED
                        params["winner"] = player
                        params["prompt"] = f"player {player} is the winner !!!"
                    elif self.draw_game():
                        params["result"] = Server_res.WINNER_DETECTED
                        params["winner"] = "Both"
                        params["prompt"] = f"It's a drawn game, please restart or close"
                    else:
                        params["result"]=Server_res.VALID_MOVE_RES
                        params["prompt"]=None
                
                server_response=Message(params)
                serialized_msg = pickle.dumps(server_response)
                connection.sendall(serialized_msg)

        connection.close()
        print("Game server has been closed")

    def test_winner(self):
        for row in self.board:
            if(row[0]==row[1]==row[2] and row[0] != " "):
                return True, row[0]
            
        for col in range(3):
            if(self.board[0][col]==self.board[1][col]==self.board[2][col] and self.board[0][col]!=" "):
                return True, self.board[0][col]
        
        if(self.board[0][0]==self.board[1][1]==self.board[2][2] and self.board[0][0]!=" "):
            return True, self.board[0][0]
        
        if(self.board[0][2]==self.board[1][1]==self.board[2][0] and self.board[0][2]!=" "):
            return True, self.board[0][2]

        return False, None
    
    def draw_game(self):
        cnt=0
        for i in range(3):
            for j in range(3):
                if self.board[i][j]!=" ":
                    cnt+=1
        return cnt==9

Server_port=int(sys.argv[1])
server = Server(Server_port)
server.run()






