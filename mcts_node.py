import math

class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state  # The TicTacToe object
        self.parent = parent          # Parent node (None for root)
        self.move = move              # The move index that created this node
        
        self.children = {}            # Dict mapping move_index -> MCTSNode
        self.visit_count = 0
        self.value_sum = 0            # Cumulative reward (wins)
        
        # Keep track of moves we haven't explored yet from this state
        self.untried_moves = list(game_state.get_legal_moves())

    @property
    def q_value(self):
        """Returns the average win rate (exploitation component)"""
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        # A node is terminal if someone won or it's a draw
        return self.game_state.check_winner() is not None

    def select_child(self, exploration_constant=1.41):
        """
        Uses the UCB1 formula to pick the most 'interesting' child.
        """
        best_score = -float('inf')
        best_child = None

        for child in self.children.values():
            # UCB1 = Exploitation + Exploration
            # Note: We use self.visit_count as the 'N' (parent visits)
            exploitation = child.q_value
            exploration = exploration_constant * math.sqrt(
                math.log(self.visit_count) / child.visit_count
            )
            score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def expand(self):
        """
        Picks an untried move, creates a new state, and adds it as a child.
        """
        move = self.untried_moves.pop()
        next_state = self.game_state.make_move(move)
        child_node = MCTSNode(next_state, parent=self, move=move)
        self.children[move] = child_node
        return child_node