import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import json

class TasksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.user_id = None
        self.project_id = None
        self.project_name = None
        self.task_data = {}

        self.header_label = tk.Frame(self, bg="white", height=50)
        self.header_label.pack(fill=tk.X, side=tk.TOP)

        self.back_image = Image.open("data/images/back_sign.png")
        self.back_image = self.back_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.back_image = ImageTk.PhotoImage(self.back_image)
        back_button = tk.Button(self.header_label, image=self.back_image, command=self.go_back, bg="white", bd=0)
        back_button.place(x=10, y=10)

        self.plus_image = Image.open("data/images/plus_sign.png")
        self.plus_image = self.plus_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.plus_image = ImageTk.PhotoImage(self.plus_image)
        profile_button = tk.Button(self.header_label, image=self.plus_image, command=self.add_task, bg="white", bd=0)
        profile_button.place(x=1050, y=10)

        self.title_label = tk.Label(
            self.header_label,
            text="Task Board of {project_name}",
            bg="white",
            font=("Arial", 16, "bold"),
        )
        self.title_label.pack(side=tk.TOP, pady=10)
        self.header_label.pack_propagate(False)

        self.main_frame = tk.Frame(self, bg="white", width=1100, height=550)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="white", width=1100, height=550)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        section_width = 1100 // 3

        self.section_a = tk.Frame(self.scrollable_frame, bg="#f0f0f0", width=section_width - 1, height=550)
        self.section_b = tk.Frame(self.scrollable_frame, bg="#e6e6e6", width=section_width - 2, height=550)
        self.section_c = tk.Frame(self.scrollable_frame, bg="#d9d9d9", width=section_width - 1, height=550)

        self.section_a.grid(row=0, column=0, sticky="nsew")
        self.section_b.grid(row=0, column=2, sticky="nsew")
        self.section_c.grid(row=0, column=4, sticky="nsew")

        divider_a = tk.Frame(self.scrollable_frame, bg="black", width=2, height=550)
        divider_b = tk.Frame(self.scrollable_frame, bg="black", width=2, height=550)

        divider_a.grid(row=0, column=1, sticky="ns")
        divider_b.grid(row=0, column=3, sticky="ns")

        tk.Label(self.section_a, text="Not started", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.section_b, text="In progress", bg="#e6e6e6", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.section_c, text="Done", bg="#d9d9d9", font=("Arial", 14, "bold")).pack(pady=10)

        self.scrollable_frame.columnconfigure(0, weight=1, minsize=section_width - 1)
        self.scrollable_frame.columnconfigure(1, weight=0)
        self.scrollable_frame.columnconfigure(2, weight=1, minsize=section_width - 2)
        self.scrollable_frame.columnconfigure(3, weight=0)
        self.scrollable_frame.columnconfigure(4, weight=1, minsize=section_width - 1)

        self.load_tasks()

    def load_tasks(self):
        try:
            with open("data/jsons/users.json", "r") as file:
                data = json.load(file)

            for user in data:
                if user["user_id"] == self.user_id:
                    for project in user["projects"]:
                        if project["project_id"] == self.project_id:
                            for task in project["tasks"]:
                                task_name = task.get("name", "Unnamed Task")
                                task_description = task.get("description", "No description available")
                                task_priority = task.get("priority", "Unknown priority")
                                task_type = task.get("_type", "Unknown type")
                                task_status = task.get("status", "unknown")

                                dynamic_field = ""
                                if task_type == "DevTask":
                                    dynamic_field = f"Language: {task.get('language', 'N/A')}"
                                elif task_type == "QATask":
                                    dynamic_field = f"Test Type: {task.get('test_type', 'N/A')}"
                                elif task_type == "DocTask":
                                    dynamic_field = f"Document: {task.get('document', 'N/A')}"

                                task_status = task_status.lower()

                                if task_status == "not started":
                                    parent_section = self.section_a
                                elif task_status == "in progress":
                                    parent_section = self.section_b
                                elif task_status == "done":
                                    parent_section = self.section_c
                                else:
                                    continue

                                task_frame = tk.Frame(parent_section, bg="#ffffff", relief="solid", bd=1)
                                task_frame.pack(pady=5, fill=tk.X)

                                task_label_text = f"{task_name}\nPriority: {task_priority}\nType: {task_type}\nDescription: {task_description}\n{dynamic_field}"
                                task_label = tk.Label(
                                    task_frame,
                                    text=task_label_text,
                                    bg="#ffffff",
                                    font=("Arial", 12),
                                    anchor="w"
                                )
                                task_label.pack(side=tk.LEFT, padx=5, pady=5)

                                delete_button = tk.Button(
                                    task_frame,
                                    text="Delete",
                                    command=lambda task=task: self.delete_task(task),
                                    font=("Arial", 10)
                                )
                                delete_button.pack(side=tk.RIGHT, padx=5)
                                task_label.bind("<Button-1>", lambda e, task=task: self.open_task_popup(task))
                            return
        except FileNotFoundError:
            print("JSON file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    import json

    def delete_task(self, task):
        try:
            with open("data/jsons/users.json", "r") as file:
                data = json.load(file)

            for user in data:
                if user["user_id"] == self.user_id:
                    for project in user["projects"]:
                        if project["project_id"] == self.project_id:
                            project["tasks"] = [t for t in project["tasks"] if t["task_id"] != task["task_id"]]

                            with open("data/jsons/users.json", "w") as file:
                                json.dump(data, file, indent=4)

                            print(f"Task '{task['name']}' deleted successfully.")

                            self.clear_tasks()
                            self.load_tasks()
                            return

            print(f"Task with ID {task['task_id']} not found.")

        except FileNotFoundError:
            print("JSON file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def open_task_popup(self, task):
        def on_task_saved():
            self.clear_tasks()
            self.load_tasks()
        TaskPopup(self, self.user_id, self.project_id, task_data=task, on_save_callback=on_task_saved)


    def set_arguments(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.project_id = kwargs.get("project_id")
        self.name = kwargs.get("name")
        self.title_label.config(text=f"Task Board of {self.name}")
        self.load_tasks()

    def go_back(self):
        self.clear_tasks()
        projects_page = self.controller.frames["ProjectsPage"]
        projects_page.user_id = self.user_id
        projects_page.display_projects()

        self.controller.show_frame("ProjectsPage", user_id=self.user_id)

    def clear_tasks(self):
        for section in [self.section_a, self.section_b, self.section_c]:
            for widget in section.winfo_children():
                if isinstance(widget, tk.Label) and ("Not started" in widget.cget("text") or "In progress" in widget.cget("text")
                        or "Done" in widget.cget("text")):
                    continue
                widget.destroy()

    def add_task(self):
        def on_task_saved():
            self.clear_tasks()
            self.load_tasks()
        TaskPopup(self, user_id=self.user_id, project_id=self.project_id, on_save_callback=on_task_saved)


class TaskPopup(tk.Toplevel):
    def __init__(self, parent, user_id, project_id, task_data=None, on_save_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.project_id = project_id
        self.on_save_callback = on_save_callback
        self.task_data = task_data
        self.title("Edit Task" if task_data else "Add New Task")

        self.create_task_form()

    def create_task_form(self):
        # Task Name Entry
        self.name_label = tk.Label(self, text="Task Name")
        self.name_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=20, pady=5)
        if self.task_data:
            self.name_entry.insert(0, self.task_data.get("name", ""))

        self.description_label = tk.Label(self, text="Description")
        self.description_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=1, column=1, padx=20, pady=5)
        if self.task_data:
            self.description_entry.insert(0, self.task_data.get("description", ""))

        self.priority_label = tk.Label(self, text="Priority")
        self.priority_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.priority_combobox = ttk.Combobox(self, values=["LOW", "MEDIUM", "HIGH", "CRITICAL"], state="readonly")
        self.priority_combobox.grid(row=2, column=1, padx=20, pady=5)
        if self.task_data:
            self.priority_combobox.set(self.task_data.get("priority", ""))

        self.status_label = tk.Label(self, text="Status")
        self.status_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.status_combobox = ttk.Combobox(self, values=["Not started", "In progress", "Done"], state="readonly")
        self.status_combobox.grid(row=3, column=1, padx=20, pady=5)
        if self.task_data:
            self.status_combobox.set(self.task_data.get("status", ""))

        self.type_label = tk.Label(self, text="Type")
        self.type_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.type_combobox = ttk.Combobox(self, values=["DevTask", "QATask", "DocTask"], state="readonly")
        self.type_combobox.grid(row=4, column=1, padx=20, pady=5)
        if self.task_data:
            self.type_combobox.set(self.task_data.get("_type", ""))

        self.type_combobox.bind("<<ComboboxSelected>>", self.update_dynamic_field)

        self.dynamic_label = tk.Label(self, text="")
        self.dynamic_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        self.dynamic_entry = tk.Entry(self)
        self.dynamic_entry.grid(row=5, column=1, padx=20, pady=5)
        if self.task_data:
            dynamic_value = self.task_data.get("language") or self.task_data.get("test_type") or self.task_data.get(
                "document")
            self.dynamic_entry.insert(0, dynamic_value)

        self.save_button = tk.Button(self, text="Save", command=self.save_task)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=20)

        if self.task_data:
            self.update_dynamic_field(None)

    def update_dynamic_field(self, event):
        task_type = self.type_combobox.get()

        if task_type == "DevTask":
            self.dynamic_label.config(text="Language")
            self.dynamic_entry.grid(row=5, column=1, padx=20, pady=5)
        elif task_type == "QATask":
            self.dynamic_label.config(text="Test Type")
            self.dynamic_entry.grid(row=5, column=1, padx=20, pady=5)
        elif task_type == "DocTask":
            self.dynamic_label.config(text="Document")
            self.dynamic_entry.grid(row=5, column=1, padx=20, pady=5)
        else:
            self.dynamic_label.config(text="")
            self.dynamic_entry.grid_forget()

    def save_task(self):
        task_name = self.name_entry.get()
        task_description = self.description_entry.get()
        task_priority = self.priority_combobox.get()
        task_status = self.status_combobox.get()
        task_type = self.type_combobox.get()
        dynamic_value = self.dynamic_entry.get()

        if not task_name or not task_description or not task_priority or not task_status or not task_type:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        if self.task_data:
            task_id = self.task_data.get("task_id")
        else:
            task_id = self.generate_unique_task_id()

        task_data = {
            "task_id": task_id,
            "name": task_name,
            "description": task_description,
            "priority": task_priority,
            "status": task_status,
            "_type": task_type
        }

        if task_type == "DevTask":
            task_data["language"] = dynamic_value
        elif task_type == "QATask":
            task_data["test_type"] = dynamic_value
        elif task_type == "DocTask":
            task_data["document"] = dynamic_value

        try:
            with open("data/jsons/users.json", "r") as file:
                users = json.load(file)

            for user in users:
                if user["user_id"] == self.user_id:
                    for project in user["projects"]:
                        if project["project_id"] == self.project_id:
                            if self.task_data:
                                for index, task in enumerate(project["tasks"]):
                                    if task["task_id"] == self.task_data["task_id"]:
                                        project["tasks"][index] = task_data
                                        break
                            else:
                                project["tasks"].append(task_data)

            with open("data/jsons/users.json", "w") as file:
                json.dump(users, file, indent=4)

            messagebox.showinfo("Success", "Task saved successfully.")

            if self.on_save_callback:
                self.on_save_callback()

            self.destroy()

        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to parse user data.")

    def generate_unique_task_id(self):
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

        task_ids = []
        for project in user["projects"]:
            task_ids.extend([task["task_id"] for task in project["tasks"]])

        if not task_ids:
            return 1

        return max(task_ids) + 1

