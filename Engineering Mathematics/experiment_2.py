# -*- coding = utf-8 -*-
# @Time : 2021/10/12 {TIME}
# @Author: 陈杰
# @File : experiment_2.py
# Software : PyCharm

import matplotlib.pyplot as plt
import numpy as np

# 最小二乘曲线拟合函数-解法方程
def curve_fitting_1(x_list, y_list, omiga_list=[]):
    # 目标是求出Ax=b这个方程组的解向量x，x的各个值组成了多项式的系数

    # 如果没有传入权重列表，则自动为其赋值为1
    if omiga_list == []:
        for i in range(len(x_list)):
            omiga_list.append(1)

    # ------------------- 内置函数 -------------------
    # 求系数矩阵A的元素，元素值与下标之和相关
    def A_item(index_sum):
        result = 0
        for x, omiga in zip(x_list, omiga_list):
            result += omiga * (x ** index_sum)
        return result

    # 求向量b的元素，元素值与下标相关
    def b_item(index):
        result = 0
        for x, y, omiga in zip(x_list, y_list, omiga_list):
            result += omiga * (x ** index) * y
        return result

    # ------------------- 求出系数矩阵A -------------------
    A = []              # 系数矩阵，应注意到此矩阵是一个对称矩阵
    item = []           # 系数矩阵中可能存在的元素值
    for i in range(5):  # 计算矩阵中的元素值，只有5个可能的取值
        item.append(A_item(i))
    for i in range(3):  # 为系数矩阵赋值
        row = []
        for j in range(3):
            row.append(item[i+j])   # 此系数矩阵是个对称矩阵，行号列号之和相同的元素的值也相同
        A.append(row)               # 将行向量加入系数矩阵中

    # ------------------- 求出向量b -------------------
    b = []              # 存储了函数值的列向量
    for i in range(3):
        b.append(b_item(i))

    # ------------------- 调用numpy函数解方程 -------------------
    x = np.linalg.solve(A, b)   # 计算解向量的值，下标为i的值是x^(2-i)的系数

    # ------------------- 绘图 -------------------
    x = list(reversed(x))       # 调用poly1d函数前，需先将x逆转，使其下标为i的值是x^i的系数
    p = np.poly1d(x)            # 使用poly1d函数生成多项式
    print(p)
    i = np.linspace(0, 1, 1000) # 取绘图点的横坐标
    p_i = p(i)                  # 取绘图点的纵坐标
    plt.plot(i, p_i)            # 绘制拟合曲线图
    plt.plot(x_list, y_list, marker='.', linestyle='')  # 描原始点
    plt.title("Method: Normal Equation")                # 标题
    plt.show()                  # 展示图像

# 最小二乘曲线拟合函数-点集上的正交多项式
def curve_fitting_2(x_list, y_list, omiga_list=[]):
    # 设多项式p_0,..,p_n关于点集x_0,..,x_m带权omiga_0,..,omiga_m正交
    # 则f(x)的最小二乘多项式为S=a_0*p_0(x) + a_1 * p_1(x) + a_2 * p_2(x)
    # 其中a与p的表达式较复杂，见PPT

    # 如果没有传入权重列表，则自动为其赋值为1
    if omiga_list == []:
        for i in range(len(x_list)):
            omiga_list.append(1)

    # ------------------- 内置函数 -------------------
    # 函数：根据给定公式求p_i(x)
    def p(index, x):
        if index == 0:
            return 1
        if index == 1:
            return x - alpha(0)
        if index == 2:
            return (x - alpha(1)) * p(1, x) - beta(1) * p(0, x)

    # 函数：根据给定公式求alpha_i
    def alpha(index):
        top = 0
        for x,y,omiga in zip(x_list,y_list,omiga_list):
            top += x * p(index, x) * p(index, x) * omiga
        bottom = 0
        for x, omiga in zip(x_list, omiga_list):
            bottom += p(index, x) * p(index, x) * omiga
        return top / bottom

    # 函数：根据给定公式求beta_i
    def beta(index):
        top = 0
        for x, omiga in zip(x_list, omiga_list):
            top += p(index, x) * p(index, x) * omiga
        bottom = 0
        for x, omiga in zip(x_list, omiga_list):
            bottom += p(index-1, x) * p(index-1, x) * omiga
        return top / bottom

    # 函数：根据给定公式求a_i
    def a(index):
        top = 0
        for x, y, omiga in zip(x_list, y_list, omiga_list):
            top += p(index, x) * y * omiga
        bottom = 0
        for x, omiga in zip(x_list, omiga_list):
            bottom += p(index, x) * p(index, x) * omiga
        return top / bottom

    # ------------------- 计算 -------------------
    x = np.linspace(0, 1, 1000)
    S = a(0) * p(0, x) + a(1) * p(1, x) + a(2) * p(2, x)
    print(a(0),a(1),a(2))

    # ------------------- 绘图 -------------------
    plt.plot(x, S)  # 绘制拟合曲线
    plt.plot(x_list, y_list, marker='.', linestyle='')  # 描原始点
    plt.title("Method: Orthogonal Polynomials")         # 标题
    plt.show()      # 展示图像


# 实验数据
x_list = [0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
y_list = [1.2, 1.5, 1.7, 2., 2.24, 2.40, 2.75, 3.]
omiga_list = [1, 1, 50, 1, 1, 1, 1, 1]

# 例题数据-解法方程
# x_list = [0,0.25,0.50,0.75,1.]
# y_list = [1.0,1.2840,1.6487,2.1170,2.7183]

# 例题数据-正交多项式
# x_list = [0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# y_list = [1.,1.75,1.96,2.19,2.44,2.71,3.]

curve_fitting_2(x_list,y_list,omiga_list)


# 解方程示例
# a = np.array([[5.,2.5,1.875], [2.5,1.875,1.5625],[1.875,1.5625,1.3828]])    # 系数矩阵
# b = np.array([8.7680,5.4514,4.4015])    # 解向量
# x = np.linalg.solve(a, b)   # 计算
# print(x)


