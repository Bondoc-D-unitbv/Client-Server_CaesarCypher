import random
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


def transpose_encrypt(text, key):
    indices = list(range(len(text)))
    random.seed(key)  
    random.shuffle(indices)
    encrypted = ''.join([text[i] for i in indices])
    return encrypted, indices

class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Client")

        self.method = tk.StringVar()
        self.method.set("caesar")

        tk.Label(master, text="Mesaj:").pack()
        self.entry = tk.Entry(master, width=50)
        self.entry.pack()

        tk.Label(master, text="Metoda de criptare:").pack()
        tk.OptionMenu(master, self.method, "caesar", "transposition").pack()

        self.send_button = tk.Button(master, text="Trimite", command=self.send_message)
        self.send_button.pack()

        self.disconnect_button = tk.Button(master, text="Deconectează", command=self.disconnect)
        self.disconnect_button.pack()

        self.log = scrolledtext.ScrolledText(master, width=60, height=20, state='disabled')
        self.log.pack()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 12345))
        self.shared_key = self.key_exchange()
        self.send_method_to_server()
        self.log_msg(f"Cheia comună (Diffie-Hellman): {self.shared_key}")

    def log_msg(self, msg):
        self.log.config(state='normal')
        self.log.insert(tk.END, msg + '\n')
        self.log.config(state='disabled')
        self.log.see(tk.END)

    def key_exchange(self):
        private = 15
        public = pow(g, private, p)
        self.sock.send(str(public).encode())
        server_public = int(self.sock.recv(1024).decode())
        return pow(server_public, private, p)

    def send_method_to_server(self):
        self.sock.send(self.method.get().encode())

    def send_message(self):
        text = self.entry.get()
        if not text.strip():
            return

        method = self.method.get()
        if method == "caesar":
            encrypted = caesar_encrypt(text, self.shared_key)
        else:
            encrypted, _ = transpose_encrypt(text, self.shared_key)

        self.sock.send(encrypted.encode())
        self.log_msg(f"[Trimis cu {method}] {encrypted}")
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
