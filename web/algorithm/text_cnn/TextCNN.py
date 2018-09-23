import logging
import sys
from collections import Counter

sys.path += ["/home/sqzhang/sentiment_analysis_demo/"]

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.utils.data as D
from pandas._libs import json

from web.algorithm.text_cnn.data_set import TextDataSet

"""
文本分类 https://arxiv.org/pdf/1510.03820.pdf
"""

vocabulary_size = 8268
embedding_dim = 128
class_num = 4
kernel_num = 100
kernel_sizes = [1, 2, 3, 4]


class TextCNN(nn.Module):
    def __init__(self, channel_size=1):
        """
        :param vocabulary_size: 字典大小
        :param embedding_dim: 词语维度
        :param class_num: 分类种类
        :param kernel_num: 卷积核数量
        :param kernel_sizes: 卷积核大小
        :param channel_size:
        :param dropout_ratio:
        """
        super(TextCNN, self).__init__()

        self.embedding = nn.Embedding(vocabulary_size, embedding_dim)
        # self.conv1 = nn.ModuleList(
        #     [nn.Conv2d(channel_size, kernel_num, (kernel_size, embedding_dim)) for kernel_size in kernel_sizes])

        self.convs = nn.ModuleList([nn.Sequential(
            nn.Conv2d(in_channels=channel_size,
                      out_channels=kernel_num,
                      kernel_size=(kernel_size, embedding_dim)),
            nn.BatchNorm2d(kernel_num),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=kernel_num,
                      out_channels=kernel_num,
                      kernel_size=(kernel_size, 1)),
            nn.BatchNorm2d(kernel_num),
            nn.ReLU(inplace=True),
        )
            for kernel_size in kernel_sizes])

        self.fc = nn.Sequential(
            nn.Linear(kernel_num * len(kernel_sizes), 100),
            nn.BatchNorm1d(num_features=100),
            nn.ReLU(inplace=True),

            nn.Linear(100, 100),
            nn.BatchNorm1d(num_features=100),
            nn.ReLU(inplace=True),

            nn.Linear(100, 100),
            nn.BatchNorm1d(num_features=100),
            nn.ReLU(inplace=True),

            nn.Linear(100, 100),
            nn.BatchNorm1d(num_features=100),
            nn.ReLU(inplace=True),

            nn.Linear(100, class_num),
            nn.BatchNorm1d(num_features=class_num),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, x):
        x = self.embedding(x)
        x = x.unsqueeze(1)

        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs]
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]

        x = torch.cat(x, 1)
        x = self.fc(x)

        return x


if __name__ == '__main__':
    train_loader = D.DataLoader(TextDataSet(train=True, usecols=["dish_taste", "content", "id"]),
                                batch_size=256,
                                shuffle=True, num_workers=32)

    test_loader = D.DataLoader(TextDataSet(train=False, usecols=["dish_taste", "content", "id"]),
                               batch_size=256,
                               shuffle=True, num_workers=32)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = TextCNN().to(device)

    character_index_dict = json.loads(open("character_index_file.json", "r").readline())

    if torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)

    optimizer = optim.Adadelta(params=model.parameters())

    model.train()
    for epoch in range(1, 100):

        for batch_index, line in enumerate(train_loader):
            contents, dish_tastes = line["content"], line["dish_taste"]

            content_indexes = [[character_index_dict[c] for c in content] for content in contents]

            max_len = max([len(content_index) for content_index in content_indexes])

            content_indexes_padding = [content_index + (max_len - len(content_index)) * [0] for content_index in
                                       content_indexes]

            data = torch.tensor(content_indexes_padding, dtype=torch.long).to(device)
            target = torch.tensor([dish_taste + 2 for dish_taste in dish_tastes]).to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = F.cross_entropy(input=output, target=target)
            loss.backward()
            optimizer.step()

            pred = output.max(1, keepdim=True)[1]
            correct = pred.eq(target.view_as(pred)).sum().item()

            if batch_index % 100 == 0:
                print("Train Epoch: {} [{}/{} ({:.0f})]\tLoss: {}\t, Accuracy: ({:.2f}%)".format(
                    epoch, batch_index * len(data), len(train_loader.dataset),
                           100. * batch_index / len(train_loader), loss.item(),
                           100. * correct / len(contents)
                ))

        logging.info("epoch {} done!".format(epoch))
        print("epoch {} done!".format(epoch))

        with torch.no_grad():
            model.eval()
            test_loss = 0
            correct = 0
            result = Counter()

            for batch_index, line in enumerate(test_loader):
                contents, dish_tastes = line["content"], line["dish_taste"]

                content_indexes = [[character_index_dict[c] for c in content if c in character_index_dict] for content
                                   in contents]

                max_len = max([len(content_index) for content_index in content_indexes])

                content_indexes_padding = [content_index + (max_len - len(content_index)) * [0] for content_index in
                                           content_indexes]

                data = torch.tensor(content_indexes_padding, dtype=torch.long).to(device)
                target = torch.tensor([dish_taste + 2 for dish_taste in dish_tastes]).to(device)
                output = model(data)

                test_loss += F.nll_loss(input=output, target=target)
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(target.view_as(pred)).sum().item()

                pred_target_tuple = [(p.item(), t.item()) for p, t in zip(pred, target)]

                for i in range(class_num):
                    result["TP_{}".format(i)] += sum(
                        [1 for _ in filter(lambda items: items[0] == i and items[1] == i, pred_target_tuple)])
                    result["FP_{}".format(i)] += sum(
                        [1 for _ in filter(lambda items: items[0] == i and items[1] != i, pred_target_tuple)])
                    result["FN_{}".format(i)] += sum(
                        [1 for _ in filter(lambda items: items[0] != i and items[1] == i, pred_target_tuple)])
                    result["TF_{}".format(i)] += sum(
                        [1 for _ in filter(lambda items: items[0] != i and items[1] != i, pred_target_tuple)])

            F1 = []
            for i in range(class_num):
                precision = result["TP_{}".format(i)] / (result["TP_{}".format(i)] + result["FP_{}".format(i)])
                recall = result["TP_{}".format(i)] / (result["TP_{}".format(i)] + result["FN_{}".format(i)])

                F1.append(2 * (precision * recall) / (precision + recall))
            F1_ave = sum(F1) / class_num

            test_loss /= len(test_loader.dataset)

            print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%), F1: {}, F1_AVE: {} \n'
                  .format(test_loss, correct, len(test_loader.dataset),
                          100. * correct / len(test_loader.dataset), F1, F1_ave))
