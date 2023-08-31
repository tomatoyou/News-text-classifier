from jieba import lcut
from torchtext.vocab import vocab
from collections import OrderedDict, Counter
from torchtext.transforms import VocabTransform
from torch.nn.utils.rnn import pad_sequence
from sklearn.preprocessing import LabelEncoder
import scipy.io as io
import torch
import pickle
from gensim.models.word2vec import LineSentence

# 去非中文词
def reserve_chinese(content):
    content_str = ''
    for i in content:
        if (i >= '\u4e00' and i <= '\u9fa5'):
            content_str += i
    return content_str

def dataParse(text, stop_words):
    text_split = text.split('\t')
    if len(text_split) == 2:
        content, label = text_split
        content = reserve_chinese(content)
        words = lcut(content)
        words = [i for i in words if not i in stop_words]
        return words, int(label)
    else:
        content = reserve_chinese(text_split[0].strip('\n'))
        words = lcut(content)
        words = [i for i in words if not i in stop_words]
        return words, int(0)

def getStopWords():
    file = open('input/stopwords.txt', 'r', encoding='utf8')
    words = [i.strip() for i in file.readlines()]
    file.close()
    return words

def txt_to_words(file_path_txt: str):
    file = open(file_path_txt, 'r',encoding='utf8')
    texts = file.readlines()
    file.close()
    stop_words = getStopWords()
    all_words = []
    all_labels = []
    for text in texts:
        content, label = dataParse(text, stop_words)
        if len(content) <= 0:
            continue
        all_words.append(content)
        all_labels.append(label)
    return all_words, all_labels

# 自制词表Vocab
def get_vocab(word_lst):
    ws = sum(word_lst, [])
    set_ws = Counter(ws)
    keys = sorted(set_ws, key=lambda x: set_ws[x], reverse=True)
    dict_words = dict(zip(keys, list(range(1, len(set_ws) + 1))))
    ordered_dict = OrderedDict(dict_words)
    my_vocab = vocab(ordered_dict, specials=['<UNK>', '<SEP>'])
    my_vocab.set_default_index(0)
    with open('model_and_dict/vocab.pkl', 'wb') as f:
        pickle.dump(my_vocab, f)
    print('vocab saved!')

def word_to_vector(word_lst):
    with open('model_and_dict/vocab.pkl', 'rb') as f:
        my_vocab = pickle.load(f)
    vocab_transform = VocabTransform(my_vocab)
    vector = vocab_transform(word_lst)
    vector = [torch.tensor(i) for i in vector]
    return vector


def word_to_mat(word_lst, label_lst):
    with open('model_and_dict/vocab.pkl', 'rb') as f:
        my_vocab = pickle.load(f)
    vocab_transform = VocabTransform(my_vocab)
    vector = vocab_transform(word_lst)
    vector = [torch.tensor(i) for i in vector]
    pad_seq = pad_sequence(vector, batch_first=True)
    labelencoder = LabelEncoder()
    labels = labelencoder.fit_transform(label_lst)
    data = pad_seq.numpy()
    data = {'X': data,
            'label': labels,
            'num_words': len(my_vocab)}
    io.savemat('model_and_dict/data.mat', data)
    print('mat saved!')

if __name__ == '__main__':
    word_lst, label_lst = txt_to_words('input/train.txt')
    word_to_mat(word_lst, label_lst)
    # ss = LineSentence(open('input/vocab_train_data.txt', 'r', encoding='utf8'))
    # word_lst = [x for x in ss]
    # print('读取完毕')
    # get_vocab(word_lst)


