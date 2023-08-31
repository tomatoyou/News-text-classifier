# -*- coding: utf-8 -*-
import scipy.io as io
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from torch.optim import Adam
import numpy as np
import time
import torch

from utils import metrics, safeCreateDir
from model_def import textCNN
from plot import plot_acc, plot_loss

def get_num_words(file_path_load_mat):
    data = io.loadmat(file_path_load_mat)
    return data['num_words'].item()

class Data_train(Dataset):
    def __init__(self):
        data = io.loadmat('model_and_dict/data.mat')
        self.X = data['X']
        self.y = data['label'].squeeze()
        self.num_words = data['num_words'].item()

    def __getitem__(self, item):
        return self.X[item], self.y[item]

    def __len__(self):
        return self.X.shape[0]

class getDataLoader():
    def __init__(self, batch_size):
        train_data = Data_train()
        self.traindl = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=4)
        self.num_words = train_data.num_words

def init_model():
    textCNN_param = {
        'vocab_size': get_num_words('model_and_dict/data.mat'),
        'embed_dim': 64,
        'class_num': 10,
        "kernel_num": 16,
        "kernel_size": [3, 4, 5],
        "dropout": 0.5,
    }
    net = textCNN(textCNN_param)
    opt = Adam(net.parameters(), lr=1e-4, weight_decay=5e-4)
    cri = nn.CrossEntropyLoss()
    return (net, opt, cri)

def train(epochs):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    data = getDataLoader(batch_size=64)
    traindl = data.traindl
    net, opt, cri = init_model()
    print('init net...')
    net.init_weight()
    print(net)
    patten = 'Epoch: %d   [===========]  cost: %.2fs;  loss: %.4f;  train acc: %.4f;'
    train_accs = []
    c_loss = []
    for epoch in range(epochs):
        cur_preds = np.empty(0)
        cur_labels = np.empty(0)
        cur_loss = 0
        start = time.time()
        for batch, (inputs, targets) in enumerate(traindl):
            inputs = inputs.to(device)
            targets = targets.to(device)
            net.to(device)
            pred = net(inputs)
            loss = cri(pred, targets)
            opt.zero_grad()
            loss.backward()
            opt.step()
            cur_preds = np.concatenate([cur_preds, pred.cpu().detach().numpy().argmax(axis=1)])
            cur_labels = np.concatenate([cur_labels, targets.cpu().numpy()])
            cur_loss += loss.item()
        acc, precision, f1, recall = metrics(cur_preds, cur_labels)
        train_accs.append(acc)
        c_loss.append(cur_loss)
        end = time.time()
        print(patten % (epoch + 1, end - start, cur_loss, acc))
    torch.save(net.state_dict(), 'model_and_dict/cnn.pt')
    print('Model saved!')
    plot_acc(train_accs)
    plot_loss(c_loss)

if __name__ == "__main__":
    train(epochs=30)
