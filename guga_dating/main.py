import tkinter as tk
from tkinter import ttk
from question_engine import get_questions
from advice_engine import generate_advice
from tone_engine import style_output
import time
import traceback
import threading


class DatingAdviceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dating Advice AI")

        self.answers = {}

        self.issue_label = tk.Label(root, text="Select issue:")
        self.issue_label.pack()

        self.issue_var = tk.StringVar()
        self.issue_dropdown = ttk.Combobox(
            root,
            textvariable=self.issue_var,
            values=["Texting", "Mixed Signals", "Conflict", "Ex", "Situationship"]
        )
        self.issue_dropdown.pack()

        self.tone_label = tk.Label(root, text="Select tone:")
        self.tone_label.pack()

        self.tone_var = tk.StringVar()
        self.tone_dropdown = ttk.Combobox(
            root,
            textvariable=self.tone_var,
            values=["honest", "brutal", "calm", "slightly_toxic"]
        )
        self.tone_dropdown.pack()

        self.start_button = tk.Button(root, text="Start", command=self.load_questions)
        self.start_button.pack()

        self.question_widgets = []

        self.result_box = tk.Text(root, height=10, width=60)
        self.result_box.pack()

    def load_questions(self):
        if not self.issue_var.get():
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, "Please select an issue first.")
            return

        if not self.tone_var.get():
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, "Please select a tone first.")
            return

        for widget in self.question_widgets:
            widget.destroy()
        self.question_widgets.clear()

        self.start_button.config(state="disabled", text="Loading...")
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, "Fetching questions...")

        # Run API call in background thread so UI doesn't freeze
        thread = threading.Thread(target=self._fetch_questions)
        thread.daemon = True
        thread.start()

    def _fetch_questions(self):
        try:
            questions = get_questions(self.issue_var.get())
            # Schedule UI update back on main thread
            self.root.after(0, self._display_questions, questions)
        except Exception as e:
            self.root.after(0, self._show_error, f"Error loading questions:\n{e}")
            self.root.after(0, self.start_button.config, {"state": "normal", "text": "Start"})

    def _display_questions(self, questions):
        self.start_button.config(state="normal", text="Start")
        self.result_box.delete("1.0", tk.END)
    
    # ADD THIS CHECK:
        if questions is None:
            self.result_box.insert(tk.END, "Failed to load questions. Check your API key and URL.")
            return

        self.entries = {}
    # ... rest of your code ...

        for q in questions:
            label = tk.Label(self.root, text=q)
            label.pack()
            self.question_widgets.append(label)

            entry = tk.Entry(self.root, width=60)
            entry.pack()
            self.question_widgets.append(entry)

            self.entries[q] = entry

        submit_button = tk.Button(self.root, text="Generate Advice", command=self.process_answers)
        submit_button.pack()
        self.question_widgets.append(submit_button)

    def process_answers(self):
        answers = {q: e.get() for q, e in self.entries.items()}

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, "Generating advice...")

        # Run API calls in background thread
        thread = threading.Thread(target=self._fetch_advice, args=(answers,))
        thread.daemon = True
        thread.start()

    def _fetch_advice(self, answers):
        try:
            advice = generate_advice(answers)
            time.sleep(1)
            styled = style_output(advice, self.tone_var.get())
            self.root.after(0, self._display_advice, styled)
        except Exception as e:
            self.root.after(0, self._show_error, f"Error generating advice:\n{e}")

    def _display_advice(self, styled):
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, styled)

    def _show_error(self, message):
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, message)


try:
    root = tk.Tk()
    app = DatingAdviceApp(root)
    root.mainloop()
except Exception as e:
    traceback.print_exc()
    input("Press Enter to exit...")