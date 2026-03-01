import torch
import torch.nn as nn
import torch.nn.functional as F

class TicTacToeNet(nn.Module):
    def __init__(self, hidden_size=64):
        super(TicTacToeNet, self).__init__()
        
        # Input: 2 planes of 3x3 = 18 values
        self.fc_body = nn.Sequential(
            nn.Linear(18, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )
        
        # Policy Head: Probability of each of the 9 squares
        self.policy_head = nn.Linear(hidden_size, 9)
        
        # Value Head: Expected outcome (-1 to 1)
        self.value_head = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x shape: (batch_size, 2, 3, 3)
        x = x.view(x.size(0), -1) # Flatten to (batch_size, 18)
        body_out = self.fc_body(x)
        
        policy = self.policy_head(body_out) # Logits (raw scores)
        value = torch.tanh(self.value_head(body_out)) # Scalar -1 to 1
        
        return policy, value