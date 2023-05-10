import random
import sys
import numpy as np
from board import Board
import math
CORNERS = [(0,0), (0,7), (7,0), (7,7)]

class Computer_Player:
    def __init__(self, max_id, difficulty_level):
        assert max_id == 'B' or 'W'
        assert difficulty_level > 0
        self.difficulty = difficulty_level
        self.max_id = max_id
        if self.max_id == 'B':
            self.min_id = 'W'
            self.max_tile = '*'
            self.min_tile = 'o'
        else:
           self.min_id = 'B'
           self.max_tile = 'o'
           self.min_tile = '*'

    def pick_move(self, board):
        possible_moves = board.all_legal_moves(self.max_id)
        best_val = -math.inf
        best_x, best_y = 0, 0
        best_tiles = []
        for x,y in possible_moves:
            tiles_flipped = board.is_legal_move(x, y, self.max_tile)
            move_score = self.minimax(board, self.difficulty, self.max_id, -math.inf, math.inf)
            if move_score > best_val:
                best_x, best_y = x, y
                best_val = move_score
                best_tiles = tiles_flipped
        board.flip_tiles(best_tiles, self.max_id)
        print("Computer chose: " + "[" + str(best_x + 1) + "," + str(best_y + 1) + "]")
        

    def minimax(self, board, depth, cur_id, alpha, beta):
        if depth == 0 or board.is_terminal():
            return self.heuristic_score(board)
        if cur_id == self.max_id:
            best_score = -math.inf
            possible_moves = board.all_legal_moves(cur_id)
            for x, y in possible_moves:
                tiles = board.is_legal_move(x, y, self.max_tile)
                board.flip_tiles(tiles, self.max_id)
                new_score = self.minimax(board, depth - 1, self.min_id)
                best_score = max(best_score, new_score)
                alpha = max(alpha, best_score)
                board.undo_move(tiles, self.max_id)
                if beta <= alpha:
                    break
        else:
            best_score = math.inf
            possible_moves = board.all_legal_moves(self.min_id)
            for x, y in possible_moves:
                tiles = board.is_legal_move(x, y, self.min_tile)
                board.flip_tiles(tiles, self.min_id)
                new_score = self.minimax(board, depth - 1, self.max_id)
                best_score = min(best_score, new_score)
                beta = min(beta, best_score)
                board.undo_move(tiles, self.min_id)
                if beta <= alpha:
                    break
        board.print_board()
        return best_score


    def heuristic_score(self, board):
        score = 0
        score += self.coin_parity(board)
        score += self.mobility_score(board)
        score += self.corners_captured(board)
        return score
    
    def coin_parity(self, board):
        score = board.get_score()
        max_coins, min_coins = score[self.max_id], score[self.min_id]
        return 100 * (max_coins - min_coins) / (max_coins + min_coins)
    
    def mobility_score(self, board):
        max_moves, min_moves = len(board.all_legal_moves(self.max_id)), len(board.all_legal_moves(self.min_id))
        if max_moves + min_moves == 0:
            return 0
        else:
            return 100 * (max_moves - min_moves) / (max_moves + min_moves)

    def corners_captured(self, board):
        max_corners, min_corners = 0, 0
        for x, y in CORNERS:
            if board.board[x][y] == self.max_tile:
                max_corners += 1
            elif board.board[x][y] == self.min_tile:
                min_corners += 1
        if max_corners + min_corners == 0:
            return 0
        else:
            return (max_corners - min_corners) / (max_corners + min_corners)

    def stability_score(self, board):
        pass

# def main():
#     print("REVERSI")
#     correct_input = False
#     player_id, computer_id = '', ''
#     computer_turn = False
#     while(not correct_input):
#         player_id = input("Do you want to play black or white? Enter 'B' or 'W': ")
#         if player_id == 'B':
#             computer_id = 'W'
#             correct_input = True
#         elif player_id == 'W':
#             computer_id = 'B'
#             correct_input = True
#             computer_turn = True

#     board = Board(player_id, computer_id)
#     computer = Computer_Player(computer_id, 1)
#     while not board.is_terminal():
#         board.print_board()
#         print(board.is_terminal())
#         if not computer_turn:
#             # print(board.all_legal_moves(board.player_id))
#             # if board.all_legal_moves(board.computer_id) == []:
#             #     print("No more legal moves! Player 2 goes again.")
#             #     break
#             board.make_player_move()
#             computer_turn = True
#             # break
#         else:
#             print("COMPUTER TURN")
#             # if board.all_legal_moves(board.player_id) == []:
#             #     print("No more legal moves! Player 1 goes again.")
#             #     break
#             # computer.pick_move(board)
#             board.make_computer_move()
#             computer_turn = False

#         print("Score is: " + str(board.get_score()))
#     #loop broken, determine winner
#     winner = board.find_winner()
#     if winner == 0:
#         print("Tie match! Good game :)")
#     elif winner == 1:
#         print("White won! Thank you for playing. ")
#     else:
#         print("Black won! Thank you for playing. ")
#     sys.exit()

# if __name__ == "__main__":
#     main()
        
