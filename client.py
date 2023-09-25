import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # open socket (domain: AF_INET, type: SOCK_STREAM (TCP), SOCK_DGRAM (UDP)) 
    s.connect((host, port)) # connect to host 
    s.send(request) # send request
    s.shutdown(socket.SHUT_WR) # send done
    result = s.recv(BYTES_TO_READ) # keep reading incoming data 
    while (len(result)>0): 
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close() # close socket

#get("www.google.com", 80)
get("localhost", 8080)