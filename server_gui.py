import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

p = 23
g = 5

def caesar_decrypt(ciphertext, key):
    decrypted = ''
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - offset - key) % 26 + offset)
        else:
            decrypted += char
    return decrypted

class ServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Server")

        self.log = scrolledtext.ScrolledText(master, width=60, height=20, state='disabled')
        self.log.pack()

        self.running = True
        threading.Thread(target=self.start_server, daemon=True).start()

    def log_msg(self, msg):
        self.log.config(state='normal')
        self.log.insert(tk.END, msg + '\n')
        self.log.config(state='disabled')
        self.log.see(tk.END)

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 12345))
        server.listen(1)
        self.log_msg("Aștept conexiune de la client...")

        conn, addr = server.accept()
        self.log_msg(f"Conectat la {addr}")

        client_public = int(conn.recv(1024).decode())
        self.log_msg(f"Cheia publică a clientului: {client_public}")

        server_private = 6
        server_public = pow(g, server_private, p)
        conn.send(str(server_public).encode())

        shared_key = pow(client_public, server_private, p)
        self.log_msg(f"Cheia comună: {shared_key}")

        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()

                if message == "__disconnect__":
                    self.log_msg("[CLIENT DECONECTAT]")
                    break

                self.log_msg(f"[CRIPTAT] {message}")
                decrypted = caesar_decrypt(message, shared_key)
                self.log_msg(f"[DECRIPTAT] {decrypted}")
            except:
                break

        conn.close()
        self.log_msg("Conexiune închisă.")

root = tk.Tk()
app = ServerApp(root)
root.mainloop()
