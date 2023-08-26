import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from gensim.models import Word2Vec

# 加载预训练的Word2Vec词向量模型构建词汇表和词向量矩阵
word2vec_model = Word2Vec.load('temp_and_file/word2vec_model.model')
vocab = word2vec_model.wv.key_to_index
embedding_matrix = torch.FloatTensor(word2vec_model.wv.vectors)

# 定义TextCNN模型
class TextCNN(nn.Module):
    def __init__(self, embedding_dim, num_filters, filter_sizes, num_classes):
        super(TextCNN, self).__init__()
        self.embedding = nn.Embedding.from_pretrained(embedding_matrix)
        self.convs = nn.ModuleList([
            nn.Conv2d(1, num_filters, (k, embedding_dim)) for k in filter_sizes
        ])
        self.fc = nn.Linear(num_filters * len(filter_sizes), num_classes)

    def forward(self, x):
        x = self.embedding(x)
        x = x.unsqueeze(1)
        x = [torch.relu(conv(x)).squeeze(3) for conv in self.convs]
        x = [torch.max_pool1d(conv, conv.size(2)).squeeze(2) for conv in x]
        x = torch.cat(x, 1)
        logits = self.fc(x)
        return logits

# 创建TextCNN模型实例
embedding_dim = word2vec_model.vector_size
num_filters = 100
filter_sizes = [3, 4, 5]
num_classes = 10
model = TextCNN(embedding_dim, num_filters, filter_sizes, num_classes)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 准备训练数据
train_data = []
train_labels = []
with open('THUCNews/data/train.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        title, category = line.split('	')
        train_data.append(title)
        train_labels.append(int(category))

# 文本预处理函数，将单词转换为对应的索引
def preprocess_text(text):
    tokenized_text = text.split()
    indexed_text = [word2vec_model.wv.key_to_index[word] if word in word2vec_model.wv.key_to_index else 0 for word in tokenized_text]
    return indexed_text

# 将文本转换为索引序列，并补齐到固定长度
max_len = 20
train_data = [preprocess_text(text)[:max_len] for text in train_data]
train_data = [np.pad(seq, (0, max_len - len(seq)), 'constant') for seq in train_data]
train_data = np.array(train_data)
train_labels = torch.LongTensor(train_labels)

# 将numpy数组转换为张量
train_data = torch.from_numpy(train_data).long()
train_labels = torch.LongTensor(train_labels)

# 训练模型
num_epochs = 10
batch_size = 32
total_samples = len(train_data)
total_batches = total_samples // batch_size

for epoch in range(num_epochs):
    permutation = torch.randperm(total_samples)
    train_loss = 0.0

    for i in range(total_batches):
        indices = permutation[i * batch_size:(i + 1) * batch_size]
        batch_inputs = train_data[indices]
        batch_labels = train_labels[indices]

        optimizer.zero_grad()
        outputs = model(batch_inputs)
        loss = criterion(outputs, batch_labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    avg_train_loss = train_loss / total_batches
    print(f'Epoch {epoch + 1}/{num_epochs}, Training Loss: {avg_train_loss:.4f}')

torch.save(model.state_dict(), 'temp_and_file/textcnn_model.pth')  # 保存模型