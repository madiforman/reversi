"""
===================================================================================
Name: board.py
Author: Madi Sanchez-Forman
Version: 5.10.23
Decription: This script defines the utility of the Reversi board.  
===================================================================================
"""
import random
import sys
import numpy as np
from collections import Counter

#******************* Constants *******************#
EMPTY, BLACK, WHITE = '.', '*', 'o'
TIE, WHITE_WIN, BLACK_WIN = 0, 1, -1
TILES_TO_COLOR = {'B': '*', 'W': 'o'}
SIZE, TOTAL_SPOTS = 8, 64
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]

#******************* Board Class *******************#
class Board():

    def __init__(self, player_id, computer_id):
        """
        Initalizes board class, which handles functionality of the Reversi game
        """
        self.array = self.init_board() #2D array that represents board 
        self.player_id = player_id #id of one player, will be either a computer or human
        self.computer_id = computer_id #always computer
        self.score = self.get_score() #Dictionary representing score of the baord

    def init_board(self):
        """
        Initalizes the inital Reversi board
        Returns: 2D array of board with starting positions
        """
        board = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                row.append(EMPTY)
            board.append(row)
        board[3][3], board[3][4] = WHITE, BLACK
        board[4][3], board[4][4] = BLACK, WHITE
        return board

    def is_terminal(self):
        """
        Checks if game is over
        Returns: True if game is over, else otherwise
        """
        flat_board = set([val for sublist in self.array for val in sublist]) #board as just a list
        if EMPTY not in flat_board: #if the board is completely full
            return True
        elif BLACK not in flat_board or WHITE not in flat_board: #if either color is completely gone
            return True
        elif self.all_legal_moves(self.player_id) == False and self.all_legal_moves(self.computer_id) == False: #or if both players are out of moves
            print("No moves left for either player!")
            return True
        else:
            return False

    def find_winner(self):
        """
        Finds out who won the game or if it was a tie. 
        Returns: 0 -> tie, 1 -> white won, -1 -> black won 
        """
        black_count, white_count = 0, 0
        for x in range(SIZE):
            for y in range(SIZE):
                if self.array[x][y] == BLACK:
                    black_count += 1
                elif self.array[x][y] == WHITE:
                    white_count += 1
        if white_count == black_count:
            return TIE
        elif white_count > black_count:
            return WHITE_WIN
        elif white_count < black_count:
            return BLACK_WIN
            
    def print_board(self):
        """
        Prints the board
        """
        print(" ", end = " ")
        nums = [print("" + str(i), end=" ") for i in range(1, SIZE + 1)]
        print()
        for i in range(SIZE):
            print(i + 1, end=" ")
            for j in range(SIZE):
                print(self.array[i][j], end=" ")
            print()

    def is_on_board(self, x, y):
        """
        Checks if a move x,y is on the board.
        Params: x, y coordinate of the board
        Returns: true if on board false otherwise
        """
        return 0 <= x < SIZE and 0 <= y < SIZE

    def is_empty(self, x, y):
        """
        Checks if an x,y coordinate on the board is empty
        Params: x, y coordinates of the board
        Returns: true if empty false otherwise
        """
        if self.array[x][y] == EMPTY:
            return True
        return False

    def find_tiles_taken(self, xstart, ystart, tile):
        """
        Given a move, this function finds what tiles would be flipped after it.
        Params: x, y coordinates and tile of player making move
        Returns: list of x,y coordiantes of tiles that would be flipped (does not flip them)
        """
        self.array[xstart][ystart] = tile #temporarily set the tile
        flipped_tiles = [] 
        for d in range(len(DIRECTIONS)): #for each direction
            ctr = 0 #holds all flipped tiles
            for i in range(SIZE): #start moving in that direction
                dx = xstart + DIRECTIONS[d][0] * (i + 1) 
                dy = ystart + DIRECTIONS[d][1] * (i + 1)
                if not self.is_on_board(dx, dy): #if this move is off the board -> break
                    ctr = 0
                    break
                elif self.array[dx][dy] == tile: #if we hit one of our own tiles -> break
                    break
                elif self.array[dx][dy] == EMPTY: #or if we run  into an empty tile -> break
                    ctr = 0
                    break
                else: #otherwise we found a tile to flip
                    ctr += 1
            for i in range(ctr): #for each tile found
                dx = xstart + DIRECTIONS[d][0] * (i + 1) #find its x,y coord
                dy = ystart + DIRECTIONS[d][1] * (i + 1)
                flipped_tiles.append([dx, dy]) # add to list
        self.array[xstart][ystart] = EMPTY #make sure to reset the board
        if len(flipped_tiles) != 0: #if there are tiles to flip, add the starting index at the end (so the starting index is always at the last index of the list, will be used later)
            flipped_tiles.append([xstart, ystart])
        return flipped_tiles #return list of tiles

    def get_score(self):
        """
        Returns a dictionary representing score of board
        Returns: dictionary of board score
        """
        score = {'B': 0, 'W': 0}
        for x in range(SIZE):
            for y in range(SIZE):
                if self.array[x][y] == BLACK:
                    score['B'] += 1
                elif self.array[x][y] == WHITE:
                    score['W'] += 1
        return score

    def all_legal_moves(self, id):
        """
        Finds all legal moves of player
        Params: id of player
        Returns: list of all legal moves
        """
        moves = []
        for x in range(SIZE):
            for y in range(SIZE):
                if self.is_legal(x, y, TILES_TO_COLOR[id]) == True:
                    moves.append([x,y])
        return moves

    def is_legal(self, x, y, tile):
        """
        Checks if a given move is legal
        Params: x, y move, and tile of player
        Returns: True/False
        """
        if not self.is_on_board(x, y): #if its not on the board
            return False
        elif not self.is_empty(x, y): #if its already been used
            return False
        tiles = self.find_tiles_taken(x, y, tile) 
        if len(tiles) == 0: #if there are no possible tiles to flip
            return False
        return True
    
    def flip_tiles(self, tiles_to_flip, cur_id):
        """
        Given a list of x,y coords, flip the tiles to the current id
        Params: list of tiles, id of current player
        """
        tile = TILES_TO_COLOR[cur_id]
        for x, y in tiles_to_flip:
            self.array[x][y] = tile
            
    def undo_move(self, tiles_taken, cur_id):
        """
        Undoes a move, used in minimax so we dont have to copy board
        Params: tiles that were flipped, and id of current player
        """
        if cur_id == 'B':
            other_id = 'W'
        else:
            other_id = 'B'
        tile = TILES_TO_COLOR[other_id]
        for i in range(len(tiles_taken) - 1): #for each tile exceptthe last
            x, y = tiles_taken[i][0], tiles_taken[i][1]
            self.array[x][y] = tile #change it
        init_x, init_y = tiles_taken[-1] 
        self.array[init_x][init_y] = EMPTY #mark starting tile as empty

    def show_valid_moves(self, id):
        """
        Shows user their legal moves
        Params: id of player
        """
        legal_moves = self.all_legal_moves(id)
        for x,y in legal_moves:
            x += 1
            y += 1
            print("[" + str(x) + "," + str(y) + "]", end = " ")
        print()

    def make_player_move(self):
        """
        Asks user to enter a move
        """
        correct_input = False
        while(not correct_input):
            try:
                move = input("Enter a move x,y (row x column): ")
                x, y = int(move[0]) - 1, int(move[2]) - 1
            except ValueError:
                print("Please enter a move x, y: ")      
            else:
                if self.is_legal(x, y, TILES_TO_COLOR[self.player_id]):
                    flipped_tiles = self.find_tiles_taken(x, y, TILES_TO_COLOR[self.player_id])
                    self.flip_tiles(flipped_tiles, self.player_id)
                    correct_input = True
                    return
                else:
                    print("Invalid move. your valid moves are:", end = " ")
                    self.show_valid_moves(self.player_id)
                    correct_input = False

    def is_end_game(self):
        """
        Checks if game is close to being over, i chose to define that as at least 75% of squares being filled
        Retuns: T/F if 75% of squares are filled
        """
        non_empty = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if self.array[x][y] != EMPTY:
                    non_empty += 1
        if non_empty / TOTAL_SPOTS > .75: #if at least 75% of tiles are filled
            return True
        return False

