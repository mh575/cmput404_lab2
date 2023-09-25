import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" #IP is localhost
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ) # with a connection, recieve request data
            if not data: # break when empty byte str recieved
                break
            print(data)
            conn.sendall(data)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # init socket 
        s.bind((HOST,PORT)) # bind ip and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # set socket options as self and manually free socket when finished
        s.listen # listen for connections
        conn, addr = s.accept() # accept incoming client 
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2) # backlog of <= 2 connections queue
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()
