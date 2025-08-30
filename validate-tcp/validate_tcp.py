def ip_to_bytes(ip: str) -> bytes:
    s = list(map(lambda x: int(x), ip.split('.')))
    res = b""
    for d in s:
        res += d.to_bytes()
    return res

def checksum(data: bytes) -> int:
    total = 0
    offset = 0   
    while offset < len(data):
        word = int.from_bytes(data[offset:offset + 2], "big")
        total += word
        total = (total & 0xFFFF) + (total >> 16)
        offset += 2   
    return ~total & 0xFFFF


for i in range(9):
    ip_header = b''
    with open(f'tcp_data/tcp_addrs_{i}.txt', 'r') as f:
        for ip in f.readline().strip().split(" "):
            ip_header += ip_to_bytes(ip)
    ip_header += b'\x00\x06'  # Zero + TCP

    tcp_original = b''
    with open(f'tcp_data/tcp_data_{i}.dat', 'rb') as f:
        tcp_original += f.read()
    ip_header += len(tcp_original).to_bytes(2, byteorder="big")

    tcp_zero_checksum = tcp_original[:16] + b'\x00\x00' + tcp_original[18:]
    if len(tcp_zero_checksum) % 2 != 0:
        tcp_zero_checksum += b'\x00'
        
    chsum = checksum(ip_header+tcp_zero_checksum)
    chsum_og = int.from_bytes(tcp_original[16:18], "big")

    print(f"Packet {i+1}: ", end="")
    if chsum == chsum_og:
        print("\033[92mPASS\033[0m")
    else:
        print("\033[91mFAIL\033[0m")
