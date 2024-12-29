import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import json
from shutil import copyfile
from PIL import Image, ImageTk

class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.user_id = None
        self.user_data = None

    def set_arguments(self, **kwargs):
        self.user_id = next(iter(kwargs.values()))
        print(self.user_id)
        self.user_data = self.load_user_data()
        self.create_widgets()

    def load_user_data(self):
        try:
            with open("data/jsons/users.json", "r") as file:
                users = json.load(file)
                for user in users:
                    if user["user_id"] == self.user_id:
                        return user
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
            return None
        return {}

    def create_widgets(self):
        self.back_image = Image.open("data/images/back_sign.png")
        self.back_image = self.back_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.back_image = ImageTk.PhotoImage(self.back_image)
        back_button = tk.Button(self, image=self.back_image, command=self.go_back, bg="white", bd=0)
        back_button.place(x=10, y=10)

        logout_button = tk.Button(self, text="Logout", command=self.logout)
        logout_button.place(x=1050, y=10)

        welcome_text = f"Welcome, {self.user_data['name']} {self.user_data['surname']}"
        welcome_label = tk.Label(self, text=welcome_text, bg="white", font=("Arial", 14, "bold"))
        welcome_label.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="n")

        profile_image_path = self.user_data.get('profile_image_path', None)
        if not profile_image_path or not os.path.exists(profile_image_path):
            profile_image_path = "data/profile_images/default.png"
        try:
            pil_image = Image.open(profile_image_path)
            pil_image = pil_image.resize((150, 150))
            self.image = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = None

        if self.image:
            image_label = tk.Label(self, image=self.image)
            image_label.grid(row=0, column=0, columnspan=2, pady=10)
        else:
            print("No image to display")

        change_profile_image_button = tk.Button(self, text="Change Profile Image", command=self.change_profile_image)
        change_profile_image_button.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="n")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        name_label = tk.Label(self, text=f"Name: {self.user_data['name']}", bg="white")
        name_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="n")

        surname_label = tk.Label(self, text=f"Surname: {self.user_data['surname']}", bg="white")
        surname_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="n")

        email_label = tk.Label(self, text=f"Email: {self.user_data['email']}", bg="white")
        email_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="n")

        edit_button = tk.Button(self, text="Edit Profile", command=self.edit_profile)
        edit_button.grid(row=7, column=0, columnspan=2, padx=20, pady=20)

    def change_profile_image(self):
        file_path = filedialog.askopenfilename(title="Select Image",
                                               filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.gif")])

        if file_path:
            image_name = self.generate_image_names()

            profile_images_dir = "data/profile_images"
            if not os.path.exists(profile_images_dir):
                os.makedirs(profile_images_dir)
            new_image_path = os.path.join(profile_images_dir, image_name)
            copyfile(file_path, new_image_path)

            self.user_data["profile_image_path"] = new_image_path
            self.update_user_json()

            print(f"Profile image updated: {new_image_path}")
            self.create_widgets()

    def generate_image_names(self):
        user = self.user_data
        return f"{user['user_id']}_{user['name']}_{user['surname']}_{user['email'].split('@')[0]}.png"

    def update_user_json(self):
        json_file_path = "data/jsons/users.json"

        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as file:
                users_data = json.load(file)
        else:
            users_data = []

        for user in users_data:
            if user["user_id"] == self.user_data["user_id"]:
                user["profile_image_path"] = self.user_data["profile_image_path"]
                break
        else:
            users_data.append(self.user_data)

        with open(json_file_path, "w") as file:
            json.dump(users_data, file, indent=4)

    def go_back(self):
        projects_page = self.controller.frames["ProjectsPage"]
        projects_page.user_id = self.user_id
        projects_page.display_projects()

        self.controller.show_frame("ProjectsPage", user_id=self.user_id)

    def logout(self):
        messagebox.showinfo("Logout", "You have logged out successfully.")
        self.controller.show_frame("LoginPage")

    def edit_profile(self):
        VerifyPopup(self)

class VerifyPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Verify Identity")

        email_label = tk.Label(self, text="Email:")
        email_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=0, column=1, padx=20, pady=10)

        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=20, pady=10)

        verify_button = tk.Button(self, text="Verify", command=self.verify_credentials)
        verify_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.geometry("300x200")

    def verify_credentials(self):
        entered_email = self.email_entry.get()
        entered_password = self.password_entry.get()

        if (entered_email == self.parent.user_data['email'] and
                entered_password == self.parent.user_data['password']):
            self.destroy()
            EditPopup(self.parent)
        else:
            messagebox.showerror("Error", "Incorrect email or password.")
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


class EditPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Edit Profile")

        self.name_entry = self.create_edit_field("Name", parent.user_data['name'], 0)
        self.surname_entry = self.create_edit_field("Surname", parent.user_data['surname'], 1)
        self.email_entry = self.create_edit_field("Email", parent.user_data['email'], 2)
        self.password_entry = self.create_edit_field("Password", parent.user_data['password'], 3)

        save_button = tk.Button(self, text="Save", command=self.save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.geometry("300x300")

    def create_edit_field(self, label_text, initial_value, row):
        label = tk.Label(self, text=label_text)
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = tk.Entry(self)
        entry.insert(0, initial_value)
        entry.grid(row=row, column=1, padx=20, pady=10)
        return entry

    def save_changes(self):
        new_name = self.name_entry.get()
        new_surname = self.surname_entry.get()
        new_email = self.email_entry.get()
        new_password = self.password_entry.get()

        self.parent.user_data['name'] = new_name
        self.parent.user_data['surname'] = new_surname
        self.parent.user_data['email'] = new_email
        self.parent.user_data['password'] = new_password

        try:
            with open("data/jsons/users.json", "r+") as file:
                users = json.load(file)
                for user in users:
                    if user["user_id"] == self.parent.user_id:
                        user["name"] = new_name
                        user["surname"] = new_surname
                        user["email"] = new_email
                        user["password"] = new_password
                file.seek(0)
                json.dump(users, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
            return

        messagebox.showinfo("Success", "Profile updated successfully.")
        self.parent.create_widgets()
        self.destroy()

