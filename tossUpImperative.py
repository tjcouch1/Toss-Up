#
# TJ Couch
# CS 424-01
# 10 March 2018
# Program 2: An implementation of Toss Up!
#   2 players can play the game Toss Up! against one another as many times
#   as they desire
# Python 3.6
#
# tossUp.py:  Runs Toss Up!
#
import random
from collections import Counter

#global vars

#dictionaries
#dictionary for names of dice values
diceNames = {0:"red", 1:"yellow", 2:"green"}

#player stuffs
numPlayers = 2
#player names
playerName = []

#game vars
#players' scores
score = []
#score to win
scoreCap = 100
#temporary score for while rolling
tempScore = 0
#number of remaining dice in this roll
numDiceCap = 10
numDice = numDiceCap

#welcomes the players. Does not return
def printIntro():
    print("Welcome to TJ's Toss Up! game! Find a friend, roll dice, and hope you win big!")

#asks the prompt, then returns T/F based on yes or no or whatever
def getConfirmation(prompt, confirms="ypr",rejects="nqs"):
    conf = None
    while conf == None:
        numSlashes = 1
        if len(confirms) == 0 or len(rejects) == 0:
            numSlashes = 0
        conf = input(prompt + " (" + confirms + numSlashes * "/" + rejects + ") ").lower()

        #acceptable responses
        if (len(conf) > 0):
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

#runs through a player's roll - rolls dice, calculates temporary score. Does not return
def playerRoll(turn):
    #roll dice
    global numDice, tempScore
    print("  You roll " + str(numDice) + " dice!")
    dice = [random.randint(0,2) for _ in range(numDice)]

    #print dice rolls
    diceString = "  You rolled "
    for i, dieVal in enumerate(dice):#range(len(dice)):
        ending = ", "
        if i == len(dice) - 2:
            ending = ", and "
        if i >= len(dice) - 1:
            ending = "."
        diceString += diceNames[dice[i]] + ending
    print(diceString)

    #calculate score
    faces = Counter(dice)
    if faces[2] > 0:#if rolled greens
        tempScore += faces[2]#get points
        numDice -= faces[2]#lose dice
        print("  You got " + str(faces[2]) + " greens!")
        if numDice == 0:
            print("  You got all greens! You get all " + str(numDiceCap) + " dice back.")
            numDice = numDiceCap
    elif faces[0] > 0:#if no greens and at least one red
        numDice = 0
        tempScore = 0

    #print score
    print("  " + playerName[turn] + "'s score for this turn is " + str(tempScore) + ".")

#runs through the chosen player's turn. Does not return
def playerTurn(turn):
    print(playerName[turn] + "'s turn!")

    #player gets numDiceCap dice at start of turn
    global numDice, tempScore
    numDice = numDiceCap
    tempScore = 0

    #player keeps rolling until he has 0 dice or says stop
    keepRolling = getConfirmation(" You have " + str(numDice) + " dice. Would you like to roll them?", rejects="")
    while keepRolling:
        playerRoll(turn)

        if (numDice == 0):
            print("You ran out of dice! Your turn is over.")
            keepRolling = False
        else:
            #ask to continue
            keepRolling = getConfirmation(" You have " + str(numDice) + " dice left. Do you want to keep rolling?")

    #player gets score
    score[turn] += tempScore

    for i, scr in enumerate(score):
        print(" " + playerName[i] + "'s score is " + str(scr) + ".")

#returns a list of indices of max value in the list
def getMaxIndices(list):
    high = -10000000000
    indices = []
    for i, value in enumerate(list):
        if value > high:
            high = value
            indices = [i]
        elif value == high:
            indices.append(i)
    return indices

#execute the game with dice rolls and such. Does not return
def playGame():
    print("Let's start a new game!")

    #players' scores
    global score, playerName
    score = [0 for _ in range(numPlayers)]
    playerName = ["Player " + str(i + 1) for i in range(numPlayers)]

    #starts on 1st player
    turn = 0
    #index of player who has reached scoreCap
    endPlayer = -1

    #turn loop. Keep taking turns until someone gets scoreCap then let everyone go once
    while endPlayer < 0 or turn is not endPlayer:
        #player's turn
        playerTurn(turn)

        #player reaches scoreCap
        if (endPlayer < 0):
            if (score[turn] >= scoreCap):
                endPlayer = turn
                turnString = "Everyone else"
                if numPlayers == 2:
                    otherPlayer = 1
                    if endPlayer == 1:
                        otherPlayer = 0
                    turnString = playerName[otherPlayer]
                print(playerName[endPlayer] + " has passed " + str(scoreCap) + " points! " + turnString +
                      " gets one last turn!")

        #increment turn
        turn = (turn + 1) % numPlayers

    #get player who wins
    print("The game is over!")
    for player in getMaxIndices(score):
        print(playerName[player] + " won with " + str(score[player]) + " points!")

#main program that runs at the start. Does not return
def main():
    printIntro()

    #make the overarching game loop
    playing = getConfirmation("Would you like to play?")
    while playing:
        playGame()

        playing = getConfirmation("Would you like to play again?")

    print("Thank you for playing Toss Up!")


main()
