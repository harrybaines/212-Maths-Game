__author__ = "Harry Baines"

import random

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *

class MathGame(object):

    """ This class implements various mathematical operations
    such as addition, subtraction, multiplication and division
    on a set of randomly generated operands """

    def get_sum(self, event):
        val = int(entryBox.get())
        print("Value = " + val)


    def get_data(self, event=None):
        print("String : ", self.strVar.get())
        print("Integer : ", self.intVar.get())
        print("Boolean : ", self.boolVar.get())

    def bind_button(self, event=None):
        if self.boolVar.get():
            self.getDataButton.unbind("<Button-1>")
        else:
            self.getDataButton.bind("<Button-1>", self.get_data)

    def open_msg_box(self):
        tk.messagebox.showwarning(
            "Event Triggered",
            "Button Clicked"
        )


    # Constructor to initialise a new game
    def __init__(self, root):

        root.title("Maths Game")
        root.geometry("800x400+300+300")
        root.resizable(width=True, height=False)

        frame = tk.Frame(root)

        style = ttk.Style()
        style.configure("TButton",
                        foreground="midnight blue",
                        font="Times 20 bold italic",
                        padding=20)

        self.strVar = tk.StringVar(root, value="")
        self.intVar = tk.IntVar()
        self.boolVar = tk.BooleanVar()

        strEntry = tk.Entry(frame, textvariable=self.strVar)
        strEntry.pack(side=tk.LEFT)

        strEntry = tk.Entry(frame, textvariable=self.intVar)
        strEntry.pack(side=tk.LEFT)

        print(ttk.Style().theme_names())

        ttk.Style().theme_use('clam')

        checkButton = tk.Checkbutton(frame, text="Switch", variable=self.boolVar)
        checkButton.bind("<Button-1>", self.bind_button)
        checkButton.pack(side=tk.LEFT)

        self.addButton = ttk.Button(frame, text="1. Addition", command=self.open_msg_box)
        self.subButton = ttk.Button(frame, text="1. Addition", command=self.open_msg_box)
        self.multButton = ttk.Button(frame, text="1. Addition", command=self.open_msg_box)
        self.divButton = ttk.Button(frame, text="1. Addition", command=self.open_msg_box)
        self.randButton = ttk.Button(frame, text="1. Addition", command=self.open_msg_box)
        self.randButton = ttk.Button(frame, text="1. Addition", command=self.open_msg_box)

        # self.getDataButton.bind("<Button-1>", self.get_data)
        self.getDataButton['state'] = 'disabled'
        self.getDataButton['state'] = 'normal'
        self.getDataButton.pack(side=tk.LEFT)

        frame.pack()

        # Label(root, text="Description").grid(row=0, column=0, sticky=W)
        # entryBox = Entry(root, width=50).grid(row=0, column=1)
        # changeButton = Button(root, text="Submit")
        # changeButton.grid(row=0, column=8)
        # changeButton.bind("<Button-1>", get_sum)

        # Label(root, text="Difficulty").grid(row=1, column=0, sticky=W)
        # Radiobutton(root, text="Easy", value=1).grid(row=2, column=0, sticky=W)
        # Radiobutton(root, text="Medium", value=2).grid(row=3, column=0, sticky=W)
        # Radiobutton(root, text="Hard", value=3).grid(row=4, column=0, sticky=W)
        # Radiobutton(root, text="Insane", value=4).grid(row=5, column=0, sticky=W)

        # Label(root, text="Benefits").grid(row=1, column=1, sticky=W)
        # Checkbutton(root, text="Free Shipping").grid(row=2, column=1, sticky=W)
        # Checkbutton(root, text="Bonus Gift").grid(row=3, column=1, sticky=W)

        # frame = Frame(root)
        # labelText = StringVar()

        # Label(root, text="First Name").grid(row=0, sticky=W, padx=4)
        # Entry(root).grid(row=0, column=1, sticky=E, pady=4)

        # Label(root, text="First Name").grid(row=1, sticky=W, padx=4)
        # Entry(root).grid(row=1, column=1, sticky=E, pady=4)

        # Button(root, text="Submit").grid(row=3)

        # Button(frame, text="B1").pack(side=LEFT, fill=Y)
        # Button(frame, text="B2").pack(side=TOP, fill=X)
        # Button(frame, text="B3").pack(side=RIGHT, fill=X)
        # Button(frame, text="B4").pack(side=LEFT, fill=X)

        # frame.pack()

        # Initialise instance variables
        self.__startMin = 1
        self.__startMax = 4
        self.__maxLevel = 10
        self.__minBound = self.__startMin
        self.__maxBound = self.__startMax
        
        # Dictionary of function names
        self.__mathFuncDict = {1: self.add, 2: self.sub, 3: self.mult, 
                               4: self.div, 5: self.randSums, 6: quit}

        self.__consecutiveRight = 0
        self.__consecutiveWrong = 0

        # Display menu to user + obtain user input
        #self.displayMenu()

    def displayMenu(self):

        self.__maxBound = 4
        self.__consecutiveRight = 0
        self.__consecutiveWrong = 0

        # Get user input from menu + call function relevant to user selection
        opt = self.getMenuOpt()

        # Repeat selected option
        while True:
            self.__mathFuncDict[opt]()

    def getOperands(self):
        return [self.getNextRand(), self.getNextRand()]

    def randSums(self):
        randOperator = random.randint(1,4)
        self.__mathFuncDict[randOperator]()

    def add(self):
        # Get 2 numbers and prompt user
        operands = self.getOperands()
        print("\nWhat is " + str(operands[0]) + "+" + str(operands[1]) + "?")
        self.checkAnswer(operands[0] + operands[1])

    def sub(self):
        # Get 2 numbers and prompt user
        operands = self.getOperands()

        # Flips operands if answer is -ve
        if operands[0] - operands[1] < 0:
            temp = operands[0]
            operands[0] = operands[1]
            operands[1] = temp

        print("\nWhat is " + str(operands[0]) + "-" + str(operands[1]) + "?")
        self.checkAnswer(operands[0] - operands[1])

    def mult(self):
        # Get 2 numbers and prompt user
        operands = self.getOperands()
        print("\nWhat is " + str(operands[0]) + "*" + str(operands[1]) + "?")
        self.checkAnswer(operands[0] * operands[1])

    def div(self):
        # Get 2 numbers and prompt user
        while True:
            operands = self.getOperands()
            result = operands[0] / operands[1]
            if result == int(result):
                break

        print("\nWhat is " + str(operands[0]) + "/" + str(operands[1]) + "?")
        self.checkAnswer(result)

    def checkAnswer(self, answer):

        # Check for correct answer and if they're carrying on
        if self.getUserInput() == answer:

            print("\n\033[1m That is correct, well done! \033[0m")
            self.__consecutiveRight += 1
            self.__consecutiveWrong = 0

            if (self.__consecutiveRight % 3 == 0) and (self.__maxBound != self.__maxLevel):
                self.__maxBound += 1
        else:

            print("\n\033[1m Not right, the correct answer is: " + str(int(answer)) + "\033[0m")
            self.__consecutiveWrong += 1
            self.__consecutiveRight = 0

            if (self.__consecutiveWrong % 3 == 0) and (self.__maxBound != self.__startMax):
                self.__maxBound -= 1

        # Display menu again if user wants to change option
        if not(self.isCarryingOn()):
            self.displayMenu()

    def getUserInput(self):
        while True:
            try:
                answer = int(input("> "))
                break
            except (ValueError, TypeError):
                print("\nPlease enter a whole number.\n")
        return answer
       
    def getNextRand(self):
        return random.randint(self.__minBound, self.__maxBound)

    def isCarryingOn(self):
        print("\nPress Y to try another sum or N to stop.")
        while True:
            try:
                carryOn = input("> ").lower()
                if carryOn == "y":
                    return True
                elif carryOn == "n":
                    return False
                else:
                    print("\nPlease enter Y or N.") 
            except (ValueError, TypeError):
                print("\nPlease enter a letter - Y or N.") 

    def getMenuOpt(self):
        while True:
            try:
                print("\nSelect one of the following options:\n") 
                print("(1) Addition (2) Subtraction (3) Multiplication (4) Division (5) Random sums (6) Quit\n")
                opt = int(input("> "))
                if opt in self.__mathFuncDict:
                    break
                else:
                    print("\nPlease enter a number between 1 and 6.\n")
            except (ValueError, TypeError):
                print("\nPlease enter a whole number.\n")
        return opt

# Main function to create a new MathGame instance
def main():
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

