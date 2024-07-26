import torch.optim as optim
from transformers import Trainer


class CustomTrainer(Trainer):
    def create_optimizer(self):
        # Custom optimizer configuration
        optimizer = optim.AdamW(self.model.parameters(), lr=1e-3, weight_decay=0.01)
        return optimizer