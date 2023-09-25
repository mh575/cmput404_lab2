import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request): # send client's request to host:port (server)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # init client socket 
        client_socket.connect((host,port)) # connect socket to host:port
        client_socket.send(request) # send request
        client_socket.shutdown(socket.SHUT_WR) # shutdown socket.

        data = client_socket.recv(BYTES_TO_READ) # get server response
        result = b'' + data
        while len(data) > 0: # read until data termininates 
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        return result # return response 
    
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}") 

        request = b''
        while True: # while client keeps socket open
            data = conn.recv(BYTES_TO_READ) # read some data from socket
            if not data: # break if socket terminates
                break
            print(data) # print data 
            request += data
        response = send_request("www.google.com", 80, request) # send data as request to www.google.com
        conn.sendall(response) # return response from www.google.com back to client

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()


