#!/usr/bin/python3

import socket
from datetime import datetime
import threading

UDP_IP = ""
UDP_PORT = 51415

now = datetime.now()
fileName = now.strftime("%b-%d-%Y_%H-%M-%S.txt")
#print("Press CTRL+c to stop the server.")
file = open(fileName,"a")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("server started")
while True:
    data, addr = sock.recvfrom(1024)
    print(data.decode("utf-8"))
    file.write(str(addr) + "\n>" + data.decode("utf-8") +"\n")
    file.flush()
