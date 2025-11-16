import tkinter as tk
from tkinter import scrolledtext

class FuturisticGUI:
    def __init__(self, root, niblit):
        self.niblit = niblit
        self.chat = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state="disabled", bg="#111", fg="#0f0")
        self.chat.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=40, bg="#222", fg="#0f0")
        self.entry.pack(side="left", padx=10, pady=5)

        self.button = tk.Button(root, text="Send", command=self.send_message)
        self.button.pack(side="left", padx=5)

    def send_message(self):
        msg = self.entry.get()
        if not msg.strip():
            return
        self.entry.delete(0, tk.END)
        self.display(f"You: {msg}")
        response = self.niblit.respond(msg)
        self.display(f"Niblit: {response}")

    def display(self, text):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, text + "\n")
        self.chat.configure(state="disabled")
        self.chat.yview(tk.END)