import customtkinter as ctk
from datetime import datetime as dt
import gui

class Calendar(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("340x350")
        self.title("Select Date")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self.today = dt.now()                       # cache today's date
        self.selected_year = self.today.year
        self.selected_month = self.today.month
        self.selected_day = self.today.day          # ← start with today selected by default

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))

        self.btn_prev = ctk.CTkButton(
            self.header, text="← Back", width=90, height=34, command=self.prev_month
        )
        self.btn_prev.grid(row=0, column=0, padx=(0, 6), sticky="w")

        self.btn_year = ctk.CTkButton(
            self.header,
            text=str(self.selected_year),
            width=140,
            height=34,
            fg_color="#1f538d",
            hover_color="#2a6dc5",
            command=self.toggle_year_selection,
        )
        self.btn_year.grid(row=0, column=1, padx=6)

        self.btn_next = ctk.CTkButton(
            self.header, text="Next →", width=90, height=34, command=self.next_month
        )
        self.btn_next.grid(row=0, column=2, padx=(6, 0), sticky="e")

        self.header.columnconfigure(1, weight=1)

        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Year selection frame (hidden initially)
        self.year_frame = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        for y in range(self.today.year - 10, self.today.year + 21):
            btn = ctk.CTkButton(
                self.year_frame,
                text=str(y),
                height=38,
                fg_color="#2b2b2b",
                hover_color="#3a3a3a",
                command=lambda val=y: self.set_year(val),
            )
            btn.pack(pady=5, padx=20, fill="x")

        # Calendar grid frame
        self.calendar_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.calendar_frame.pack(fill="both", expand=True)

        self.build_month_view()

    def build_month_view(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month_name = dt(self.selected_year, self.selected_month, 1).strftime("%B")
        self.btn_year.configure(text=f"{month_name} {self.selected_year}")

        # Weekday headers
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekdays):
            lbl = ctk.CTkLabel(
                self.calendar_frame,
                text=day,
                width=41,
                height=32,
                font=("Arial", 13),
                text_color="gray",
            )
            lbl.grid(row=0, column=i, padx=2, pady=(0, 8))

        # Days grid
        first_day = dt(self.selected_year, self.selected_month, 1)
        start_col = first_day.weekday()  # 0 = Monday

        is_current_month = (
            self.selected_year == self.today.year and self.selected_month == self.today.month
        )

        row = 1
        col = start_col

        for day in range(1, 32):
            try:
                date = dt(self.selected_year, self.selected_month, day)
            except ValueError:
                break

            is_today = is_current_month and day == self.today.day
            is_selected = day == self.selected_day and self.selected_year == date.year and self.selected_month == date.month

            # Choose appearance based on state
            if is_selected:
                fg_color = "#2ecc71"          # green for selected
                hover_color = "#27ae60"
                text_color = "#ffffff"
                border_width = 3
                border_color = "#1abc9c"
            elif is_today:
                fg_color = "#4a6a8a"          # your original today color
                hover_color = "#5a7a9a"
                text_color = "#e0f0ff"
                border_width = 2
                border_color = "#8ab4f8"
            else:
                fg_color = "#2b2b2b"
                hover_color = "#3a3a3a"
                text_color = "#ffffff"
                border_width = 0
                border_color = None

            btn = ctk.CTkButton(
                self.calendar_frame,
                text=str(day),
                width=35,
                height=35,
                corner_radius=10,
                font=("Arial", 14),
                fg_color=fg_color,
                hover_color=hover_color,
                text_color=text_color,
                border_width=border_width,
                border_color=border_color,
                command=lambda d=day: self.select_day(d),
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

            col += 1
            if col == 7:
                col = 0
                row += 1

    def prev_month(self):
        self.selected_month -= 1
        if self.selected_month == 0:
            self.selected_month = 12
            self.selected_year -= 1
        self.build_month_view()

    def next_month(self):
        self.selected_month += 1
        if self.selected_month == 13:
            self.selected_month = 1
            self.selected_year += 1
        self.build_month_view()

    def toggle_year_selection(self):
        if self.year_frame.winfo_ismapped():
            self.year_frame.pack_forget()
            self.calendar_frame.pack(fill="both", expand=True)
        else:
            self.calendar_frame.pack_forget()
            self.year_frame.pack(fill="both", expand=True)

    def set_year(self, year):
        self.selected_year = year
        self.toggle_year_selection()  # hide year list
        self.build_month_view()

    def select_day(self, day):
        self.selected_day = day
        date_str = f"{self.selected_year}-{self.selected_month:02d}-{day:02d}"
        gui.ToplevelWindow.task_date = date_str
        self.build_month_view()          # ← rebuild → new selected day gets highlighted


if __name__ == "__main__":
    app = Calendar()
    app.mainloop()