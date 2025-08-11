import time
import socket

PORT = 37
URL = "time.nist.gov"


def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch
  
s = socket.socket()
s.connect((URL, PORT))

request = (
  "GET / HTTP/1.1\r\n"
  f"Host: {URL}\r\n"
  "Connection: close\r\n"
  "\r\n"
)

response = s.recv(1024)
print("NIST time : ", int.from_bytes(response))
print("System time : ", system_seconds_since_1900()) 