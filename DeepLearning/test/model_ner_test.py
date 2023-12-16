import sys
sys.path.append('../Capstone_ThreeIdiots/DeepLearning/utils/')
from Preprocess import Preprocess

sys.path.append('../Capstone_ThreeIdiots/DeepLearning/')
from ner.NerModel import NerModel

p = Preprocess(word2index_dic='../Capstone_ThreeIdiots/DeepLearning/train_tools/dict/chatbot_dict.bin',
               userdic = '../Capstone_ThreeIdiots/DeepLearning/utils/user_dic.tsv')

ner = NerModel(model_name='../Capstone_ThreeIdiots/DeepLearning/ner/ner_model.h5', proprocess=p)
query = '내일 드디어 집에 갈 수 있는 날이야!'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)