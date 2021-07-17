import pandas as pd

from utils import Utils
from defination import Defination
from Model import Model
import torch
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm
from ast import literal_eval
from torch import nn


genre = Defination.genre_dict


def one_hot(anime_list, input):
    # initialize one hot encoding with all genre list
    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit([anime_list])
    #print(enc.categories_)

    # format genre data
    input = format_data(input)

    # check if input need padding # sorted genre before vectorize
    test_genre = genre_vector_padding(anime_list, sorted(input))

    # encoding one hot input
    my_enc = enc.transform([test_genre]).toarray()

    # reshape to vector
    my_enc = my_enc.reshape(-1, 1)
    return my_enc

def genre_vector_padding(genre_list, current_anime_genre):
    missing = find_missing_index(genre_list, current_anime_genre)
    for i in missing:
        current_anime_genre.insert(i, 0)
    return current_anime_genre

def find_missing_index(genre_list , current_anime_genre):
    missing_list = []
    for index, element in enumerate(genre_list):
        if element not in current_anime_genre:
            missing_list.append(index)
    return missing_list

def format_data(genre):
    for i in range(0, len(genre)):
        if len(genre[i]) >= 2:
            genre[i] = genre[i].replace(' ', '_')
    return genre

if __name__ == "__main__":
    # get all genres and sort them using alphabetical order
    target = sorted(genre.keys())

    # load data
    data = pd.read_csv('data_dir/anime_processed.csv', index_col=None, header=None)
    enc_genre_list = []
    score_list = []
    for score in data[2]:
        score_list.append(float(score))

    score_list = np.array(score_list)
    score_list = torch.Tensor(score_list.reshape(-1,1))
    # one hot using all keys as base
    print('Staring encoding vector')
    for genre in tqdm(data[1]):
        enc_genre_list.append(one_hot(target, literal_eval(genre)))

    # sanity check
    assert len(enc_genre_list) == len(data[2])
    print('Assertion data ok')

    enc_test = np.array(enc_genre_list)
    enc_test = torch.Tensor(enc_test)
    enc_test = torch.squeeze(enc_test)

    print(np.shape(score_list))
    print(np.shape(enc_test))
    # set seed
    torch.manual_seed(59)
    # load model
    model = Model(43, 1)

    # training parameters
    criterion = nn.MSELoss()  # criteria network performance
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)
    epochs = 200
    losses = []  # keep track MSE

    for i in range(epochs):
        i += 1
        # PREDICTING FORWARD PASS
        y_pred = model.forward(enc_test)
        print('prediction: ', y_pred)

        # CALCULATE LOSS
        loss = criterion(y_pred, score_list)

        # RECORD LOSS
        losses.append(loss.detach().numpy())

        print(f"epoch {i} loss: {loss.item()}")

        optimizer.zero_grad()  # gradien culmilative each step

        loss.backward()
        optimizer.step()  # update hyperparameters

    print(model.linear.weight)
    torch.save(model.state_dict(), './model_weights.pth')




