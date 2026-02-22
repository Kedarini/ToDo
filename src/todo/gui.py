from edit_task import EditWindow
import customtkinter as ctk
import json


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("TODO APP")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.resizable(False, False)

        self.normal_font = ctk.CTkFont(family="Arial", size=12)
        self.hover_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self.theme = "Dark"
        self.tasks = []
        self.task_rows = []

        ctk.set_appearance_mode(self.theme)

        self.load_tasks()

        # ====================
        #     Theme Button
        # ====================

        self.theme_button = ctk.CTkButton(
            self,
            width=20,
            height=20,
            text=self.theme,
            command=lambda: self.toggle_theme(),
        )

        self.theme_button.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        # ====================
        #      NEW TASK
        # ====================

        self.add_button = ctk.CTkButton(
            self, width=25, height=25, text="+", command=lambda: self.add_task()
        )

        self.add_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=12,
            sticky="nw",
        )

        self.task_entry = ctk.CTkEntry(self, placeholder_text="New Task")

        self.task_entry.grid(
            row=0,
            column=0,
            padx=50,
            pady=10,
            sticky="nw",
        )

        # ====================
        #       TASKS
        # ====================

        self.tasks_frame = ctk.CTkFrame(self, width=1280, height=600)

        self.tasks_frame.grid(
            row=1,
            columnspan=2,
            padx=25,
            pady=(0, 25),
            sticky="nsew",
        )

        self.refresh_tasks()
        self.toplevel_window = None

    def toggle_theme(self):
        self.theme = "Light" if self.theme == "Dark" else "Dark"
        ctk.set_appearance_mode("Light" if self.theme == "Light" else "Dark")
        self.theme_button.configure(text=self.theme)

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.tasks = data
                else:
                    self.tasks = []
                    print(
                        "Warning: tasks.json had wrong format, starting with empty list"
                    )
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return

        new_task = {
            "text": text,
            "note": "",
            "date": None,
            "hour": "",
            "done": False,
        }

        self.tasks.append(new_task)
        self.save_tasks()
        self.task_entry.delete(0, "end")
        self.refresh_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()
            self.refresh_tasks()

    def toggle_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.save_tasks()

    def open_toplevel(self, index):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            task = self.tasks[index]
            self.toplevel_window = EditWindow(self, task_index=index, task_data=task)
        else:
            self.toplevel_window.task_index = index
            self.toplevel_window.task_data = self.tasks[index]
            self.toplevel_window.title("Description")
            self.toplevel_window.focus()

    def save_and_close_toplevel(self):
        if self.toplevel_window and self.toplevel_window.winfo_exists():
            self.toplevel_window.destroy()
            self.toplevel_window = None

    # In GUI class

    def edit_task(self, index, **updates):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.update(updates)

            self.save_tasks()
            self.refresh_tasks()

    def refresh_tasks(self):
        for row in self.task_rows:
            row.destroy()
        self.task_rows.clear()

        for idx, task in enumerate(self.tasks):
            row = ctk.CTkFrame(self.tasks_frame)
            row.pack(fill="x", pady=5, padx=5)

            isDone = ctk.BooleanVar(value=task["done"])

            checkbox = ctk.CTkCheckBox(
                row,
                height=20,
                width=20,
                checkbox_width=20,
                checkbox_height=20,
                variable=isDone,
                text="",
                command=lambda task_idx=idx: self.toggle_done(task_idx),
            )
            checkbox.pack(
                side="left",
                padx=(6, 0),
            )

            text_button = ctk.CTkButton(
                row,
                text=(f"{idx + 1}. " + task["text"]),
                width=1000,
                hover=False,
                fg_color="transparent",
                anchor="w",
                cursor="hand2",
                command=lambda task_idx=idx: self.open_toplevel(task_idx),
            )
            text_button.pack(side="left", anchor="nw", padx=(0, 5), pady=5)

            remove_button = ctk.CTkButton(
                row,
                width=20,
                height=20,
                corner_radius=6,
                text="✕",
                fg_color="red",
                command=lambda task_idx=idx: self.remove_task(task_idx),
            )
            remove_button.pack(side="right", padx=5, pady=5)

            self.task_rows.append(row)
