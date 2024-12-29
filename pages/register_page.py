import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.user_data_file = "data/jsons/users.json"

        title_frame = tk.Frame(self, bg="white")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        title_label = tk.Label(title_frame, text="Register Page", font=("Helvetica", 16, "bold"), bg="white")
        title_label.pack()

        self.back_button_image = Image.open("data/images/back_sign.png")
        self.back_button_image = self.back_button_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.back_button_image = ImageTk.PhotoImage(self.back_button_image)

        back_button = tk.Button(self, image=self.back_button_image, command=self.go_back, bg="white", bd=0)
        back_button.place(x=self.winfo_width() + 1050, y=10)

        center_frame = tk.Frame(self, bg="white")
        center_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        profile_image = Image.open("data/images/profile_icon.png")
        profile_image = profile_image.resize((150, 150), Image.Resampling.LANCZOS)
        profile_image = ImageTk.PhotoImage(profile_image)

        profile_label = tk.Label(center_frame, image=profile_image, bg="white")
        profile_label.pack(pady=20)
        profile_label.image = profile_image

        input_frame = tk.Frame(center_frame, bg="white")
        input_frame.pack(pady=20)

        name_label = tk.Label(input_frame, text="Name:", font=("Helvetica", 12), bg="white")
        name_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        surname_label = tk.Label(input_frame, text="Surname:", font=("Helvetica", 12), bg="white")
        surname_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.surname_entry = tk.Entry(input_frame)
        self.surname_entry.grid(row=1, column=1, pady=5)

        email_label = tk.Label(input_frame, text="Email:", font=("Helvetica", 12), bg="white")
        email_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame)
        self.email_entry.grid(row=2, column=1, pady=5)

        password_label = tk.Label(input_frame, text="Password:", font=("Helvetica", 12), bg="white")
        password_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(input_frame, show="*")
        self.password_entry.grid(row=3, column=1, pady=5)

        register_button = tk.Button(center_frame, text="Register", command=self.register_clicked)
        register_button.pack(pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)

    def go_back(self):
        self.controller.show_frame("LoginPage")

    def register_clicked(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        self.email = self.email_entry.get()
        password = self.password_entry.get()

        if name and surname and self.email and password:
            check = self.check_if_already_existing()
            if (check):
                user_id = self.generate_unique_user_id()
                user_data = {
                    "user_id": user_id,
                    "name": name,
                    "surname": surname,
                    "email": self.email,
                    "password": password,
                    "profile_image_path": "data/profile_images/default.png",
                    "projects": []
                }
                self.save_user_data(user_data)
                messagebox.showinfo("Success", "User registered successfully!")
                self.controller.show_frame("LoginPage")
            else:
                messagebox.showerror("Error", "User already exists.")
        else:
            messagebox.showerror("Error", "Please fill out all fields.")

    def check_if_already_existing(self):
        if self.email == "Admin":
            messagebox.showerror("Error", "Email can't be Admin")
            return False
        with open(self.user_data_file, "r") as file:
            users = json.load(file)

        for user in users:
            if user.get("email") == self.email:
                return False
        return True

    def generate_unique_user_id(self):
        if not os.path.exists(self.user_data_file):
            return 1
        with open(self.user_data_file, "r") as file:
            try:
                data = json.load(file)
                if data:
                    max_id = max(user["user_id"] for user in data)
                    return max_id + 1
                return 1
            except json.JSONDecodeError:
                return 1

    def save_user_data(self, user_data):
        if not os.path.exists(self.user_data_file):
            with open(self.user_data_file, "w") as file:
                json.dump([user_data], file, indent=4)
        else:
            with open(self.user_data_file, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
            data.append(user_data)
            with open(self.user_data_file, "w") as file:
                json.dump(data, file, indent=4)
