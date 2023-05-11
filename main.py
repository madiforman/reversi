from board import Board
from computer_player import Computer_Player

def get_player_color():
    correct_input = False
    while(not correct_input):
        player_id = input("Do you want to play black or white? Enter 'B' or 'W': ")
        if player_id == 'B':
            computer_id = 'W'
            correct_input = True
        elif player_id == 'W':
            computer_id = 'B'
            correct_input = True
    return player_id, computer_id

def get_difficulty():
    correct_input = False
    while(not correct_input):
        try:
            difficulty = int(input('Choose the difficulty level of your bot! Enter a number 1-5: '))
        except ValueError:
            print("Thats not a number. Try again.")
        else:
            if 1 <= difficulty <= 5:
                correct_input = True
            else:
                print("Thats too hard! Try again. ")
    return difficulty
    
def print_winner(winner):
    if winner == 0:
        print("Tie match! Good game :)")
    elif winner == 1:
        print("White won! Thank you for playing. ")
    else:
        print("Black won! Thank you for playing. ")

def main():
    print("******************************")
    print("\tWelcome to Reversi\t")
    print("******************************")
    player_id, computer_id = get_player_color()
    computer_turn = False
    if computer_id == 'B':
        computer_turn = True
    board = Board(player_id, computer_id)
    difficulty = get_difficulty()
    computer = Computer_Player(computer_id, difficulty)

    while not board.is_terminal():
        board.print_board()
        print("Score is: " + str(board.get_score()))
        if not computer_turn:
            print("Your turn!")
            if not board.all_legal_moves(board.player_id):
                print("No more legal moves! Player 2 goes again.")
                break
            board.make_player_move()
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

if __name__ == "__main__":
    main()
        
#  https://barberalec.github.io/pdf/An_Analysis_of_Othello_AI_Strategies.pdf