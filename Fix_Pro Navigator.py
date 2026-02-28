import tkinter as tk
from PIL import Image, ImageTk
import threading
import subprocess

class ProNavigator:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Navigator")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height-40}+0+0")

        try:
            self.background_image = Image.open(r"C:\Users\Friza Chintia Putri\Documents\VSCODE SEM 3\Fix_Pro Navigator\landing_page.png")
            self.background_image = self.background_image.resize((self.screen_width, self.screen_height - 40), Image.Resampling.LANCZOS)
            self.background_image_tk = ImageTk.PhotoImage(self.background_image)
        except FileNotFoundError:
            self.background_image_tk = None
            print("File 'landing_page.png' tidak ditemukan.")

        self.frame_home = tk.Frame(self.root, width=self.screen_width, height=self.screen_height - 40)
        self.frame_home.pack_propagate(False)
        self.frame_home.pack(fill="both", expand=True)

        self.show_home()

    def add_background(self, frame):
        if self.background_image_tk:
            label_background = tk.Label(frame, image=self.background_image_tk)
            label_background.image = self.background_image_tk 
            label_background.place(x=0, y=0, relwidth=1, relheight=1)

    def run_subprocess(self, script_name):
        def target():
            subprocess.run(["python", script_name])
        threading.Thread(target=target, daemon=True).start()

    def show_home(self):
        for widget in self.frame_home.winfo_children():
            widget.destroy()

        self.add_background(self.frame_home)

        try:
            button_image = Image.open(r"C:\Users\Friza Chintia Putri\Documents\VSCODE SEM 3\Fix_Pro Navigator\button.PNG")
            button_image = button_image.resize((246, 40), Image.Resampling.LANCZOS)
            button_image_tk = ImageTk.PhotoImage(button_image)
        except FileNotFoundError:
            print("File 'button.PNG' tidak ditemukan.")
            return

        button_ucs = tk.Button(self.frame_home, image=button_image_tk, command=lambda: self.run_subprocess("Uniform_algorithm.py"), borderwidth=0)
        button_ucs.place(x=155, y=580)

        button_dijkstra = tk.Button(self.frame_home, image=button_image_tk, command=lambda: self.run_subprocess("Djikstra_algorithm.py"), borderwidth=0)
        button_dijkstra.place(x=500, y=580)

        button_greedy = tk.Button(self.frame_home, image=button_image_tk, command=lambda: self.run_subprocess("Greedy_algorithm.py"), borderwidth=0)
        button_greedy.place(x=860, y=580)

        button_ucs.image = button_image_tk
        button_dijkstra.image = button_image_tk
        button_greedy.image = button_image_tk

root = tk.Tk()
app = ProNavigator(root)
root.mainloop()