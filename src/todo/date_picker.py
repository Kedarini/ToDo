import customtkinter as ctk
from datetime import datetime as dt, date


class Calendar(ctk.CTkToplevel):
    def __init__(self, parent=None, initial_date=None):
        super().__init__(parent)
        self.parent = parent
        self.geometry("340x380")
        self.title("Select Date")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")  # you can remove if you want system mode

        if initial_date is None:
            initial_date = dt.today().date()

        self.today = dt.today().date()
        self.selected_date = initial_date

        self.selected_year = self.selected_date.year
        self.selected_month = self.selected_date.month
        self.selected_day = self.selected_date.day

        # ── Header ───────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 6))

        ctk.CTkButton(header, text="←", width=60, command=self.prev_month).pack(side="left", padx=(0, 4))

        self.btn_month_year = ctk.CTkButton(
            header,
            text=self.selected_date.strftime("%B %Y"),
            command=self.toggle_year_selection
        )
        self.btn_month_year.pack(side="left", fill="x", expand=True, padx=6)

        ctk.CTkButton(header, text="→", width=60, command=self.next_month).pack(side="right", padx=(4, 0))

        # ── Content area ─────────────────────────────────
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=12, pady=6)

        # Year scrollable list (hidden by default)
        self.year_frame = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        for y in range(self.today.year - 12, self.today.year + 15):
            ctk.CTkButton(
                self.year_frame,
                text=str(y),
                command=lambda val=y: self.set_year(val)
            ).pack(pady=3, padx=20, fill="x")

        # Calendar grid
        self.cal_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.cal_frame.pack(fill="both", expand=True)

        self.build_calendar()

    def build_calendar(self):
        for w in self.cal_frame.winfo_children():
            w.destroy()

        self.btn_month_year.configure(text=self.selected_date.strftime("%B %Y"))

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, wd in enumerate(weekdays):
            ctk.CTkLabel(
                self.cal_frame, text=wd, width=38, anchor="center", text_color="gray"
            ).grid(row=0, column=i, padx=2, pady=(0, 6))

        first = date(self.selected_year, self.selected_month, 1)
        start_col = first.weekday()  # 0 = Monday

        row, col = 1, start_col

        for d in range(1, 32):
            try:
                day_date = date(self.selected_year, self.selected_month, d)
            except ValueError:
                break

            is_today = day_date == self.today
            is_selected = day_date == self.selected_date

            fg = "#2ecc71" if is_selected else \
                "#3a5f8f" if is_today else "#2b2b2b"
            hover = "#27ae60" if is_selected else \
                "#4a7ab0" if is_today else "#3a3a3a"
            txt_color = "black" if is_selected else "white"

            btn = ctk.CTkButton(
                self.cal_frame,
                text=str(d),
                width=38, height=38,
                fg_color=fg, hover_color=hover,
                text_color=txt_color,
                command=lambda val=day_date: self.select_date(val)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)

            col += 1
            if col == 7:
                col = 0
                row += 1

    def prev_month(self):
        m = self.selected_month - 1
        y = self.selected_year
        if m == 0:
            m = 12
            y -= 1
        self.selected_date = date(y, m, min(self.selected_day, 28))
        self.build_calendar()

    def next_month(self):
        m = self.selected_month + 1
        y = self.selected_year
        if m == 13:
            m = 1
            y += 1
        self.selected_date = date(y, m, min(self.selected_day, 28))
        self.build_calendar()

    def toggle_year_selection(self):
        if self.year_frame.winfo_ismapped():
            self.year_frame.pack_forget()
            self.cal_frame.pack(fill="both", expand=True)
        else:
            self.cal_frame.pack_forget()
            self.year_frame.pack(fill="both", expand=True)

    def set_year(self, year):
        self.selected_year = year
        self.selected_date = date(year, self.selected_month, min(self.selected_day, 28))
        self.toggle_year_selection()
        self.build_calendar()

    def select_date(self, selected_date):
        self.selected_date = selected_date
        self.build_calendar()
        self.destroy()  # close after selection

    def get_selected_date(self):
        return self.selected_date