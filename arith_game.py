import shelve
from func_timeout import *
import time
import copy
from pathlib import Path
from tabulate import tabulate
import secrets

"""
@class User: Keeps the player's info.
@class Question: Forms the question.
@class GameMode: Extends the behaviour of the Question class according to specific game mode.
@class Answer: Extends the GameMode class to check user's response and show the correct answer.
@class Scoreboard: Extends the User class to store score and high scores.
@class Game: Combines all objects to play game.
@class AboutGame: Shows the game guidelines.
@exception FunctionTimedOut: Exception raised when Question times out.
 """


class User:
    """
    A class that gets user's name and initializes score.

    :param name <str>: The user's name.
    """

    # Get the user's name  and initialize score
    def __init__(self, name):
        """
        The constructor of the User class

        Initializes and keeps user info of name and score.

        :param name <str>: The player's name
        """""
        self.name = name
        self.score = 0

    # show object as a string of player's name and score
    def __str__(self):
        """ :returns rep <str>: Returns a string of user's name and score """

        rep = self.name + " : " + str(self.score)
        return rep


# Generate question
class Question:
    """
    A class that generates question according to game difficulty level .

    :param level_list <list>: A list of the number of digits for
                             the first and second numbers for game level .

    @method count: Method that counts the number of digits of a number.
    @method make_num: Method that  generates two random numbers of specific digits.
    @method get_question: Method that generates and asks questions.
    """
    def __init__(self, level_list):
        """
        Constructor for Question class.

        Instantiates make_num.

       :param level_list <list>: A list of the number of digits for
                                  the first and second numbers for game level .
        """

        self.level_list = level_list
        self.nums = self.make_num()  # Instantiate  make_num
        self.response = None
        self.ques = None
        self.operator = None
        self.num1 = self.num2 = None

    # Count the Number of digits
    @staticmethod
    def count(num):
        """
        Method that counts the number of digits of a number.

        :param num:<int>: The number whose digits is to be counted.

        :return num_of_digits<int>: Returns the number of digits.
        """
        num_of_digits = 0
        for i in str(num):
            num_of_digits += 1
        return num_of_digits

    # Generate two numbers of specific digits
    def make_num(self):
        """
           Method that  generates two random numbers of specific digits.

           :return num1, num2: Returns two numbers of specified digits.
        """
        digit1, digit2 = (i for i in self.level_list)
        num1 = num2 = None

        while (num1 and num2) == 0 or digit1 != self.count(num1) or digit2 != self.count(num2):
            num1 = secrets.randbelow(10000)
            num2 = secrets.randbelow(10000)
        return num1, num2

    # Generate and ask question
    def get_question(self):
        """
        Method that generates and asks questions.

        :return response:<str>: returns the user's response
        """
        operators = ["+", "-", "x", "\u00F7"]
        operator = secrets.choice(operators)
        self.operator = copy.deepcopy(operator)
        num1, num2 = self.make_num()
        if operator == "\u00F7":
            while num1 % num2 != 0:
                num1, num2 = self.make_num()
        self.num1 = copy.deepcopy(num1)
        self.num2 = copy.deepcopy(num2)
        quest = "Solve: {} {} {}".format(num1, operator, num2)
        if self.response == "None":
            response = (input(quest + "\n Press the Enter key to enter response below: "))
        else:
            response = (input(quest + "\n Enter response here: "))
        return response


# Extend question for each game mode
class GameMode(Question):
    """"
    A class that extends Question class for each game mode

    @method classic_quest: A method to display questions for classic mode.
    @method arcade_quest: A method to display questions for arcade mode.
    """

    # Display question for classic mode
    def classic_quest(self):
        """"
        Method to display questions for classic game mode

        Gets user's response.

        :return response<str>: Returns question for classic mode.
        """
        self.response = self.get_question()
        return self.response

    def arcade_quest(self, quest_time):
        """"
        Method to display questions for classic game mode

        Gets user's response.

        :return response<str>: Returns question for arcade mode.
        """
        try:
            self.response = func_timeout(quest_time, self.get_question,)
        except FunctionTimedOut:
            print("Your time has elapsed")
            self.response = "None"
        return self.response


# cross check answers
class Answer(GameMode):
    """
    Cross checks user's answers to award points and show answers

    @method get_get_answer: A method to generate answer to question.
    @method show_answer: A method to show correct answer.
    """

    # Generate answer
    def get_answer(self):
        """
        A method to generate answer to question.

        :return answer<str>: Returns the answer to question in string format.
        """
        num1 = self.num1
        num2 = self.num2

        if self.operator == "+":
            answer = num1 + num2
        elif self.operator == "-":
            answer = num1 - num2
        elif self.operator == "x":
            answer = num1 * num2
        else:
            answer = num1 // num2
        answer = str(answer)
        return answer

    # Check if user's response is correct
    def check_answer(self):
        """ Checks if the player's response is right or wrong.

        :returns:<boolean> Returns True if player is right or False if player is wrong"""

        if self.response == self.get_answer():
            return True
        return False

    # Print the correct answer
    def show_answer(self):
        """Shows the correct answer if the player's response is wrong."""

        if self.check_answer():
            print("Correct!")

        else:
            print("Wrong, the right answer is: {}".format(self.get_answer()))


