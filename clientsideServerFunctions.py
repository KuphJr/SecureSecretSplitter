from tkinter import messagebox

def sendBytesToServer(b):
    import socket
    import rsa
    global serverPublicKey, s
    try:
        s.send(rsa.encrypt(b, serverPublicKey))
    except:
        messagebox.showerror("Error", "Failed to communicate with the server.")    


# function to encrypt a string message with RSA and send it to the server
def sendMsgToServer(msg):
    import socket
    import rsa
    global serverPublicKey, s
    try:
        s.send(rsa.encrypt(msg.encode("ascii"), serverPublicKey))
    except:
        messagebox.showerror("Error", "Failed to communicate with the server.")


# function to decrypt a string received from the server with RSA
def recvMsgFromServer():
    import socket
    import rsa
    global clientPrivateKey, s
    try:
        data = s.recv(1024)
    except:
        messagebox.showerror("Error", "Failed to communicate with the server.")
        return ""
    return rsa.decrypt(data, clientPrivateKey).decode("ascii")

# function to establish a socket with the server
# exchanges RSA keys between the client and the server for security
def establishServerConnection():
    import socket
    import rsa
    global s, clientPublicKey, clientPrivateKey, serverPublicKey
    # close any exisiting sockets just in case on is open
    try:
        s.close()
    except:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("31.220.51.32", 51515))

        # Receive server public RSA key from server
        data = s.recv(1024).decode("ascii")
        serverPublicKeyN = int(data.split(",")[0])
        serverPublicKeyE = int(data.split(",")[1])
        serverPublicKey = rsa.PublicKey(serverPublicKeyN,serverPublicKeyE)
        print("Server public key: " + str(serverPublicKey))

        # Send client public RSA key to server
        global clientPublicKey, clientPrivateKey
        clientPublicKey, clientPrivateKey = rsa.newkeys(512)
        msgToServer = str(clientPublicKey["n"]) + "," + str(clientPublicKey["e"])
        print("Client public key: " + msgToServer)
        s.send(msgToServer.encode("ascii"))

        # check to ensure key exchange was valid
        data = s.recv(1024)
        decodedData = rsa.decrypt(data, clientPrivateKey)
        decodedData = decodedData.decode("ascii")
        print(decodedData)
        if decodedData != "hi":
            return False
        # send test message to server
        msgToServer = "hello"
        msgToServer = msgToServer.encode("ascii")
        s.send(rsa.encrypt(msgToServer, serverPublicKey))
    except:
        messagebox.showerror("Error", "Failed to connect to the server.")
        return False
    return True
