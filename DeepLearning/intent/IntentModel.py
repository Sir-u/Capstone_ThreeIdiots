import tensorflow as tf
from keras.models import Model, load_model
from keras import preprocessing

#의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, proprocess):
        
        # 의도 클래스별 레이블
        self.labels = {0: "인사", 1:"욕설", 2:"주문", 3: "예약", 4 : "노여워하는",
                        5 : "느긋",6 : "걱정스러운",7 : "당혹스러운",8 : "당황",9 : "마비된",
                        10 : "만족스러운",11 : "배신당한",12 : "버려진",13 : "부끄러운",14 : "분노",
                        15 : "불안",16 : "비통한",17 : "상처",18 : "성가신",19 : "스트레스 받는",
                        20 : "슬픔",21 : "신뢰하는",22 : "신이 난",23 : "실망한",24 : "악의적인",
                        25 : "안달하는",26 : "안도",27 : "억울한",28 : "열등감",29 : "염세적인",
                        30 : "외로운",31 : "우울한",32 : "고립된",33 : "좌절한",34 : "후회되는",
                        35 : "혐오스러운",36 : "한심한",37 : "자신하는",38 : "기쁨",39 : "툴툴대는",
                        40 : "남의 시선을 의식하는",41 : "회의적인",42 : "죄책감의",43 : "혼란스러운",44 : "초조한",
                        45 : "흥분",46 : "충격 받은",47 : "취약한",48 : "편안한",49 : "방어적인",
                        50 : "질투하는",51 : "두려운",52 : "눈물이 나는",53 : "짜증내는",54 : "조심스러운",
                        55 : "낙담한",56 : "환멸을 느끼는",57 : "희생된",58 : "감사하는",59 : "구역질 나는",
                        60 : "괴로워하는",61 : "가난한, 불우한", 62 : "기타"
}

        #의도 분류 모델 불러오기
        self.model = load_model(model_name)
        
        # 챗봇 Preprocess 객체
        self.p = proprocess
        
    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)
        
        #문장 내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]
        
        # #단어 시퀀스 벡터 크기
        import sys
        sys.path.append('../Capstone_ThreeIdiots/DeepLearning/')
        from config.GlobalParams import MAX_SEQ_LEN
        
        #패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding="post")
        
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]
