import tkinter as tk
import customtkinter as ctk
from question_engine import get_questions
from advice_engine import analyze_dimensions, generate_advice
from tone_engine import style_output

# Set global appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DatingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Love Overflow")
        self.geometry("380x700") # Slightly wider for better text flow
        self.configure(fg_color="#F8FAFC") # Softer off-white

        # --- Color Palette ---
        self.primary_color = "#6366F1"  # Indigo
        self.bg_color = "#F8FAFC"
        self.card_color = "#FFFFFF"
        self.text_main = "#1E293B"
        self.text_sub = "#64748B"

        # Main content container
        self.home_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.home_frame.pack(fill='both', expand=True)

        self.setup_home_ui()
        
        # Navigation bar (Persistent at bottom)
        self.setup_nav_bar()

        # Page Containers
        self.question_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.profile_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        
        self.entries = {}
        self.tab_buttons = {}

    def setup_home_ui(self):
        # Header
        self.header = ctk.CTkLabel(
            self.home_frame, text="Love Overflow", 
            font=("Inter", 32, "bold"), text_color=self.primary_color
        )
        self.header.pack(pady=(40, 5), padx=25, anchor="w")

        self.sub_header = ctk.CTkLabel(
            self.home_frame, text="Your AI Wingman.", 
            font=("Inter", 16), text_color=self.text_sub
        )
        self.sub_header.pack(padx=25, anchor="w")

        # Hero Card
        self.card = ctk.CTkFrame(
            self.home_frame, corner_radius=24, fg_color=self.card_color, 
            border_width=1, border_color="#E2E8F0"
        )
        self.card.pack(pady=30, padx=20, fill="x")

        self.icon = ctk.CTkLabel(
            self.card, text="✨", font=("Helvetica", 60),
            height=160, fg_color="#EEF2FF", corner_radius=20
        )
        self.icon.pack(pady=20, padx=20, fill="x")

        self.welcomeMessage = ctk.CTkLabel(
            self.card, text="Ready for clarity?", 
            font=("Inter", 22, "bold"), text_color=self.text_main
        )
        self.welcomeMessage.pack(padx=20, anchor="w")

        self.description = ctk.CTkLabel(
            self.card, text="Analyze your chats and get tactical advice.",
            font=("Inter", 13), text_color=self.text_sub, wraplength=280, justify="left"
        )
        self.description.pack(padx=20, pady=(5, 20), anchor="w")

        self.start_q_btn = ctk.CTkButton(
            self.card, text="Get Started", height=45, corner_radius=12,
            font=("Inter", 14, "bold"), fg_color=self.primary_color,
            hover_color="#4F46E5", command=self.load_questions
        )
        self.start_q_btn.pack(padx=20, pady=(0, 25), fill="x")

    def setup_nav_bar(self):
        self.nav_bar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="white", border_width=1, border_color="#E2E8F0")
        self.nav_bar.pack(side="bottom", fill="x")

        nav_config = [
            ("🏠", self.show_home),
            ("💬", self.load_questions),
            ("👤", self.show_profile)
        ]

        for icon, cmd in nav_config:
            btn = ctk.CTkButton(
                self.nav_bar, text=icon, width=60, height=45, font=("Inter", 20),
                fg_color="transparent", text_color=self.text_main, 
                hover_color="#F1F5F9", command=cmd
            )
            btn.pack(side="left", expand=True, pady=10)

    # --- Questionnaire Logic (Improved UX) ---
    def load_questions(self):
        for child in self.question_frame.winfo_children():
            child.destroy()

        self.home_frame.pack_forget()
        self.profile_frame.pack_forget()
        self.question_frame.pack(fill='both', expand=True)

        # Progress Header
        header = ctk.CTkLabel(self.question_frame, text="The Situation", font=("Inter", 24, "bold"), text_color=self.text_main)
        header.pack(pady=(30, 10), padx=25, anchor="w")

        # Styled Selection Container
        select_card = ctk.CTkFrame(self.question_frame, fg_color="white", corner_radius=15)
        select_card.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(select_card, text="What's happening?", font=("Inter", 13, "bold")).pack(pady=(15, 0), padx=15, anchor="w")
        self.issue_menu = ctk.CTkOptionMenu(
            select_card, values=['Texting', 'Mixed Signals', 'Conflict', 'Ex', 'Situationship'],
            fg_color="#F1F5F9", text_color=self.text_main, button_color="#CBD5E1", button_hover_color="#94A3B8"
        )
        self.issue_menu.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(select_card, text="Desired Tone", font=("Inter", 13, "bold")).pack(pady=(10, 0), padx=15, anchor="w")
        self.tone_menu = ctk.CTkOptionMenu(
            select_card, values=['honest', 'brutal', 'calm', 'slightly_toxic'],
            fg_color="#F1F5F9", text_color=self.text_main, button_color="#CBD5E1"
        )
        self.tone_menu.pack(fill="x", padx=15, pady=(10, 20))

        next_btn = ctk.CTkButton(self.question_frame, text="Continue →", height=45, corner_radius=12, fg_color=self.primary_color, command=self.show_questions)
        next_btn.pack(pady=20, padx=20, fill="x")

    def show_questions(self):
        selected_issue = self.issue_menu.get()
        for child in self.question_frame.winfo_children():
            child.destroy()

        ctk.CTkLabel(self.question_frame, text=f"About {selected_issue}", font=("Inter", 24, "bold")).pack(pady=(30, 5), padx=25, anchor="w")
        
        q_scroll = ctk.CTkScrollableFrame(self.question_frame, fg_color="transparent", height=320)
        q_scroll.pack(fill="both", expand=True, padx=10)

        questions = get_questions(selected_issue) or ["Describe the situation:"]
        self.entries.clear()

        for q in questions:
            container = ctk.CTkFrame(q_scroll, fg_color="white", corner_radius=12)
            container.pack(fill="x", pady=5, padx=10)
            
            ctk.CTkLabel(container, text=q, font=("Inter", 12), text_color=self.text_main, wraplength=280).pack(pady=(10, 5), padx=15, anchor="w")
            ent = ctk.CTkEntry(container, placeholder_text="Type here...", border_width=1, height=35)
            ent.pack(fill="x", padx=15, pady=(0, 15))
            self.entries[q] = ent

        btn_row = ctk.CTkFrame(self.question_frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=20, padx=20)

        self.submit_btn = ctk.CTkButton(btn_row, text="Generate Advice ✨", height=45, corner_radius=12, fg_color=self.primary_color, command=self.process_answers)
        self.submit_btn.pack(fill="x")

        # Advice Output (Using CTkTextbox for better styling)
        self.result_box = ctk.CTkTextbox(self.question_frame, height=150, corner_radius=15, border_width=1, font=("Inter", 13))
        self.result_box.pack(padx=20, pady=(0, 20), fill="x")

    def process_answers(self):
        answers = {q: e.get() for q, e in self.entries.items()}
        scores = analyze_dimensions(answers)
        advice = generate_advice(scores)
        tone = self.tone_menu.get()
        styled = style_output(advice, tone)

        self.result_box.configure(state="normal")
        self.result_box.delete('1.0', tk.END)
        self.result_box.insert(tk.END, styled)
        self.result_box.configure(state="disabled") # Make read-only

    # --- Profile & Navigation ---
    def show_home(self):
        self.question_frame.pack_forget()
        self.profile_frame.pack_forget()
        self.home_frame.pack(fill='both', expand=True)

    def show_profile(self):
        # 1. Clear the frame entirely to prevent duplicate "Profile" labels
        for child in self.profile_frame.winfo_children():
            child.destroy()

        # 2. Header: Large iOS-style Title
        header_label = ctk.CTkLabel(
            self.profile_frame, 
            text="Profile", 
            font=("SF Pro Display", 34, "bold"), 
            text_color="#000000"
        )
        header_label.pack(pady=(60, 20), padx=25, anchor="w")

        # 3. Profile "Business Card" (User Summary)
        user_card = ctk.CTkFrame(self.profile_frame, fg_color="white", corner_radius=15)
        user_card.pack(fill="x", padx=20, pady=(0, 20))
        
        # User Avatar Placeholder
        avatar = ctk.CTkLabel(user_card, text="👤", font=("Arial", 40), fg_color="#E5E5EA", corner_radius=30, width=60, height=60)
        avatar.pack(side="left", padx=15, pady=15)
        
        info_text = ctk.CTkLabel(
            user_card, 
            text="User Name\nuser@example.com", 
            font=("SF Pro Text", 16, "bold"), 
            justify="left",
            text_color="#000000"
        )
        info_text.pack(side="left", pady=15)

        # 4. Segmented Control (The Tab Switcher)
        tab_container = ctk.CTkFrame(self.profile_frame, fg_color="#E3E3E8", corner_radius=10, height=40)
        tab_container.pack(fill="x", padx=20, pady=10)
        
        self.tabs = {}
        for tab_name in ['Account', 'Settings', 'About']:
            btn = ctk.CTkButton(
                tab_container, 
                text=tab_name, 
                height=32,
                fg_color="transparent", 
                text_color="#000000",
                hover_color="#FFFFFF",
                command=lambda t=tab_name.lower(): self._update_profile_tab(t)
            )
            btn.pack(side="left", expand=True, padx=2, pady=2)
            self.tabs[tab_name.lower()] = btn

        # 5. Content Area (The "Grouped List")
        self.profile_content = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        self.profile_content.pack(fill="both", expand=True, padx=20)

        # Show default tab
        self._update_profile_tab('account')

        # Navigation logic
        self.home_frame.pack_forget()
        self.question_frame.pack_forget()
        self.profile_frame.pack(fill='both', expand=True)

    def _update_profile_tab(self, tab_name):
        # Clear previous tab content
        for child in self.profile_content.winfo_children():
            child.destroy()

        # Create the iOS "Grouped" container
        list_group = ctk.CTkFrame(self.profile_content, fg_color="white", corner_radius=12)
        list_group.pack(fill="x", pady=10)

        if tab_name == 'account':
            self._add_list_item(list_group, "Display Name", "User Name", True)
            self._add_list_item(list_group, "Email", "user@example.com", True)
            self._add_list_item(list_group, "Member Since", "March 2026", False)
        
        elif tab_name == 'settings':
            self._add_list_item(list_group, "Push Notifications", "Enabled", True)
            self._add_list_item(list_group, "FaceID / Passcode", "On", True)
            self._add_list_item(list_group, "Theme", "Light", False)

        elif tab_name == 'about':
            self._add_list_item(list_group, "Version", "1.0.0 (Build 42)", True)
            self._add_list_item(list_group, "Privacy Policy", ">", True)
            self._add_list_item(list_group, "Terms of Service", ">", False)

    def _add_list_item(self, master, label, value, show_divider):
        """Helper to create that clean Apple list row."""
        row = ctk.CTkFrame(master, fg_color="transparent", height=45)
        row.pack(fill="x", padx=15)
        
        lbl = ctk.CTkLabel(row, text=label, font=("SF Pro Text", 15), text_color="#000000")
        lbl.pack(side="left", pady=10)
        
        val = ctk.CTkLabel(row, text=value, font=("SF Pro Text", 15), text_color="#8E8E93")
        val.pack(side="right", pady=10)
        
        if show_divider:
            divider = ctk.CTkFrame(master, height=1, fg_color="#C6C6C8")
            divider.pack(fill="x", padx=(15, 0))

if __name__ == "__main__":
    app = DatingApp()
    app.mainloop()