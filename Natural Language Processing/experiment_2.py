"""
==================================
@author:    陈杰
@time:      2022/3/17 15:14
@function: 利用给定语料，构建HMM模型。编写能够满足下面要求的程序：程序运行之后，能够输出三个模型参数文件
==================================
"""

import re
from collections import defaultdict
from time import perf_counter

# 计算开始时间
start = perf_counter()

# ------------------------------------------ 配置参数 ------------------------------------------
corpus_path = "199801-UTF8.txt"
pi_path = "./experiment_2/pi.txt"
A_path = "./experiment_2/A.txt"
B_path = "./experiment_2/B.txt"

# ------------------------------------------ 处理语料 ------------------------------------------

# 句首词性频率 --- 用于计算初始状态的概率pi
postag_begin_freq = defaultdict(int)
# 句首词性总数 --- 用于计算初始状态概率pi
postag_begin_num = 0
# 词性序列 --- 用于计算状态转移矩阵A
postag_seq = []
# 词性发射频率，即某词性映射为了某词语多少次 --- 用于计算发射矩阵B
postag_to_word_freq = {}

# 载入语料
with open(corpus_path, encoding="utf8") as f:
    sentences = f.readlines()
    for sentence in sentences:
        # 忽略空行
        if sentence == "\n":
            continue
        # 删除句首无用的时间标记
        sentence = re.sub("199.*?/m", "", sentence)
        # 将句子分为多个元素，形如"古琴/n"
        sentence = sentence.split()

        for i, item in enumerate(sentence):
            # 将句子元素分为词语和词性，其中item[0]为词语，item[1]为词性
            item = item.split("/")
            word = item[0]
            postag = item[1]

            # 去除复合词组中的"["标记
            if word[0] == "[":
                word = re.sub("^\[", "", word)
            # 去除复合词组中的"]"标记以及紧跟其后的标签
            if "]" in postag:
                postag = re.sub("].*", "", postag)

            # 记录句首词性频率 --- 用于计算初始状态概率pi
            if i == 0:
                postag_begin_freq[postag] += 1
                postag_begin_num += 1

            # 如果词性发射频率字典中无此词性，则新增关于此词性的映射 --- 用于计算发射矩阵B
            if postag not in postag_to_word_freq:
                postag_to_word_freq[postag] = defaultdict(int)
            # 记录此词词性转化为了哪个词，将对应词的词频加1
            postag_to_word_freq[postag][word] += 1

            # 将词性加入到词性序列中
            postag_seq.append(postag)

# ------------------------------------------ 数据计算 ------------------------------------------


# 遍历词性序列，计算词性转换为下一个词性的频率 --- 用于计算状态转移矩阵A
postag_to_next_freq = {}
for i, postag in enumerate(postag_seq):
    # 最后一个词性不会转换为下一个词性，不进行计算
    if i == len(postag_seq) - 1:
        break
    if postag not in postag_to_next_freq:
        postag_to_next_freq[postag] = defaultdict(int)
    postag_to_next_freq[postag][postag_seq[i + 1]] += 1

# 将 下一个词性频率 转换为概率 --- 此概率即为状态转移矩阵A
for key, val in postag_to_next_freq.items():
    num = 0
    for freq in val.values():
        num += freq
    for postag, freq in val.items():
        postag_to_next_freq[key][postag] = freq / num

# 将 句首词性频率 转换为概率 --- 此概率即为初始状态的概率pi
for key, val in postag_begin_freq.items():
    postag_begin_freq[key] = val / postag_begin_num

# 将 词性发射频率 转换为概率 --- 此概率即为发射矩阵B
for key, val in postag_to_word_freq.items():
    num = 0
    for freq in val.values():
        num += freq
    for word, freq in val.items():
        postag_to_word_freq[key][word] = freq / num

# ------------------------------------------ 数据验证 ------------------------------------------

# 计算初始概率pi之和是否为1，若不为1则可能发生了数据溢出
sum = 0
for postag, prob in postag_begin_freq.items():
    sum += prob
print("初始状态概率之和为%s。" % sum)
print()

# 计算状态转移矩阵A每一行的概率和是否为1，若不为1则可能发生了数据溢出
for postag, val in postag_to_next_freq.items():
    sum = 0
    for prob in val.values():
        sum += prob
    print("词性%s的下一个词性概率之和为%s" % (postag, sum))
print()

# 计算发射矩阵B的每一行的和是否为1，若不为1则可能发生了数据溢出
for postag, val in postag_to_word_freq.items():
    sum = 0
    for prob in val.values():
        sum += prob
    print("词性%s的发射概率之和为%s" % (postag, sum))
print()

# ------------------------------------------ 写入文件 ------------------------------------------

with open(pi_path, "w") as f:
    # 将pi中键值对按概率值降序排列，返回结果是一个由元组构成的列表
    sorted_tup = sorted(postag_begin_freq.items(), key=lambda x: x[1], reverse=True)
    for postag, prob in sorted_tup:
        f.write("%s : %s\n" % (postag, prob))

with open(A_path, "w") as f:
    for postag_source, val in postag_to_next_freq.items():
        # 将A的一行结果按概率值降序排列，返回结果是一个由元组构成的列表
        sorted_tup = sorted(val.items(), key=lambda x: x[1], reverse=True)
        for postag_target, prob in sorted_tup:
            f.write("%s -> %s : %s\n" % (postag_source, postag_target, prob))
        f.write("\n")

with open(B_path, "w") as f:
    for postag, val in postag_to_word_freq.items():
        # 将B的一行结果按概率值降序排列，返回结果是一个由元组构成的列表
        sorted_tup = sorted(val.items(), key=lambda x: x[1], reverse=True)
        for word, prob in sorted_tup:
            f.write("%s -> %s : %s\n" % (postag, word, prob))
        f.write("\n")

# ------------------------------------------ 程序结束 ------------------------------------------

end = perf_counter()
print("程序运行完成，共耗时%s秒~" % (end - start))