# Manage player's score
class ScoreBoard(User):
    """
    Extends the User class to save scores and high scores.

    @method update_score: Increases player's score.
    @staticmethod  file_path: Generates path to the file that stores the high score of GameModes' levels.
    @method upload_score: Uploads score to GameMode's file.
    @staticmethod high_scores: Prints the top 5 high score values in the GameMode's file.
    @method show_score: Shows the player's current score.
    @method final_high_score: Extends high_score to Show the player's final score and high score.
    """

    # Increase player's score for correct response
    def update_score(self, answer):
        """
        Increases player's score

        Increases the player's score by 1 point if they answer the question correctly.
        """

        if answer.check_answer():
            self.score += 1

    # Generate  file path to store scores
    @staticmethod
    def file_path(game_mode, level):
        """
        Generates path to the file that stores the scores.

        creates new Game level folder and file for scores if non exists.

        :param game_mode:<str>: folder  for GameMode.
        :param level:<str>: folder for game level.

        :return: file<str>: Returns the file path as file in str format.
        """
        data_folder = Path("high_score_DB/" + game_mode)
        data_folder.mkdir(parents=True, exist_ok=True)
        file = str(data_folder) + "/" + level
        return file

    # Add player's score to  file
    def upload_score(self, game_mode, level):
        """
         Uploads player's score to  scoreboard.

        :param game_mode:<str>: folder  for GameMode.
        :param level:<str>: folder  for game level.
        """

        file = ScoreBoard.file_path(game_mode, level)
        scoreboard = shelve.open(file)
        scoreboard[self.name] = self.score
        print("Score uploaded!")

    # Print the top 5 high scores
    @staticmethod
    def high_scores(game_mode, level):
        """
        Prints the top 5 high score values in GameMode file.


        :param game_mode:<str>: file name for GameMode.
        :param level:<str>: file name for game level

        :return: high_score_values<list> : Returns a list of the 5 highest score values.
        """
        file = ScoreBoard.file_path(game_mode, level)
        scoreboard = shelve.open(file)
        high_scores = sorted(scoreboard.items(), reverse=True, key=lambda x: x[1])[:5]
        high_score_values = []
        print(tabulate(high_scores, headers=['Name', 'Score'], tablefmt='orgtbl'))
        for e_score in high_scores:
            high_score_values.append(e_score[1])
        scoreboard.close()
        return high_score_values

    # Show the player's score
    def show_score(self):
        """
        Shows the player's current score.

        :return score:<int>: Returns player's scores
        """
        print("{}: current score: {}".format(self.name, self.score))
        return self.score

    # Print the high score
    # Print the player's high score position if score is in high score
    def final_high_score(self, game_mode, level):
        """"
         Prints the top 5 high score of the GameMode's file.

         Prints the player's high score position if score is in top 5 scores.
         Congratulates the player if they make the high score.
         Shows the player how many points they were off an high score position
          if they don't make high score.

         :param game_mode:<str>: folder for GameMode.
         :param level:<str>: folder  for game level
        """

        print("\n Game Completed \n Your Final Score is: {}".format(self.score))
        high_scores_values = ScoreBoard.high_scores(game_mode, level)
        high_score_position = ["1st", "2nd", "3rd", "4th", "5th"]
        if self.score in high_scores_values:
            high_score_index = high_scores_values.index(self.score)
            print("""Congratulations! {}  
You are {} in High scores""".format(self.name, high_score_position[high_score_index]))

        else:
            difference = high_scores_values[-1] - self.score
            print("Jumble Completed \n Your Final Score is: {}".format(self.score))
            print("You are {} points short of an High score position".format(difference))


# Play game
class Game(object):
    """
    Combines all objects to play game.

    :param: name<str>: Player's name.
    :param game_mode:<str>: folder for GameMode.
    :param level:<str>: folder  for  game level

    @method play_game - Method to play Game.
    """

    # Instantiate classes to play game
    def __init__(self, name, game_mode, level):
        """
        Constructor for Game class.

        Instantiates Answer(GameMode) and ScoreBoard(User) classes

        :param name<str>: Player's name
        :param game_mode:<str>: file name for GameMode
        """

        self.game_mode = game_mode
        self.level = level
        LEVELS = {"level_1": [2, 1],
                  "level_2": [2, 2],
                  "level_3": [3, 2],
                  "level_4": [3, 3],
                  "level_5": [4, 3]}
        self.answer = Answer(LEVELS[level])
        self.scoreboard = ScoreBoard(name)

    # Play game
    def play_game(self):
        """
        Method that combines objects to play game.

        Extends the objects to play jumble word game.
        """
        quest_time = 20
        counter = 0
        while counter < 15:
            print("Question: ", counter+1)
            if self.game_mode == "classic":
                self.answer.classic_quest()
            else:
                self.answer.arcade_quest(quest_time)
            self.answer.show_answer()
            self.scoreboard.update_score(self.answer)
            self.scoreboard.show_score()
            counter += 1
            print()
        time.sleep(2)
        self.scoreboard.upload_score(self.game_mode, self.level)
        self.scoreboard.final_high_score(self.game_mode, self.level)


# Print game guidelines
class AboutGame:
    def __str__(self):
        """
        A class that shows the game guidelines.

        :return about<str>: Returns a string of the game guidelines
        """

        about = ("""        This is an  Arithmetic game that displays questions on the four basic operations.
        The game has 2 main game modes, the classic and arcade modes.
       
        
         User is to answer  15 questions in each game mode and awards 1 point for each correctly answered question.
         There are 5 difficulty levels for each game mode depending on the user's grade level.
         
         The user is given a time limit to answer questions in the arcade mode.
         
         Users are not awarded any point for wrong answers questions with elapsed time.

        
       After the each completed game mode, the player is shown the final score and congratulated if they make 
       the high score or shown how far off they were if they don't.
    """)
        return about
