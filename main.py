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
    
def main():
    print("REVERSI")
    player_id, computer_id = get_player_color()
    computer_turn = False
    if computer_id == 'B':
        computer_turn = True
    board = Board(player_id, computer_id)
    computer = Computer_Player(computer_id, 1)
    while not board.is_terminal():
        board.print_board()
        if not computer_turn:
            if board.all_legal_moves(board.computer_id) == []:
                print("No more legal moves! Player 2 goes again.")
                break
            board.make_player_move()
            computer_turn = True
            # break
        else:
            print("COMPUTER TURN")
            if board.all_legal_moves(board.player_id) == []:
                print("No more legal moves! Player 1 goes again.")
                break
            board.make_computer_move()
            computer_turn = False

        print("Score is: " + str(board.get_score()))
    #loop broken, determine winner
    winner = board.find_winner()
    if winner == 0:
        print("Tie match! Good game :)")
    elif winner == 1:
        print("White won! Thank you for playing. ")
    else:
        print("Black won! Thank you for playing. ")
    sys.exit()

if __name__ == "__main__":
    main()
        
