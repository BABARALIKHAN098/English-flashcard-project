import random
import pandas as pd
from tkinter import *

# ---------------------------- DATA ------------------------------- #
# Try to load words to learn; if not found, load original data
try:
    data_frame = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data_frame = pd.read_csv("data/french_words.csv")

data_con = data_frame.to_dict(orient="records")

def gen_word():
    """Return a random French-English word pair."""
    random_word = random.choice(data_con)
    french = random_word['French']
    english = random_word['English']
    return random_word, french, english

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# --- Load Images ---
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

# --- Canvas Setup ---
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# ---------------------------- FUNCTIONS ------------------------------- #
def show_random_word():
    """Display a random French word and schedule English translation."""
    global current_word, current_french, current_english, flip_timer
    window.after_cancel(flip_timer)  # cancel any previous timer

    current_word, current_french, current_english = gen_word()
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_french, fill="black")

    flip_timer = window.after(3000, flip_card)  # flip after 3 seconds

def flip_card():
    """Flip the card to show English translation."""
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_english, fill="white")

def known_word():
    """Remove known word and save the updated data."""
    data_con.remove(current_word)  # remove from list
    new_data = pd.DataFrame(data_con)
    new_data.to_csv("data/words_to_learn.csv", index=False)  # overwrite with updated data
    show_random_word()  # show next word

# ---------------------------- BUTTONS ------------------------------- #
wrong_button = Button(image=wrong_image, highlightthickness=0, command=show_random_word)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_image, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)

# ---------------------------- START ------------------------------- #
flip_timer = window.after(3000, flip_card)
show_random_word()

window.mainloop()
