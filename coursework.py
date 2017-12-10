__author__ = "Harry Baines"

import random

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *

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

        # Math type label
        label = tk.Label(self.topLevel, text=self.button_names[math_key-1], bg="#80ff80", font=(self.font_name, 70, "bold"))
        label.grid(row=0, column=0, columnspan=3, pady=50)
        
        # Call relevant math function to obtain the question
        self.math_func = self.__mathFuncDict[math_key]
        self.questionVar = tk.StringVar()
        self.questionVar.set(self.math_func())

        # Label for question
        self.questionLbl = tk.Label(self.topLevel, text=self.questionVar.get(), bg="#80ff80", font=(self.font_name, 60, "bold"))
        self.questionLbl.grid(row=1, columnspan=3, pady=30)

        # Label displays if user was correct/wrong
        self.was_correct_var = tk.StringVar()
        self.was_correct_lbl = tk.Label(self.topLevel, textvariable=self.was_correct_var, bg="#80ff80", fg="midnight blue", font=(self.font_name, 20, "bold"))
        self.was_correct_lbl.grid(row=2, columnspan=3, pady=20)

        # User entry box
        self.user_entry = tk.StringVar()
        self.entry = ttk.Entry(self.topLevel, textvariable=self.user_entry)
        self.entry.grid(row=3, column=0, columnspan=3)
        self.entry.delete(0, 'end')
        self.entry.focus()

        # Entry button
        entryBtn = ttk.Button(self.topLevel, text="ENTER", command=self.check_answer)
        entryBtn.grid(row=4, column=0, columnspan=3)

        # Return home
        goHomeButton = ttk.Button(self.topLevel, text="Back", command=self.go_home)
        goHomeButton.grid(row=5, column=0, columnspan=3)

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
        self.pack(fill="none", expand=True)

        self.master = master
        self.master.configure(background="#80ff80")
        self.font_name = "Tahoma"
        self.button_names = ["Addition", "Subtraction", "Multiplication",
                            "Division", "Random Sums", "Quit"]
        self.geom_string = "1000x500+200+50"

        # Initialise instance variables
        self.__startMin = 1
        self.__startMax = 4
        self.__maxLevel = 10
        self.__minBound = self.__startMin
        self.__maxBound = self.__startMax
        
        # Dictionary of function names
        self.__mathFuncDict = {1: self.get_add_question, 2: self.get_sub_question, 3: self.get_mult_question, 
                               4: self.get_div_question, 5: self.randSums, 6: quit}

        self.__consecutiveRight = 0
        self.__consecutiveWrong = 0


        # Display menu to user + obtain user input
        #self.displayMenu()

        self.master.title("Maths Game")
        self.master.geometry(self.geom_string)
        self.master.resizable(width=False, height=False)

        self.style = ttk.Style()
        self.style.configure("Home.TFrame",
                             background="blue")
        self.style.configure("Title.TLabel",
                        font=self.font_name + " 50 bold",
                        foreground="medium blue",
                        background="#80ff80")
        self.style.configure("Option.TButton",
                        foreground="medium blue",
                        background="#80ff80",
                        font=self.font_name + " 18 bold",
                        padding=(10,50,10,50))

        self.titleLabel = tk.Label(self, text="Maths Game!", bg="#80ff80", fg="medium blue", font=(self.font_name, 50, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=6, pady=30)
        self.titleLabel.grid_columnconfigure(0, weight=1)

        self.selectLabel = tk.Label(self, text="Select an option:", bg="#80ff80", fg="medium blue", font=(self.font_name, 35, "bold"))
        self.selectLabel.grid(row=1, column=0, columnspan=6, pady=30)

        # Loop to initialise buttons
        for i in range(1,6):

            # Lambda command for each button - call relevant function
            button = ttk.Button(self, text="%s" % self.button_names[i-1], style="Option.TButton",
                                command=lambda key=i: self.open_answer_window(key)) 
            button.grid(row=2, column=i-1, padx=1, columnspan=1)

        button = ttk.Button(self, text="Quit", command=quit, style="Option.TButton").grid(row=2, column=5, padx=1)

    def getOperands(self):
        return [self.getNextRand(), self.getNextRand()]

    def randSums(self):
        randOperator = random.randint(1,4)
        self.__mathFuncDict[randOperator]()

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
        # Get 2 numbers and prompt user
        while True:
            operands = self.getOperands()
            result = operands[0] / operands[1]
            if result == int(result):
                break

        self.answer = operands[0] / operands[1]
        question = str(operands[0]) + " / " + str(operands[1]) + " = ?"
        return question

    def check_answer(self):

        entry = self.user_entry.get()
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

                self.was_correct_var.set("Not right, the correct answer is: " + str(int(self.answer)))

        except (ValueError):
            self.was_correct_var.set("Enter a whole number!")

        self.update_top_level()
       
    def getNextRand(self):
        return random.randint(self.__minBound, self.__maxBound)

    # print("\nPlease enter a number between 1 and 6.\n")
    # print("\nPlease enter a whole number.\n")

# Main function to create a new MathGame instance
def main():
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

