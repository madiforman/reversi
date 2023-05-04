import math
import numpy as np
from copy import copy

__author__ = "Madison Sanchez-Forman"
__license__ = "University of Puget Sound"
__date__ = "3.5.2023"

class ComputerPlayer:

    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        assert difficulty_level > 0
        assert id == 1 or id == 2
        self.id = id
        if id == 1: #setting the opponent id for ease later on
            self.opp_id = 2
        else:
            self.opp_id = 1
        self.difficulty = difficulty_level

    def pick_move(self, rack):
        """
        The main utility function. It takes a rack, or instance of the board (column major), 
        calls minimax and returns the column chosen. 
        """
        col, minimax_score = self.minimax(np.array(rack), self.difficulty, self.id) #I converted the rack to a numpy array for ease of splicing when evaluating the board
        return col

    def minimax(self, rack, depth, id):
        """
        Minimax. This function takes a rack, the depth (i.e. plies or difficulty level), and the id of the current player
        It returns a tuple where the first element is the column chosen and the second is the heuristic score of the board
        """
        valid_locations = self.get_valid_locations(rack) #what columns can currently be played in
        score = self.evaluation_function(rack) #score the current board to check if winning condition met
        if self.is_terminal_state(rack) or depth == 0: #base case: depth = 0 or a player has one
            return(None, score)
        if id == self.id:   #if maximizing
            value = -math.inf   #set initial value to negative infinity
            col = 0
            for c in valid_locations:       #look at each valid location
                temp = copy(rack)       #make a copy of current board
                temp = self.drop_disc(temp, c, self.id)     #drop the disk
                new_score = self.minimax(temp, depth - 1, self.opp_id)[1]   #look at the score of temp board and recur on opponent
                if new_score > value:   #if we found a new best score
                    value = new_score   #reset score
                    col = c     #reset col
            return col, value   #return best found move

        else:   #everything is the same, but inverted if we are minimizing
            value = math.inf    #set inital score to positive infinity
            col = 0
            for c in valid_locations:
                temp = copy(rack)
                temp = self.drop_disc(temp, c, self.opp_id)     #drop disc of opponent
                new_score = self.minimax(temp, depth - 1, self.id)[1]   #look at the score of temp and recur on self
                if new_score < value:
                    value = new_score
                    col = c                    
            return col, value

    def evaluation_function(self, rack):
        """
        Evaluation function takes an instance of rack and returns the heuristic score after evaluating
        all 69 possible quartets on board
        """
        score = 0
        num_rows = len(rack[0])
        num_cols = len(rack)
        score += self.evaluate_horizontal(rack, num_rows) #horizontal
        score += self.evaluate_vertical(rack, num_cols)   #vertical
        score += self.evaluate_diagonals(rack, num_cols, num_rows)  #positive and negative diagonals
        return score

    def evaluate_horizontal(self, rack, num_rows):
        """
        Evaluate horizontal calculates the heuristic score of horizontal quartets on the board.
        It takes the rack, number of rows, and then returns the score based on evaluation function
        """
        score = 0 
        for col in rack:    #for each column in the rack
            for r in range(num_rows - 3): 
                quartet = col[r : r + 4]    #build lists of four
                score += self.evaluate_quartet(quartet.tolist())
        return score

    def evaluate_vertical(self, rack, num_cols):
        """
        Evaluate vertical calculates the heuristic score of vertical quartets on the board.
        It takes the rack, number of columns, and then returns the score based on evaluation function
        """
        score = 0
        transpose = rack.T #get transpose of rack to make iterating easier
        for row in transpose:
            for c in range(num_cols - 3):
                quartet = row [c : c + 4]
                score += self.evaluate_quartet(quartet.tolist())
        return score

    def evaluate_diagonals(self, rack, num_cols, num_rows):
        """
        Evaluate diagonals calculates the heuristic score of the diagonal quartets on the board.
        It takes the rack, number of columns/rows, and then returns the score based on evaluation function
        """
        score = 0
        #negative diagonal
        for c in range(num_cols - 3):
            for r in range(num_rows - 3):
                quartet = [rack[c + 3 - i][r + i] for i in range(4)]
                score += self.evaluate_quartet(quartet)
        #positive diagonal
        for c in range(num_cols - 3):
            for r in range(num_rows - 3):
                quartet = [rack[c + i][r + i] for i in range(4)]
                score += self.evaluate_quartet(quartet)
        return score
    def evaluate_quartet(self, quartet):
        """
        Evaluate quartet looks at a set of four spots on the board, and calculates its heuristic score based 
        on the given requirements
        """
        self_count = quartet.count(self.id)     #count the number of self pieces
        opp_count = quartet.count(self.opp_id)  #count the number of opponent pieces
        empty_count = quartet.count(0)          #count the number of empty pieces
        if self_count == 4:     #if self won
            return math.inf   
        if opp_count == 4:      #if opponenet won
            return -math.inf
        if self_count == 3 and empty_count == 1:    #if self can win in one move
            return 100
        if opp_count == 3 and empty_count == 1:     #if opponentcan win in one move
            return -100
        if self_count == 2 and empty_count == 2:    #else check other given conditions
            return 10
        if opp_count == 2 and empty_count == 2:
            return -10
        if self_count == 1 and empty_count == 3:
            return 1
        if opp_count == 1 and empty_count == 3:
            return -1   
        else:
            return 0

    def get_valid_locations(self, rack):
        """
        Get valid locations takes a instance of rack and returns a list of the open column positions. The majority of the time
        this will be the same array until the endgame
        """
        num_cols = len(rack)
        valid_locations = []
        for col in range(num_cols):
            if self.is_valid_move(rack, col):   #if the column has not been filled up
                valid_locations.append(col)
        return valid_locations

    def is_valid_move(self, rack, col):
        """
        Is_valid_move() takes an instance of rack and a column to play in and ensures that the column has spots left to play.
        Returns T/F depending on if column is full
        """
        return rack[col][-1] == 0

    def is_winning_move(self, rack):
        """
        Is_winning_move() returns T/F depending on if heuristic score of board is +/- infinity
        """
        score = self.evaluation_function(rack)
        if score == math.inf or score == -math.inf:     #if either player has four in a row
            return True
        return False

    def is_terminal_state(self, rack):
        """
        Is_terminal_state() checks to see if the game is over. It calls is_winning_move() and checks if there
        are any valid moves left. If either are true, it will return true, else false.
        """
        return self.is_winning_move(rack) or (len(self.get_valid_locations(rack)) == 0)

    def drop_disc(self, rack, col, id):
        """
        Drop_disc() makes a move on the board given an instance of the rack, a column to play in, and the id of the player.
        It returns the board with the new move. 
        """
        end_row = 0
        while rack[col][end_row] != 0 : end_row += 1    #this was taken from the code given to us 
        rack[col][end_row] = id
        return rack
 
