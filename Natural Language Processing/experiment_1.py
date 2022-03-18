"""
==================================
@author:    陈杰
@time:      2022/3/13 9:55
@function:  利用给定语料，构建BiGram模型。当用户输入一个句子之后，输出该句子的概率。
==================================
"""
import re
from collections import defaultdict
from ltp import LTP

# ------------------------------------------ 配置参数 ------------------------------------------
corpus_path = "199801-UTF8.txt"
delta = 0.5     # 加δ平滑的参数δ

# ------------------------------------------ 处理语料 ------------------------------------------

# 载入语料，建立词表
all_words = []
with open(corpus_path, encoding="utf8") as f:
    sentences = f.readlines()
    for sentence in sentences:
        # 删除句首的时间标记，减小词表
        sentence = re.sub("199.*?/m", "", sentence)
        # 替换掉语料中的词性标记
        words = re.sub("/.*? ", " ", sentence).split()
        # 增加句子开始符号
        all_words.append("<BOS>")
        # 将句子单词加入词表
        all_words += words
        # 增加句子结束符号
        all_words.append("<EOS>")

# 统计词频，建立词典
word_freqs = defaultdict(int)
for word in all_words:
    word_freqs[word] += 1

# ------------------------------------------ 输入句子并分词 ------------------------------------------

# 分词工具
ltp = LTP()

def judge():

    input_sentence = input("请输入一个句子：")
    # input_sentence = "同胞们、朋友们、女士们、先生们" # 测试用例
    input_words, _ = ltp.seg([input_sentence])
    input_words = ["<BOS>"] + input_words[0] + ["<EOS>"]

# ------------------------------------------ 计算概率 ------------------------------------------

    p = 1
    for i, input_word in enumerate(input_words):
        if input_word == "<BOS>":
            continue
        m = delta
        for j, word in enumerate(all_words):
            if j == 0:
                continue
            if word == input_word and all_words[j - 1] == input_words[i - 1]:
                m += 1
        n = word_freqs[input_words[i-1]] + delta * len(word_freqs) - 2
        p *= m / n
        print("The word is %s, m = %s, n = %s, p = %s" %(input_word, m, n, p))

    print("您输入句子的概率的是%s\n" % p)

if __name__ == '__main__':
    for _ in range(100):
        judge()
