import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.utils.data as D
from pandas._libs import json

from .data_set import TextDataSet

"""
文本分类 https://arxiv.org/pdf/1510.03820.pdf
"""

vocabulary_size = 8268
embedding_dim = 100
class_num = 4
kernel_num = 3
kernel_sizes = [2, 3, 4]


class TextCNN(nn.Module):
    def __init__(self, channel_size=1, dropout_ratio=0.1):
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
        self.conv1 = nn.ModuleList(
            [nn.Conv2d(channel_size, kernel_num, (kernel_size, embedding_dim)) for kernel_size in kernel_sizes])

        # self.dropout = nn.Dropout(dropout_ratio)

        self.mlp_1_f = nn.Linear(kernel_num * len(kernel_sizes), 100)
        self.mlp_2_f = nn.Linear(100, class_num)

    def forward(self, x):
        x = self.embedding(x)
        x = x.unsqueeze(1)  # 变化为 3D c=1, w, d

        x = [F.relu(conv(x)).squeeze(3) for conv in self.conv1]
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]

        x = torch.cat(x, 1)

        # x = self.dropout(x)  # (N, len(Ks)*Co)

        x = F.relu(self.mlp_1_f(x))  # (N, C)
        x = F.softmax(self.mlp_2_f(x), dim=1)  # (N, C)

        return x


if __name__ == '__main__':
    train_loader = D.DataLoader(TextDataSet(train=True, usecols=["dish_taste", "content", "id"]), batch_size=256,
                                shuffle=True, num_workers=32)

    test_loader = D.DataLoader(TextDataSet(train=True, usecols=["dish_taste", "content", "id"]), batch_size=64,
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

            data = torch.Tensor(content_indexes_padding, dtype=torch.long).to(device)
            target = dish_tastes.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = F.cross_entropy(input=output, target=target)
            loss.backward()
            optimizer.step()

            if batch_index % 10 == 0:
                print("Train Epoch: {} [{}/{} ({:.0f})]\tLoss: {}".format(
                    epoch, batch_index * len(data), len(train_loader.dataset),
                           100. * batch_index / len(train_loader), loss.item()
                ))
        with torch.no_grad():
            model.eval()
            test_loss = 0
            correct = 0

            for line in test_loader:
                contents, dish_tastes = line["content"], line["dish_taste"]

                content_indexes = [[character_index_dict[c] for c in content] for content in contents]

                max_len = max([len(content_index) for content_index in content_indexes])

                content_indexes_padding = [content_index + (max_len - len(content_index)) * [0] for content_index in
                                           content_indexes]

                data = torch.Tensor(content_indexes_padding, dtype=torch.long).to(device)
                target = dish_tastes.to(device)
                output = model(data)

                test_loss += F.nll_loss(input=output, target=target)
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(target.view_as(pred)).sum().item()

            test_loss /= len(test_loader.dataset)

            print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'
                  .format(test_loss, correct, len(test_loader.dataset),
                          100. * correct / len(test_loader.dataset)))
