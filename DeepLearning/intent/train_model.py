import pandas as pd
import tensorflow as tf
from keras import preprocessing
from keras.models import Model
from keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate, BatchNormalization
from keras.callbacks import ModelCheckpoint, EarlyStopping

# 데이터 읽어오기
train_file = "../Capstone_ThreeIdiots/DeepLearning/intent/ADD_train_data.csv"
data = pd.read_csv(train_file, delimiter=',')
queries = data['query'].tolist()
intents = data['intent'].tolist()

# Preprocess 클래스 불러오기
import sys
sys.path.append('../Capstone_ThreeIdiots/DeepLearning/utils/')
from Preprocess import Preprocess
p = Preprocess(word2index_dic='../Capstone_ThreeIdiots/DeepLearning/train_tools/dict/chatbot_dict.bin',
               userdic='../Capstone_ThreeIdiots/DeepLearning/utils/user_dic.tsv')

# 단어 시퀀스 생성
sequences = []
for sentence in queries:
   pos = p.pos(sentence)
   keywords = p.get_keywords(pos, without_tag=True)
   seq = p.get_wordidx_sequence(keywords)
   sequences.append(seq)

# 단어 인덱스 시퀀스 벡터
MAX_SEQ_LEN = 40
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

# 학습용, 검증용, 테스트용 데이터셋 생성
ds = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
ds = ds.shuffle(len(queries))

train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

# 하이퍼 파라미터 설정
dropout_prob = 0.5
EMB_SIZE = 128
EPOCH = 100
VOCAB_SIZE = len(p.word_index) + 1

# 클래스 수 추출
num_classes = len(set(intents))

# CNN 모델
input_layer = Input(shape=(MAX_SEQ_LEN,))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

# 여러 컨볼루션 레이어와 필터 크기 사용
conv1 = Conv1D(filters=128, kernel_size=3, padding='valid', activation=tf.nn.relu)(dropout_emb)
conv2 = Conv1D(filters=128, kernel_size=4, padding='valid', activation=tf.nn.relu)(dropout_emb)
conv3 = Conv1D(filters=128, kernel_size=5, padding='valid', activation=tf.nn.relu)(dropout_emb)
conv4 = Conv1D(filters=128, kernel_size=6, padding='valid', activation=tf.nn.relu)(dropout_emb)
conv5 = Conv1D(filters=128, kernel_size=7, padding='valid', activation=tf.nn.relu)(dropout_emb)

# 각 컨볼루션 레이어 뒤에 배치 정규화 레이어 추가
conv1 = BatchNormalization()(conv1)
conv2 = BatchNormalization()(conv2)
conv3 = BatchNormalization()(conv3)
conv4 = BatchNormalization()(conv4)
conv5 = BatchNormalization()(conv5)

# 각 컨볼루션 레이어의 결과를 풀링 레이어로 가져옴
pool1 = GlobalMaxPool1D()(conv1)
pool2 = GlobalMaxPool1D()(conv2)
pool3 = GlobalMaxPool1D()(conv3)
pool4 = GlobalMaxPool1D()(conv4)
pool5 = GlobalMaxPool1D()(conv5)

# 모든 풀링 레이어를 concatenate
concat = concatenate([pool1, pool2, pool3, pool4, pool5])

# Dense 층 추가
hidden1 = Dense(256, activation=tf.nn.relu)(concat)
dropout_hidden1 = Dropout(rate=dropout_prob)(hidden1)

hidden2 = Dense(128, activation=tf.nn.relu)(dropout_hidden1)
dropout_hidden2 = Dropout(rate=dropout_prob)(hidden2)

logits = Dense(num_classes, name='logits')(dropout_hidden2)
predictions = Dense(num_classes, activation=tf.nn.softmax)(logits)

# 모델 생성
model = Model(inputs=input_layer, outputs=predictions)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 콜백 함수 설정
checkpoint = ModelCheckpoint('../Capstone_ThreeIdiots/DeepLearning/intent/best_intent_model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1)

# 모델 학습
history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCH, callbacks=[checkpoint, early_stopping], verbose=1)

# 최상의 성능을 보인 모델 불러오기
model.load_weights('../Capstone_ThreeIdiots/DeepLearning/intent/best_intent_model.h5')

# 테스트 데이터 셋을 이용한 모델 평가
loss, accuracy = model.evaluate(test_ds, verbose=1)
print('Test Accuracy: {:.2f}%'.format(accuracy * 100))
print('Test Loss: {:.4f}'.format(loss))

# 훈련과 검증의 정확도와 손실 그래프 그리기
import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
