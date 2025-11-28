# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select


def run_server(port):
    listner_socket = socket.socket()
    listner_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listner_socket.bind(("", port))
    listner_socket.listen()
    print(f"Listening on port: {port}")
    read_set = {listner_socket}
    while True:
        ready_set,_,_ = select.select(read_set, {}, {})
        for s in ready_set:
            if s == listner_socket:
                connection = listner_socket.accept()
                print(f"{connection[1]} Connected!");
                new_socket = connection[0]
                read_set.add(new_socket)
            else:
                d = s.recv(4096)
                if len(d) != 0:
                    print(f"{s.getpeername()} {len(d)} bytes: {d}")
                else:
                    print(f"{s.getpeername()} Disconnected")
                    read_set.remove(s)


def usage():
    print("usage: select_server.py port", file=sys.stderr)


def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
