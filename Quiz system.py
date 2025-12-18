import tkinter as tk
import random
from owlready2 import *

#tkinter
root = tk.Tk()
root.title("Element Quiz ITS")
root.geometry("500x500")
root.resizable(False, False)
root.config(bg="#D8DBDE")

# data
elements = [
    {"name": "Hydrogen", "symbol": "H", "classification": "Nonmetal",
     "reason": "Hydrogen is a nonmetal because it is a gas and does not conduct electricity."},
    {"name": "Helium", "symbol": "He", "classification": "Nonmetal",
     "reason": "Helium is a nonmetal because it is an inert gas."},
    {"name": "Lithium", "symbol": "Li", "classification": "Metal",
     "reason": "Lithium is a metal because it conducts electricity."},
    {"name": "Beryllium", "symbol": "Be", "classification": "Metal",
     "reason": "Beryllium is a metal because it has metallic properties."},
    {"name": "Boron", "symbol": "B", "classification": "Metalloid",
     "reason": "Boron is a metalloid because it has properties of metals and nonmetals."},
    {"name": "Carbon", "symbol": "C", "classification": "Nonmetal",
     "reason": "Carbon is a nonmetal because it does not conduct electricity."},
    {"name": "Nitrogen", "symbol": "N", "classification": "Nonmetal",
     "reason": "Nitrogen is a nonmetal because it is a gas."},
    {"name": "Oxygen", "symbol": "O", "classification": "Nonmetal",
     "reason": "Oxygen is a nonmetal because it is a gas."},
    {"name": "Fluorine", "symbol": "F", "classification": "Nonmetal",
     "reason": "Fluorine is a nonmetal because it is very reactive."},
    {"name": "Neon", "symbol": "Ne", "classification": "Nonmetal",
     "reason": "Neon is a nonmetal because it is an inert gas."}
]

random.shuffle(elements)

#ontology setup 
onto_path.append(r"C:\Users\Lenovo\Desktop\assignment.owl")
onto = get_ontology(r"C:\Users\Lenovo\Desktop\assignment.owl").load()

#ontology function
def get_ontology_entity(name):
    """
    Searches the ontology for an entity matching the given name.
    Returns the entity if found, otherwise None.
    """
    entity = onto.search_one(iri=f"*{name}")
    return entity

#global state
current_index = 0
current_correct_answer = ""
missed_questions = []
buttons = []

#fonts
title_font = ("Comic Sans MS", 22, "bold")
question_font = ("Arial", 16, "bold")
button_font = ("Arial", 14, "bold")
feedback_font = ("Arial", 14)

#screen
def show_welcome():
    clear_window()

    frame = tk.Frame(root, bg="#034826")
    frame.pack(expand=True, fill="both")

    tk.Label(
        frame,
        text="Welcome to the Element Quiz",
        font=title_font,
        bg="#034826",
        fg="white"
    ).pack(pady=30)

    tk.Label(
        frame,
        text="Answer questions about elements.\nGreen = Correct | Red = Incorrect",
        font=feedback_font,
        bg="#034826",
        fg="white",
        justify="center"
    ).pack(pady=20)

    tk.Button(
        frame,
        text="Start Quiz",
        font=button_font,
        bg="#FF4500",
        fg="white",
        width=18,
        height=2,
        command=start_quiz
    ).pack(pady=20)

