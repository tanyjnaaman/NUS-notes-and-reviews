import re
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

from sys import argv
import random
from copy import deepcopy


class Piece:

    PIECES = {
        "King": "K",
        "Queen": "Q",
        "Rook": "R",
        "Bishop": "B",
        "Knight": "N",
        "Obstacle": "X",
        "Attack": "!"
        }
    
    ASCII_OFFSET = ord('a')

    def __init__(
        self, 
        piece_type: str, 
        current_position: tuple((int, int)), 
        goal_positions: list(tuple((int, int))) = None, 
        is_opponent: bool = True):

        self.piece_type:str  = piece_type
        self.current_position = current_position
        self.goal_positions = goal_positions
        self.is_opponent: bool = is_opponent
        self.symbol: str = self.PIECES[self.piece_type]
    
    def possibleMoves_upTo(self, board) -> list(tuple((int, int))):
        
        def kingMoves():
            possibleMoves = []
            for col_offset in range(-1, 2):
                for row_offset in range(-1, 2):

                    # ignore current position
                    if row_offset == 0 and col_offset == 0:
                        continue
                        
                    # find valid positions
                    new_col = col + col_offset
                    new_row = row + row_offset
                    new_position = (new_col, new_row)

                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)
                        if (board.isPositionInBoard(new_position) 
                            and board.isPositionOccupied(new_position)):
                            break

            return possibleMoves
        
        def queenMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):

                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                possibleMoves.append(new_position)
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if row_offset == 0:
                    continue

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            return possibleMoves

        def rookMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):
                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                 
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            return possibleMoves

        def bishopMoves():
            possibleMoves = []

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            return possibleMoves
        
        def knightMoves():
            possibleMoves = []
            offset_1 = [1, -1]
            offset_2 = [2, -2]

            # col offset by 1, row offset by 2
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_1
                    new_row = row + delta_2
                    new_position = (new_col, new_row)
                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)

                    if (board.isPositionInBoard(new_position) 
                        and board.isPositionOccupied(new_position)):                    
                        break

            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)
                    if board.isPositionInBoard(new_position):                        
                        possibleMoves.append(new_position)
                    
                    if (board.isPositionInBoard(new_position) 
                        and board.isPositionOccupied(new_position)):                    
                        break
            
            return possibleMoves

        col, row = self.current_position
        
        if self.piece_type == "King":
            return kingMoves()
        elif self.piece_type == "Queen":
            return queenMoves()
        elif self.piece_type == "Rook":
            return rookMoves()
        elif self.piece_type == "Bishop":
            return bishopMoves()
        elif self.piece_type == "Knight":
            return knightMoves()
        elif self.piece_type == "Obstacle":
            return []
        elif self.piece_type == "Attack":
            pass
            # raise RuntimeError("Attack piece should not be calling Piece.possibleMoves_upTo")
        else:
            pass
            # raise RuntimeError("Unidentified piece type calling Piece.possibleMoves_upTo")

    def possibleMoves(self, board) -> list(tuple((int, int))): 
        
        def kingMoves():
            possibleMoves = []
            for col_offset in range(-1, 2):
                for row_offset in range(-1, 2):

                    # ignore current position
                    if row_offset == 0 and col_offset == 0:
                        continue
                        
                    # find valid positions
                    new_col = col + col_offset
                    new_row = row + row_offset
                    new_position = (new_col, new_row)

                    if (board.isPositionInBoard(new_position)
                        and not board.isPositionOccupied(new_position)):
                        possibleMoves.append(new_position)

            return possibleMoves
        
        def queenMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):

                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if row_offset == 0:
                    continue

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            return possibleMoves

        def rookMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):
                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            return possibleMoves

        def bishopMoves():
            possibleMoves = []

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            return possibleMoves
        
        def knightMoves():
            possibleMoves = []
            offset_1 = [1, -1]
            offset_2 = [2, -2]

            # col offset by 1, row offset by 2
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_1
                    new_row = row + delta_2
                    new_position = (new_col, new_row)
                    if (board.isPositionInBoard(new_position) and 
                        not board.isPositionOccupied(new_position)):
                        possibleMoves.append(new_position)

            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)
                    if (board.isPositionInBoard(new_position) and 
                        not board.isPositionOccupied(new_position)):                        
                        possibleMoves.append(new_position)
            
            return possibleMoves

        col, row = self.current_position
        
        if self.piece_type == "King":
            return kingMoves()
        elif self.piece_type == "Queen":
            return queenMoves()
        elif self.piece_type == "Rook":
            return rookMoves()
        elif self.piece_type == "Bishop":
            return bishopMoves()
        elif self.piece_type == "Knight":
            return knightMoves()
        elif self.piece_type == "Obstacle":
            return []
        elif self.piece_type == "Attack":
            pass
            # raise RuntimeError("Attack piece should not be calling Piece.possibleMoves")
        else:
            pass
            # raise RuntimeError("Unidentified piece type calling Piece.possibleMoves")

    def possibleMoves_passThrough(self, board) -> list(tuple((int, int))):
        
        def kingMoves():
            possibleMoves = []
            for col_offset in range(-1, 2):
                for row_offset in range(-1, 2):

                    # ignore current position
                    if row_offset == 0 and col_offset == 0:
                        continue
                        
                    # find valid positions
                    new_col = col + col_offset
                    new_row = row + row_offset
                    new_position = (new_col, new_row)

                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)

            return possibleMoves
        
        def queenMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):

                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                possibleMoves.append(new_position)

                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if row_offset == 0:
                    continue

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)


            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            return possibleMoves

        def rookMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):
                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            return possibleMoves

        def bishopMoves():
            possibleMoves = []

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)


            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)


            return possibleMoves
        
        def knightMoves():
            possibleMoves = []
            offset_1 = [1, -1]
            offset_2 = [2, -2]

            # col offset by 1, row offset by 2
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_1
                    new_row = row + delta_2
                    new_position = (new_col, new_row)
                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)


            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)
                    if board.isPositionInBoard(new_position):                        
                        possibleMoves.append(new_position)

            
            return possibleMoves

        col, row = self.current_position
        
        if self.piece_type == "King":
            return kingMoves()
        elif self.piece_type == "Queen":
            return queenMoves()
        elif self.piece_type == "Rook":
            return rookMoves()
        elif self.piece_type == "Bishop":
            return bishopMoves()
        elif self.piece_type == "Knight":
            return knightMoves()
        elif self.piece_type == "Obstacle":
            return []
        elif self.piece_type == "Attack":
            pass
            # raise RuntimeError("Attack piece should not be calling Piece.possibleMoves_passThrough")
        else:
            pass
            # raise RuntimeError("Unidentified piece type calling Piece.possibleMoves_passThrough")

    def possibleAttacks(self, board) -> list:
        attackPieces = []
        for col, row in self.possibleMoves_upTo(board):
            attackPieces.append((col, row, Piece("Attack", (col, row), is_opponent = True)))
        return attackPieces

    def possibleAttacks_passThrough(self, board) -> list:
        attackPieces = []
        for col, row in self.possibleMoves_passThrough(board):
            attackPieces.append((col, row, Piece("Attack", (col, row), is_opponent = True)))
        return attackPieces
    

    @staticmethod
    def convertAsciiPositionToXy(ascii_position: str) -> tuple((int, int)):
        assert(len(ascii_position) <= 3)
        col, row = ascii_position[0], ascii_position[1:]
        col, row = int(ord(col) - Piece.ASCII_OFFSET), int(row)
        return (col, row)

    @staticmethod
    def convertXyToAsciiTuple(position: tuple((int, int))) -> str:
        col, row = position
        return (chr(col + Piece.ASCII_OFFSET), row)

    def positionToAsciiTuple(self):
        return Piece.convertXyToAsciiTuple(self.current_position)


    def __repr__(self) -> str:
        if self.is_opponent:
            return "\033[1;31m" + self.symbol + "\033[0;0m" # red
        else:
            return "\033[1;32m" + self.symbol + "\033[0;0m" # green

    def __str__(self) -> str:
        return self.symbol

    def __hash__(self) -> int:
        hashcode = hash(self.current_position, self.piece_type) # hash by current position and piece type
        return hashcode 
    
    def __lt__(self, other: object):
        return False # no notion of less or more than

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False
        
        return self.current_position == other.current_position


