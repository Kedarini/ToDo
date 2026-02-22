import customtkinter as ctk
from datetime import datetime as dt
from date_picker import Calendar


class EditWindow(ctk.CTkToplevel):
    def __init__(self, parent, task_index, task_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.task_index = task_index
        self.task_data = task_data
        self.task_date = None
        self.new_date = None  # ← will store the selected date object

        self.geometry("300x300")
        self.title("Edit/View Task")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.task_label = ctk.CTkLabel(
            self, text=("Task: " + task_data["text"]), font=("Arial", 20), width=300
        )
        self.task_label.grid(row=0, pady=(10, 0), sticky="nw")

        self.name_label = ctk.CTkLabel(self, text="Name", wraplength=700)
        self.name_label.grid(row=0, column=0, padx=15, pady=(30, 0), sticky="nw")

        self.name_entry = ctk.CTkEntry(
            self,
            text_color="white",
            placeholder_text_color="grey",
            placeholder_text="Edit task name here",
            height=20,
            width=280,
        )
        self.name_entry.insert(0, task_data.get("text", ""))
        self.name_entry.grid(row=0, padx=10, pady=(55, 0), sticky="nw")

        self.note_label = ctk.CTkLabel(self, text="Note", wraplength=700)
        self.note_label.grid(row=0, padx=15, pady=(90, 0), sticky="nw")

        self.note_entry = ctk.CTkEntry(
            self,
            text_color="white",
            placeholder_text_color="grey",
            placeholder_text="Additional notes here",
            width=280,
        )
        if task_data.get("note") != "":
            self.note_entry.insert(0, task_data.get("note", ""))
        self.note_entry.grid(row=0, padx=10, pady=(115, 0), sticky="nw")

        self.date_label = ctk.CTkLabel(self, text="Date", wraplength=700)
        self.date_label.grid(row=0, padx=15, pady=(155, 0), sticky="nw")

        # Try to show existing date if it exists in task_data
        initial_date_text = dt.now().date().strftime("%d/%m/%Y")
        if "date" in task_data:
            if isinstance(task_data["date"], str):
                try:
                    d = dt.strptime(task_data["date"], "%Y-%m-%d").date()
                    initial_date_text = d.strftime("%d/%m/%Y")
                    self.new_date = d
                except:
                    pass
            elif hasattr(task_data["date"], "strftime"):
                initial_date_text = task_data["date"].strftime("%d/%m/%Y")
                self.new_date = task_data["date"]

        self.date_button = ctk.CTkButton(
            self,
            text_color=["gray52", "gray62"],
            border_color=["#979DA2", "#565B5E"],
            fg_color=["#F9F9FA", "#343638"],
            border_width=2,
            cursor="hand2",
            hover=False,
            text=initial_date_text,
            anchor="w",
            width=100,
            command=self.get_new_date,
        )
        self.date_button.grid(row=0, padx=10, pady=(180, 0), sticky="nw")

        self.hour_label = ctk.CTkLabel(self, text="Hour", wraplength=700)
        self.hour_label.grid(row=0, pady=(155, 0), padx=120, sticky="nw")

        self.hour_button = ctk.CTkButton(
            self,
            text_color=["gray52", "gray62"],
            border_color=["#979DA2", "#565B5E"],
            fg_color=["#F9F9FA", "#343638"],
            border_width=2,
            cursor="hand2",
            hover=False,
            text="9:35    ⌚",
            anchor="w",
            width=100,
        )
        self.hour_button.grid(row=0, padx=115, pady=(180, 0), sticky="nw")

        self.accept_button = ctk.CTkButton(
            self, width=50, height=20, text="Done", command=self.save_and_close
        )
        self.accept_button.grid(
            row=1,
            pady=10,
            padx=40,
            sticky="se",
        )

        self.remove_button = ctk.CTkButton(
            self,
            width=50,
            height=20,
            fg_color="red",
            text="Remove",
            command=lambda: [self.parent.remove_task(task_index), self.destroy()],
        )
        self.remove_button.grid(row=1, padx=(0, 100), pady=(0, 10), sticky="se")

        # Load initial date for button
        initial_date_text = dt.now().date().strftime("%d/%m/%Y")
        self.new_date = None

        if "date" in self.task_data:
            raw = self.task_data["date"]
            if isinstance(raw, str):
                try:
                    d = dt.fromisoformat(raw).date()
                    initial_date_text = d.strftime("%d/%m/%Y")
                    self.new_date = d
                except ValueError:
                    pass
            elif hasattr(raw, "strftime") and callable(
                raw.strftime
            ):  # duck-type date/datetime
                self.new_date = raw.date() if hasattr(raw, "date") else raw
                initial_date_text = self.new_date.strftime("%d/%m/%Y")

    def get_new_date(self):
        cal = Calendar(self)  # ← parent = self so it appears on top
        self.wait_window(cal)  # ← wait until user closes it
        selected = cal.get_selected_date()  # ← assuming your Calendar has this method
        if selected:
            self.new_date = selected
            self.date_button.configure(text=selected.strftime("%d/%m/%Y"))

    def save_and_close(self):
        new_text = self.name_entry.get().strip()
        if not new_text:
            return

        update_data = {
            "text": new_text,
            "note": self.note_entry.get().strip(),
        }

        if self.new_date is not None:
            update_data["date"] = self.new_date.isoformat()  # ← save as string

        # Later when you add hour:
        # if self.new_hour is not None:
        #     update_data["hour"] = self.new_hour

        self.parent.edit_task(index=self.task_index, **update_data)
        self.destroy()
