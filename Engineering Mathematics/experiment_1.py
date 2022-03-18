# 实验内容：对原始函数f(x)=1/(1+x^2)进行多项式插值，绘制（-5,5）区间内的原始图像和多项式插值图像
# 注意：过程中会出现龙格现象

import matplotlib.pyplot as plt
import numpy as np

# 拉格朗日插值多项式绘制函数，输入参数为等距节点的数量
def lagrange_interpolation(p_numbers) :
    # 等距节点的x坐标列表
    x_nodes = []
    # 等距节点的y坐标列表
    y_nodes = []

    # 求x、y的具体值
    i = 0
    while i < p_numbers:
        x_nodes.append(-5 + 10 / (p_numbers + 1) * (i + 1))
        y_nodes.append(1 / (1 + x_nodes[i] * x_nodes[i]))
        i = i + 1

    # 用拉格朗日差值计算近似值
    def L(x):
        # 多项式求和
        i = 0
        result = 0
        while i < p_numbers:
            result = result + item(i, x)
            i = i + 1
        return result

    # 求拉格朗日差值多项式的第i项
    def item(i, x):
        # 分子，初始值为yi
        top = y_nodes[i]
        # 分母
        bottom = 1

        # 多项式求积
        j = 0
        while j < p_numbers:
            if (j != i):
                top = top * (x - x_nodes[j])
                bottom = bottom * (x_nodes[i] - x_nodes[j])
            j = j + 1
        return top / bottom

    # 插值多项式图像
    lx = np.linspace(-5, 5, 10000)
    ly = L(lx)
    plt.plot(lx, ly)

# 绘制原始图像
x = np.linspace(-5, 5, 10000)
y = 1 / (1 + x * x)
plt.plot(x, y)

# 绘制插值多项式图像
lagrange_interpolation(15)

# 限制横轴坐标区间为（-5,5），纵轴坐标区间为（-0.1,1.1）
plt.axis([-5, 5, -0.1, 1.1])
# 图像标题
plt.title("original vs 101")
# 显示图像
plt.show()