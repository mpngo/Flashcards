import turtle
from tkinter import *
from tkinter import messagebox
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
word_list = {}
chosen = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("french_words.csv")
else:
    word_list = data.to_dict(orient="records")


def next_card():
    global chosen, flip_timer
    window.after_cancel(flip_timer)
    chosen = random.choice(word_list)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(card_word, text=chosen["French"], fill="black")
    canvas.itemconfig(card_background, image=front_img)
    flip_timer = window.after(5000, func=flip_card)


def remove_card():
    word_list.remove(chosen)
    next_card()
    data = pandas.DataFrame(word_list)
    data.to_csv("words_to_learn.csv")
    next_card()

def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(card_word, text=chosen["English"], fill="white")
    canvas.itemconfig(card_background, image=back_img)


window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_img = PhotoImage(file="card_front.png")
back_img = PhotoImage(file="card_back.png")
right_img = PhotoImage(file="right.png")
wrong_img = PhotoImage(file="wrong.png")

card_background = canvas.create_image(400, 263, image=front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
language = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 50, "bold"))


right_button = Button(image=right_img, highlightthickness=0, command=remove_card)
right_button.grid(column=0, row=1)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()
