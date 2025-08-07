import sys
import socket
import os
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
        request.append(d)
        # print(d)
        if "\r\n\r\n" in d.decode("ISO-8859-1"):
            break
    request = b''.join(request)
    print(request.decode("ISO-8859-1"))
    header = request.split(b"\r\n\r\n")[0].split(b"\r\n")
    full_path = header[0].split(b" ")[1].decode(("ISO-8859-1"))
    path = os.path.split(full_path)[-1]
    extension = os.path.splitext(path)[1]
    content_type = ""
    match extension:
        case ".txt":
            content_type = "text/plain"
        case ".html":
            content_type = "text/html"

    response = ""
    try:
        with open(path, "r") as f:
            data = f.read()
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {extension}\r\n"
                f"Content-Length: {len(data)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{data}"
            )
            
    except:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 13\r\n"
            "Connection: close\r\n"
            "\r\n"
            "404 not found\r\n"
        )
    new_socket.sendall(response.encode("ISO-8859-1"))
    new_socket.close()
    print(f"{new_conn[1]} Disonnected")
