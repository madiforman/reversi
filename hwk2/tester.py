
from connect4player import ComputerPlayer
import numpy as np
def make_blank_board(x,y):
    list = [[0 for i in range(y)] for j in range(x)]
    return np.array(list)


################################################################################
# MAIN(): PARSE COMMAND LINE & START PLAYING
################################################################################

if __name__ == "__main__":
    
    player = ComputerPlayer(1,0)

    #test scoring algorithm
    assert player.evaluation_function(make_blank_board(7,6)) == 0 # test with blank
    
    test_board = make_blank_board(7,6)

    test_board[0][0] = 1
    assert player.evaluation_function(test_board) == 3 # test with 1 in corner
    assert -player.evaluation_function(test_board) == -3 # test with 1 in corner

    test_board[0][0] = 2
    assert player.evaluation_function(test_board) == -3 # test with 1 in corner
    assert -player.evaluation_function(test_board) == 3 # test with 1 in corner

    test_board[1][0] = 2
    assert player.evaluation_function(test_board) == -15 # test with 1 in corner
    assert -player.evaluation_function(test_board) == 15 # test with 1 in corner

    test_board[2][0] = 1
    assert player.evaluation_function(test_board) == -1 # test with 1 in corner
    assert -player.evaluation_function(test_board) == 1 # test with 1 in corner

    #test minimax

    test_board = make_blank_board(7,6)
    print(player.minimax(test_board,2,1))