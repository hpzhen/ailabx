import torch
import torch.nn as nn
import torch.nn.functional as F
from ainlp.basemodel import BaseModel
from ainlp.data.datahandler import NlpDataset
import torch.optim as optim

words = """When forty winters shall besiege thy brow,
    And dig deep trenches in thy beauty's field,
    Thy youth's proud livery so gazed on now,
    Will be a totter'd weed of small worth held:
    Then being asked, where all thy beauty lies,
    Where all the treasure of thy lusty days;
    To say, within thine own deep sunken eyes,
    Were an all-eating shame, and thriftless praise.
    How much more praise deserv'd thy beauty's use,
    If thou couldst answer 'This fair child of mine
    Shall sum my count, and make my old excuse,'
    Proving his beauty by succession thine!
    This were to be new made when thou art old,
    And see thy blood warm when thou feel'st it cold.""".split()

handler = NlpDataset()
handler.build_ngram(words)


class CBOW(BaseModel):
    def __init__(self, n_word, n_dim, context_size):
        super(CBOW, self).__init__()
        self.embedding = nn.Embedding(n_word, n_dim)
        self.project = nn.Linear(n_dim, n_dim, bias=False)
        self.linear1 = nn.Linear(n_dim, 128)
        self.linear2 = nn.Linear(128, n_word)

    def forward(self, x):
        x = self.embedding(x)
        x = self.project(x)
        x = torch.sum(x, 0, keepdim=True)
        x = self.linear1(x)
        x = F.relu(x, inplace=True)
        x = self.linear2(x)
        x = F.log_softmax(x)
        return x

CONTEXT_SIZE=2

model = CBOW(len(handler.vocab), 100, CONTEXT_SIZE)
model.compile(optimizer=optim.SGD, loss=nn.NLLLoss)
model.fit_dataloader(handler,num_epochs=1000,batch_size=1)

