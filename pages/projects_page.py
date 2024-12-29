import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import json

class ProjectsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.user_id = None

        self.profile_image = Image.open("data/images/profile_icon.png")
        self.profile_image = self.profile_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.profile_image = ImageTk.PhotoImage(self.profile_image)
        profile_button = tk.Button(self, image=self.profile_image, command=self.go_to_profile_page, bg="white", bd=0)
        profile_button.place(x=20, y=10)

        self.add_project_image = Image.open("data/images/plus_sign.png")
        self.add_project_image = self.add_project_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.add_project_image = ImageTk.PhotoImage(self.add_project_image)

        add_project_button = tk.Button(self, image=self.add_project_image, command=self.add_project, bg="white", bd=0)
        add_project_button.place(x=1050, y=10)

        label = tk.Label(self, text="Here is a list of all projects", font=("Helvetica", 16), bg="white")
        label.pack(pady=30)

        self.create_scrollable_area()
        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

    def create_scrollable_area(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=scrollbar.set)

        def _on_mouse_wheel(event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    def display_projects(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        try:
            with open("data/jsons/users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load user data: {e}")
            return

        user = next((u for u in users if u["user_id"] == self.user_id), None)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        projects = user.get("projects", [])
        if not projects:
            tk.Label(self.inner_frame, text="No projects found.").pack(pady=10)
            return

        for project in projects:
            frame = tk.Frame(self.inner_frame, pady=5, bg="white")
            frame.pack(fill=tk.X, padx=10, pady=5)

            project_name = tk.Label(frame, text=project["name"], fg="blue", cursor="hand2", font=("Arial", 12, "bold"),
                                    bg="white")
            project_name.pack(anchor="w", pady=2)
            project_name.bind("<Button-1>", lambda e, p=project: self.open_project(p["project_id"], p["name"]))

            button_frame = tk.Frame(frame, bg="white")
            button_frame.pack(anchor="e", padx=5)

            edit_button = tk.Button(button_frame, text="Edit", command=lambda p=project: self.edit_project(p))
            edit_button.pack(side="left", padx=5)

            delete_button = tk.Button(button_frame, text="Delete", command=lambda p=project: self.delete_project(p))
            delete_button.pack(side="left", padx=5)

            description = tk.Label(frame, text=f"Description: {project['description']}", font=("Arial", 10), bg="white")
            description.pack(anchor="w", pady=2)

            deadline = tk.Label(frame, text=f"Deadline: {project['deadline']}", font=("Arial", 10), bg="white")
            deadline.pack(anchor="w", pady=2)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def open_project(self, project_id, name):
        tasks_page = self.controller.frames["TasksPage"]
        tasks_page.user_id = self.user_id
        tasks_page.project_id = project_id
        self.controller.show_frame("TasksPage", user_id=self.user_id, project_id=project_id, name = name)

    def edit_project(self, project):
        edit_project_popup = tk.Toplevel(self)
        edit_project_popup.title("Edit Project")
        edit_project_popup.geometry("400x300")
        edit_project_popup.configure(bg="white")

        title_label = tk.Label(edit_project_popup, text="Project Title", bg="white")
        title_label.pack(pady=10)

        title_entry = tk.Entry(edit_project_popup, width=30)
        title_entry.insert(0, project["name"])
        title_entry.pack(pady=5)

        description_label = tk.Label(edit_project_popup, text="Project Description", bg="white")
        description_label.pack(pady=10)

        description_entry = tk.Entry(edit_project_popup, width=30)
        description_entry.insert(0, project["description"])
        description_entry.pack(pady=5)

        deadline_label = tk.Label(edit_project_popup, text="Project Deadline (YYYY-MM-DD)", bg="white")
        deadline_label.pack(pady=10)

        deadline_entry = tk.Entry(edit_project_popup, width=30)
        deadline_entry.insert(0, project["deadline"])
        deadline_entry.pack(pady=5)

        def save_edited_project():
            project_name = title_entry.get().strip()
            project_description = description_entry.get().strip()
            project_deadline = deadline_entry.get().strip()

            if not project_name or not project_description or not project_deadline:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                with open("data/jsons/users.json", "r") as file:
                    users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Failed to load user data: {e}")
                return

            user = next((u for u in users if u["user_id"] == self.user_id), None)
            if not user:
                messagebox.showerror("Error", "User not found.")
                return

            for p in user["projects"]:
                if p["project_id"] == project["project_id"]:
                    p["name"] = project_name
                    p["description"] = project_description
                    p["deadline"] = project_deadline
                    break

            try:
                with open("data/jsons/users.json", "w") as file:
                    json.dump(users, file, indent=4)
            except IOError as e:
                messagebox.showerror("Error", f"Failed to save user data: {e}")
                return

            edit_project_popup.destroy()

            self.display_projects()

        save_button = tk.Button(edit_project_popup, text="Save", command=save_edited_project)
        save_button.pack(pady=20)

        cancel_button = tk.Button(edit_project_popup, text="Cancel", command=edit_project_popup.destroy)
        cancel_button.pack(pady=5)

    def delete_project(self, project):
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete the project '{project['name']}'?")
        if not confirm:
            return

        try:
            with open("data/jsons/users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load user data: {e}")
            return

        user = next((u for u in users if u["user_id"] == self.user_id), None)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        user["projects"] = [p for p in user["projects"] if p["project_id"] != project["project_id"]]

        try:
            with open("data/jsons/users.json", "w") as file:
                json.dump(users, file, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save user data: {e}")
            return

        self.display_projects()

    def add_project(self):
        add_project_popup = tk.Toplevel(self)
        add_project_popup.title("Add New Project")
        add_project_popup.geometry("400x300")
        add_project_popup.configure(bg="white")

        title_label = tk.Label(add_project_popup, text="Project Title", bg="white")
        title_label.pack(pady=10)

        title_entry = tk.Entry(add_project_popup, width=30)
        title_entry.pack(pady=5)

        description_label = tk.Label(add_project_popup, text="Project Description", bg="white")
        description_label.pack(pady=10)

        description_entry = tk.Entry(add_project_popup, width=30)
        description_entry.pack(pady=5)

        deadline_label = tk.Label(add_project_popup, text="Project Deadline (YYYY-MM-DD)", bg="white")
        deadline_label.pack(pady=10)

        deadline_entry = tk.Entry(add_project_popup, width=30)
        deadline_entry.pack(pady=5)

        def save_project():
            project_name = title_entry.get().strip()
            project_description = description_entry.get().strip()
            project_deadline = deadline_entry.get().strip()

            if not project_name or not project_description or not project_deadline:
                messagebox.showerror("Error", "All fields are required!")
                return

            project_id = self.generate_unique_project_id()

            try:
                with open("data/jsons/users.json", "r") as file:
                    users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Failed to load user data: {e}")
                return

            user = next((u for u in users if u["user_id"] == self.user_id), None)
            if not user:
                messagebox.showerror("Error", "User not found.")
                return

            new_project = {
                "project_id": project_id,
                "name": project_name,
                "description": project_description,
                "tasks": [],
                "deadline": project_deadline
            }

            user["projects"].append(new_project)

            try:
                with open("data/jsons/users.json", "w") as file:
                    json.dump(users, file, indent=4)
            except IOError as e:
                messagebox.showerror("Error", f"Failed to save user data: {e}")
                return

            add_project_popup.destroy()

            self.display_projects()

        save_button = tk.Button(add_project_popup, text="Save", command=save_project)
        save_button.pack(pady=20)

        cancel_button = tk.Button(add_project_popup, text="Cancel", command=add_project_popup.destroy)
        cancel_button.pack(pady=5)

    def generate_unique_project_id(self):
        try:
            with open("data/jsons/users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load user data: {e}")
            return None

        user = next((u for u in users if u["user_id"] == self.user_id), None)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return None

        project_ids = [project["project_id"] for project in user["projects"]]

        if not project_ids:
            return 1

        return max(project_ids) + 1

    def set_arguments(self, **kwargs):
        self.user_id = next(iter(kwargs.values()))
        print(self.user_id)

    def go_to_profile_page(self):
        profile_page = self.controller.frames["ProfilePage"]
        self.controller.show_frame("ProfilePage", user_id = self.user_id)