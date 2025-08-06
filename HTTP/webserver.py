import sys
import socket

PORT = 28333
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT))
s.listen()
print(f"Listening on port: {PORT}")
while True:
    new_conn = s.accept()
    print(f"{new_conn[1]} Connected")
    new_socket = new_conn[0]
    request = []
    while True:
        d = new_socket.recv(4096)
        print(d)
        if "\r\n\r\n" in d.decode("ISO-8859-1"):
            break
    response = "HTTP/1.1 200 OK\r\n\
Content-Type: text/html\r\n\
Content-Length: 26\r\n\
Connection: close\r\n\r\n\
<h1>Hello from Python</h1>\r\n"
    new_socket.sendall(response.encode("ISO-8859-1"))
    new_socket.close()
    print(f"{new_conn[1]} Disonnected")
