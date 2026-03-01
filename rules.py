import numpy as np

class TicTacToe:
    # TODO Init board
    def __init__(self, board=None, current_player=1):
        if board is None:
            self.board = np.zeros((2,3,3), dtype=np.float32)
        else:
            self.board = board
        self.current_player=current_player

    # TODO Get legal moves
    def get_legal_moves(self):
        occupied = self.board[0] + self.board[1]
        return np.where(occupied.flatten() == 0)[0]
        

    # TODO Make move that returns board object 
    def make_move(self, move: int):
        # Create a copy of new board
        new_board = np.copy(self.board)

        # Gather the row and col of the move (square 1-9)
        row, col = divmod(move, 3)

        # Select player plane 0 or 1
        plane = 0 if self.current_player == 1 else 1

        # Make new move on new board
        new_board[plane, row, col] = 1

        # Return instance of new TicTacToe object
        return TicTacToe(new_board, current_player = -self.current_player)


    # TODO Check winner
    def check_winner(self):
        for p in [0,1]:
            plane = self.board[p]

            # Check rows and columns
            if np.any(np.sum(plane, axis=0)==3) or np.any(np.sum(plane, axis=1) ==3):
                return 1 if p == 0 else -1
            
            # Check diagonals
            if np.any(np.trace(plane)==3) or np.any(np.trace(np.fliplr(plane))==3):
                return 1 if p == 0 else -1
        # Check for draw
        if len(self.get_legal_moves()) == 0:
            return 0
        
        return None # Game is still ongoing

    def get_canonical_state(self): # This lets the nn always see itself as plane 0
        if self.current_player == 1:
            return self.board
        else:
            # Swap planes
            return np.flip(self.board, axis=0)
    
    # Direct copied from Gemini
    def __repr__(self):
        # A simple string view to help you debug
        chars = {1: 'X', -1: 'O', 0: '.'}
        display = ""
        flat_board = np.zeros(9)
        for i in range(9):
            r, c = divmod(i, 3)
            if self.board[0, r, c] == 1: flat_board[i] = 1
            elif self.board[1, r, c] == 1: flat_board[i] = -1
            
        for i in range(0, 9, 3):
            display += " ".join([chars[x] for x in flat_board[i:i+3]]) + "\n"
        return display

   