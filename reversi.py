import random
import sys
import numpy as np
from board import Board

b = Board('B', 'W')
b.print_board()

class Computer_Player:
    def __init__(self, id, difficulty_level):
        assert id == 'B' or 'W'
        assert difficulty_level > 0

        def pick_move(self, board):
            pass
        
        def minimax(self, board, depth, id):
            pass

        def heuristic_score(self, board):
            pass
        
        def coin_parity(self, board):
            
        
