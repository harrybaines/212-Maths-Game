__author__ = "Harry Baines"

from mathengine import *

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

""" This module provides classes to model a simple mathamatics game aimed at 5-7 year olds.
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
        """ Constructor to initialise a new Toplevel window.

        Args:
            home: the HomeFrame object reference.
            master: the master window currently displayed.
            math_key: the key used to access relevant math mode function in the dictionary.
        """
        tk.Toplevel.__init__(self)

        # Initialise instance variables
        self._master = master
        self._master.withdraw()
        self._home = home
        self._font_name = self._home.font_name
        self._geom_string = self._home.geom_string
        self._bg_col = "#80ff80"
        
        # New math engine instance for math functionality
        self._mathengine = MathEngine(self)   

        # Window details
        self.title("Maths Game")
        self.grid_columnconfigure(1, weight=1)
        self.configure(background=self._bg_col)
        self.geometry(self._geom_string)
        self.resizable(width=False, height=False)
        self.bind('<Return>', lambda event: self._mathengine.check_answer())

        # Widget custom styling
        self._style = ttk.Style()
        self._style.configure(".", foreground="royal blue")
        self._style.configure("Enter.TButton", font=self._font_name + " 18 bold", padding=(2,20,2,20))
        self._style.configure("Back.TButton", font=self._font_name + " 14 bold", padding=5)
        self._style.configure("Entry.TEntry", font=self._font_name + " 40 bold", padding=(2,20,2,20))

        # Math type label
        self._math_type_lbl = tk.Label(self, text=self._home.button_names[math_key-1], bg=self._bg_col, fg="medium blue", font=self._font_name + " 74 bold")
        self._math_type_lbl.grid(row=0, column=0, columnspan=4)

        # Info label for user
        self._info_var = tk.StringVar()
        self._info_var.set("Answer as many as you can!")
        self._info_lbl = tk.Label(self, textvariable=self._info_var, font=self._font_name + " 26 bold", bg=self._bg_col)
        self._info_lbl.grid(row=1, column=1)

        # Time label for time attack mode
        self._time_var = tk.StringVar()
        self._time_var.set("")
        self._time_lbl = tk.Label(self, textvariable=self._time_var, font=self._font_name + " 30 bold", bg=self._bg_col, fg="red")
        self._time_lbl.grid(row=2, column=1)
        
        # Call relevant math function to obtain the question to display
        self._math_func = self._mathengine.math_func_dict[math_key]
        self._question_var = tk.StringVar()
        self._question_var.set(self._math_func())

        # Label for question
        self._questionLbl = tk.Label(self, textvariable=self._question_var, bg=self._bg_col, font=self._font_name + " 88 bold")
        self._questionLbl.grid(row=3, columnspan=4, pady=5)

        # Label displays if user was correct/wrong
        self._was_correct_var = tk.StringVar()
        self._was_correct_lbl = tk.Label(self, textvariable=self._was_correct_var, bg=self._bg_col, fg="midnight blue", font=self._font_name + " 18 bold")
        self._was_correct_lbl.grid(row=4, columnspan=4, pady=5)

        # User entry box
        self._user_entry = tk.StringVar()
        self._entry = ttk.Entry(self, textvariable=self._user_entry, style="Entry.TEntry", width=5, justify="center", font=self._font_name + " 42 bold")
        self._entry.grid(row=5, columnspan=2)
        self._entry.delete(0, 'end')
        self._entry.focus()

        # Entry button
        self._entryBtn = ttk.Button(self, text="ENTER", style="Enter.TButton", width=10, command=self._mathengine.check_answer)
        self._entryBtn.grid(row=6, columnspan=2)

        # Return home
        self._goHomeButton = ttk.Button(self, text="BACK", style="Back.TButton", command=self.go_home)
        self._goHomeButton.grid(row=7, columnspan=2, pady=5)

    def go_home(self):
        """ Returns to the HomeFrame and removes this top level window. """
        self.destroy()
        self._master.geometry(self._geom_string)
        self._master.deiconify()

        # Displays summary if necessary
        if self._mathengine.display_info:
            self.display_summary("You got:\n\n" + str(self._mathengine.total_right) + " answer(s) correct.\n" + str(self._mathengine.total_wrong) + " answer(s) wrong.")

    def display_summary(self, result_str):
        """ Displays a summary pop up window with details on how the user performed.

        Args:
            result_str: the result string to display.
        """
        tk.messagebox.showinfo("Summary", result_str)

    def update_top_level(self):
        """ Updates this top level window after a result has been checked and displayed. """
        self.user_entry = ""

        # Get next question
        self._question_var.set(self._math_func())

    @property
    def user_entry(self):
        """ Returns the user's entry from the entry box.

        Returns:
            the user's entry.
        """
        return self._user_entry.get().replace(" ","")

    @user_entry.setter
    def user_entry(self, entry_str):
        """ Empties the user entry box - used for validation inside the math engine.

        Args:
            entry_str: the string to set the user entry box to.
        """
        self._user_entry.set(entry_str)
        self._entry.focus()

    @property
    def result_str(self):
        """ Returns the string value holding text to display if the user was right or wrong.

        Returns:
            the value currently in the string variable.
        """
        return self._was_correct_var

    @result_str.setter
    def result_str(self, result_str):
        """ Mutator to set the result text to the passed parameter.

        Args
            result_str: the string to set the result string to.
        """
        self._was_correct_var.set(result_str)

    @property
    def info_var(self):
        """ Returns the info string variable for game details on this window.

        Returns:
            the string variable holding brief info.
        """
        return self._info_var

    @info_var.setter
    def info_var(self, info_str):
        """ Mutator to set the info string to the passed parameter.

        Args:
            info_str: the string to set the info variable to.
        """
        self.info_var.set(info_str)

    @property
    def time_var(self, time_str):
        """ Returns the variable holding the current time in the time attack game mode.

        Returns:
            the time currently in the string.
        """
        return self._time_var

    @time_var.setter
    def set_time(self, time_str):
        """ Returns the string value holding text to display if the user was right or wrong.

        Returns:
            the value currently in the string variable.
        """
        self._time_var.set(time_str)


class HomeFrame(tk.Frame):

    """ This class implements a simple home window which is displayed
        to the user when the program begins. An AnswerWindow instance
        will be created when the user selects a game mode. """

    def __init__(self, master):
        """ Constructor to initialise a new HomeFrame window.
        This window is displayed to the user when the program starts.

        Args:
            master: the master window to display.
        """
        self._bg_col = "#80ff80"
        tk.Frame.__init__(self, master, bg=self._bg_col)
        
        # Initialise instance variables
        self._master = master
        self._geom_string = "1200x750+200+50"
        self._font_name = "Tahoma"
        self._button_names = ["Addition", "Subtraction", "Multiplication", "Division", 
                              "Random Sums", "Time Attack", "Unlimited Mode", "Quit"]
        self._master.title("Maths Game")
        self._master.geometry(self.geom_string)
        self._master.resizable(width=False, height=False)
        self._master.configure(background=self._bg_col)
        self.pack()
        
        # Custom widget styling
        self._style = ttk.Style()
        self._style.configure("Option.TButton", foreground="royal blue", font=self._font_name + " 20 bold", padding=(20,60,20,60))

        # Home window widgets
        self._titleLabel = tk.Label(self, text="Maths Game!", bg=self._bg_col, fg="medium blue", font=self._font_name + " 50 bold")
        self._titleLabel.grid(row=0, column=0, columnspan=6, pady=20)

        self._selectLabel = tk.Label(self, text="Select an option:", bg=self._bg_col, fg="medium blue", font=self._font_name + " 28 bold")
        self._selectLabel.grid(row=1, column=0, columnspan=6, pady=20)

        # Loop to initialise all option buttons
        for i in range(1, len(self._button_names)+1):

            # Lambda command for each button - opens answer window for given game mode
            button = ttk.Button(self, text=self._button_names[i-1], style="Option.TButton",
                                command=lambda key=i: AnswerWindow(self, self._master, key)) 

            # Button placement
            row = 3 if i > 4 else 2 
            column = i-5 if i > 4 else i-1
            button.grid(row=row, column=column, padx=2, pady=2, sticky="NSEW")

        self._name_lbl = tk.Label(self, text="2017 Harry Baines", font=self._font_name + " 14", bg=self._bg_col)
        self._name_lbl.grid(row=row+1, columnspan=len(self._button_names), pady=20)

    @property
    def geom_string(self):
        """ Accessor to obtain the string of window geometry values.

        Returns:
            the geometry string.
        """
        return self._geom_string

    @property
    def font_name(self):
        """ Accessor to obtain the font name being used in the system.

        Returns:
            the font name as a string.
        """
        return self._font_name

    @property
    def button_names(self):
        """ Accessor to obtain the list of option button names corresponding to game modes.

        Returns:
            the list of option button names.
        """
        return self._button_names


# Main function to create a new HomeFrame instance
def main():
    root = tk.Tk()
    game = HomeFrame(root)
    root.mainloop()

# Program entry point
if __name__ == "__main__":
    main()
