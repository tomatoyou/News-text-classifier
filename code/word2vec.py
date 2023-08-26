from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing

# with open('temp_and_file/word2vec_train_data.txt', 'r', encoding='utf-8') as file:
#     documents = file.read()

cores = multiprocessing.cpu_count() # 获取CPU核心数
model = Word2Vec(
    LineSentence(open('temp_and_file/word2vec_train_data.txt', 'r', encoding='utf8')),
    min_count=5,
    window=5,
    vector_size=100,
    workers=cores-1
)
model.save('temp_and_file/word2vec_model.model')


