import tkinter as tk
from tkinter import ttk
from question_engine import get_questions
from advice_engine import analyze_dimensions
from tone_engine import style_output

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
        for widget in self.question_widgets:
            widget.destroy()
        self.question_widgets.clear()

        questions = get_questions(self.issue_var.get())

        self.entries = {}

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

        category = classify_situation(answers)
        advice = generate_advice(category)
        styled = style_output(advice, self.tone_var.get())

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, styled)

root = tk.Tk()
app = DatingAdviceApp(root)
root.mainloop()