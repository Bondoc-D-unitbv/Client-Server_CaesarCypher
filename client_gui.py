import socket
import tkinter as tk
from tkinter import scrolledtext

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

class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Client")

        self.entry = tk.Entry(master, width=50)
        self.entry.pack()

        self.send_button = tk.Button(master, text="Trimite", command=self.send_message)
        self.send_button.pack()

        self.disconnect_button = tk.Button(master, text="Deconectează", command=self.disconnect)
        self.disconnect_button.pack()

        self.log = scrolledtext.ScrolledText(master, width=60, height=20, state='disabled')
        self.log.pack()

        self.shared_key = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 12345))
        self.init_key_exchange()

    def log_msg(self, msg):
        self.log.config(state='normal')
        self.log.insert(tk.END, msg + '\n')
        self.log.config(state='disabled')
        self.log.see(tk.END)

    def init_key_exchange(self):
        client_private = 15
        client_public = pow(g, client_private, p)
        self.sock.send(str(client_public).encode())
        server_public = int(self.sock.recv(1024).decode())
        self.shared_key = pow(server_public, client_private, p)
        self.log_msg(f"Cheia comună: {self.shared_key}")

    def send_message(self):
        message = self.entry.get()
        if not message.strip():
            return
        encrypted = caesar_encrypt(message, self.shared_key)
        self.sock.send(encrypted.encode())
        self.log_msg(f"Trimis (criptat): {encrypted}")
        self.entry.delete(0, tk.END)

    def disconnect(self):
        try:
            self.sock.send("__disconnect__".encode())
            self.sock.close()
            self.log_msg("[Deconectat de la server]")
            self.send_button.config(state="disabled")
            self.disconnect_button.config(state="disabled")
        except:
            self.log_msg("[Eroare la deconectare]")

root = tk.Tk()
app = ClientApp(root)
root.mainloop()
