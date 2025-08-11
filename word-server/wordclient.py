import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2


def usage():
    print("usage: wordclient.py server port", file=sys.stderr)


packet_buffer = b''


def get_next_word_packet(s: socket.socket) -> bytes | None:
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    global packet_buffer
    while True:
        packet_buffer += s.recv(8)
        
        if len(packet_buffer) == 0:
            return None
        if len(packet_buffer) < WORD_LEN_SIZE: 
            continue
        
        word_packet_length = WORD_LEN_SIZE +  int.from_bytes(packet_buffer[:WORD_LEN_SIZE], "big")
        
        if word_packet_length <= len(packet_buffer):
            word_packet = packet_buffer[:word_packet_length]
            packet_buffer = packet_buffer[word_packet_length:]
            return word_packet
        


def extract_word(word_packet: bytes) -> str:
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    word = word_packet[WORD_LEN_SIZE:].decode("utf-8")
    return word

def main(argv: list[str]):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
