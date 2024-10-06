from enum import Enum


class Server_res(enumerate):
    ERROR_MOV = 0
    VALID_MOVE_RES = 1
    WINNER_DETECTED = 2
    RESTART_ACK = 3
    CLOSE_SERVER=4


class Message:
    def __init__(self, params) -> None:
        if params["side"]=="client":
            if params["management"] is None:
                self.player = params["player"]
                self.coordinate = params["coordinate"]
                self.management=params=None
            else:
                self.management=params["management"]
        
        else:
            self.result = params["result"]
            self.prompt=params["prompt"]
            self.board = params["board"]
            
            if self.result == Server_res.WINNER_DETECTED:
                self.winner = params["winner"]

