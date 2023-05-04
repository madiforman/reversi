import random
import sys
import numpy as np
EMPTY, BLACK, WHITE = '.', '*', 'o'
PIECES = (EMPTY, BLACK, WHITE)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]
dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]
class Board():
    def __init__(self, player):
        self.board = self.init_board()
        self.curr_player = player
        if player == PLAYERS[BLACK]:
           self.opp_id = PLAYERS[WHITE]
        else:
            self.opp_id = PLAYERS[BLACK]

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
            
    def is_on_board(self, row, col):
        return 0 <= row <= SIZE and 0 <= col <= SIZE

    def is_empty(self, x, y):
        if self.board[x][y] == EMPTY:
            return True
        return False

    def make_valid_move(self, x, y, player):
        total_tiles = 0
        self.board[x][y] = player
        for i in range(len(DIRECTIONS)):
            ctr = 0
            for j in range(SIZE):
                dx = x + DIRECTIONS[i][0] * (j + 1)
                dy = y + DIRECTIONS[i][1] * (j + 1)
                if not self.is_on_board(x, y):
                    ctr = 0
                    break
                elif self.board[dx][dy] == player:
                    break
                elif self.is_empty(dx, dy):
                    ctr = 0
                    break
                else:
                    ctr += 1
            total_tiles += ctr
            if total_tiles != 0:
                for j in range(ctr):
                    dx = x + dirx[i] * (j + 1)
                    dy = y + diry[i] * (j + 1)
                    self.board[dx][dy] = player
            else:
                return False
        return (self.board, total_tiles)




b = Board([PLAYERS[BLACK]])
b.print_board()
b.make_valid_move(5, 4, BLACK)
b.make_valid_move(5, 4, BLACK)
b.make_valid_move(5, 5, WHITE)
b.make_valid_move(4, 5, BLACK)
print(b.make_valid_move(3, 5, WHITE))



b.print_board()


# b.get_valid_moves(self, WHITE)