#
# TJ Couch
# CS 424-01
# 29 March 2018
# Program 3: An implementation of Toss Up! in Object Oriented Style
#   2 players can play the game Toss Up! against one another as many times
#   as they desire
# Python 3.6.5
#
# tossUp.py:  Runs Toss Up!
#
import random
from collections import Counter


# a die that rolls randomly on initialization
class Die:
    # static dictionary for names of dice values
    FACE_NAMES = {0: "red", 1: "yellow", 2: "green"}

    # randomizes the die face
    def __init__(self):
        # symbolizes what face the die has. Not private so Counter can use it (line 72)
        self.face = random.randint(0, len(Die.FACE_NAMES) - 1)


# Player is a player who can take a turn and stuff
class Player:

    # sets up standard player variables
    def __init__(self, name="Player", score=0):
        # name of player
        self.__name = name
        # player's score
        self.__score = score
        # number of dice the player has
        self.__numDice = 0

    # gets player's name
    def get_name(self):
        return self.__name

    # gets player score
    def get_score(self):
        return self.__score

    # sets player score
    def set_score(self, score):
        self.__score = score

    # runs through a player's roll with dice cap - rolls dice, calculates temporary score. returns temp score
    def roll_dice(self, num_dice_cap, temp_score):
        # roll dice
        print("  You roll " + str(self.__numDice) + " dice!")
        dice = [Die() for _ in range(self.__numDice)]

        # print dice rolls
        dice_string = "  You rolled "
        for i, die in enumerate(dice):
            ending = ", "
            if i == len(dice) - 2:
                ending = ", and "
            elif i >= len(dice) - 1:
                ending = "."
            dice_string += Die.FACE_NAMES[dice[i].face] + ending
        print(dice_string)

        # calculate score
        faces = Counter(getattr(die, "face") for die in dice)
        if faces[2] > 0:  # if rolled greens
            temp_score += faces[2]  # get points
            self.__numDice -= faces[2]  # lose dice
            print("  You got " + str(faces[2]) + " greens!")
            if self.__numDice == 0:
                print("  You got all greens! You get all " + str(num_dice_cap) + " dice back.")
                self.__numDice = num_dice_cap
        elif faces[0] > 0:  # if no greens and at least one red
            self.__numDice = 0
            temp_score = 0

        # print score
        print("  " + self.__name + "'s score for this turn is " + str(temp_score) + ".")

        return temp_score

    # runs through the chosen player's turn with the number of dice assigned. Does not return
    def take_turn(self, num_dice_cap):
        print(self.__name + "'s turn!")

        # player gets numDiceCap dice at start of turn
        self.__numDice = num_dice_cap
        temp_score = 0

        # player keeps rolling until he has 0 dice or says stop
        keep_rolling = Game.get_confirmation(" You have " + str(self.__numDice) + " dice. Would you like to roll them?",
                                             rejects="")
        while keep_rolling:
            temp_score = self.roll_dice(num_dice_cap, temp_score)

            if self.__numDice == 0:
                print("You ran out of dice! Your turn is over.")
                keep_rolling = False
            else:
                # ask to continue
                keep_rolling = Game.get_confirmation(
                    " You have " + str(self.__numDice) + " dice left. Do you want to keep rolling?")

        # player gets score
        self.__score += temp_score


# Game runs tossup
class Game:

    # initializes standard game variables
    def __init__(self):
        # game vars
        # number of players
        self.__numPlayers = 2
        # list of players
        self.__players = [Player("Player " + str(i + 1)) for i in range(self.__numPlayers)]
        # score to win
        self.__scoreCap = 100
        # number of total dice per roll roll
        self.__numDiceCap = 10

    # asks the prompt, then returns T/F based on yes or no or whatever
    @staticmethod
    def get_confirmation(prompt, confirms="ypr", rejects="nqs"):
        conf = None
        while conf is None:
            num_slashes = 1
            if len(confirms) == 0 or len(rejects) == 0:
                num_slashes = 0
            conf = input(prompt + " (" + confirms + num_slashes * "/" + rejects + ") ").lower()

            # acceptable responses
            if len(conf) > 0:
                if conf[0] in confirms:
                    conf = True
                elif conf[0] in rejects:
                    conf = False
                else:
                    conf = None
                    print("Sorry, but I didn't understand that. ")
            else:
                conf = None
                print("Sorry, but I didn't understand that. ")
        return conf

    # returns a list of indices of players with the highest score
    def get_high_players(self):
        high = -10000000000
        winning_players = []
        for player in self.__players:
            if player.get_score() > high:
                high = player.get_score()
                winning_players = [player]
            elif player.get_score() == high:
                winning_players.append(player)
        return winning_players

    # welcomes the players. Does not return
    @staticmethod
    def print_intro():
        print("Welcome to TJ's Toss Up! game! Find a friend, roll dice, and hope you win big!")

    # execute the game with dice rolls and such. Does not return
    def play_game(self):
        print("Let's start a new game!")

        # starts on 1st player
        turn = 0
        # index of player who has reached scoreCap
        end_player = -1
        # reset all players' scores
        for player in self.__players:
            player.set_score(0)

        # turn loop. Keep taking turns until someone gets scoreCap then let everyone go once
        while end_player < 0 or turn is not end_player:
            # player's turn
            self.__players[turn].take_turn(self.__numDiceCap)

            # after player's turn, print all scores
            for p in self.__players:
                print(" " + p.get_name() + "'s score is " + str(p.get_score()) + ".")

            # player reaches scoreCap
            if end_player < 0:
                if self.__players[turn].get_score() >= self.__scoreCap:
                    end_player = turn
                    turn_string = "Everyone else"
                    if self.__numPlayers == 2:
                        other_player = 1
                        if end_player == 1:
                            other_player = 0
                        turn_string = self.__players[other_player].get_name()
                    print(self.__players[end_player].get_name() + " has passed " + str(self.__scoreCap) + " points! " +
                          turn_string + " gets one last turn!")

            # increment turn
            turn = (turn + 1) % self.__numPlayers

        # get player who wins
        print("The game is over!")
        for player in self.get_high_players():
            print(player.get_name() + " won with " + str(player.get_score()) + " points!")

    # main program that runs at the start. Does not return
    @staticmethod
    def main():
        Game.print_intro()

        # make the overarching game loop
        playing = Game.get_confirmation("Would you like to play?")
        game = Game()
        while playing:
            game.play_game()

            playing = Game.get_confirmation("Would you like to play again?")

        print("Thank you for playing Toss Up!")


Game.main()
