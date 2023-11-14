import sys
sys.path.append('../DeepLearning/utils/')
from Preprocess import Preprocess
from NerModel import NerModel

p = Preprocess(word2index_dic='../Capstone_ThreeIdiots/DeepLearning/train_tools/dict/chatbot_dict.bin',
               userdic = '../Capstone_ThreeIdiots/DeepLearning/utils/user_dic.tsv')

ner = NerModel(model_name='../Capstone_ThreeIdiots/DeepLearning/ner/ner_model.h5', proprocess=p)
query = '오늘 오전 13시 2분에 탕수육 주문하고 싶어요'
predicts = ner.predict(query)
print(predicts)