'''
    File:server.py
    Author:JingKai Zhou
    Purpose: This file I will create a simple HTTP server of mine. The server can serve data
            to multiple clients at the same time.
'''
from socket import *
from threading import *
import os.path
from pip._vendor.pep517.compat import FileNotFoundError


def main():
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_addr = ("0.0.0.0",8080)
    server_sock.bind(server_addr)
    server_sock.listen(5)

    while True:
        (conn_sock, conn_addr) = server_sock.accept()
        print("Connection request received from"+str(conn_addr))
        msg = conn_sock.recv(1024).decode()
        msglist = msg.split()
        filename = msglist[1].strip("/")
        print("filename:"+filename)
        thread_handle = Thread(target= handle ,args=(filename,conn_sock))
        thread_handle.start()


def handle(filename,conn_sock):
    '''
    In the handle function, I will handle the filename that I get for server_sock
    and find it in local and sent it all as byte.
    :param filename: string
    :param conn_sock: socket
    :return: no return
    '''
    if os.path.exists(filename):
        try:
            fobj = open(filename, "rb")
            whole_file = fobj.read()
            size=len(whole_file)
            conn_sock.sendall("HTTP/1.1 200 OK\n\n".encode())
            conn_sock.sendall(whole_file)
            print("HTTP/1.1 200 OK\n")
            print ("Content-Length:"+str(size)+"\n")
            print(whole_file)
            conn_sock.shutdown(SHUT_WR)
        except FileNotFoundError:
            print("We only go here if the open() fails")

    else:
        print("HTTP/1.1 404 Not Found")
        print("\n")

main()







