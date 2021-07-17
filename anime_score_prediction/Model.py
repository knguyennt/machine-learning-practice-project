import torch
from torch import nn

class Model(nn.Module):
    # infeatures should equal to genre dimension and out is 1 for score
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)  # linear layer
        '''self.linear_softmax = nn.Sequential(
            nn.Linear(in_features, out_features),  # linear layer
            nn.Softmax(dim=1)
        )'''

    def forward(self,x):
        y_pred = self.linear(x)
        #y_pred = self.linear_softmax(x)
        return y_pred