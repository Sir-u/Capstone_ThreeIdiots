import pandas as pd
import tensorflow as tf
from keras import preprocessing
from keras.models import Model
from keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate, BatchNormalization
from keras.callbacks import ModelCheckpoint, EarlyStopping

# 데이터 읽어오기
train_file = "../Capstone_ThreeIdiots/DeepLearning/intent/ADD_train_data3.csv"
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
val_size = int(len(padded_seqs) * 0.1)
test_size = int(len(padded_seqs) * 0.2)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

# 하이퍼 파라미터 설정
dropout_prob = 0.3
EMB_SIZE = 128
EPOCH = 20
num_filters = 512
VOCAB_SIZE = len(p.word_index) + 1

# # 클래스 수 추출
# num_classes = len(set(intents))
# print(num_classes)

# CNN 모델
input_layer = Input(shape=(MAX_SEQ_LEN,))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)


pool_layers = []
filter_sizes = [2, 3, 4]
for filter_size in filter_sizes:
   conv = Conv1D(num_filters, kernel_size=filter_size, padding='valid', activation=tf.nn.relu)(embedding_layer)
   conv = BatchNormalization()(conv)
   pool = GlobalMaxPool1D()(conv)
   pool_layers.append(pool)

# 모든 풀링 레이어를 concatenate
concat = concatenate(pool_layers)
output = Dropout(rate=dropout_prob)(concat)
predictions = Dense(15, activation=tf.nn.softmax)(output)

# 모델 생성
model = Model(inputs=input_layer, outputs=predictions)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# 콜백 함수 설정
checkpoint = ModelCheckpoint('../Capstone_ThreeIdiots/DeepLearning/intent/best_intent_model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1)

# 모델 학습
history = model.fit(train_ds, batch_size=64, validation_data=val_ds, epochs=EPOCH, callbacks=[checkpoint, early_stopping], verbose=1)

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
