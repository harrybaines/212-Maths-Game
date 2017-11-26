__author__ = "Harry Baines"

import random
from enum import Enum

class MathType(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4

# Class to represent a game
class Game:

    __minBound = 1
    __maxBound = 4

    __correctAnswers = 0
    __options = [i for i in range(1,7)]

    # Constructor to initialise a new game
    def __init__(self):

        # Display menu to user + obtain user input
        self.displayMenu()

    def displayMenu(self):

        print("\nSelect one of the following options:\n")
        print("(1) Addition (2) Subtraction (3) Multiplication (4) Division (5) Random sums (6) Quit\n")
 
        # Get user input from menu
        opt = self.getMenuOpt()

        # Call function relevant to user selection
        if opt == 1:
            self.add()
        elif opt == 2:
            self.sub()
        elif opt == 3:    
            self.mult()
        elif opt == 4:
            self.div()
        elif opt == 5:
            self.add()
        else:
            quit()

    def add(self):
        while (True):
            # Get 2 numbers and prompt user
            firstNum = self.getNextRand()
            secondNum = self.getNextRand()
            answer = firstNum + secondNum
            print("\nWhat is " + str(firstNum) + "+" + str(secondNum) + "?")
            self.checkAnswer(answer)

    def sub(self):
        while (True):
            # Get 2 numbers and prompt user
            firstNum = self.getNextRand()
            secondNum = self.getNextRand()
            answer = firstNum - secondNum
            print("\nWhat is " + str(firstNum) + "-" + str(secondNum) + "?")
            self.checkAnswer(answer)

    def mult(self):
        while (True):
            # Get 2 numbers and prompt user
            firstNum = self.getNextRand()
            secondNum = self.getNextRand()
            answer = firstNum * secondNum
            print("\nWhat is " + str(firstNum) + "x" + str(secondNum) + "?")
            self.checkAnswer(answer)

    def div(self):
        while (True):
            # Get 2 numbers and prompt user
            firstNum = self.getNextRand()
            secondNum = self.getNextRand()
            answer = firstNum / secondNum
            print("\nWhat is " + str(firstNum) + "/" + str(secondNum) + "?")
            self.checkAnswer(answer)


    def checkAnswer(self, answer):
        # Check for correct answer and if they're carrying on
        if self.getUserInput() == answer:
            print("\n\033[1m That is correct, well done! \033[0m")
            self.__correctAnswers += 1
        else:
            print("\n\033[1m Not right, the correct answer is: " + str(answer) + "\033[0m")

        # Display menu again if user wants to change option
        if not(self.isCarryingOn()):
            self.displayMenu()

    def getUserInput(self):
        while True:
            try:
                answer = int(input("> "))
                break
            except ValueError:
                print("\nPlease enter a number.\n")
        return answer
       
    def isCarryingOn(self):
        print("\nPress Y to try another sum or N to stop.")
        while True:
            try:
                carryOn = input("> ").lower()
                if carryOn not in ("y", "n"):
                    print("\nPlease enter Y or N.")    
                    continue
                break
            except ValueError:
                print("\nPlease enter Y or N.") 

        if carryOn == "y":
            return True
        else:
            return False

    def getNextRand(self):
        return random.randint(self.__minBound, self.__maxBound)

    def incRange(self):
        self.__maxBound += 1

    def getMenuOpt(self):
        opt = 0
        while True:
            try:
                opt = int(input("> "))
                if opt not in self.__options:
                    print("\nPlease enter a number between 1 and 6.\n")
                    continue
                break
            except ValueError:
                print("\nPlease enter a number.\n")
        return opt

# Main function to create a new game instance
def main():
    g = Game()

if __name__ == "__main__":
    main()