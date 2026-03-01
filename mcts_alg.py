import random
from mcts_node import MCTSNode

class MCTS:
    def __init__(self, iterations=1000, exploration_constant=1.41):
        self.iterations = iterations
        self.exploration_constant = exploration_constant

    def search(self, initial_state):
        # Start the tree with the current game state
        root = MCTSNode(initial_state)

        for _ in range(self.iterations):
            node = root

            # 1. SELECT: Follow UCB1 until we hit a node that can be expanded or is terminal
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.select_child(self.exploration_constant)

            # 2. EXPAND: Add a new move to the tree
            if not node.is_terminal():
                node = node.expand()

            # 3. SIMULATE (Rollout): Play randomly from this new node to the end
            winner = self._random_rollout(node.game_state)

            # 4. BACKPROPAGATE: Update stats from leaf back to root
            self._backpropagate(node, winner)

        # Return the move index of the child with the most visits
        # (Visits are more robust than raw win-rate in MCTS)
        best_move = max(root.children.items(), key=lambda item: item[1].visit_count)[0]
        return best_move

    def _random_rollout(self, state):
        """Plays a random game until a winner is found."""
        current_rollout_state = state
        while True:
            winner = current_rollout_state.check_winner()
            if winner is not None:
                return winner
            
            possible_moves = current_rollout_state.get_legal_moves()
            action = random.choice(possible_moves)
            current_rollout_state = current_rollout_state.make_move(action)

    def _backpropagate(self, node, winner):
        """Updates visit counts and values up the tree."""
        while node is not None:
            node.visit_count += 1
            
            # Logic: If it's a draw, value is 0. 
            # If the winner is the person who JUST MOVED to get to this state, it's a +1.
            # We use parent.current_player because the 'node' state has already switched players.
            if winner == 0:
                node.value_sum += 0
            elif node.parent and winner == node.parent.game_state.current_player:
                node.value_sum += 1
            else:
                node.value_sum -= 1
                
            node = node.parent