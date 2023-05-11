"""
===================================================================================
Name: main.py
Author: Madi Sanchez-Forman
Version: 5.10.23
Decription: This script uses the Board class and Computer player class to run an 
othello game. 
===================================================================================
"""
from board import Board
from computer_player import Computer_Player
import sys
#******************* Helpers *******************#
def get_player_color():
    """
    Asks user what color they want to play
    """
    correct_input = False
    while(not correct_input):
        player_id = input("Do you want to play black or white? Enter 'B' or 'W': ").upper()
        if player_id == 'B':
            computer_id = 'W'
            correct_input = True
        elif player_id == 'W':
            computer_id = 'B'
            correct_input = True
    return player_id, computer_id

def get_difficulty():
    """
    Asks user to set the difficulty of the bot. Restricts it to 10 ply lookahead because of time
    """
    correct_input = False
    while(not correct_input):
        try:
            difficulty = int(input('Choose the difficulty level of your bot (or bots)! Enter a number 1-5: '))
        except ValueError:
            print("Thats not a number. Try again.")
        else:
            if 1 <= difficulty <= 10:
                correct_input = True
            else:
                print("Thats too hard! Try again. ")
    return difficulty
    
def print_winner(winner):
    """
    Prints the winner of the game
    """
    if winner == 0:
        print("Tie match! Good game :)")
    elif winner == 1:
        print("White won! Thank you for playing. ")
    else:
        print("Black won! Thank you for playing. ")

def show_options():
    """
    Asks user if they want to play against a bot or watch two bots play eachother
    """
    correct_input = False
    while(not correct_input):
        try:
            print("Would you like to:")
            print("1. Play against the bot")
            print("2. Watch two bots play eachother")
            answer = int(input("Choose an option 1 or 2: "))
        except ValueError:
            print("Thats not a number. Try again.")
        else:
            if 1 <= answer <= 2:
                correct_input = True
            else:
                print("Not an option. Please choose 1 or 2. ")
    return answer

def computer_vs_computer():
    """
    Game function for computer vs computer
    """
    computer0_id, computer1_id = 'B', 'W' #initalize ids
    board = Board(computer0_id, computer1_id) #set up board
    difficulty = get_difficulty() #ask user for number of plies
    computer0 = Computer_Player(computer0_id, difficulty) #set up bots
    computer1 = Computer_Player(computer1_id, difficulty)
    computer0_turn = True #black goes first
    while not board.is_terminal(): #while the game isnt ovre
        board.print_board() #print the board and score
        print("Score is: " + str(board.get_score()))
        if computer0_turn:
            print("Computer 1's Turn! Thinking...")
            if not board.all_legal_moves(board.player_id): #check to see if white goes twie
                print("No more legal moves! Black goes again.")
                computer0_turn = False
            else:
                computer0.pick_move(board) #minimax for computer 0
                computer0_turn = False
        else:
            print("Computer 2's turn. Thinking...")
            if not board.all_legal_moves(board.computer_id): #check to see if black goes twice
                print("No more legal moves! White goes again.")
                computer0_turn = True
            else:
                computer1.pick_move(board) #minimax for computer 1
                computer0_turn = True
    #loop broken, determine winner
    winner = board.find_winner() 
    print_winner(winner) #show winner
    sys.exit() #exit cleanly


def computer_vs_human():
    """
    Game function for human vs computer
    """
    player_id, computer_id = get_player_color() #ask player if they want to play black or white
    computer_turn = False
    if computer_id == 'B':
        computer_turn = True #if they chose white, set computer to go first
    board = Board(player_id, computer_id) #instaniate board
    difficulty = get_difficulty() #ask user for difficulty level
    computer = Computer_Player(computer_id, difficulty) #insantiate AI

    while not board.is_terminal(): #while game isnt over
        board.print_board()
        print("Score is: " + str(board.get_score()))
        if not computer_turn:
            print("Your turn!")
            if not board.all_legal_moves(board.player_id): #check to see if double turn
                print("No more legal moves! Player 2 goes again.")
                break
            board.make_player_move() #ask user to input move
            computer_turn = True
            # break
        else:
            print("Computer turn. Thinking...")
            if not board.all_legal_moves(board.computer_id):
                print("No more legal moves! Player 1 goes again.")
                break
            computer.pick_move(board)
            computer_turn = False
        
    #loop broken, determine winner
    winner = board.find_winner()
    print_winner(winner)
    sys.exit()

#******************* Main Driver Function *******************#
def main():
    print("******************************")
    print("\tWelcome to Reversi\t")
    print("******************************")
    answer = show_options() #check to see what kind of game
    if answer == 1:
        computer_vs_human()
    else:
        computer_vs_computer()
    sys.exit()

if __name__ == "__main__":
    main()
        
