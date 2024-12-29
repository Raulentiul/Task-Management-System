import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        title_frame = tk.Frame(self, bg="white")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        title_label = tk.Label(title_frame, text="Task Management System", font=("Helvetica", 16, "bold"), bg="white")
        title_label.pack()

        center_frame = tk.Frame(self, bg="white")
        center_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        profile_image = Image.open("data/images/profile_icon.png")
        profile_image = profile_image.resize((150, 150), Image.Resampling.LANCZOS)
        profile_image = ImageTk.PhotoImage(profile_image)

        profile_label = tk.Label(center_frame, image=profile_image, bg="white")
        profile_label.pack(pady=20)
        profile_label.image = profile_image

        input_frame = tk.Frame(center_frame, bg="white")
        input_frame.pack(pady=10)

        email_label = tk.Label(input_frame, text="Email:", font=("Helvetica", 12), bg="white")
        email_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame)
        self.email_entry.grid(row=2, column=1, pady=5)

        password_label = tk.Label(input_frame, text="Password:", font=("Helvetica", 12), bg="white")
        password_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(input_frame, show="*")
        self.password_entry.grid(row=3, column=1, pady=5)

        register_label = tk.Label(center_frame, text="Register", fg="blue", bg="white", cursor="hand2")
        register_label.pack(pady=5)
        register_label.bind("<Button-1>", self.register_clicked)

        login_button = tk.Button(center_frame, text="Login", command=self.login_clicked)
        login_button.pack(pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)

    def register_clicked(self, event):
        self.controller.show_frame("RegisterPage")

    def login_clicked(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if (email == "Admin" and password == "1234"):
            self.controller.show_frame("AdminPage")
            return

        with open("data/jsons/users.json", "r") as file:
            users = json.load(file)

            for user in users:
                if user["email"] == email and user["password"] == password:
                    user_id = user["user_id"]
                    projects_page = self.controller.frames["ProjectsPage"]

                    projects_page.user_id = user_id
                    projects_page.display_projects()

                    self.controller.show_frame("ProjectsPage", user_id=user_id)
                    return

        messagebox.showerror("Login", "Error: Incorrect email or password")

    def get_user_id(self,email, password):
        try:
            with open("data/jsons/users.json", "r") as file:
                users = json.load(file)
                for user in users:
                    if user["email"] == email and user["password"] == password:
                        return user["user_id"]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return None