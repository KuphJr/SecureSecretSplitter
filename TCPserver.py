#!/usr/bin/python3

import socket
from _thread import *
import threading
import rsa
import os.path
import os
  
loginInfo = threading.Lock()
savedKeys = threading.Lock()

class Client:
    numClients = 0

    # generate and share key with the client & receive key from client
    def __init__(self, clientSocket):
        Client.numClients += 1
        # generate and send key to client
        self.clientSocket = clientSocket
        serverPublicKey, self.serverPrivateKey = rsa.newkeys(512)
        msgToClient = str(serverPublicKey["n"]) + "," + str(serverPublicKey["e"])
        clientSocket.send(msgToClient.encode("ascii"))
        # get key from client
        data = self.clientSocket.recv(1024).decode("ascii")
        clientPublicKeyN = int(data.split(",")[0])
        clientPublicKeyE = int(data.split(",")[1])
        self.clientPublicKey = rsa.PublicKey(clientPublicKeyN,clientPublicKeyE)
        # test to ensure key exchange was valid
        self.sendMsg("test message from server")
        data = self.recvMsg()
        if data != "test message from client":
            raise Exception("Key exchange with client was invalid")


    def sendMsg(self, msg):
        msg = msg.encode("ascii")
        self.clientSocket.send(rsa.encrypt(msg, self.clientPublicKey))        
    

    def recvMsg(self):
        data = self.clientSocket.recv(1024)
        decodedData = rsa.decrypt(data, self.serverPrivateKey)
        return decodedData.decode("ascii")

    def recvBytes(self):
        data = self.clientSocket.recv(1024)
        return rsa.decrypt(data, self.serverPrivateKey)

def handleLoggedInClient(client, username):
    global s
    userDirPath = os.path.join("/root/encryptedKeys/", username)
    data = client.recvMsg()
    if data == "save":
        while True:
            fileName = client.recvMsg()
            filePath = os.path.join(userDirPath, fileName)
            if not os.path.isfile(filePath):
                break
            client.sendMsg("Save file name is already in use")
        with open(filePath, "w") as safeFile:
            data = data.recvMsg()
            while data != "endall":
                writeData = ""
                while data != "endkey":
                    writeData += data
                    data.recvMsg()
                safeFile.write(writeData + "/n")
                data.recvMsg()
        client.sendMsg("success")
    elif data == "load":
        with os.listdir(userDirPath) as files:
            for file in files:
                client.sendMsg(file)
        reqFileName = client.recvMsg()
        reqFilePath = os.path.join(userDirPath, reqFileName)
        with open(reqFilePath, "r") as reqFile:
            # send text in the requested save file back to the user
            # be sure to break it up such that endline characters are not included
            for line in reqFile:
                lineWOendline = line[:-1]
                print(lineWOendline + "endOfLine")
                numPackets = (len(line) // 257) + 1
                start = 0
                for i in range(numPackets):
                    end = start + 255
                    if end >= len(numPackets):
                        client.sendMsg(line[start:])
                    else:
                        client.sendMsg(line[start:end])
                        start += 256
                client.sendMsg("endkey")
            client.sendMsg("endall")
    else:
        client.sendMsg("Error: invalid command")
    s.close()
    c.close()
    

  
# multithreaded function to handle a client
def handleClient(c):
    global s
    # create a client object with the RSA keys to handle communication
    try:
        client = Client(c)
    except Exception as e:
        print(e)
        return
    try:
        # check for a login
        data = client.recvMsg()
        if data == "create":
            print("start create")
            with open("hashedUserAccounts.txt", "a+") as userFile:
                while True:
                    sentUsername = client.recvMsg()
                    if all(sentUsername != username.split(",", 1)[0] for username in userFile):
                        break
                    client.sendMsg("exists")
                print("username is new")
                client.sendMsg("new")
                sentPassword = client.recvBytes()
                userFile.write(sentUsername + ",")
                userFile.write(sentPassword)
                userFile.write("\n")
                path = os.path.join("/root/encryptedKeys/", sentUsername)
                os.mkdir(path)
                print("created account")
                client.sendMsg("created")
                try:
                    handleLoggedInClient(client, sentUsername)
                except Exception as e:
                    print(e)
                    c.close()
                    s.close()
                    return
                else:
                    client.sendMsg("username exists")
        elif data == "login":
            sentUsername = client.recvMsg()
            with open("hashedUserAccounts.txt", "r") as userFile:
                for account in userFile:
                    sentPassword = client.recvMsg()
                    username, password = split(",", 1)
                    if sentUser == username:
                        if sentPassword == password:
                            try:
                                handleLoggedInClient(client, sentUsername)
                            except Exception as e:
                                print(e)
                                c.close()
                                return
                        else:
                            break
                client.sendMsg("username or password is not valid")
        else:
            client.sendMsg("Error: invalid command")
    except Exception as e:
        print(e)
        c.close()
        s.close()
        return
  
  
def main():
    host = ""
    port = 51515
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)
    s.bind((host, port))
    print("socket bound")
  
    s.listen(5)
    print("socket listening")
  
    # a forever loop until client wants to exit
    while True:
        c, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        c.settimeout(20)
        start_new_thread(handleClient, (c,))
    s.close()
  
  
if __name__ == '__main__':
    main()
