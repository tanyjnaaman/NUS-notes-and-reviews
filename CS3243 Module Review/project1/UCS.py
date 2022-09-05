import heapq
from sys import argv


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
        is_opponent: bool = True,
        previousPiece = None):

        self.piece_type:str  = piece_type
        self.current_position = current_position
        self.goal_positions = goal_positions
        self.is_opponent: bool = is_opponent
        self.symbol: str = self.PIECES[self.piece_type]
        self.previousPiece = previousPiece
    
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
            raise RuntimeError("Attack piece should not be calling Piece.possibleMoves")
        else:
            raise RuntimeError("Unidentified piece type calling Piece.possibleMoves")

    def possibleAttacks(self, board) -> list:
        attackPieces = []
        for col, row in self.possibleMoves(board):
            attackPieces.append((col, row, Piece("Attack", (col, row), is_opponent = True)))
        return attackPieces
    
    def possibleMoves_wrapped(self, board):
        possibleMoves = self.possibleMoves(board)
        wrapped = []
        for new_position in possibleMoves:
            wrapped.append(Piece(self.piece_type, new_position, self.goal_positions, self.is_opponent, previousPiece = self))
        return wrapped

    def isAtGoal(self):
        return self.current_position in self.goal_positions

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


    def getHistory(self):
        piece: Piece = self
        previousPiece: Piece = piece.previousPiece
        history = []

        # traverse linkedlist in reverse order
        while piece.previousPiece != None:

            history.insert(0, (piece.previousPiece.positionToAsciiTuple(), piece.positionToAsciiTuple()))
            piece = piece.previousPiece

        return history

    def addGoalPositions(self, goal_positions: list(tuple((int, int)))):
        self.goal_positions = goal_positions

    def __repr__(self) -> str:
        if self.is_opponent:
            return "\033[1;31m" + self.symbol + "\033[0;0m" # red
        else:
            return "\033[1;32m" + self.symbol + "\033[0;0m" # green

    def __hash__(self) -> int:
        hashcode = hash(self.current_position) # hash by current position
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
        self.costs_grid: list(list(int)) = [[1 for x in range(self.columns)] for y in range(self.rows)]

    def addPiece(self, piece: Piece, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = piece

    def addPiece_withAttacks(self, piece: Piece, piece_position: tuple((int, int))):
        # add piece to board
        self.addPiece(piece, piece_position)
        
        # update position with "Attack"
        for col, row, attackPiece in piece.possibleAttacks(self):
            self.pieces_grid[row][col] = attackPiece

    def removePiece(self, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = None

        
    def movePiece(self, piece: Piece, new_position: tuple((int, int))):
        # current position
        current_position = piece.getPosition()

        # clear and place
        self.removePiece(current_position)
        self.addPiece(piece, new_position)


    def getPositionCost(self, position: tuple((int, int))) -> int:
        col, row = position
        return self.costs_grid[row][col]

    def setPositionCost(self, position: tuple((int, int)), cost: int):
        col, row = position
        self.costs_grid[row][col] = cost

    def isPositionOccupied(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.pieces_grid[row][col] != None

    def isPositionInBoard(self, position: tuple((int, int))) -> bool:
        col, row = position
        return (col < self.columns and col >= 0) and (row < self.rows and row >= 0)

    def __repr__(self) -> str:
        out = ""
        verticalSeperator = (self.columns + 1) * 2 * " -" + "\n"
        horizontalSeparator = " | "
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                piece = self.pieces_grid[i][j]
                if piece == None:
                    item = " "
                elif isinstance(piece, str):
                    item = piece
                else:
                    item = repr(piece)
                row += item + horizontalSeparator
            out += row + "\n"
        
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

        out += verticalSeperator
        out += letters
        out += "\n\n\n"

        # print costs
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                cost = self.costs_grid[i][j]
                if cost > 1:
                    cost =  "\033[1;33m" + str(cost) + "\033[0;0m"
                else:
                    cost = str(cost)
                row += cost + horizontalSeparator # yellow costs
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

    board = Board(rows, columns)

    # ===== obstacles =====

    # read in obstacles
    obstacles = []
    num_obstacles = int(lines[2][20:])
    if num_obstacles > 0: # has obstacles
        obstacle_positions = lines[3].split(":")[1].strip("\n").split(" ")
        obstacle_positions = list(map(Piece.convertAsciiPositionToXy, obstacle_positions))
        obstacles = [Piece("Obstacle", obstacle_positions[i]) for i in range(num_obstacles)]
    
    # place obstacles on board
    for i in range(num_obstacles):
        obstacle = obstacles[i]
        obstacle_position = obstacle_positions[i]
        board.addPiece(obstacle, obstacle_position)

    # ===== move costs =====
    line_index = 5
    line = lines[line_index]
    while "[" in line:
        position, cost = line.strip("\n[]").split(",")
        position = Piece.convertAsciiPositionToXy(position)
        board.setPositionCost(position, int(cost))
        line_index += 1
        line = lines[line_index]

    # ===== enemy pieces =====
    # read number of pieces
    line = lines[line_index]
    num_enemy_pieces = line.split(":")[1].split(" ")
    num_enemy_pieces = sum(map(int, num_enemy_pieces))
    line_index += 2

    # read in positions of pieces and add to board
    for i in range(num_enemy_pieces):
        line = lines[line_index].strip("[]\n\r")
        piece_type, ascii_position = line.split(",")
        position = Piece.convertAsciiPositionToXy(ascii_position)
        enemy_piece = Piece(piece_type, position)
        board.addPiece_withAttacks(enemy_piece, position)

        # next iteration
        line_index += 1

    # ===== friendly pieces =====
    line = lines[line_index]
    num_friendly_pieces = line.split(":")[1].strip("\n").split(" ")
    num_friendly_pieces = sum(map(int, num_friendly_pieces))
    line_index += 2
    for i in range(num_friendly_pieces):

        # read in piece
        line = lines[line_index].strip("[]\n\r")
        piece_type, ascii_position = line.split(",")
        position = Piece.convertAsciiPositionToXy(ascii_position)
        friendly_piece = Piece(piece_type, position, is_opponent = False)

        # first piece is player
        if i  == 0:
            player = friendly_piece

        # else add to board
        board.addPiece(friendly_piece, position)

        # next iteration
        line_index += 1

    # ===== goal position =====
    line = lines[line_index]
    goal_positions = line.split(":")[1].strip("\n\r").split(" ")
    goal_positions = list(map(Piece.convertAsciiPositionToXy, goal_positions))
    player.addGoalPositions(goal_positions)

    return board, player
    

def evaluation_function(current_cost: float, board: Board, new_piece: Piece) -> tuple((float, float)):
    
    # update cost 
    cost_to_position = current_cost + board.getPositionCost(new_piece.current_position)

    return cost_to_position, cost_to_position

class customPriorityQueue():

    def __init__(self):
        self.q = []

    def push(self, item):
        heapq.heappush(self.q, item)
    
    def pop(self) -> object:
        return heapq.heappop(self.q)

    def empty(self) -> bool:
        return len(self.q) == 0

    def __repr__(self) -> str:
        return repr(self.q)


def search(board: Board, player: Piece, f): # limited graph implementation
    
    # initialize
    frontier = customPriorityQueue() 
    explored = set() # set of piece objects, hashed by their position
    numNodesExplored = 0

    # create and put
    initial_node = (0, 0, player) # (evaluation, cost, player object)
    frontier.push(initial_node) # order by cost by default

    # search
    while not frontier.empty():
        
        # pop and goal test
        evaluation, current_cost, piece = frontier.pop()
        explored.add(piece)
        numNodesExplored += 1

        if piece.isAtGoal():
            return piece.getHistory(), numNodesExplored, current_cost
        
        # add neighbours 
        possibleMoves = piece.possibleMoves_wrapped(board)
        for new_piece in possibleMoves:
            
            if new_piece not in explored:                
                explored.add(new_piece)
                evaluation, cost_to_position =  f(current_cost, board, new_piece)
                new_node = (evaluation, cost_to_position, new_piece)
                frontier.push(new_node)

    return [], numNodesExplored, -1


def test_run():
    input_filepath = argv[1]
    board, player = parse(input_filepath)
    print(board)
    print(f"Goal positions: {player.goal_positions}")

    moves, numNodesExplored, cost = search(board, player, f = evaluation_function)
    print(f"Moves: {moves}")
    print(f"Num nodes: {numNodesExplored}")
    print(f"Cost: {cost}")

    # visualize path    
    for move in moves:
        move = move[1]
        board.pieces_grid[move[1]][ord(move[0]) - ord('a')] = "\033[1;34;45m" + "P" + "\033[0m"
    print(board)
    print("\n")

test_run()

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():
    # You can code in here but you cannot remove this function or change the return type
    input_filepath = argv[1]
    board, player = parse(input_filepath)
    moves, numNodesExplored, cost = search(board, player, f = evaluation_function)

    return moves, numNodesExplored, cost #Format to be returned
    