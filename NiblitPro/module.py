import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import os
import webbrowser

# === Core App ===
class NiblitUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Niblit AI Companion")
        self.root.geometry("480x800")  # Smartphone aspect ratio
        self.root.configure(bg="black")

        # Default wallpaper
        self.wallpaper = None
        self.set_wallpaper("default_wallpaper.jpg")

        # Main frame
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        # App grid
        self.apps = [
            ("Weather", self.open_weather),
            ("News", self.open_news),
            ("Stocks", self.open_stocks),
            ("Currency", self.open_currency),
            ("Crime", self.open_crime),
            ("Predictive", self.open_predictive),
            ("Chat", self.open_chat),
            ("Health", self.open_health),
            ("Files", self.open_file_manager),
            ("Media", self.open_media_player),
            ("Browser", self.open_browser),
            ("Settings", self.open_settings)
        ]
        self.draw_grid()

    # === Wallpaper ===
    def set_wallpaper(self, img_path):
        if os.path.exists(img_path):
            self.wallpaper = Image.open(img_path).resize((480,800))
            self.bg_img = ImageTk.PhotoImage(self.wallpaper)
            bg_label = tk.Label(self.root, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # === App Grid ===
    def draw_grid(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        rows, cols = 4, 3
        for index, (name, action) in enumerate(self.apps):
            row, col = divmod(index, cols)
            btn = tk.Button(self.main_frame, text=name, command=action,
                            font=("Arial", 12, "bold"),
                            fg="white", bg="#222", width=12, height=4,
                            relief="flat")
            btn.grid(row=row, column=col, padx=10, pady=10)

    # === App Functions ===
    def open_weather(self): messagebox.showinfo("Weather", "Weather module here")
    def open_news(self): messagebox.showinfo("News", "News module here")
    def open_stocks(self): messagebox.showinfo("Stocks", "Stocks module here")
    def open_currency(self): messagebox.showinfo("Currency", "Currency module here")
    def open_crime(self): messagebox.showinfo("Crime", "Crime prediction module")
    def open_predictive(self): messagebox.showinfo("Predictive", "Predictive analysis")
    def open_chat(self): messagebox.showinfo("Chat", "Chat with Niblit")
    def open_health(self): messagebox.showinfo("Health", "Health tracker")
    
    # === File Manager ===
    def open_file_manager(self):
        file = filedialog.askopenfilename()
        if file:
            messagebox.showinfo("File Selected", f"You chose: {file}")

    # === Media Player Placeholder ===
    def open_media_player(self):
        file = filedialog.askopenfilename(filetypes=[("Media files", "*.mp3 *.mp4 *.wav *.avi *.mkv")])
        if file:
            messagebox.showinfo("Media Player", f"Now playing: {file}")

    # === Browser Launcher ===
    def open_browser(self):
        webbrowser.open("https://www.google.com")

    # === Settings ===
    def open_settings(self):
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("400x600")

        tk.Label(settings, text="Settings", font=("Arial", 16, "bold")).pack(pady=10)

        # Wallpaper Change
        tk.Button(settings, text="Change Wallpaper", command=self.change_wallpaper).pack(pady=10)

        # Theme
        tk.Button(settings, text="Change Theme Color", command=self.change_theme).pack(pady=10)

    def change_wallpaper(self):
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if file:
            self.set_wallpaper(file)

    def change_theme(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.root.configure(bg=color)
            self.main_frame.configure(bg=color)

# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = NiblitUI(root)
    root.mainloop()