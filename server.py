import socket
import time
from threading import Thread


def accept_connection():
    while True:
        c, ca = SERVER.accept()
        print("Time is {}:{}\n client {} has connected".format(time.localtime().tm_hour, time.localtime().tm_min,
                                                               ca))
        c.send(bytes("You are now connected to chat!", "utf8"))
        addresses[c] = ca
        Thread(target=handle_client, args=(c,)).start()


def handle_client(c):
    name = c.recv(BUFSIZ).decode("utf8")
    # try:
    welcome = 'Hello %s!\nIf you want to quit, type {quit} to exit.' % name
    c.send(bytes(welcome, "utf8"))

    msg = "Mezuval {} has joined the chat".format(name)

    broadcast(bytes(msg, "utf8"))
    # except OSError:
    #     print("{} has made an error!".format(name))
    clients[c] = name

    while True:
        # try:
        msg = c.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            c.send(bytes("{quit}", "utf8"))
            c.close()
            del clients[c]
            msg = "Mezuval {} has quit the fun".format(name)
            broadcast(bytes(msg, "utf8"))
            break
        # except OSError:
        #     print("{} has made an error!".format(name))


def broadcast(msg, prefix=""):
    for s in clients:
        s.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(10)
    print("Connection is open!\nWaiting for clients...")
    A_THREAD = Thread(target=accept_connection())
    A_THREAD.start()
    A_THREAD.join()
    SERVER.close()
