__author__ = "Harry Baines"

import random
import time

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

"""
This module provides classes to model a simple mathamatics game aimed at 5-7 year olds.
The HomeFrame will be displayed to the user when the program begins - the user can then
select a mathematical game mode to play. An AnswerWindow will be displayed to the user
and they can input their entry. The user can go back and select another game mode if 
they wish. The game supports tailored learning and dynamically increases the level
for mathematical question generation.
"""

class AnswerWindow(tk.Toplevel):

    """ This class provides a simple implementation of an answer window
        displayed to the user and uses Toplevel on top of the master window. 
        An instance of this class is created once the user has selected a game 
        mode on the home screen in the HomeFrame class. """

    def __init__(self, home, master, math_key):
        """
        Initialises a new Toplevel window.

        Args:
            home: the HomeFrame object reference.
            master: the master window currently displayed.
            math_key: the key used to access relevant math mode function in dictionary.
        """
        tk.Toplevel.__init__(self)

        # Initialise instance variables
        self.master = master
        self.master.withdraw()
        self.home = home
        self.font_name = self.home.get_window_font()
        self.geom_string = self.home.get_geom_string()

        self.consec_right = 0
        self.consec_wrong = 0
        self.total_right = 0
        self.total_wrong = 0
        self.correct = True

        self.begun_time_attack = False
        self.begun_unlimited = False
        self.start_time = 15

        self.start_min = 1
        self.start_max = 4
        self.max_level = 10
        self.min_bound = self.start_min
        self.max_bound = self.start_max

        # Dictionary of function names
        self.math_func_dict = {1: self.get_add_question, 2: self.get_sub_question, 3: self.get_mult_question, 4: self.get_div_question, 
                               5: self.get_rand_operator, 6: self.time_attack, 7: self.unlimited_mode, 8: quit}
                               
        # Window details
        self.title("Maths Game")
        self.grid_columnconfigure(1, weight=1)
        self.configure(background="#80ff80")
        self.geometry(self.geom_string)
        self.resizable(width=False, height=False)

        # Widget custom styling
        self.style = ttk.Style()
        self.style.configure(".", foreground="royal blue")
        self.style.configure("Enter.TButton", font=self.font_name + " 18 bold", padding=(2,20,2,20))
        self.style.configure("Back.TButton", font=self.font_name + " 14 bold", padding=5)
        self.style.configure("Entry.TEntry", font=self.font_name + " 40 bold", padding=(2,20,2,20))

        # Math type label
        self.math_type_lbl = tk.Label(self, text=self.home.get_button_names()[math_key-1], bg="#80ff80", fg="medium blue", font=(self.font_name, 74, "bold"))
        self.math_type_lbl.grid(row=0, column=0, columnspan=4)

        # Info label for user
        self.info_var = tk.StringVar()
        self.info_var.set("Answer as many as you can!")
        self.info_lbl = tk.Label(self, textvariable=self.info_var, font=(self.font_name, 26, "bold"), bg="#80ff80")
        self.info_lbl.grid(row=1, column=1)

        # Time label for time attack mode
        self.time_var = tk.StringVar()
        self.time_var.set("")
        self.time_lbl = tk.Label(self, textvariable=self.time_var, font=(self.font_name, 30, "bold"), bg="#80ff80", fg="red")
        self.time_lbl.grid(row=2, column=1)
        
        # Call relevant math function to obtain the question to display
        self.math_func = self.math_func_dict[math_key]
        self.question_var = tk.StringVar()
        self.question_var.set(self.math_func())

        # Label for question
        self.questionLbl = tk.Label(self, textvariable=self.question_var, bg="#80ff80", font=(self.font_name, 88, "bold"))
        self.questionLbl.grid(row=3, columnspan=4, pady=5)

        # Label displays if user was correct/wrong
        self.was_correct_var = tk.StringVar()
        self.was_correct_lbl = tk.Label(self, textvariable=self.was_correct_var, bg="#80ff80", fg="midnight blue", font=(self.font_name, 20, "bold"))
        self.was_correct_lbl.grid(row=4, columnspan=4, pady=5) # CHANGE?

        # User entry box
        self.user_entry = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.user_entry, style="Entry.TEntry", width=5, justify="center", font=(self.font_name, 42, "bold"))
        self.entry.grid(row=5, columnspan=2)
        self.entry.delete(0, 'end')
        self.entry.focus()

        # Entry button
        self.entryBtn = ttk.Button(self, text="ENTER", style="Enter.TButton", width=10, command=self.check_answer)
        self.entryBtn.grid(row=6, columnspan=2)

        # Return home
        self.goHomeButton = ttk.Button(self, text="Back", style="Back.TButton", command=self.go_home)
        self.goHomeButton.grid(row=7, columnspan=2, pady=5)

    def go_home(self):
        """
        Returns to the HomeFrame and removes this top level window.
        """
        self.destroy()
        self.master.geometry(self.geom_string)
        self.master.deiconify()

        # Display summary window for modes other than time attack
        if (not self.begun_time_attack and (self.total_right != 0 or self.total_wrong != 0)):
            self.display_summary("You got:\n\n" + str(self.total_right) + " answer(s) correct.\n" + str(self.total_wrong) + " answer(s) wrong.")

    def display_summary(self, result_str):
        """
        Displays a summary pop up window with details on how the user performed.

        Args:
            result_str: the result string to display.
        """
        tk.messagebox.showinfo("Summary", result_str)

    def update_top_level(self):
        """
        Updates this top level window after a result has been checked and displayed.
        """
        self.user_entry.set("0")
        self.entry.delete(0, 'end')
        self.entry.focus()

        # Get next question
        self.question_var.set(self.math_func())

    def update_timer(self):
        """
        Updates the timer by 1 second and is used in the time attack game mode.
        """
        self.time_var.set("Time: " + str(self.sec))
        self.sec -= 1
        self.after(1000, self.update_timer)

        # Return home if finished
        if self.sec == -1:
            self.go_home()
            self.sec = self.start_time
            if self.total_right != 0:
                self.display_summary("You got " + str(self.total_right) + " answer(s) correct in " + str(self.start_time) + " seconds!")

    def get_operands(self):
        """
        Returns a list of 2 new randomly generated operands for use in the next mathematical equation.

        Returns:
            the list of 2 new operands.
        """
        return [self.get_next_rand(), self.get_next_rand()]

    def get_next_rand(self):
        """
        Returns a randomly generated number between the minimum and maximum bounds specified.

        Returns:
            the new randomly generated operand.
        """
        return random.randint(self.min_bound, self.max_bound)

    def check_answer(self):
        """
        Checks the user entry against a pre-calculated answer from the randomly generated operands.

        Raises:
            ValueError: if the entry is not a whole number.
        """
        entry = self.user_entry.get().replace(" ","")
        try:
            # User gets question right if entry is whole number
            if int(entry) == self.answer:
                self.consec_right += 1
                self.consec_wrong = 0
                self.total_right += 1
                self.correct = True
                self.was_correct_var.set("That is correct, well done!")

                # Dynamically increase level
                if (self.consec_right % 3 == 0) and (self.max_bound != self.max_level):
                    self.max_bound += 1

            # User gets question wrong
            else:
                self.consec_wrong += 1
                self.consec_wrong = 0
                self.total_wrong += 1
                self.correct = False
                self.was_correct_var.set("Not right, the correct answer was: " + str(int(self.answer)))

                # Dynamically decrease level
                if (self.consec_wrong % 3 == 0) and (self.max_bound != self.start_max):
                    self.max_bound -= 1

        except ValueError:
            self.correct = False
            self.was_correct_var.set("Not right, enter a whole number!")
            self.total_wrong += 1
            
        # Go home or carry on depending on selected game mode
        if not self.correct and self.begun_unlimited:
            self.go_home()
        else:
            self.update_top_level()

    """
    GAME MODE FUNCTIONS
    """
    def get_add_question(self):
        """
        Returns a mathematical question string based on addition.

        Returns:
            the addition question string.
        """
        operands = self.get_operands()
        self.answer = operands[0] + operands[1]
        question = str(operands[0]) + " + " + str(operands[1]) + " = ?"
        return question

    def get_sub_question(self):
        """
        Returns a mathematical question string based on subtraction.
        If the calculated result is negative, the operands are flipped.

        Returns:
            the subtraction question string.
        """
        operands = self.get_operands()

        # Flips operands if answer is -ve
        if operands[0] - operands[1] < 0:
            temp = operands[0]
            operands[0] = operands[1]
            operands[1] = temp

        self.answer = operands[0] - operands[1]
        question = str(operands[0]) + " - " + str(operands[1]) + " = ?"
        return question

    def get_mult_question(self):
        """
        Returns a mathematical question string based on multiplication.

        Returns:
            the multiplication question string.
        """
        operands = self.get_operands()
        self.answer = operands[0] * operands[1]     # could be changed (get_question()?)
        question = str(operands[0]) + " x " + str(operands[1]) + " = ?" # could be changed
        return question

    def get_div_question(self):
        """
        Returns a mathematical question string based on division.
        If the calculated result is a decimal, the operands are re-calculated.

        Returns:
            the division question string.
        """
        while True:
            operands = self.get_operands()
            result = operands[0] / operands[1]
            if result == int(result):
                break

        self.answer = operands[0] / operands[1]
        question = str(operands[0]) + " / " + str(operands[1]) + " = ?"
        return question

    def get_rand_operator(self):
        """
        Returns a question string based on a random mathematical operator (+, -, *, /).
        This method is used in the random sums, time attack and unlimited game modes.

        Returns:
            the random mathematical operator question string.
        """
        rand_operator = random.randint(1,4)
        return self.math_func_dict[rand_operator]()

    def time_attack(self):
        """
        Returns a question string based on a random mathematical operator (+, -, *, /).
        Random questions are generated within the maximum time specified (e.g. 15 seconds).

        Returns:
            the random mathematical operator question string.
        """
        if not self.begun_time_attack:
            self.sec = self.start_time
            self.info_var.set("Random sums in 15 seconds!")
            self.begun_time_attack = True
            self.update_timer()

        return self.get_rand_operator()

    def unlimited_mode(self):
        """
        Returns a question string based on a random mathematical operator (+, -, *, /).
        Random questions are generated provided the user is consecutively answering questions correctly.

        Returns:
            the random mathematical operator question string.
        """
        if not self.begun_unlimited:
            self.info_var.set("Get one wrong, you lose!")
            self.begun_unlimited = True

        if self.correct:
            return self.get_rand_operator()