class Board:
    def __init__(self, rows: int, columns: int):
        self.rows: int = rows
        self.columns:int  = columns 
        self.pieces_grid: list(list(Piece)) = [[None for x in range(self.columns)] for y in range(self.rows)]
        self.attacks_grid: list(list(int)) = [[0 for x in range(self.columns)] for y in range(self.rows)]
        self.pieces_table: dict = dict()

    def clear_attack_grid(self):
        self.attacks_grid = [[None for x in range(self.columns)] for y in range(self.rows)]

    def getPiece(self, piece_position: tuple((int, int))) -> Piece:
        return self.pieces_table.get(piece_position)

    def addPiece(self, piece: Piece, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = piece
        self.pieces_table[piece_position] = piece

    def addPiece_withAttacks(self, piece: Piece, piece_position: tuple((int, int))):
        # add piece to board

        self.addPiece(piece, piece_position)
        
        # update position with "Attack"
        for col, row, _ in piece.possibleAttacks(self):
            self.attacks_grid[row][col] += 1

    def addPiece_withAttacks_passThrough(self, piece: Piece, piece_position: tuple((int, int))):
        # add piece to board

        self.addPiece(piece, piece_position)
        
        # update position with "Attack"
        for col, row, _ in piece.possibleAttacks_passThrough(self):
            self.attacks_grid[row][col] += 1

    def removePiece_withAttacks(self, piece_position: tuple((int, int))):

        # get piece
        piece: Piece = self.pieces_table.get(piece_position)

        # remove piece from board
        self.removePiece(piece_position)
        
        # update position with "Attack" by reducing count
        for col, row, _ in piece.possibleAttacks(self):
            self.attacks_grid[row][col] -= 1

    def removePiece_withAttacks_passThrough(self, piece_position: tuple((int, int))):

        # get piece
        piece: Piece = self.pieces_table.get(piece_position)

        # remove piece from board
        self.removePiece(piece_position)
        
        # update position with "Attack" by reducing count
        for col, row, _ in piece.possibleAttacks_passThrough(self):
            self.attacks_grid[row][col] -= 1

    def removePiece(self, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = None
        self.pieces_table.pop(piece_position)



    def isPositionOccupied(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.pieces_grid[row][col] != None

    def isPositionAttacked(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.attacks_grid[row][col] != None

    def isPositionInBoard(self, position: tuple((int, int))) -> bool:
        col, row = position
        return (col < self.columns and col >= 0) and (row < self.rows and row >= 0)

    def toDictionary(self) -> dict:
        out = {}
        for y in range(self.rows):
            for x in range(self.columns):
                piece: Piece = self.pieces_grid[y][x]
                if  piece != None and piece.symbol != "X":
                    out[Piece.convertXyToAsciiTuple((x, y))] = piece.piece_type
        return out

    def isSolutionTo8Queens(self) -> bool:
        
        count = 0
        positions = self.getPiecePositions()
        
        for pos in positions:
            piece: Piece = self.getPiece(pos)
            if piece.symbol == "X":
                continue
            x, y = pos
            if self.attacks_grid[y][x]:
                count += 1
        return count == 0

    def getPiecePositions(self) -> list(tuple((int, int))):
        return list(self.pieces_table.keys())
                

    def __repr__(self) -> str:
        out = ""
        verticalSeperator = (self.columns + 1) * 2 * " -" + "\n"
        horizontalSeparator = " | "

        # # print board
        # for i in range(self.rows):
        #     out += verticalSeperator
        #     row = str(i) + horizontalSeparator
        #     for j in range(self.columns):
        #         piece = self.pieces_grid[i][j]
        #         if piece == None:
        #             item = " "
        #         elif isinstance(piece, str):
        #             item = piece
        #         else:
        #             item = repr(piece)
        #         row += item + horizontalSeparator
        #     out += row + "\n"
        
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

        # out += verticalSeperator
        # out += letters
        # out += "\n\n\n"

        # print attacks
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                attack = self.attacks_grid[i][j]
                piece = self.pieces_grid[i][j]
                if piece != None:
                    item = repr(piece) 
                    if attack == 0:
                        item = "\033[1;32m" + str(piece) + "\033[0;0m"
                elif attack != 0:
                    item = "\033[1;31m" + str(attack) + "\033[0;0m" # red
                else:
                    item = str(attack)


                row += item + horizontalSeparator
            out += row + "\n"
        
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

        out += verticalSeperator
        out += letters

        return out


def parse(file_path: str):

    # read file piped in
    with open(file_path) as f:
        lines = f.readlines()
    
    # ===== game board =====
    rows = int(lines[0][5:])
    columns = int(lines[1][5:])

    # ===== obstacles =====

    # read in obstacles
    obstacles = []
    num_obstacles = int(lines[2][20:])
    if num_obstacles > 0: # has obstacles
        obstacle_positions = lines[3].split(":")[1].strip("\n").split(" ")
        obstacle_positions = list(map(Piece.convertAsciiPositionToXy, obstacle_positions))
        obstacles = [(obstacle_positions[i], 
                        Piece("Obstacle", obstacle_positions[i])) for i in range(num_obstacles)]


    # ===== k =====
    k = int(lines[4].split(":")[-1])


    # ===== pieces =====
    # read number of pieces
    line_index = 5
    line = lines[line_index]
    num_pieces = line.split(":")[1].split(" ")
    num_pieces = sum(map(int, num_pieces))
    line_index += 2

    # read in positions of pieces add to list of pieces
    pieces = []
    for i in range(num_pieces):
        line = lines[line_index].strip("[]\n\r")
        piece_type, ascii_position = line.split(",")
        position = Piece.convertAsciiPositionToXy(ascii_position)
        piece = Piece(piece_type, position)
        pieces.append((position, piece))

        # next iteration
        line_index += 1

    
    return rows, columns, pieces, k, num_pieces, obstacles
    

def evaluation_function(board: Board) -> float:

    def numberInAttackPositions():
        count = 0
        positions = board.getPiecePositions()
        
        for pos in positions:
            piece: Piece = board.getPiece(pos)
            x, y = pos
            if (board.attacks_grid[y][x] != 0) and (piece.symbol != "X"):
                count += 1
        return count

    def numberInAttackPositions_notZeroWithPieceValues():

        PIECES_VALUE = {
        "King": 8,
        "Queen": 26,
        "Rook": 10,
        "Bishop": 13,
        "Knight": 8,
        "Obstacle": "X",
        "Attack": "!"
        }

        value = numberInAttackPositions()
        if value != 0:
            # value by piece type
            pieces = [PIECES_VALUE.get(board.getPiece(i).piece_type) for i in board.getPiecePositions()]
            pieces = list(filter(lambda item: isinstance(item, int), pieces))
            value += sum(pieces)

        return value
            
    value = numberInAttackPositions_notZeroWithPieceValues()

    return value

def successor_generation(board: Board, reservePieces: list) -> tuple((Board, tuple((int, int)))): # only by removing pieces

    def top1():

        # initialize
        bestPositionToRemove = None
        bestReserveToAddIndex = None
        bestValue = evaluation_function(board)

        # find best to remove
        positions = board.getPiecePositions()
        for p in positions:

            # remove position
            removedPiece = board.getPiece(p)
            board.removePiece_withAttacks_passThrough(p)

            for i in range(len(reservePieces)):

                pos, piece = reservePieces[i]
                
                # add reserve piece
                board.addPiece_withAttacks_passThrough(piece, pos)

                # evaluate and rank
                val = evaluation_function(board)
                if val < bestValue:
                    bestValue = val
                    bestPositionToRemove = p
                    bestReserveToAddIndex = i

                # remove reserve piece to restore state
                board.removePiece_withAttacks_passThrough(pos)

            # add back to restore state
            board.addPiece_withAttacks_passThrough(removedPiece, p)
        
        # apply best change permanently, if no changes, return
        if bestPositionToRemove is None:
            return board, bestValue, reservePieces

        # remove existing, put to reserve
        piece = board.getPiece(bestPositionToRemove)
        board.removePiece_withAttacks_passThrough(bestPositionToRemove) 
        reservePieces.append((bestPositionToRemove, piece))

        # move from reserve to main board
        pos, piece = reservePieces.pop(bestReserveToAddIndex) 
        board.addPiece_withAttacks_passThrough(piece, pos)
        

        return board, bestValue, reservePieces

    def stochastic_first():

        # initialize
        values = []
        bestPositionToRemove = None
        bestReserveToAddIndex = None
        bestValue = evaluation_function(board)

        # find best to remove
        positions = board.getPiecePositions()
        for p in positions:

            # remove position
            removedPiece = board.getPiece(p)
            board.removePiece_withAttacks_passThrough(p)

            for i in range(len(reservePieces)):

                pos, piece = reservePieces[i]
                
                # add reserve piece
                board.addPiece_withAttacks_passThrough(piece, pos)

                # evaluate and rank
                val = evaluation_function(board)
                if val < bestValue:
                    bestValue = val
                    bestPositionToRemove = p
                    bestReserveToAddIndex = i
                    break

                # remove reserve piece to restore state
                board.removePiece_withAttacks_passThrough(pos)

            # add back to restore state
            board.addPiece_withAttacks_passThrough(removedPiece, p)
        
        # apply best change permanently, if no changes, return
        if bestPositionToRemove is None:
            return board, bestValue, reservePieces

        # remove existing, put to reserve
        piece = board.getPiece(bestPositionToRemove)
        board.removePiece_withAttacks_passThrough(bestPositionToRemove) 
        reservePieces.append((bestPositionToRemove, piece))

        # move from reserve to main board
        pos, piece = reservePieces.pop(bestReserveToAddIndex) 
        board.addPiece_withAttacks_passThrough(piece, pos)
        
        return board, bestValue, reservePieces

    def stochastic_topk():

        # initial value
        initial_val = evaluation_function(board)

        k = 5

        positions = board.getPiecePositions()
        possibilities = []
        for p in positions:

            # remove position
            removedPiece = board.getPiece(p)
            board.removePiece_withAttacks_passThrough(p)

            for i in range(len(reservePieces)):

                pos, piece = reservePieces[i]
                
                # add reserve piece
                board.addPiece_withAttacks_passThrough(piece, pos)

                # evaluate and rank
                val = evaluation_function(board)                
                possibilities.append((val, p, i))

                # remove reserve piece to restore state
                board.removePiece_withAttacks_passThrough(pos)

            # add back to restore state
            board.addPiece_withAttacks_passThrough(removedPiece, p)

        # sort and rank
        possibilities.sort(key = lambda tup : tup[0])

        # take randomly from top k
        select = random.randint(0, k - 1)
        val, pos, i = possibilities[select]

        # remove existing, put to reserve
        piece = board.getPiece(pos)
        board.removePiece_withAttacks_passThrough(pos) 
        reservePieces.append((pos, piece))

        # move from reserve to main board
        pos, piece = reservePieces.pop(i) 
        board.addPiece_withAttacks_passThrough(piece, pos)
        # print(board)
        # print("value: ", val, "\n")

        return board, val, reservePieces
        
    board, value, newReservePieces = stochastic_topk()
    return board, value, newReservePieces

  

def local_search(board: Board, offBoardPieces: list):

    current = board
    reservePieces = offBoardPieces
    current_value = evaluation_function(board)

    while True:

        # generate successor
        best_successor, value, reservePieces = successor_generation(current, reservePieces)
        # print("\ncurrent value: ", current_value)
        # print("best successor value: ", value)
        # print(best_successor)

        # see if need to terminate
        if (value > current_value) or value == 0:
            return board.toDictionary(), board

        else:
            current = best_successor
            current_value = value

def random_initialization_search(rows: int, cols: int, n: int, k: int, pieces: list, obstacles: list):
    

    # print("\n ===== NEW SEARCH =====")
    # initialize
    board = Board(rows, cols)
    for pos, obs in obstacles:
        board.addPiece(obs, pos)

    # random initialization
    indices = [i for i in range(n)]
    random.shuffle(indices)
    indices = indices[:k]


    for i in indices:
        pos, piece = pieces[i]
        board.addPiece_withAttacks_passThrough(piece, pos)

    remainingPieces = []
    for i in range(n):
        if i not in indices:
            remainingPieces.append(pieces[i])
    
    # search
    # print(indices)
    # print(repr(board))
    # print(remainingPieces)
    return local_search(board, remainingPieces)





### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.

    rows, cols, pieces, k, n, obstacles = parse(testfile)

    # random initialization search
    isGoal = False
    while not isGoal:
        dictionary, board = random_initialization_search(rows ,cols, n, k, pieces, obstacles)
        isGoal = board.isSolutionTo8Queens()

    goalState = dictionary

    return goalState #Format to be returned

runs
print(run_local())

def test_run():

    print("===== TEST RUN =====")
    
    input_filepath = argv[1]
    rows, cols, pieces, k, n, obstacles = parse(input_filepath)
    print("board dimensions are (rows x cols): ", rows, "x", cols)
    print("k is :", k)
    print("pieces are: \n", pieces)
    print("obstacles are: \n", obstacles)

    # random initialization search
    isGoal = False
    while not isGoal:
        dictionary, board = random_initialization_search(rows ,cols, n, k, pieces, obstacles)
        isGoal = board.isSolutionTo8Queens()

    print("\nSOLUTION!")
    print(repr(board))
    print(dictionary)
    print("===========")


test_run()