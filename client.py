import socket

# Diffie-Hellman parameters
p = 23
g = 5

def caesar_encrypt(text, key):
    encrypted = ''
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - offset + key) % 26 + offset)
        else:
            encrypted += char
    return encrypted

# Conectare la server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

# cheia privată a clientului
client_private = 15
client_public = pow(g, client_private, p)
client.send(str(client_public).encode())

# cheia publică a serverului
server_public = int(client.recv(1024).decode())
shared_key = pow(server_public, client_private, p)
print(f"Cheia comună: {shared_key}")

message = input("Introdu mesajul de trimis: ")
encrypted_msg = caesar_encrypt(message, shared_key)
client.send(encrypted_msg.encode())
print(f"Mesaj criptat trimis: {encrypted_msg}")

client.close()
