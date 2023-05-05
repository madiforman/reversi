import random
import sys
import numpy as np
EMPTY, BLACK, WHITE = '.', '*', 'o'
PIECES = (EMPTY, BLACK, WHITE)
TILES_TO_COLOR = {'B': '*', 'W': 'o'}
PLAYERS = ('B', 'W')
SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]
VALID_MOVES = [i for i in range(1, SIZE+1)]
class Board():
    def __init__(self, player_id, computer_id):
        self.board = self.init_board()
        self.player_id = player_id
        self.computer_id = computer_id
        # self.curr_player = player
        # if player == PLAYERS[0]:
        #    self.opp_id = PLAYERS[1]
        # else:
        #     self.opp_id = PLAYERS[0]

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
        return 0 <= x < SIZE and 0 <= y < SIZE

    def is_empty(self, x, y):
        if self.board[x][y] == EMPTY:
            return True
        return False
    
    def is_legal_move(self, xstart, ystart, tile):
        total_tiles = 0
        tiles_taken = []
        self.board[xstart][ystart] = tile
        for i in range(len(DIRECTIONS)):
            ctr = 0
            for j in range(SIZE):
                dx = xstart + DIRECTIONS[i][0] * (j + 1)
                dy = ystart + DIRECTIONS[i][1] * (j + 1)
                if not self.is_on_board(dx, dy):
                    ctr = 0
                    break
                elif self.board[dx][dy] == tile:
                    break
                elif self.is_empty(dx,dy):
                    ctr = 0
                    break
                else:
                    tiles_taken.append([dx, dy])
                    ctr += 1
            total_tiles += ctr
        self.board[xstart][ystart] = EMPTY
        if total_tiles == 0:
            return False
        return tiles_taken

    def is_legal(self, x, y, tile):
        if not self.is_on_board(x, y):
            return False
        elif self.board[x][y] != EMPTY:
            return False
        tiles = self.is_legal_move(x, y, tile)
        if tiles == False:
            return False
        else:
            return True

    def all_legal_moves(self, id):
        moves = []
        for x in range(SIZE):
            for y in range(SIZE):
                if self.is_legal(x, y, TILES_TO_COLOR[id]) == True:
                    moves.append([x,y])
        return moves

    def place_tile(self,  xstart, ystart, tile):
        tiles_taken = self.is_legal_move(xstart, ystart, tile)
        print("Tiles taken are " + str(tiles_taken))
        self.board[xstart][ystart] = tile
        for (x, y) in tiles_taken:
            self.board[x][y] = tile
        # self.print_board()
        return True

    def make_player_move(self):
        while True:
            move = input("Enter a move x,y: ")
            x, y = int(move[0]) - 1, int(move[2]) - 1
            if self.is_legal(x, y, TILES_TO_COLOR[self.player_id]):
                self.place_tile(x, y, TILES_TO_COLOR[self.player_id])
            # else:
            #     print("INVALID")
            #     print(self.is_legal_move(x, y, TILES_TO_COLOR[self.player_id]))    
            return

    def make_computer_move(self):
        legal_moves = self.all_legal_moves(self.computer_id)
        x, y = random.choice(legal_moves)
        self.place_tile(x, y, TILES_TO_COLOR[self.computer_id])
        print("Computer chose: " + str([x, y]))
        return


def main():
    print("REVERSI")
    board = Board('B', 'W')
    turn = board.player_id
    computer_turn = False
    while True:
        board.print_board()
        if not computer_turn:
            # print(board.all_legal_moves(board.player_id))
            board.make_player_move()
            if board.all_legal_moves(board.computer_id) == []:
                break
            computer_turn = True
            # break
        else:
            print("COMPUTER TURN")
            board.make_computer_move()
            # board.print_board()
            if board.all_legal_moves(board.player_id) == []:
                break
            computer_turn = False


if __name__ == "__main__":
    main()

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