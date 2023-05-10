import random
import sys
import numpy as np
from collections import Counter
EMPTY, BLACK, WHITE = '.', '*', 'o'
PIECES = (EMPTY, BLACK, WHITE)
TIE, WHITE_WIN, BLACK_WIN = 0, 1, -1

TILES_TO_COLOR = {'B': '*', 'W': 'o'}
PLAYERS = ('B', 'W')
SIZE, TOTAL_SPOTS = 8, 64
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]
#1) The board is full, with no empty spaces 2) The board has coins of only one color 3) When no player has a valid move
class Board():
    def __init__(self, player_id, computer_id):
        self.board = self.init_board()
        self.player_id = player_id
        self.computer_id = computer_id
        self.score = self.get_score()

    def init_board(self):
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
        flat_board = set([val for sublist in self.board for val in sublist])
        if EMPTY not in flat_board:
           return True
        elif BLACK not in flat_board or WHITE not in flat_board:
            return True
        elif self.all_legal_moves(self.player_id) == False and self.all_legal_moves(self.computer_id) == False:
            return True
        else:
            return False

    def find_winner(self):
        black_count, white_count = 0, 0
        for x in range(SIZE):
            for y in range(SIZE):
                if self.board[x][y] == BLACK:
                    black_count += 1
                elif self.board[x][y] == WHITE:
                    white_count += 1
        if white_count == black_count:
            return TIE
        elif white_count > black_count:
            return WHITE_WIN
        elif white_count < black_count:
            return BLACK_WIN
            

    def print_board(self):
        print(" ", end = " ")
        emDash = u'\u2014'
        nums = [print(i, end=" ") for i in range(1, SIZE + 1)]
        print()
        for i in range(SIZE):
            print(i + 1, end=" ")
            for j in range(SIZE):
                print(self.board[i][j], end=" ")
            print()
            
    def is_on_board(self, x, y):
        return 0 <= x < SIZE - 1 and 0 <= y < SIZE - 1

    def is_empty(self, x, y):
        if self.board[x][y] == EMPTY:
            return True
        return False

    def is_legal_move(self, xstart, ystart, tile):
        total = 0
        self.board[xstart][ystart] = tile
        flipped_tiles = []
        for d in range(len(DIRECTIONS)):
            ctr = 0
            for i in range(SIZE):
                dx = xstart + DIRECTIONS[d][0] * (i + 1)
                dy = ystart + DIRECTIONS[d][1] * (i + 1)
                if not self.is_on_board(dx, dy):
                    ctr = 0
                    break
                elif self.board[dx][dy] == tile:
                    break
                elif self.board[dx][dy] == EMPTY:
                    ctr = 0
                    break
                else:
                    ctr += 1
                    # flipped_tiles.append([dx, dy])
            for i in range(ctr): 
                dx = xstart + DIRECTIONS[d][0] * (i + 1)
                dy = ystart + DIRECTIONS[d][1] * (i + 1)
                flipped_tiles.append([dx, dy])
        self.board[xstart][ystart] = EMPTY
        if len(flipped_tiles) != 0:
            flipped_tiles.append([xstart, ystart])
        return flipped_tiles
    def get_score(self):
        score = {'B': 0, 'W': 0}
        for x in range(SIZE):
            for y in range(SIZE):
                if self.board[x][y] == BLACK:
                    score['B'] += 1
                elif self.board[x][y] == WHITE:
                    score['W'] += 1
        return score

    def all_legal_moves(self, id):
        moves = []
        for x in range(SIZE):
            for y in range(SIZE):
                if self.is_legal(x, y, TILES_TO_COLOR[id]) == True:
                    moves.append([x,y])
        return moves

    def is_legal(self, x, y, tile):
        if not self.is_on_board(x, y):
            return False
        elif not self.is_empty(x, y):
            return False
        tiles = self.is_legal_move(x, y, tile)
        if not tiles:
            return False
        else:
            return True
    
    def flip_tiles(self, tiles_to_flip, cur_id):
        tile = TILES_TO_COLOR[cur_id]
        for x, y in tiles_to_flip:
            self.board[x][y] = tile
            
    def place_tile(self,  xstart, ystart, cur_id):
        tile = TILES_TO_COLOR[cur_id]
        tiles_taken = self.is_legal_move(xstart, ystart, tile)
        print(tiles_taken)
        # print("tiles flipped are: " + str(tiles_taken))
        # self.board[xstart][ystart] = tile
        for (x, y) in tiles_taken:
            self.board[x][y] = tile
        self.score = self.get_score()
        return True
    
    def undo_move(self, tiles_taken, cur_id):
        if cur_id == 'B':
            other_id = 'W'
        else:
            other_id = 'B'
        tile = TILES_TO_COLOR[other_id]
        for i in range(len(tiles_taken) - 1):
            x, y = tiles_taken[i][0], tiles_taken[i][1]
            self.board[x][y] = tile
        init_x, init_y = tiles_taken[-1]
        self.board[init_x][init_y] = EMPTY

    def show_valid_moves(self, id):
        legal_moves = self.all_legal_moves(id)
        for x,y in legal_moves:
            x += 1
            y += 1
            print("[" + str(x) + "," + str(y) + "]", end = " ")
        print()

    def make_player_move(self):
        while True:
            move = input("Enter a move x,y: ")
            x, y = int(move[0]) - 1, int(move[2]) - 1
            is_valid = self.is_legal(x, y, TILES_TO_COLOR[self.player_id])
            if is_valid:
                self.place_tile(x, y, self.player_id)
                
                return
            else:
                print("Invalid move. your valid moves are:", end = " ")
                self.show_valid_moves(self.player_id)
  
    def make_computer_move(self):
        legal_moves = self.all_legal_moves(self.computer_id)
        print(legal_moves)
        x, y = random.choice(legal_moves)
        xprint, yprint = x + 1, y + 1
        print("Computer chose: " + str([xprint, yprint]))
        self.place_tile(x, y, self.computer_id)

        return


# board = Board('B', 'W')
# print(board.player_id)
# board.print_board()
# # board.board = [['o' for j in range(SIZE)] for i in range(SIZE)]
# print(board.is_terminal())
# board.make_player_move()
# board.print_board()
# board.make_computer_move()
# board.print_board()
# board.print_board()
# board.make_computer_move()
# board.print_board()
# # b.get_valid_moves(self, WHITE)
#     def is_legal_move(self, tile, xstart, ystart):
#         tiles_taken = []
#         self.board[xstart][ystart] == tile
#         if tile == '*':
#             opp_tile = 'o'
#         else:
#             opp_tile = '*'
    
#         for xdir, ydir in DIRECTIONS:
#             x, y = xstart, ystart
#             x += xdir
#             y += ydir
#             if self.is_on_board(x, y) and self.board[x][y] == opp_tile:
#                 x += xdir
#                 y += ydir
#                 if not self.is_on_board(x,y):
#                     continue
#                 while self.board[x][y] == opp_tile:
#                     x += xdir
#                     y += ydir
#                     if not self.is_on_board(x, y):
#                         break
#                 if not self.is_on_board(x,y):
#                     continue
#                 if self.board[x][y] == opp_tile:
#                     while True:
#                         x -= xdir
#                         y -= ydir
#                         if x == xstart and y == ystart:
#                             break
#                         tiles_taken.append([x,y])
#         self.board[xstart][ystart] = EMPTY
#         if len(tiles_taken) == 0:
#             print(len(tiles_taken))
#             return False
#         return tiles_taken