import torch
from torch.nn.utils.rnn import pad_sequence
from trainer import init_model
from data_format import txt_to_words, word_to_vector


def predict():
    net, opt, cri = init_model()
    net.load_state_dict(torch.load('model_and_dict/cnn.pt'))
    net.eval()
    all_words, all_labels = txt_to_words('input/test.txt')
    vectors = word_to_vector(all_words)
    input_vectors = pad_sequence(vectors, batch_first=True)
    with torch.no_grad():
        output = net(input_vectors)
    predicted_classes = torch.argmax(output, dim=1)
    return predicted_classes.tolist()
    # print(predicted_classes.tolist())

if __name__ == '__main__':
    predict()
