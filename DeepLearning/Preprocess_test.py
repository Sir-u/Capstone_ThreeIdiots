import sys
sys.path.append('../DeepLearning/utils/')
from Preprocess import Preprocess

#from utils.Preprocess import Preprocess

sent = "내일 오전 10시에 탕수육 주문하고 싶어"

p = Preprocess(userdic='C:/Users/dowon/Desktop/Workplace/Capstone_ThreeIdiots/DeepLearning/utils/user_dic.tsv')
#######이부분 절대경로 지정했습니다, 수정 필요###

pos = p.pos(sent)

ret = p.get_keywords(pos, without_tag=False)
print(ret)

ret = p.get_keywords(pos, without_tag=True)
print(ret)