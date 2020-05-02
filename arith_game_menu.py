from arithmetic_game.arith_game import *  # import all game attributes

""""
@function main: Combines the  Menu  and Game classes  to play game.
@class Menu: Sets the menu for the game.
"""


# Display game menu
class Menu(ScoreBoard):
    """"
    Displays the main menu for the game.

    :param name<str>: user's name.

    @method main_menu: Displays the  Game's main menu.
    @method game_mode: Displays the GameMode menu.
    """

    # Instantiate player name and score
    def __init__(self, name):
        """"
        Constructor for Menu class.

        :param name<str>: user's name.

        Gets user's name and initializes score.
        Extends the Scoreboard class' constructor.
        """
        super().__init__(name)
        self.option = None

    # Display the Game's main menu
    def main_menu(self):
        """
        Displays  GameMode menu.

        Gets the user's menu option

        :return option<str>: Returns user's choice
        """
        options = ["1", "2", "3", "4"]
        while self.option not in options:
            print("""
             Game Options 
              Enter: 
              1  Play Game
              2  High Score
              3  About
              4  Exit Game  
                     """)

            self.option = (input("Enter an option here: "))
            if self.option not in options:
                print("Invalid choice, enter any of numbers 1, 2, 3 or 4")
        return self.option

    # Display GameMode's menu.
    def game_mode_menu(self):
        """
        Displays GameMode's menu.

        Gets the user's GameMode and game level options.

        :return game_mode<str>: Returns the chosen GameMode.
        """

        self.option = None
        options = ["1", "2"]
        while self.option not in options:
            print("""
                         Game Options 
                          Enter: 
                          1  Classic
                          2  Arcade
                                 """)
            self.option = (input("Enter Game option: "))
            if self.option not in options:
                print("Invalid choice, enter any of numbers 1 and 2")

        game_modes = {"1": "classic", "2": "arcade"}
        game_mode = game_modes[self.option]

        options = ["1", "2", "3", "4", "5"]
        self.option = ""
        while self.option not in options:
            print("""
                                     Game Level: 
                                      Enter: 
                                      1  Level 1
                                      2  Level 2
                                      3  Level 3
                                      4  Level 4
                                      5  Level 5
                                             """)
            self.option = input("Enter Game Level option: ")
            if self.option not in options:
                print("Incorrect choice, enter any of numbers 1, 2, 3, 4 or 5")
        game_levels = {"1": "level_1", "2": "level_2", "3": "level_3",
                       "4": "level_4", "5": "level_5"}
        level = game_levels[self.option]
        print("You have chosen the {} Game mode and Game level {}".format(game_mode, level))
        return game_mode, level


# play game with menu
def main():

    """ Plays game with with navigation from Menu class"""

    play_again = None
    name = None
    while play_again != "n":
        if name:
            option = input("Do you want to change Player name? (y/n): ".lower())
            if option == "y":
                name = input("Enter Player's  name: ")
            else:
                pass
        else:
            name = input("Enter Player's  name: ")
        menu = Menu(name)
        option = menu.main_menu()
        if option == "1":
            game_mode, level = menu.game_mode_menu()
            user = Game(name, game_mode, level)
            user.play_game()
        elif option == "2":
            game_mode, level = menu.game_mode_menu()
            menu.high_scores(game_mode, level)
        elif option == "3":
            abt = AboutGame()
            print(abt)
        else:
            print("Exiting Game.....")
            time.sleep(1)
            break
        play_again = input("Do you want to play again? (y/n): ").lower()


main()
input("\n\n Press the enter key to exit")
