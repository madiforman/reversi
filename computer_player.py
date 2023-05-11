
"""
===================================================================================
Name: computer_player.py
Author: Madi Sanchez-Forman
Version: 5.10.23
Decription: This script builds a bot to play Othello using minimax with alpha-beta
pruning. Heuristic approach is based off of evaluation proposed in:
https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
with some slight changes. 
===================================================================================
"""
from board import Board
import math

#******************* Constants ***************************#
STATIC_WEIGHTS = [ #These are the weights of each spot on the board. The numbers are as described in the paper linked above
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
]
SIZE = 8 #size of board
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
        Params: instance of board class
        Returns: None
        """
        possible_moves = board.all_legal_moves(self.max_id) #get all legal boards associated with our ID
        best_val = -math.inf
        best_x, best_y = 0, 0
        best_tiles = []
        for x,y in possible_moves: #for each move
            tiles_flipped = board.find_tiles_taken(x, y, self.TILES_TO_COLOR[self.max_id]) #find tiles that will flip
            move_score = self.minimax_AB(board, self.difficulty, self.max_id, -math.inf, math.inf) #score the move
            if move_score > best_val: #remember move with best score
                best_x, best_y = x, y
                best_val = move_score
                best_tiles = tiles_flipped
        board.flip_tiles(best_tiles, self.max_id) #flip tiles for that move
        print("Computer chose: " + "[" + str(best_x + 1) + "," + str(best_y + 1) + "]") #print move chosen for clarity

    def minimax_AB(self, board, depth, cur_id, alpha, beta):
        """
        mininimax_AB() performs the depth first tree search on an instance of a board for a given number of plies. 
        params: Instance of board, depth of recursion, ID of current player, alpha and beta values
        returns: best_score -> score of the board
        """
        if depth == 0 or board.is_terminal():   #if the game is over
            return self.heuristic_score(board, cur_id) #return heuristic value of the board
        if cur_id == self.max_id: #if maximizing
            best_score = -math.inf
            possible_moves = board.all_legal_moves(cur_id) #find all possible moves
            if not possible_moves: #python idiom for checking if a list is empty
                best_score = self.minimax_AB(board, depth, self.min_id, alpha, beta) #if there are no possible moves, minimizing player goes twice
            for x, y in possible_moves: #for each move
                tiles = board.find_tiles_taken(x, y, self.TILES_TO_COLOR[self.max_id]) #find and flip the tiles on the board without making copy
                board.flip_tiles(tiles, self.max_id)
                score = self.minimax_AB(board, depth - 1, self.min_id, alpha, beta) #score the board
                best_score = max(best_score, score) 
                alpha = max(alpha, score)
                board.undo_move(tiles, self.max_id) #replace tiles
                if beta <= alpha: #if it is not better than anything we have seen -> prune
                    break
        else:
            best_score = math.inf #inverse of above for min player
            possible_moves = board.all_legal_moves(self.min_id)
            if not possible_moves:
                best_score = self.minimax_AB(board, depth, self.max_id, alpha, beta)
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
        """
        Heuristic_score() calculates the heuristic value of the board
        Params: an instance of Board class, and the id of current player.
        returns: Float score of board
        """
        #NOTE: Instead of using a function to check for corner spots and edges, I used the static weights of the board as proposed in the essay, I wanted a mix of a dynamic and static heuristic
        score = 0
        score += self.coin_parity(board)         
        score += self.mobility_score(board) 
        score += self.static_score(board, cur_id)
        return score
    
    def coin_parity(self, board):
        """
        Coin_parity compares the number of max and mins tiles, except it aims to minimize its own tiles and maximize the opponents during the beginning of the game.
        When the game is closer to the end, it will switch to maximizing its tiles. 
        params: instance of Board class
        returns: float coin parity score of board 
        """
        score = board.get_score()
        max_coins, min_coins = score[self.max_id], score[self.min_id]
        if not board.is_end_game(): #if it is not the end of the game => minimize tiles
            return -10 * (max_coins - min_coins) / (max_coins + min_coins)
        else:
            return 10 * (max_coins - min_coins) / (max_coins + min_coins) #otherwise we want to maximize them
    
    def mobility_score(self, board):
        """
        Mobily_score aims to estimate the future mobility (number of possible future moves) for each player, so that max can attempt to restrict the opponents mobility while
        maximizing their own.
        params: instance of Board class
        returns: float mobility score of board
        """
        max_moves, min_moves = len(board.all_legal_moves(self.max_id)), len(board.all_legal_moves(self.min_id))
        if max_moves > 0 and min_moves == 0: #want to favor bot getting two turns in a row, so if possible make note of that
            return 30
        elif max_moves == 0 and min_moves > 0: #do not want bot to give opponent two turns in a row
            return -30
        elif max_moves + min_moves == 0:
            return 0
        else:
            return 10 * (max_moves - min_moves) / (max_moves + min_moves)

    def static_score(self, board, cur_id):
        """
        Static score uses the static weights array to score the board, favoring corner positions. 
        params: instance of board class and id of current player
        returns: integer score of board
        """
        score = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if board.array[x][y] == cur_id:
                    score += STATIC_WEIGHTS[x][y]
        return score