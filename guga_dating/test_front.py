import tkinter as tk
import customtkinter as ctk
from question_engine import get_questions
from advice_engine import generate_advice
from tone_engine import style_output
import traceback
import threading


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DatingAdviceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Love Overflow")
        self.geometry("380x700")
        self.configure(fg_color="#F8FAFC")

        # Color palette
        self.primary_color = "#6366F1"
        self.bg_color      = "#F8FAFC"
        self.card_color    = "#FFFFFF"
        self.text_main     = "#1E293B"
        self.text_sub      = "#64748B"

        # File-1 logic variables
        self.answers          = {}
        self.entries          = {}
        self.question_widgets = []
        self.result_box       = None   # created only after questions load

        # Page frames
        self.home_frame     = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.question_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.profile_frame  = ctk.CTkFrame(self, fg_color=self.bg_color)

        self.home_frame.pack(fill="both", expand=True)

        self.setup_home_ui()
        self.setup_nav_bar()

    # ------------------------------------------------------------------ #
    #  HOME                                                                #
    # ------------------------------------------------------------------ #
    def setup_home_ui(self):
        ctk.CTkLabel(
            self.home_frame, text="Love Overflow",
            font=("Inter", 32, "bold"), text_color=self.primary_color
        ).pack(pady=(40, 5), padx=25, anchor="w")

        ctk.CTkLabel(
            self.home_frame, text="Your AI Wingman.",
            font=("Inter", 16), text_color=self.text_sub
        ).pack(padx=25, anchor="w")

        card = ctk.CTkFrame(
            self.home_frame, corner_radius=24, fg_color=self.card_color,
            border_width=1, border_color="#E2E8F0"
        )
        card.pack(pady=30, padx=20, fill="x")

        ctk.CTkLabel(
            card, text="✨", font=("Helvetica", 60),
            height=160, fg_color="#EEF2FF", corner_radius=20
        ).pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(
            card, text="Ready for clarity?",
            font=("Inter", 22, "bold"), text_color=self.text_main
        ).pack(padx=20, anchor="w")

        ctk.CTkLabel(
            card, text="Analyze your chats and get tactical advice.",
            font=("Inter", 13), text_color=self.text_sub,
            wraplength=280, justify="left"
        ).pack(padx=20, pady=(5, 20), anchor="w")

        self.start_button = ctk.CTkButton(
            card, text="Get Started", height=45, corner_radius=12,
            font=("Inter", 14, "bold"), fg_color=self.primary_color,
            hover_color="#4F46E5", command=self.load_questions
        )
        self.start_button.pack(padx=20, pady=(0, 25), fill="x")

    def setup_nav_bar(self):
        nav_bar = ctk.CTkFrame(
            self, height=70, corner_radius=0,
            fg_color="white", border_width=1, border_color="#E2E8F0"
        )
        nav_bar.pack(side="bottom", fill="x")

        for icon, cmd in [("🏠", self.show_home), ("💬", self.load_questions), ("👤", self.show_profile)]:
            ctk.CTkButton(
                nav_bar, text=icon, width=60, height=45, font=("Inter", 20),
                fg_color="transparent", text_color=self.text_main,
                hover_color="#F1F5F9", command=cmd
            ).pack(side="left", expand=True, pady=10)

    # ------------------------------------------------------------------ #
    #  STEP 1 — selector screen                                            #
    # ------------------------------------------------------------------ #
    def load_questions(self):
        """File-1 load_questions: clear old widgets, show selector screen."""
        for widget in self.question_widgets:
            widget.destroy()
        self.question_widgets.clear()
        self.result_box = None

        self._show_frame(self.question_frame)
        self._build_selector_screen()

    def _build_selector_screen(self):
        """Render issue + tone dropdowns only. Questions come after Continue."""
        for child in self.question_frame.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.question_frame, text="The Situation",
            font=("Inter", 24, "bold"), text_color=self.text_main
        ).pack(pady=(30, 10), padx=25, anchor="w")

        select_card = ctk.CTkFrame(self.question_frame, fg_color="white", corner_radius=15)
        select_card.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(select_card, text="What's happening?", font=("Inter", 13, "bold")).pack(pady=(15, 0), padx=15, anchor="w")
        self.issue_var = ctk.StringVar(value="Texting")
        self.issue_dropdown = ctk.CTkOptionMenu(
            select_card, variable=self.issue_var,
            values=["Texting", "Mixed Signals", "Conflict", "Ex", "Situationship"],
            fg_color="#F1F5F9", text_color=self.text_main,
            button_color="#CBD5E1", button_hover_color="#94A3B8"
        )
        self.issue_dropdown.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(select_card, text="Desired Tone", font=("Inter", 13, "bold")).pack(pady=(10, 0), padx=15, anchor="w")
        self.tone_var = ctk.StringVar(value="honest")
        self.tone_dropdown = ctk.CTkOptionMenu(
            select_card, variable=self.tone_var,
            values=["honest", "brutal", "calm", "slightly_toxic"],
            fg_color="#F1F5F9", text_color=self.text_main,
            button_color="#CBD5E1", button_hover_color="#94A3B8"
        )
        self.tone_dropdown.pack(fill="x", padx=15, pady=(10, 20))

        self.next_btn = ctk.CTkButton(
            self.question_frame, text="Continue →", height=45, corner_radius=12,
            fg_color=self.primary_color, hover_color="#4F46E5",
            command=self._validate_and_fetch
        )
        self.next_btn.pack(pady=(15, 5), padx=20, fill="x")

        # Small status label for loading feedback (no result_box yet)
        self.status_label = ctk.CTkLabel(
            self.question_frame, text="", font=("Inter", 12), text_color=self.text_sub
        )
        self.status_label.pack(pady=(0, 10))

    # ------------------------------------------------------------------ #
    #  STEP 2 — validate + fetch (file-1 logic unchanged)                  #
    # ------------------------------------------------------------------ #
    def _validate_and_fetch(self):
        """File-1 validation + background thread kick-off."""
        if not self.issue_var.get():
            self.status_label.configure(text="Please select an issue first.")
            return
        if not self.tone_var.get():
            self.status_label.configure(text="Please select a tone first.")
            return

        for widget in self.question_widgets:
            widget.destroy()
        self.question_widgets.clear()

        self.next_btn.configure(state="disabled", text="Loading...")
        self.status_label.configure(text="Fetching questions...")

        thread = threading.Thread(target=self._fetch_questions)
        thread.daemon = True
        thread.start()

    def _fetch_questions(self):
        """File-1 _fetch_questions — background thread."""
        try:
            questions = get_questions(self.issue_var.get())
            self.after(0, self._display_questions, questions)
        except Exception as e:
            self.after(0, self._show_error, f"Error loading questions:\n{e}")
            self.after(0, lambda: self.next_btn.configure(state="normal", text="Continue →"))

    # ------------------------------------------------------------------ #
    #  STEP 3 — display questions with correct pack order                  #
    # ------------------------------------------------------------------ #
    def _display_questions(self, questions):
        """
        File-1 _display_questions.
        Rebuilds question_frame from scratch so pack order is always:
            header -> scroll(questions) -> submit button -> result box
        This is the fix: previously questions were appended AFTER result_box,
        pushing them off-screen.
        """
        if questions is None:
            self.next_btn.configure(state="normal", text="Continue →")
            self.status_label.configure(text="Failed to load questions. Check your API key and URL.")
            return

        self.entries = {}

        # Tear down selector screen; rebuild cleanly
        for child in self.question_frame.winfo_children():
            child.destroy()
        self.question_widgets.clear()

        # 1. Header
        ctk.CTkLabel(
            self.question_frame,
            text=f"About {self.issue_var.get()}",
            font=("Inter", 24, "bold"), text_color=self.text_main
        ).pack(pady=(30, 5), padx=25, anchor="w")

        # 2. Scrollable question cards
        q_scroll = ctk.CTkScrollableFrame(
            self.question_frame, fg_color="transparent", height=310
        )
        q_scroll.pack(fill="both", expand=False, padx=10, pady=(5, 0))
        self.question_widgets.append(q_scroll)

        for q in questions:
            container = ctk.CTkFrame(q_scroll, fg_color="white", corner_radius=12)
            container.pack(fill="x", pady=5, padx=10)
            self.question_widgets.append(container)

            ctk.CTkLabel(
                container, text=q, font=("Inter", 12),
                text_color=self.text_main, wraplength=280
            ).pack(pady=(10, 5), padx=15, anchor="w")

            entry = ctk.CTkEntry(container, placeholder_text="Type here...", border_width=1, height=35)
            entry.pack(fill="x", padx=15, pady=(0, 15))
            self.question_widgets.append(entry)

            self.entries[q] = entry

        # 3. Submit button — packed BEFORE result_box
        submit_button = ctk.CTkButton(
            self.question_frame, text="Generate Advice ✨",
            height=45, corner_radius=12, fg_color=self.primary_color,
            hover_color="#4F46E5", command=self.process_answers
        )
        submit_button.pack(padx=20, pady=(10, 5), fill="x")
        self.question_widgets.append(submit_button)

        # 4. Result box — always last
        self.result_box = ctk.CTkTextbox(
            self.question_frame, height=130, corner_radius=15,
            border_width=1, font=("Inter", 13)
        )
        self.result_box.pack(padx=20, pady=(5, 15), fill="x")
        self.question_widgets.append(self.result_box)

    # ------------------------------------------------------------------ #
    #  STEP 4 — generate advice (file-1 logic unchanged)                   #
    # ------------------------------------------------------------------ #
    def process_answers(self):
        """File-1 process_answers."""
        answers = {q: e.get() for q, e in self.entries.items()}
        self._write_result("Generating advice...")

        thread = threading.Thread(target=self._fetch_advice, args=(answers,))
        thread.daemon = True
        thread.start()

    def _fetch_advice(self, answers):
        """File-1 _fetch_advice — background thread."""
        try:
            advice = generate_advice(answers)
            styled = style_output(advice, self.tone_var.get())
            self.after(0, self._display_advice, styled)
        except Exception as e:
            self.after(0, self._show_error, f"Error generating advice:\n{e}")

    def _display_advice(self, styled):
        """File-1 _display_advice."""
        self._write_result(styled)

    def _show_error(self, message):
        """File-1 _show_error."""
        self._write_result(message)

    # ------------------------------------------------------------------ #
    #  PROFILE                                                             #
    # ------------------------------------------------------------------ #
    def show_profile(self):
        for child in self.profile_frame.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.profile_frame, text="Profile",
            font=("SF Pro Display", 34, "bold"), text_color="#000000"
        ).pack(pady=(60, 20), padx=25, anchor="w")

        user_card = ctk.CTkFrame(self.profile_frame, fg_color="white", corner_radius=15)
        user_card.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            user_card, text="👤", font=("Arial", 40),
            fg_color="#E5E5EA", corner_radius=30, width=60, height=60
        ).pack(side="left", padx=15, pady=15)

        ctk.CTkLabel(
            user_card, text="User Name\nuser@example.com",
            font=("SF Pro Text", 16, "bold"), justify="left", text_color="#000000"
        ).pack(side="left", pady=15)

        tab_container = ctk.CTkFrame(self.profile_frame, fg_color="#E3E3E8", corner_radius=10, height=40)
        tab_container.pack(fill="x", padx=20, pady=10)

        self.tabs = {}
        for tab_name in ["Account", "Settings", "About"]:
            btn = ctk.CTkButton(
                tab_container, text=tab_name, height=32,
                fg_color="transparent", text_color="#000000",
                hover_color="#FFFFFF",
                command=lambda t=tab_name.lower(): self._update_profile_tab(t)
            )
            btn.pack(side="left", expand=True, padx=2, pady=2)
            self.tabs[tab_name.lower()] = btn

        self.profile_content = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        self.profile_content.pack(fill="both", expand=True, padx=20)

        self._update_profile_tab("account")
        self._show_frame(self.profile_frame)

    def _update_profile_tab(self, tab_name):
        for child in self.profile_content.winfo_children():
            child.destroy()

        list_group = ctk.CTkFrame(self.profile_content, fg_color="white", corner_radius=12)
        list_group.pack(fill="x", pady=10)

        if tab_name == "account":
            self._add_list_item(list_group, "Display Name", "User Name", True)
            self._add_list_item(list_group, "Email", "user@example.com", True)
            self._add_list_item(list_group, "Member Since", "March 2026", False)
        elif tab_name == "settings":
            self._add_list_item(list_group, "Push Notifications", "Enabled", True)
            self._add_list_item(list_group, "FaceID / Passcode", "On", True)
            self._add_list_item(list_group, "Theme", "Light", False)
        elif tab_name == "about":
            self._add_list_item(list_group, "Version", "1.0.0 (Build 42)", True)
            self._add_list_item(list_group, "Privacy Policy", ">", True)
            self._add_list_item(list_group, "Terms of Service", ">", False)

    def _add_list_item(self, master, label, value, show_divider):
        row = ctk.CTkFrame(master, fg_color="transparent", height=45)
        row.pack(fill="x", padx=15)
        ctk.CTkLabel(row, text=label, font=("SF Pro Text", 15), text_color="#000000").pack(side="left", pady=10)
        ctk.CTkLabel(row, text=value, font=("SF Pro Text", 15), text_color="#8E8E93").pack(side="right", pady=10)
        if show_divider:
            ctk.CTkFrame(master, height=1, fg_color="#C6C6C8").pack(fill="x", padx=(15, 0))

    # ------------------------------------------------------------------ #
    #  HELPERS                                                             #
    # ------------------------------------------------------------------ #
    def show_home(self):
        self._show_frame(self.home_frame)

    def _show_frame(self, frame):
        for f in (self.home_frame, self.question_frame, self.profile_frame):
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def _write_result(self, text):
        """File-1 result_box writer pattern."""
        if self.result_box is None:
            return
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", tk.END)
        if text:
            self.result_box.insert(tk.END, text)


try:
    root = DatingAdviceApp()
    root.mainloop()
except Exception as e:
    traceback.print_exc()
    input("Press Enter to exit...")