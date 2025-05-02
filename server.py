import socket

# Diffie-Hellman parameters
p = 23  # prim
g = 5   # generator

def caesar_decrypt(ciphertext, key):
    decrypted = ''
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - offset - key) % 26 + offset)
        else:
            decrypted += char
    return decrypted

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)
print("Serverul așteaptă conexiunea de la client...")

conn, addr = server.accept()
print(f"Conectat la: {addr}")

# Primim cheia publică a clientului
client_public = int(conn.recv(1024).decode())
print(f"Cheia publică a clientului: {client_public}")

# Alegem cheia privată a serverului
server_private = 6
server_public = pow(g, server_private, p)
conn.send(str(server_public).encode())

# Calculăm cheia secretă comună
shared_key = pow(client_public, server_private, p)
print(f"Cheia comună: {shared_key}")

# Primim mesajul criptat
encrypted_msg = conn.recv(1024).decode()
print(f"\n[CRIPTAT] Mesaj primit: {encrypted_msg}")

# Decriptare
decrypted_msg = caesar_decrypt(encrypted_msg, shared_key)
print(f"[DECRIPTAT] Mesaj original: {decrypted_msg}")

conn.close()
