__author__ = "Harry Baines"

import random

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class MathGame(tk.Frame):

    """ This class implements various mathematical operations
    such as addition, subtraction, multiplication and division
    on a set of randomly generated operands """

    def open_msg_box(self):
        tk.messagebox.showwarning(
            "Event Triggered",
            "Button Clicked"
        )

    def open_answer_window(self, math_key):

        self.master.withdraw()

        self.topLevel = tk.Toplevel(self.master)
        self.topLevel.title("Maths Game")
        self.topLevel.grid_rowconfigure(1, weight=1)
        self.topLevel.grid_columnconfigure(1, weight=1)
        self.topLevel.configure(background="#80ff80")

        self.topLevel.geometry(self.geom_string)
        self.topLevel.resizable(width=False, height=False)

        self.__maxBound = 4
        self.__consecutiveRight = 0
        self.__consecutiveWrong = 0

        self.style.configure("Enter.TButton",
                        foreground="royal blue",
                        font=self.font_name + " 18 bold",
                        padding=(2,20,2,20))
        self.style.configure("Back.TButton",
                        foreground="royal blue",
                        font=self.font_name + " 14 bold",
                        padding=(5,5,5,5))
        self.style.configure("Entry.TEntry",
                        foreground="royal blue",
                        font=self.font_name + " 40 bold",
                        padding=(2,20,2,20))

        # Math type label
        label = tk.Label(self.topLevel, text=self.button_names[math_key-1], bg="#80ff80", fg="medium blue", font=(self.font_name, 74, "bold"))
        label.grid(row=0, column=0, columnspan=4, pady=40)
        
        # Call relevant math function to obtain the question
        self.math_func = self.__mathFuncDict[math_key]
        self.questionVar = tk.StringVar()
        self.questionVar.set(self.math_func())

        # Label for question
        self.questionLbl = tk.Label(self.topLevel, text=self.questionVar.get(), bg="#80ff80", font=(self.font_name, 88, "bold"))
        self.questionLbl.grid(row=1, columnspan=4, pady=5)

        # Label displays if user was correct/wrong
        self.was_correct_var = tk.StringVar()
        self.was_correct_lbl = tk.Label(self.topLevel, textvariable=self.was_correct_var, bg="#80ff80", fg="midnight blue", font=(self.font_name, 20, "bold"))
        self.was_correct_lbl.grid(row=2, columnspan=4, pady=5)

        # User entry box
        self.user_entry = tk.StringVar()
        self.entry = ttk.Entry(self.topLevel, textvariable=self.user_entry, style="Entry.TEntry", width=5, justify="center", font=(self.font_name, 42, "bold"))
        self.entry.grid(row=3, columnspan=2)
        self.entry.delete(0, 'end')
        self.entry.focus()

        # Entry button
        entryBtn = ttk.Button(self.topLevel, text="ENTER", style="Enter.TButton", width=10, command=self.check_answer)
        entryBtn.grid(row=4, columnspan=2)

        # Return home
        goHomeButton = ttk.Button(self.topLevel, text="Back", style="Back.TButton", command=self.go_home)
        goHomeButton.grid(row=5, columnspan=2, pady=5)
        

    def update_top_level(self):
        self.user_entry.set("0")
        self.questionLbl.config(text=self.math_func())
        self.entry.delete(0, 'end')
        self.entry.focus()

    def go_home(self):
        self.topLevel.destroy()
        self.master.geometry(self.geom_string)
        self.master.deiconify()

    # Constructor to initialise a new game
    def __init__(self, master):

        tk.Frame.__init__(self, master, bg="#80ff80")
        self.pack()

        self.sec = 10

        self.master = master
        self.master.configure(background="#80ff80")
        self.font_name = "Tahoma"
        self.button_names = ["Addition", "Subtraction", "Multiplication", "Division", 
                             "Random Sums", "Time Attack", "Unlimited Mode", "Quit"]
        self.geom_string = "900x550+200+50"

        # Initialise instance variables
        self.__startMin = 1
        self.__startMax = 4
        self.__maxLevel = 10
        self.__minBound = self.__startMin
        self.__maxBound = self.__startMax
        
        # Dictionary of function names
        self.__mathFuncDict = {1: self.get_add_question, 2: self.get_sub_question, 3: self.get_mult_question, 4: self.get_div_question, 
                               5: self.rand_sums, 6: self.time_attack, 7: self.unlimited_mode, 8: quit}

        self.__consecutiveRight = 0
        self.__consecutiveWrong = 0


        self.master.title("Maths Game")
        self.master.geometry(self.geom_string)
        self.master.resizable(width=False, height=False)

        self.style = ttk.Style()
        self.style.configure("Option.TButton",
                        foreground="royal blue",
                        font=self.font_name + " 20 bold",
                        padding=(20,60,20,60))

        self.titleLabel = tk.Label(self, text="Maths Game!", bg="#80ff80", fg="medium blue", font=(self.font_name, 50, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=6, pady=20)

        self.selectLabel = tk.Label(self, text="Select an option:", bg="#80ff80", fg="medium blue", font=(self.font_name, 28, "bold"))
        self.selectLabel.grid(row=1, column=0, columnspan=6, pady=20)

        # Loop to initialise buttons
        for i in range(1,9):

            # Lambda command for each button - call relevant function
            button = ttk.Button(self, text="%s" % self.button_names[i-1], style="Option.TButton",
                                command=lambda key=i: self.open_answer_window(key)) 

            row = 3 if i > 4 else 2 
            column = i-5 if i > 4 else i-1

            button.grid(row=row, column=column, padx=2, pady=2, sticky="NSEW")

        self.name_lbl = tk.Label(self, text="2017 Harry Baines", font=(self.font_name, 14), bg="#80ff80")
        self.name_lbl.grid(row=row+1, columnspan=len(self.button_names), pady=20)

        self.master.mainloop()

    def getOperands(self):
        return [self.getNextRand(), self.getNextRand()]

    def rand_sums(self):
        randOperator = random.randint(1,4)
        return self.__mathFuncDict[randOperator]()

    def time_attack(self):
        self.update_timer()

    def update_timer(self):

        self.time_var = tk.StringVar()

        self.time_lbl = tk.Label(self.topLevel, textvariable=self.time_var).grid(row=1,columnspan=4)

        self.sec -= 1
        
        self.time_var.set(str(self.sec))
        self.topLevel.after(1000, self.update_timer)

        if self.sec == 0:
            return


    def unlimited_mode(self):
        self.update_timer()

    def get_add_question(self):
        # Get 2 numbers and prompt user
        operands = self.getOperands()
        self.answer = operands[0] + operands[1]
        question = str(operands[0]) + " + " + str(operands[1]) + " = ?"
        return question
        # self.checkAnswer(operands[0] + operands[1])

    def get_sub_question(self):
        # Get 2 numbers and prompt user
        operands = self.getOperands()

        # Flips operands if answer is -ve
        if operands[0] - operands[1] < 0:
            temp = operands[0]
            operands[0] = operands[1]
            operands[1] = temp

        self.answer = operands[0] - operands[1]
        question = str(operands[0]) + " - " + str(operands[1]) + " = ?"
        return question

    def get_mult_question(self):
        # Get 2 numbers and prompt user
        operands = self.getOperands()           # only need once?
        self.answer = operands[0] * operands[1]
        question = str(operands[0]) + " x " + str(operands[1]) + " = ?" # could be changed
        return question

    def get_div_question(self):
        while True:
            operands = self.getOperands()
            result = operands[0] / operands[1]
            if result == int(result):
                break

        self.answer = operands[0] / operands[1]
        question = str(operands[0]) + " / " + str(operands[1]) + " = ?"
        return question

    def check_answer(self):

        entry = self.user_entry.get().replace(" ","")
        try:
            # Check for correct answer and if they're carrying on
            if int(entry) == self.answer:

                self.__consecutiveRight += 1
                self.__consecutiveWrong = 0

                if (self.__consecutiveRight % 3 == 0) and (self.__maxBound != self.__maxLevel):
                    self.__maxBound += 1

                self.was_correct_var.set("That is correct, well done!")

            else:
                self.__consecutiveWrong += 1
                self.__consecutiveRight = 0

                if (self.__consecutiveWrong % 3 == 0) and (self.__maxBound != self.__startMax):
                    self.__maxBound -= 1

                self.was_correct_var.set("Not right, the correct answer was: " + str(int(self.answer)))

        except (ValueError):
            self.was_correct_var.set("Not right, enter a whole number!")

        self.update_top_level()
       
    def getNextRand(self):
        return random.randint(self.__minBound, self.__maxBound)

# Main function to create a new MathGame instance
def main():
    root = tk.Tk()
    game = MathGame(root)

if __name__ == "__main__":
    main()

