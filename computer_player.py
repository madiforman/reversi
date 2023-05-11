
"""
===================================================================================
Name: computer_player.py
Author: Madi Sanchez-Forman
Version: 5.10.23
Decription: This script builds a bot to play Othello using minimax with alpha-beta
pruning
===================================================================================
"""
from board import Board
import math
#******************* Constants ***************************#
STATIC_WEIGHTS = [ #these weights were found by the users: 
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
]
SIZE = 8 
EMPTY, BLACK, WHITE = '.', '*', 'o' #tiles
#******************* Computer Player class ***************************#
class Computer_Player:
    def __init__(self, max_id, difficulty_level):
        """
        Initalizes an instance of Computer Player. It takes the ID of the AI and the number of plies to look ahead during MiniMax
        """
        assert max_id == 'B' or 'W' #class must use an id that is either 'B' or 'W'
        assert difficulty_level > 0
        self.difficulty = difficulty_level #number of plies to look ahead
        self.max_id = max_id 
        if self.max_id == 'B':
            self.min_id = 'W' #storing the id of the other player
            self.TILES_TO_COLOR = {self.max_id: BLACK, self.min_id: WHITE} #maps id -> tile
        else:
            self.min_id = 'B'
            self.TILES_TO_COLOR = {self.max_id: WHITE, self.min_id: BLACK}

    def pick_move(self, board):
        """
        Pick_move() calls Minimax on the different possible moves and then finds the one with the highest score.
        After the best move is found, it uses the Board class to flip the tiles
        """
        possible_moves = board.all_legal_moves(self.max_id) #get all legal boards associated with our ID
        best_val = -math.inf
        best_x, best_y = 0, 0
        best_tiles = []
        for x,y in possible_moves: #for each move
            tiles_flipped = board.find_tiles_taken(x, y, self.TILES_TO_COLOR[self.max_id]) #find tiles that will flip
            move_score = self.minimax_AB(board, self.difficulty, self.max_id, -math.inf, math.inf)
            if move_score > best_val:
                best_x, best_y = x, y
                best_val = move_score
                best_tiles = tiles_flipped
        board.flip_tiles(best_tiles, self.max_id)
        # print("Computer chose: " + "[" + str(best_x + 1) + "," + str(best_y + 1) + "]")



    def minimax_AB(self, board, depth, cur_id, alpha, beta):
        if depth == 0 or board.is_terminal():
            return self.heuristic_score(board, cur_id)
        if cur_id == self.max_id:
            best_score = -math.inf
            possible_moves = board.all_legal_moves(cur_id)
            if not possible_moves:
                best_score = self.minimax_AB(board, depth, self.max_id, alpha, beta)
            for x, y in possible_moves:
                tiles = board.find_tiles_taken(x, y, self.TILES_TO_COLOR[self.max_id])
                board.flip_tiles(tiles, self.max_id)
                score = self.minimax_AB(board, depth - 1, self.min_id, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                board.undo_move(tiles, self.max_id)
                if beta <= alpha:
                    break
        else:
            best_score = math.inf
            possible_moves = board.all_legal_moves(self.min_id)
            if not possible_moves:
                best_score = self.minimax_AB(board, depth, self.min_id, alpha, beta)
            for x, y in possible_moves:
                tiles = board.find_tiles_taken(x, y, self.TILES_TO_COLOR[self.min_id])
                board.flip_tiles(tiles, self.min_id)
                score = self.minimax_AB(board, depth - 1, self.max_id, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, score)
                board.undo_move(tiles, self.min_id)
                if beta <= alpha:
                    break
        return best_score
    
    def heuristic_score(self, board, cur_id):
        score = 0
        score += self.coin_parity(board)
        score += self.mobility_score(board)
        score += self.static_score(board, cur_id)
        return score
    
    def coin_parity(self, board):
        score = board.get_score()
        max_coins, min_coins = score[self.max_id], score[self.min_id]
        return -100 * (max_coins - min_coins) / (max_coins + min_coins) #gave it a negative weight becasue i want the bot to favor making moves that flip less tiles
    
    def mobility_score(self, board):
        max_moves, min_moves = len(board.all_legal_moves(self.max_id)), len(board.all_legal_moves(self.min_id))
        if max_moves > 0 and min_moves == 0: #want to favor bot getting two turns in a row
            return 150
        elif max_moves == 0 and min_moves > 0:
            return -150
        elif max_moves + min_moves == 0:
            return 0
        else:
            return 100 * (max_moves - min_moves) / (max_moves + min_moves)

    def static_score(self, board, cur_id):
        score = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if board.board[x][y] == cur_id:
                    score += STATIC_WEIGHTS[x][y]
        return score