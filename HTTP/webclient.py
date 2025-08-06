import sys
import socket

PORT = 80
URL = ""
if len(sys.argv) < 2:
    print("Usage: python webclient.py example.com [PORT]", file=sys.stderr)
    exit(1)
URL = sys.argv[1]
if len(sys.argv) == 3:
   PORT = int(sys.argv[2]) 

s = socket.socket()
s.connect((URL, PORT))

request = f"GET / HTTP/1.1\r\n\
Host: {URL}\r\n\
Connection: close\r\n\r\n"

s.sendall(request.encode("ISO-8859-1"))

response = []
while True:
    d = s.recv(4096)
    response.append(d)  
    if len(d) == 0:
        break
    
s.close()
response = b"".join(response)
print(response.decode("ISO-8859-1"))

