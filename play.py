from rules import TicTacToe
from mcts_alg import MCTS

print("Welcome to tic-tac-toe!")
print("Rules: ")
print("- Each square corresponds to numbers 1-9 from L->R, T->B")
print("- X always starts.")
print("")
xo = input("Enter 'x' or 'o': ")
player = 1 if xo == 'x' else -1

def print_winner(board):
    winner = board.check_winner()
    if winner is player:
        print("You won")
    elif winner is -player:
        print("AI won")
    else:
        print("Game is tied.")

board = TicTacToe()
mcts = MCTS(iterations = 1000)

while board.check_winner() == None:
    print(board)
    if board.current_player is player:
        move = int(input("Make move (int from 1-9): "))-1
        board = board.make_move(move)
    else:
        print("AI is thinking...")
        move = mcts.search(board)
        board = board.make_move(move)
print(board)
print_winner(board)
