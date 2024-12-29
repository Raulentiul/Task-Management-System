import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.back_image = Image.open("data/images/back_sign.png")
        self.back_image = self.back_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.back_image = ImageTk.PhotoImage(self.back_image)
        back_button = tk.Button(self, image=self.back_image, command=self.go_back, bg="white", bd=0)
        back_button.pack(anchor="w", padx=20, pady=10)

        label = tk.Label(self, text="Welcome to the Admin Page", font=("Helvetica", 16), bg="white")
        label.pack(pady=30)

        self.create_scrollable_area()
        self.display_users()

    def go_back(self):
        self.controller.show_frame("LoginPage")

    def create_scrollable_area(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.config(yscrollcommand=scrollbar.set)

        self.users_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.users_frame, anchor="nw")
        self.users_frame.bind(
            "<Configure>",
            lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all"))
        )

        def _on_mouse_wheel(event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        self.canvas.bind("<MouseWheel>", _on_mouse_wheel)

    def display_users(self):
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        try:
            with open("data/jsons/users.json", "r") as file:
                self.users = json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return

        for user in self.users:
            user_info = f"{user['name']} {user['surname']} (Email: {user['email']})"
            user_label = tk.Label(self.users_frame, text=user_info, font=("Helvetica", 12), bg="white")
            user_label.pack(anchor="w", padx=20, pady=5)

            delete_button = tk.Button(self.users_frame, text="Delete", command=lambda user_id=user['user_id']: self.delete_user(user_id))
            delete_button.pack(anchor="e", padx=20, pady=5)

    def delete_user(self, user_id):
        self.users = [user for user in self.users if user['user_id'] != user_id]

        try:
            with open("data/jsons/users.json", "w") as file:
                json.dump(self.users, file, indent=4)
            messagebox.showinfo("Success", "User deleted successfully!")
            self.display_users()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")
