import tkinter as tk
from pages.login_page import LoginPage
from pages.admin_page import AdminPage
from pages.projects_page import ProjectsPage
from pages.profile_page import ProfilePage
from pages.register_page import RegisterPage
from pages.tasks_page import TasksPage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager System")
        self.geometry("1100x600")

        self.resizable(False, False)

        self.frames = {}
        for Page in (LoginPage, AdminPage, ProjectsPage, ProfilePage, RegisterPage, TasksPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.lower()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_frame("LoginPage")

    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]
        if hasattr(frame, "set_arguments"):
            frame.set_arguments(**kwargs)
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
