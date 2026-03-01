# How to use

Run play.py to play game. You won't win.

## Theory

The engine uses stochastic simulations to create a tree of possible board states (nodes). In each simulation, nodes are updated with the attributes: visit count, and win rate. After completing all simulations, the algorithm selects the child node with the highest visit count.

In every simulation, the engine uses a four-step process.

1. It selects a node to expand through the UCB1 formula. This balances exploiting nodes with high value (high win rate) and exploring less-visited nodes.
2. Adds a new unexplored node to the selected node
3. Plays through the selected node until the game reaches an endstate.
4. visit count and win rate are recursively updated

Through running 1000 simulations per move, the CPU seemingly always won, or drew at worst. Visit count determined better moves more consistently than win rate. This is likely because the win rate variable is chaotic, and a succession of bad child paths can corrupt a good parent path.

## Modifications

In play.py, you can edit the line `mcts = MCTS(iterations = 1000)` to change how many simulations the algorithm does. Decreasing iterations decreases performance, making the engine beatable.
