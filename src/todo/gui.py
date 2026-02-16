import customtkinter as ctk
import json

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("TODO APP")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.theme = "Dark"
        self.tasks = []
        self.task_rows = []

        self.load_tasks()

        # ====================
        #     Theme Button
        # ====================

        self.theme_button = ctk.CTkButton(
            self,
            width=20,
            height=20,
            text="SwitchTheme",
            command=lambda: self.toggle_theme(),
        )

        self.theme_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

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

        self.tasks_frame = ctk.CTkFrame(self, width=1000, height=600)

        self.tasks_frame.grid(
            row=1,
            column=0,
            padx=80,
            pady=10,
            sticky="nw",
        )

        self.refresh_tasks()

    def toggle_theme(self):
        self.theme = "Light" if self.theme == "Dark" else "Dark"
        ctk.set_appearance_mode("Light" if self.theme == "Light" else "Dark")

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

        new_task = {"text": text, "done": False}

        self.tasks.append(new_task)

        self.save_tasks()
        self.task_entry.delete(0, "end")
        self.refresh_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()
            self.refresh_tasks()

    def refresh_tasks(self):
        for row in self.task_rows:
            row.destroy()
        self.task_rows.clear()

        for idx, task in enumerate(self.tasks):
            row = ctk.CTkFrame(self.tasks_frame)
            row.pack(fill="x", pady=6, padx=6, expand=True)

            isDone = ctk.BooleanVar(value=task["done"])

            checkbox = ctk.CTkCheckBox(
                row,
                height=30,
                width=950,
                checkbox_width=20,
                checkbox_height=20,
                text=task["text"],
                variable=isDone,
                # command=lambda t=task: self.toggle_done(t)
            )
            checkbox.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5,
            )

            remove_button = ctk.CTkButton(
                row,
                width=20,
                height=20,
                text="-",
                fg_color="red",
                command=lambda task_idx=idx: self.remove_task(task_idx),
            )
            remove_button.pack(side="right", expand=True)

            self.task_rows.append(row)
