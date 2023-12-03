import sys
sys.path.append("../Capstone_ThreeIdiots/DeepLearning/")
from config.DatabaseConfig import *

import sys
sys.path.append('../Capstone_ThreeIdiots/DeepLearning/utils/')

from Database import Database
from Preprocess import Preprocess

# 전처리 객체 생성
p = Preprocess(word2index_dic='../Capstone_ThreeIdiots/DeepLearning/train_tools/dict/chatbot_dict.bin',
               userdic='../Capstone_ThreeIdiots/DeepLearning/utils/user_dic.tsv')

# 질문/답변 학습 디비 연결 객체 생성
db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME, charset='utf8'
)
db.connect()    # 디비 연결

# 원문
# query = "오늘 왜이렇게 기분이 나쁘지?"
# query = "화자의 질문 의도를 파악합니다."
query = "안녕하세요"
# query = "아 배고프다,, 자장면 먹고싶은데 어떠세요?"

# 의도 파악
from intent.IntentModel import IntentModel
intent = IntentModel(model_name='../Capstone_ThreeIdiots/DeepLearning/intent/intent_model_15.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명 인식
from ner.NerModel import NerModel
ner = NerModel(model_name='../Capstone_ThreeIdiots/DeepLearning/ner/ner_model.h5', proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : ", query)
print("=" * 100)
print("의도 파악 : ", intent_name)
print("개체명 인식 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 100)

# 답변 검색
from FindAnswer import FindAnswer

try:
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = "죄송해요 무슨 말인지 모르겠어요"

print("답변 : ", answer)

db.close() # 디비 연결 끊음