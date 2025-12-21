"""PyTorch MLP module for binary classification."""

from __future__ import annotations

import torch


class MLP(torch.nn.Module):
    """2-layer MLP for binary classification.

    This architecture is based on the proven design from aioia-core.
    """

    def __init__(self, in_dim: int, hidden: int = 256, dropout: float = 0.2):
        """Initialize MLP with specified dimensions.

        Args:
            in_dim: Input dimension (TF-IDF feature size)
            hidden: Hidden layer size (default: 256)
            dropout: Dropout probability (default: 0.2)
        """
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(in_dim, hidden),
            torch.nn.ReLU(),
            torch.nn.Dropout(dropout),
            torch.nn.Linear(hidden, 1),  # Binary output
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network.

        Args:
            x: Input tensor of shape (batch_size, in_dim)

        Returns:
            Logits of shape (batch_size,)
        """
        return self.net(x).squeeze(-1)
