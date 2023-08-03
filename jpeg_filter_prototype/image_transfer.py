import struct

def send_image(sock,data):
    size = len(data)
    sock.send(struct.pack('!I', size))
    sock.sendall(data)

def receive_image(conn):
  data = conn.recv(4)
  if not data:
    return None
  size = struct.unpack('!I', data)[0]

  data = b''
  while len(data) < size:
    packet = conn.recv(size - len(data))
    if not packet:
      return None
    data += packet
  return data
