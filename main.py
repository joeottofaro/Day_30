from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

words_dict = {}
word = {}

# Will use the full list of words unless words_to_learn exists
try:
    pandas_data = pandas.read_csv("./data/words_to_learn.csv")

except FileNotFoundError:
    pandas_data = pandas.read_csv("./data/french_words.csv")
    words_dict = pandas_data.to_dict("records")
else:
    words_dict = pandas_data.to_dict("records")


# ---------------------------- Random French Word ------------------------------- #

def next_card():
    # Global used to span outside this function
    global word, flip_timer
    # This is used to cancel the first window.after call
    # and any active ones if the user spams the buttons
    window.after_cancel(flip_timer)
    canvas.itemconfig(card, image=card_front_img)
    word = random.choice(words_dict)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=word["French"], fill="black")
    flip_timer = window.after(3000, translation_card)


# ---------------------------- English Translation Word ------------------------------- #

def translation_card():
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=word["English"], fill="white")


# ---------------------------- Remove word user knows ------------------------------- #

def known_word():
    words_dict.remove(word)
    words_to_learn = pandas.DataFrame(words_dict)
    words_to_learn.to_csv('./data/words_to_learn.csv', index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, translation_card)

# Canvas setup
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file='./images/card_front.png')
card_back_img = PhotoImage(file='./images/card_back.png')
card = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons

right_image = PhotoImage(file='./images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file='./images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