class HomeFrame(tk.Frame):

    """ This class implements a simple home window which is displayed
        to the user when the program begins. An AnswerWindow instance
        will be created when the user selects a game mode. """

    def __init__(self, master):
        """
        Initialises a new HomeFrame window.
        This window is displayed to the user when the program starts.

        Args:
            master: the master window to display.
        """
        tk.Frame.__init__(self, master, bg="#80ff80")
        
        # Initialise instance variables
        self.master = master
        self.master.title("Maths Game")
        self.geom_string = "900x550+200+50"
        self.master.geometry(self.geom_string)
        self.master.resizable(width=False, height=False)
        self.master.configure(background="#80ff80")
        self.pack()

        self.font_name = "Tahoma"
        self.button_names = ["Addition", "Subtraction", "Multiplication", "Division", 
                             "Random Sums", "Time Attack", "Unlimited Mode", "Quit"]

        # Custom widget styling
        self.style = ttk.Style()
        self.style.configure("Option.TButton", foreground="royal blue", font=self.font_name + " 20 bold", padding=(20,60,20,60))

        # Home window widgets
        self.titleLabel = tk.Label(self, text="Maths Game!", bg="#80ff80", fg="medium blue", font=(self.font_name, 50, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=6, pady=20)

        self.selectLabel = tk.Label(self, text="Select an option:", bg="#80ff80", fg="medium blue", font=(self.font_name, 28, "bold"))
        self.selectLabel.grid(row=1, column=0, columnspan=6, pady=20)

        # Loop to initialise all option buttons
        for i in range(1, len(self.button_names)+1):

            # Lambda command for each button - opens answer window for given game mode
            button = ttk.Button(self, text=self.button_names[i-1], style="Option.TButton",
                                command=lambda key=i: AnswerWindow(self, self.master, key)) 

            # Button placement
            row = 3 if i > 4 else 2 
            column = i-5 if i > 4 else i-1
            button.grid(row=row, column=column, padx=2, pady=2, sticky="NSEW")

        self.name_lbl = tk.Label(self, text="2017 Harry Baines", font=(self.font_name, 14), bg="#80ff80")
        self.name_lbl.grid(row=row+1, columnspan=len(self.button_names), pady=20)

        self.master.mainloop()

    def get_geom_string(self):
        """
        Accessor to obtain the string of window geometry values.

        Returns:
            the geometry string.
        """
        return self.geom_string

    def get_window_font(self):
        """
        Accessor to obtain the font name being used in the system.

        Returns:
            the font name as a string.
        """
        return self.font_name

    def get_button_names(self):
        """
        Accessor to obtain the list of option button names corresponding to game modes.

        Returns:
            the list of option button names.
        """
        return self.button_names


# Main function to create a new HomeFrame instance
def main():
    root = tk.Tk()
    game = HomeFrame(root)

# Program entry point
if __name__ == "__main__":
    main()
