import tkinter as tk
from tkinter import Canvas, StringVar
# import custom functions
from functions import *

# ------------------------------------------------- SET CONSTANTS ------------------------------------------------- #

TIME = 61
CPM_COUNT = 0
WPM_COUNT = 0
WRONG_CHARACTER_COUNT = 0
WRONG_WORD_COUNT = 0


# ------------------------------------------------ STATIC FUNCTIONS ------------------------------------------------ #

# after the time is out, compare the highscore and current score
def overwrite_highscore():
    if CPM_COUNT > cpm_highscore():
        with open("highscore.json", "r") as jsonFile:
            scores = json.load(jsonFile)
        scores["CPM Highscore:"] = CPM_COUNT
        with open("highscore.json", "w") as jsonFile:
            json.dump(scores, jsonFile)
    if WPM_COUNT > wpm_highscore():
        with open("highscore.json", "r") as jsonFile:
            scores = json.load(jsonFile)
        scores["WPM Highscore:"] = WPM_COUNT
        with open("highscore.json", "w") as jsonFile:
            json.dump(scores, jsonFile)


# calculate the accuracy percentage
def percentage_calculator():
    percentage = int(CPM_COUNT * 100 / (CPM_COUNT + WRONG_CHARACTER_COUNT))
    return percentage


# --------------------------------------------- SET THE MAIN APPLICATION ----------------------------------------- #

