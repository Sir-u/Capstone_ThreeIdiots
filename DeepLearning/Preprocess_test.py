import sys
sys.path.append('../DeepLearning/utils/')
from Preprocess import Preprocess

# from utils.Preprocess import Preprocess

sent = "내일 오전 10시에 탕수육 주무하고 싶어"

p = Preprocess(userdic='../utils/user_dic.tsv')

pos = p.pos(sent)

ret = p.get_keywords(pos, without_tag=False)
print(ret)

ret = p.get_keywords(pos, without_tag=True)
print(ret)