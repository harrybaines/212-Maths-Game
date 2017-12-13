__author__ = "Harry Baines"

import random
import time

""" This module provides an engine which implements simple mathamatics aimed at 5-7 year olds.
Once the user has selected a mathematical game mode to play, an AnswerWindow will be displayed 
to the user and they can input their entry. The user can go back and select another game mode if 
they wish. The game supports tailored learning and dynamically increases the level
for mathematical question generation.
"""

class MathEngine(object):

    """ This class provides methods for each mathematical game mode that a user
        could select. Values are randomly generated for the operands in the
        equation. This class can send and receive data from the relevant
        'entry_win' window to update UI changes depending on current state. """

    def __init__(self, entry_win):
        """  Constructor to initialise a new MathEngine instance.

        Args:
            entry_win: the window instance reference to make UI changes.
        """

        # Source instance of user entry
        self._entry_win = entry_win

        # Math variables to monitor player
        self._start_min = 1
        self._start_max = 4
        self._max_level = 10
        self._min_bound = self._start_min
        self._max_bound = self._start_max

        self._consec_right = self._consec_wrong = 0
        self._total_right = self._total_wrong = 0
        self._correct = True

        self._begun_time_attack = False
        self._begun_unlimited = False
        self._start_time = 15

        # Dictionary of function names
        self._math_func_dict = {1: self.get_add_question, 2: self.get_sub_question, 3: self.get_mult_question, 4: self.get_div_question, 
                                5: self.get_rand_operator, 6: self.time_attack, 7: self.unlimited_mode, 8: quit}

    def get_add_question(self):
        """ Returns a mathematical question string based on addition.

        Returns:
            the addition question string.
        """
        operands = self.get_operands()
        self._answer = operands[0] + operands[1]
        question = str(operands[0]) + " + " + str(operands[1]) + " = ?"
        return question

    def get_sub_question(self):
        """ Returns a mathematical question string based on subtraction.
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

        self._answer = operands[0] - operands[1]
        question = str(operands[0]) + " - " + str(operands[1]) + " = ?"
        return question

    def get_mult_question(self):
        """ Returns a mathematical question string based on multiplication.

        Returns:
            the multiplication question string.
        """
        operands = self.get_operands()
        self._answer = operands[0] * operands[1]
        question = str(operands[0]) + " x " + str(operands[1]) + " = ?"
        return question

    def get_div_question(self):
        """ Returns a mathematical question string based on division.
        If the calculated result is a decimal, the operands are re-calculated.

        Returns:
            the division question string.
        """
        while True:
            operands = self.get_operands()
            result = operands[0] / operands[1]
            if result == int(result):
                break

        self._answer = operands[0] / operands[1]
        question = str(operands[0]) + " / " + str(operands[1]) + " = ?"
        return question

    def time_attack(self):
        """ Returns a question string based on a random mathematical operator (+, -, *, /).
        Random questions are generated within the maximum time specified (e.g. 15 seconds).

        Returns:
            the random mathematical operator question string.
        """
        if not self._begun_time_attack:
            self._sec = self._start_time
            self._entry_win.info_var = "Random sums in 15 seconds!"
            self._begun_time_attack = True
            self.update_timer()

        return self.get_rand_operator()

    def unlimited_mode(self):
        """ Returns a question string based on a random mathematical operator (+, -, *, /).
        Random questions are generated provided the user is consecutively answering questions correctly.

        Returns:
            the random mathematical operator question string.
        """
        if not self._begun_unlimited:
            self._entry_win.info_var = "Get one wrong, you lose!"
            self._begun_unlimited = True

        # Ask next question if correct
        if self._correct:
            return self.get_rand_operator()

    def get_rand_operator(self):
        """ Returns a question string based on a random mathematical operator (+, -, *, /).
        This method is used in the random sums, time attack and unlimited game modes.

        Returns:
            the random mathematical operator question string after calling relevant math operator method.
        """
        rand_operator = random.randint(1,4)
        return self._math_func_dict[rand_operator]()

    def get_operands(self):
        """ Returns a list of 2 new randomly generated operands for use in the next mathematical equation.

        Returns:
            the list of 2 new operands.
        """
        return [self.get_next_rand(), self.get_next_rand()]

    def get_next_rand(self):
        """ Returns a randomly generated number between the minimum and maximum bounds specified.

        Returns:
            the new randomly generated operand.
        """
        return random.randint(self._min_bound, self._max_bound)

    def update_timer(self):
        """ Updates the timer by 1 second and is used in the time attack game mode.
        """
        self._entry_win.set_time = "Time: " + str(self._sec)
        self._sec -= 1
        self._entry_win.after(1000, self.update_timer)

        # Return home if finished and reset relevant variables
        if self._sec == -1:
            self._entry_win.go_home()
            self._sec = self._start_time
            if self._total_right != 0:
                self._entry_win.display_summary("You got " + str(self._total_right) + " answer(s) correct in " + str(self._start_time) + " seconds!")

    def check_answer(self):
        """ Checks the user entry against a pre-calculated answer from the randomly generated operands.

        Raises:
            ValueError: if the entry is not a whole number.
        """
        entry = self._entry_win.user_entry
        try:
            # User gets question right if entry is whole number
            if int(entry) == self._answer:
                self._correct = True
                self._entry_win.result_str = "That is correct, well done! (Press BACK to stop)"

            # User gets question wrong
            else:
                self._correct = False
                self._entry_win.result_str = "Not right, the correct answer is: " + str(int(self._answer)) + " (Press BACK to stop)"

            self.monitor_level()

        except ValueError:
        	# Inform user of invalid input - clear entry and retry
            self._entry_win.result_str = "Not right, enter a whole number! (Press BACK to stop)"
            self._entry_win.user_entry = ""

    def monitor_level(self):
        """ Monitors the current level the user is on.
        Answering 3 questions correctly in a row increases the maximum bound for random number generation.
        Answering 3 questions incorrectly in a row decreases the maximum bound for random number generation.
        Max level = 1-10, min level = 1-4
        """

        # Update consecutive and total variables
        if self._correct:
            self._consec_right += 1
            self._consec_wrong = 0
            self._total_right += 1

            # Dynamically increase level
            if (self._consec_right == 3) and (self._max_bound != self._max_level):
                self._max_bound += 1
                self._consec_right = 0
        else:
            self._consec_wrong += 1
            self._consec_right = 0
            self._total_wrong += 1
            
            # Dynamically decrease level
            if (self._consec_wrong == 3) and (self._max_bound != self._start_max):
                self._max_bound -= 1
                self._consec_wrong = 0

        # Go home or carry on depending on selected game mode
        if (not self._correct and self._begun_unlimited):
            self._entry_win.go_home()
        else:
            self._entry_win.update_top_level()

    @property
    def display_info(self):
        """ Determines if info window should be displayed to the user once game mode has finished.

        Returns:
            True if the window should be displayed.
            False if the window shouldn't be displayed.
        """
        if (not self._begun_time_attack and (self._total_right != 0 or self._total_wrong != 0)):
            return True
        return False

    @property
    def total_right(self):
        """ Returns the total number of questions answered correctly by the user.

        Returns:
            the total number of correct answers.
        """
        return self._total_right

    @property
    def total_wrong(self):
        """ Returns the total number of questions answered incorrectly by the user.

        Returns:
            the total number of incorrect answers.
        """
        return self._total_wrong

    @property
    def math_func_dict(self):
        """ Returns the dictionary of key-value pairs for mathematical functions.

        Returns:
            the dictionary of mathametical functions.
        """
        return self._math_func_dict
