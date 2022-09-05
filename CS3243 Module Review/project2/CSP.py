import sys
import random


### IMPORTANT: Remove any # print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.


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
        current_position: tuple((int, int))):

        self.piece_type:str  = piece_type
        self.current_position = current_position
        self.symbol: str = self.PIECES[self.piece_type]
        self.attacks: dict = dict()

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
                    new_position = (new_col, new_row    )

                    if board.isPositionInBoard(new_position):
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
            # raise RuntimeError("Attack piece should not be calling Piece.possibleMoves_upTo")
        else:
            pass
            # raise RuntimeError("Unidentified piece type calling Piece.possibleMoves_upTo")

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
        attacks = self.getAttacks(board, self.current_position)
        for col, row in attacks:
            attackPieces.append((col, row))
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

    def getAttacks(self, board, position: tuple) -> list:
        attacks = self.attacks.get(position)
        if attacks is None:
            original = self.current_position
            self.current_position = position
            attacks = self.possibleMoves_upTo(board)
            self.attacks[position] = attacks # store
            self.current_position = original

        return attacks

    
    def setPosition(self, position: tuple):
        self.current_position = position

    def clearPosition(self):
        self.current_position = None
    


    def __repr__(self) -> str:
        # if self.is_opponent:
        # if self.symbol == Piece.PIECES["Obstacle"]:
        #     return str(self.symbol)
        return "\033[1;33m" + self.symbol + "\033[0;0m" # red
        # else:
        #     return "\033[1;32m" + self.symbol + "\033[0;0m" # green

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
    def __init__(self, rows: int, columns: int, numObstacles: int):
        self.rows: int = rows
        self.columns:int  = columns 
        self.pieces_grid: list(list(Piece)) = [[None for x in range(self.columns)] for y in range(self.rows)]
        self.attacks_grid: list(list(int)) = [[0 for x in range(self.columns)] for y in range(self.rows)]
        self.pieces_table: dict = dict()
        self.numObstacles = numObstacles


    def getPiece(self, piece_position: tuple((int, int))) -> Piece:
        return self.pieces_table.get(piece_position)

    def addPiece(self, piece: Piece, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = piece
        self.pieces_table[piece_position] = piece
        piece.setPosition(piece_position)

    def removePiece(self, piece_position: tuple((int, int))):
        col, row = piece_position
        piece: Piece = self.pieces_grid[row][col]
        self.pieces_grid[row][col] = None
        self.pieces_table.pop(piece_position)
        piece.clearPosition()

    def addPiece_withAttacks(self, piece: Piece, piece_position: tuple((int, int))):
        
        # add piece to board
        self.addPiece(piece, piece_position)
        
        # update position with "Attack"
        attackPositions = piece.possibleAttacks(self)

        # upfate board with attacks
        for col, row in attackPositions:
            self.attacks_grid[row][col] += 1

    def removePiece_withAttacks(self, piece_position: tuple((int, int))):

        # get piece
        piece: Piece = self.pieces_table.get(piece_position)
        
        # update position with "Attack" by reducing count
        for col, row in piece.possibleAttacks(self):
            self.attacks_grid[row][col] -= 1

        # remove piece from board
        self.removePiece(piece_position)


    def isPositionOccupied(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.pieces_grid[row][col] != None

    def isPositionAttacked(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.attacks_grid[row][col] != 0
    
    def numberSafePositions(self) -> int:
        count = len(self.getEmptyNonAttackedPositions())
        return count 

    def isPositionInBoard(self, position: tuple((int, int))) -> bool:
        col, row = position
        return (col < self.columns and col >= 0) and (row < self.rows and row >= 0)

    def toDictionary(self) -> dict:
        out = {}

        PIECES = {
            "King",
            "Queen",
            "Rook",
            "Bishop",
            "Knight"
        }

        for y in range(self.rows):
            for x in range(self.columns):
                piece: Piece = self.pieces_grid[y][x]
                if piece is not None and piece.piece_type in PIECES:
                    out[Piece.convertXyToAsciiTuple((x, y))] = piece.piece_type
        return out  


    def getPiecePositions(self) -> list(tuple((int, int))):
        return list(self.pieces_table.keys())

    def isSolution(self, expectedNumPieces) -> bool:
        
        # if less then number of expected pieces, return false
        if len(self.pieces_table) - self.numObstacles < expectedNumPieces:
            return False 

        assert(len(self.pieces_table) - self.numObstacles == expectedNumPieces)

        # else, check if any piece currently is being attacked
        positions = self.getPiecePositions()

        PIECES = {
            "King",
            "Queen",
            "Rook",
            "Bishop",
            "Knight"
            }
        
        for pos in positions:
            piece: Piece = self.getPiece(pos)
            if piece.piece_type in PIECES and  self.isPositionAttacked(pos):
                return False

        return True

    def numPiecesUnderAttack(self)-> int:
        count = 0
        positions = self.getPiecePositions()
        
        for pos in positions:
            piece: Piece = self.getPiece(pos)
            if piece.symbol == "X": # ignore obstacle
                continue
            x, y = pos
            if self.attacks_grid[y][x] != 0:
                count += 1
        return count
    
    def canPlaceWithoutAttackingOthers(self, position: tuple, piece:Piece) -> bool:

        # see if can place 
        canPlace = not (self.isPositionOccupied(position) or self.isPositionAttacked(position))
        if not canPlace:
            return False

        # see if attacks will attack other pieces on board
        piecePositionsOnBoard = self.getPiecePositions()

        # get attacks by piece
        attacks = piece.getAttacks(self, position)

        for p in piecePositionsOnBoard:
            if p in attacks and self.getPiece(p).symbol != "X":
                return False # will attack
        return True

    def getEmptyNonAttackedPositions(self, shuffle = True) -> list:

        emptyNotAttacked = []
        for x in range(self.columns):
            for y in range(self.rows):
                pos = (x, y)
                if not (self.isPositionAttacked(pos) or self.isPositionOccupied(pos)):
                    emptyNotAttacked.append(pos)

        if shuffle: 
            random.shuffle(emptyNotAttacked)

        return emptyNotAttacked

    def __repr__(self) -> str:
        out = ""
        verticalSeperator = (self.columns + 1) * 2 * " -" + "\n"
        horizontalSeparator = " | "
   
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

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
                        item = "\033[1;32m" + str(piece) + "\033[0;0m" # green
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


class CSP:
    
    def backtrack(self, board: Board, unassignedPieces: list, expectedNumPieces: int):
        
        # print("\n====== NEW CALL TO BACKTRACK =====")

        if board.isSolution(expectedNumPieces):
            return board
        
        piece: Piece = unassignedPieces[0]

        positionsToPlace = board.getEmptyNonAttackedPositions()

        for position in positionsToPlace:
            # print("trying: ", position, piece)

            if not board.canPlaceWithoutAttackingOthers(position, piece):
                # print("cannot place without attacking other")
                continue # try next position

            # print("can place!")


            # place and infer by looking ahead
            board.addPiece_withAttacks(piece, position)            
            is_viable = self.infer(board, unassignedPieces[1:])
            if is_viable:
                # print("is viable!")            
                # print("after placing:")
                # print(board)
                # print(unassignedPieces[1:])

                result = self.backtrack(board, unassignedPieces[1:], expectedNumPieces)
                if result != False:
                    return result
                
            # undo
            # print("not viable, or result failed.")
            board.removePiece_withAttacks(position)
            # print("board is, after removal: ")
            # print(board)

        # print("need to backtrack!\n")
        return False


    def infer(self, board: Board, unassigned_pieces: list):
        
        def forward_checking():
            
            # if not enough safe positions left, confirm cannot
            if board.numberSafePositions() < len(unassigned_pieces):
                return False

            
            return True

        inference = forward_checking()
    
        return inference
    
    def orderPieces(self, pieces: list) -> list:

        PIECES_VALUE = {
                "King": 8,
                "Queen": 26,
                "Rook": 14,
                "Bishop": 13,
                "Knight": 9,
                "Obstacle": "X",
                "Attack": "!"
                }

        def by_piece_type():
            pieces.sort(key = lambda p : PIECES_VALUE[p.piece_type], reverse = True)
            return pieces

        def random():
            random.shuffle(pieces)
            return pieces

        sequence = by_piece_type()

        return sequence 



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

    # add obstacles
    numObstacles = len(obstacles)
    board = Board(rows, columns, numObstacles)
    for i in obstacles:
        pos = i[0]
        obs = i[1]
        board.addPiece(obs, pos)

    # ===== pieces =====
    # read number of pieces
    line_index = 4
    line = lines[line_index]
    num_pieces = list(map(int, line.split(":")[1].split(" ")))

    # create a piece with domain for each piece
    pieces = []
    for piece_type in range(len(num_pieces)):
        if piece_type == 0:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("King", None))
        elif piece_type == 1:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Queen", None))                
        elif piece_type == 2:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Bishop", None))
        elif piece_type == 3:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Rook", None))
        elif piece_type == 4:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Knight", None))
        else:
            pass # do nothing


    return pieces, board
        

# def test_run():

#     # random.seed(2)

#     # parse
#     # print("===== TEST RUN =====")
    
#     input_filepath = sys.argv[1]
#     pieces, board = parse(input_filepath)
#     # print("board is: \n", board)

#     # initialize CSP
#     csp = CSP()

#     # sort pieces in order of minimum constraints
#     pieces = csp.orderPieces(pieces)
#     # print("pieces are: \n", pieces)


#     # CSP backtracking search
#     board = csp.backtrack(board, pieces, len(pieces))

#     # print("\nSOLUTION!")
#     # print(repr(board))
#     # print(board.attacks_grid)
#     # print(board.toDictionary())
#     # print("===========")

# import time

# times = []
# n = 10
# for i in range(n):
#     start = time.time()
#     test_run()
#     end = time.time()
#     times.append(end - start)

# import statistics
# avg = statistics.geometric_mean(times)

# print("\ntook ", avg, "s on average\n")
# print("times were: ", times)
# if n > 1:
#     stdev = statistics.stdev(times)
#     print("stdev was ", stdev)
    
# print(run_CSP())

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
        
    random.seed(0)

    # parse
    pieces, board = parse(testfile)

    # initialize CSP
    csp = CSP()

    # sort pieces in order of minimum constraints
    pieces = csp.orderPieces(pieces)


    # CSP backtracking search
    board = csp.backtrack(board, pieces, len(pieces))
    solution = board.toDictionary()

    assert len(solution) == len(pieces)

    return solution

"""
Idea: 
1. each variable is a piece, and the domain is all locations on the board
2. the constraints are such that a piece cannot take up an occupied position or a position under attack. 

We can model an assignment as a given board state. We can model domains as an additional attribute of the 
Piece class. 
"""

