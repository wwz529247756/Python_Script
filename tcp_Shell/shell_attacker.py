import socket
import threading
import sys
import logging
import os
from subprocess import check_output as Execute



class reverse_sender(threading.Thread):
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

    def run(self):
        while True:
            msg = input("Send:")
            if msg == "quit":
                sys.exit(0)
                break
            else:
                self.send_data(msg)


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
        if msg == "command mode":
            self.mode = "command"
            return
        
        if msg == "message mode":
            self.mode = "message"
            return

        if self.mode == "message":
            premsg = "\nReceive:"
            postmsg = "\nSend:"
            msg = premsg + msg + postmsg
            print(msg, end="")

        else:
            command = msg.split(" ")
            output = Execute(command)
            self.sender.send_data(output.decode())

    def run(self):
        self.listenforconnection()


Usage = '''
USAGE:

    -i  integrate sender and receiver 
        -i [remote host] [remote port] [local host] [local host]
    -s  sender only
        -s [remote host] [remote port]
    -r  receiver only
        -r [local host] [local port]

    -h/--help show this information
'''


if __name__ == "__main__":
    args = sys.argv
    if args[1] == "-i":
        if len(args) != 6:
            print(Usage)
        else:
            remote_HOST = args[2]
            remote_PORT = int(args[3])
            local_HOST = args[4]
            local_PORT = int(args[5])
            sender = reverse_sender(remote_HOST, remote_PORT)
            receiver = reverse_receiver(local_HOST, local_PORT, sender)
            sender.start()
            receiver.start()

    elif args[1] == "-s":
        if len(args) != 4:
            print(Usage)
        else:
            remote_HOST = args[2]
            remote_PORT = int(args[3])
            s = reverse_sender(remote_HOST, remote_PORT)
            s.start()

    elif args[1] == "-r":
        if len(args) != 4:
            print(Usage)
        else:
            local_HOST = args[2]
            local_PORT = int(args[3])
            r = reverse_receiver(remote_HOST, remote_PORT)
            r.start()
    else:
        print(Usage)