#quiz screen
def start_quiz():
    global question_label, feedback_label, next_button

    clear_window()

    frame = tk.Frame(root, bg="#034826")
    frame.pack(expand=True, fill="both")

    content = tk.Frame(frame, bg="#034826")
    content.place(relx=0.5, rely=0.5, anchor="center")

    question_label = tk.Label(
        content,
        text="",
        font=question_font,
        bg="#034826",
        fg="white",
        wraplength=460,
        justify="center"
    )
    question_label.pack(pady=15)

    btn_frame = tk.Frame(content, bg="#034826")
    btn_frame.pack()

    buttons.clear()
    for i in range(4):
        btn = tk.Button(
            btn_frame,
            font=button_font,
            bg="white",
            width=30,
            command=lambda i=i: check_answer(i)
        )
        btn.pack(pady=5)
        buttons.append(btn)

    feedback_label = tk.Label(
        content,
        text="",
        font=feedback_font,
        bg="#034826",
        fg="white",
        wraplength=460,
        justify="center"
    )
    feedback_label.pack(pady=10)

    next_button = tk.Button(
        content,
        text="Next Question",
        font=button_font,
        bg="#752FE7",
        width=18,
        height=2,
        command=next_question
    )

    display_question()

#logic for question
def display_question():
    global current_correct_answer

    element = elements[current_index]
    feedback_label.config(text="")
    next_button.pack_forget()

    for btn in buttons:
        btn.config(bg="white", state="normal")

    question_type = random.choice(["classification", "symbol", "name"])

    if question_type == "classification":
        question_label.config(
            text=f"Classify the element:\n{element['name']} ({element['symbol']})"
        )
        options = ["Metal", "Nonmetal", "Metalloid"]
        current_correct_answer = element["classification"]

    elif question_type == "symbol":
        question_label.config(text=f"What is the symbol of {element['name']}?")
        current_correct_answer = element["symbol"]
        options = [current_correct_answer]
        while len(options) < 4:
            sym = random.choice(elements)["symbol"]
            if sym not in options:
                options.append(sym)

    else:
        question_label.config(text=f"Which element has the symbol {element['symbol']}?")
        current_correct_answer = element["name"]
        options = [current_correct_answer]
        while len(options) < 4:
            name = random.choice(elements)["name"]
            if name not in options:
                options.append(name)

    random.shuffle(options)

    for i in range(4):
        buttons[i].config(text=options[i])

#checking answer
def check_answer(index):
    element = elements[current_index]
    selected = buttons[index]["text"]

    for btn in buttons:
        btn.config(state="disabled")

    if selected == current_correct_answer:
        buttons[index].config(bg="#037b1f")
        feedback_label.config(text=f"Correct!\n{element['reason']}")
    else:
        buttons[index].config(bg="#b40819")
        feedback_label.config(text=f"Incorrect.\n{element['reason']}")
        missed_questions.append(element)
        for btn in buttons:
            if btn.cget("text") == current_correct_answer:
                btn.config(bg="#28a745")

    next_button.pack(pady=10)

#navigation
def next_question():
    global current_index
    current_index += 1
    if current_index < len(elements):
        display_question()
    else:
        show_summary()

#final screen
def show_summary():
    clear_window()

    frame = tk.Frame(root, bg="#034826")
    frame.pack(expand=True, fill="both")

    content = tk.Frame(frame, bg="#034826")
    content.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        content,
        text="Quiz Finished!",
        font=question_font,
        bg="#034826",
        fg="white"
    ).pack(pady=15)

    if missed_questions:
        tk.Label(
            content,
            text="Review these elements:",
            font=feedback_font,
            bg="#034826",
            fg="white"
        ).pack(pady=5)

        for e in missed_questions:
            tk.Label(
                content,
                text=f"{e['name']} ({e['symbol']}) - {e['classification']}",
                font=feedback_font,
                bg="#034826",
                fg="white"
            ).pack()
    else:
        tk.Label(
            content,
            text="Perfect! No missed questions 🎉",
            font=feedback_font,
            bg="#034826",
            fg="white"
        ).pack(pady=10)

    tk.Button(
        content,
        text="Restart Quiz",
        font=button_font,
        bg="#FFD700",
        width=18,
        height=2,
        command=restart_quiz
    ).pack(pady=20)

# utilities
def restart_quiz():
    global current_index, missed_questions
    current_index = 0
    missed_questions = []
    random.shuffle(elements)
    start_quiz()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

show_welcome()
root.mainloop()
