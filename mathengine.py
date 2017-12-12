__author__ = "Harry Baines"

import random
import time

"""
This module ...
"""

class MathEngine(object):

    """ This class provides a simple implementation of an answer window
        displayed to the user and uses Toplevel on top of the master window. 
        An instance of this class is created once the user has selected a game 
        mode on the home screen in the HomeFrame class. """

    def __init__(self, entry_win):
        """ This ... 

        """

        # Source instance of user entry
        self.entry_win = entry_win

        # Math variables to monitor player
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

    def time_attack(self):
        """
        Returns a question string based on a random mathematical operator (+, -, *, /).
        Random questions are generated within the maximum time specified (e.g. 15 seconds).

        Returns:
            the random mathematical operator question string.
        """
        if not self.begun_time_attack:
            self.sec = self.start_time
            self.entry_win.set_info_var("Random sums in 15 seconds!")
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
            self.entry_win.set_info_var("Get one wrong, you lose!")
            self.begun_unlimited = True

        # Ask next question if correct
        if self.correct:
            return self.get_rand_operator()

    def get_rand_operator(self):
        """
        Returns a question string based on a random mathematical operator (+, -, *, /).
        This method is used in the random sums, time attack and unlimited game modes.

        Returns:
            the random mathematical operator question string.
        """
        rand_operator = random.randint(1,4)
        return self.math_func_dict[rand_operator]()

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

    def update_timer(self):
        """
        Updates the timer by 1 second and is used in the time attack game mode.
        """
        self.entry_win.set_time("Time: " + str(self.sec))
        self.sec -= 1
        self.entry_win.after(1000, self.update_timer)

        # Return home if finished
        if self.sec == -1:
            self.entry_win.go_home()
            self.sec = self.start_time
            if self.total_right != 0:
                self.entry_win.display_summary("You got " + str(self.total_right) + " answer(s) correct in " + str(self.start_time) + " seconds!")

    def check_answer(self):
        """
        Checks the user entry against a pre-calculated answer from the randomly generated operands.

        Raises:
            ValueError: if the entry is not a whole number.
        """
        entry = self.entry_win.get_user_entry()
        try:
            # User gets question right if entry is whole number
            if int(entry) == self.answer:
                self.correct = True
                self.entry_win.set_result_str("That is correct, well done!")

            # User gets question wrong
            else:
                self.correct = False
                self.entry_win.set_result_str("Not right, the correct answer was: " + str(int(self.answer)))

        except ValueError:
            self.correct = False
            self.entry_win.set_result_str("Not right, enter a whole number!")

        # Update consecutive and total variables
        if self.correct:
            self.consec_right += 1
            self.consec_wrong = 0
            self.total_right += 1

            # Dynamically increase level
            if (self.consec_right % 3 == 0) and (self.max_bound != self.max_level):
                self.max_bound += 1
        else:
            self.consec_wrong += 1
            self.consec_right = 0
            self.total_wrong += 1
            
            # Dynamically decrease level
            if (self.consec_wrong % 3 == 0) and (self.max_bound != self.start_max):
                self.max_bound -= 1

        # Go home or carry on depending on selected game mode
        if not self.correct and self.begun_unlimited:
            self.entry_win.go_home()
        else:
            self.entry_win.update_top_level()

    def should_display_info(self):
        # Display summary window for modes other than time attack
        if (not self.begun_time_attack and (self.total_right != 0 or self.total_wrong != 0)):
            return True

        return False

    def get_total_right(self):
        return self.total_right

    def get_total_wrong(self):
        return self.total_wrong

    def get_math_dict(self):
        return self.math_func_dict