class App(tk.Tk):
    # -------------------------------- SET THE CLASS ATTRIBUTES --------------------------- #
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title("Typing speed")
        self.config(padx=50, pady=30, bg="#F7F7F7")

        # configure variables
        self.word_list = create_word_list()
        self.random_word_list = create_random_word_list()

        # configure Canvas
        self.canvas = Canvas()
        self.canvas.config(height=400, width=900)
        self.canvas.grid(column=0, row=1, columnspan=9, rowspan=10)
        self.canvas.create_line(0, 45, 900, 45)

        # set title label
        self.title_label = tk.Label(text="Typing speed", font=("Arvo", 22, "bold"), highlightthickness=1, bg="#F7F7F7")
        self.title_label.grid(column=0, row=0, pady=20, columnspan=9)

        # set options list
        self.options_list = ["CPM Highscore:", "WPM Highscore:"]
        self.value_inside = StringVar()
        self.value_inside.set("CPM Highscore:")

        # set highscore label
        self.highscore_label = tk.OptionMenu(self, self.value_inside, *self.options_list, command=self.change_highscore)
        self.highscore_label.grid(column=0, row=1)
        self.highscore_label.config(font=("Arvo", 10, "bold"))

        # set highscore value label
        self.highscore_value_label = tk.Label(text=cpm_highscore(), font=("Arvo", 12, "bold"))
        self.highscore_value_label.grid(column=1, row=1, padx=(0, 5))

        # set characters per minute label
        self.cpm_label = tk.Label(text="CPM:", font=("Arvo", 12, "bold"))
        self.cpm_label.grid(column=2, row=1)

        # set characters per minute label value
        self.cpm_value_label = tk.Label(text="0", font=("Arvo", 12, "bold"))
        self.cpm_value_label.grid(column=3, row=1, padx=(0, 5))

        # set words per minute label
        self.wpm_label = tk.Label(text="WPM:", font=("Arvo", 12, "bold"))
        self.wpm_label.grid(column=4, row=1)

        # set words per minute label value
        self.wpm = tk.Label(text="0", font=("Arvo", 12, "bold"))
        self.wpm.grid(column=5, row=1, padx=(0, 5))

        # set time left label
        self.time_label = tk.Label(text="Time left:", font=("Arvo", 12, "bold"))
        self.time_label.grid(column=6, row=1)

        # set time left value label
        self.time_value_label = tk.Label(text="01:00", font=("Arvo", 12, "bold"))
        self.time_value_label.grid(column=7, row=1, padx=(0, 5))

        # set restart button label
        self.restart_button = tk.Button(text=" Restart ", font=("Consolas", 10, "bold"), fg="#FBFBFB", bg="#2B2B2B",
                                        command=self.restart)
        self.restart_button.config(height=1)
        self.restart_button.grid(column=8, row=1)

        # set text area label
        self.text_area = tk.Label(text=f"{self.random_word_list[0]} {self.random_word_list[1]} "
                                       f"{self.random_word_list[2]} {self.random_word_list[3]} "
                                       f"{self.random_word_list[4]}", font=("Consolas", 25, "bold"), fg="#212121")
        self.text_area.grid(column=0, row=3, pady=50, columnspan=9)

        # set text entry field
        self.input_text = tk.Entry(font=("Arvo", 20, "bold"), fg="#212121")
        self.input_text.grid(column=0, row=5, columnspan=9)
        self.input_text.insert(0, "type your words here")
        self.input_text.configure(state="disabled")

        # set the onclick id
        self.on_click_id = self.input_text.bind("<Button-1>", self.on_click)
        self.input_text.bind("<space>", self.main)

    # ------------------------ SET THE CLASS METHODS --------------------------- #

    # destroy the app, reset the constant's values to the default, start the app
    def restart(self):
        global TIME, CPM_COUNT, WPM_COUNT, WRONG_CHARACTER_COUNT, WRONG_WORD_COUNT
        TIME = 61
        CPM_COUNT = 0
        WPM_COUNT = 0
        WRONG_CHARACTER_COUNT = 0
        WRONG_WORD_COUNT = 0
        for after_id in self.tk.eval("after info").split():
            self.after_cancel(after_id)
        self.destroy()
        App()

    # change highscore label, and show the corresponding score
    def change_highscore(self, choice):
        score_type = self.value_inside.get()
        if score_type == "CPM Highscore:":
            self.highscore_value_label.config(text=cpm_highscore())
        elif score_type == "WPM Highscore:":
            self.highscore_value_label.config(text=wpm_highscore())

    # delete the first word from the sample list, and insert a new random word to the end of the list
    def word_manager(self):
        self.update()
        self.random_word_list.pop(0)
        random_number = random.randint(0, len(self.word_list) - 1)
        self.random_word_list.insert(4, self.word_list[random_number])
        self.text_area.config(text=f"{self.random_word_list[0]} {self.random_word_list[1]} {self.random_word_list[2]}"
                                   f" {self.random_word_list[3]} {self.random_word_list[4]}")
        self.cpm_value_label.config(text=CPM_COUNT)
        self.wpm.config(text=WPM_COUNT)
        self.update()

    # start the countdown
    def countdown(self, count):
        if count >= 0:
            if count > 59:
                self.time_value_label.config(text=f"01:00")
            elif count > 9:
                self.time_value_label.config(text=f"00:{count}")
            elif 9 >= count > 0:
                self.time_value_label.config(text=f"00:0{count}")
            # if the time is out, disable the text input
            elif count == 0:
                self.time_value_label.config(text=f"00:0{count}")
                self.input_text.delete(0, "end")
                self.input_text.config(state="disabled")
                overwrite_highscore()
                self.highscore_value_label.config(text=cpm_highscore())
                try:
                    self.input_text.unbind("<space>", self.main)
                except TypeError:
                    pass
                # check the percentage
                if WRONG_WORD_COUNT == 0:
                    self.text_area.config(text=f"You typed {WPM_COUNT} words and {CPM_COUNT} characters\n"
                                               f"per minute. Your percentage is {percentage_calculator()}%\n")
                else:
                    self.text_area.config(text=f"You typed {WPM_COUNT} words and {CPM_COUNT} characters\n"
                                               f"per minute. Your percentage is {percentage_calculator()}%\n"
                                               f"Wrong words: {WRONG_WORD_COUNT}")
            self.after(1000, self.countdown, count - 1)

    # manage the click inside the input text box, and enable typing
    def on_click(self, event):
        self.input_text.configure(state="normal")
        self.input_text.delete(0, "end")

        # make the callback only work once
        self.input_text.unbind("<Button-1>", self.on_click_id)

    # if the time is 61, start countdown
    def time_manager(self):
        global CPM_COUNT, WPM_COUNT, TIME
        if TIME == 61:
            TIME -= 1
            CPM_COUNT = 0
            WPM_COUNT = 0
            self.countdown(TIME)

    # main function
    def main(self, event):
        global TIME, WRONG_CHARACTER_COUNT, WRONG_WORD_COUNT
        global CPM_COUNT, WPM_COUNT
        # remove white spaces from the word
        word = self.input_text.get().replace(" ", "")
        # check if typed word is correct, increase cpm and wpm count
        if word == self.random_word_list[0]:
            self.input_text.delete(0, "end")
            if TIME < 61:
                CPM_COUNT += len(word)
                WPM_COUNT += 1
            self.word_manager()
            self.time_manager()
            return "break"
        # check if typed word is incorrect, increase wrong words count
        else:
            self.input_text.delete(0, "end")
            WRONG_CHARACTER_COUNT += len(word)
            WRONG_WORD_COUNT += 1
            self.word_manager()
            self.time_manager()
            return "break"


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
