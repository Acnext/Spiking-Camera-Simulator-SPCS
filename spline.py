from geomdl import fitting
from geomdl.visualization import VisMPL as vis
import matplotlib.pyplot as plt
import math
import random
import numpy as np
# The NURBS Book Ex9.1
def rand_points(n = 10, degree = 3):
    temp = [(0, 0, 0)]
    for i in range(n):
        temp.append((random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8)))
    return tuple(temp)
def dis(a, b, degree):
    if degree == 2:
        return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2]))
def get_node(points = ((0, 0, 0), (10, 10, 10), (20, 20, 20), (30, 30, 30), (40, 40, 40)), degree = 3, step_size = 0.0005, rand_flag = True, rand_num = 15, num_action = 10):
    #根据输入节点生成相机轨迹(其中step_size控制节点步长,即两点之间的距离) rand_flag表示使用随机点生成轨迹 否则使用用户输入的点进行轨迹生成
    #print(type(points)) 
    if rand_flag:#输入节点
        points = rand_points(rand_num, degree)
    #degree = 2  # cubic curve #节点维度
    # Do global curve interpolation
    curve = fitting.interpolate_curve(points, degree) #生成spline, spline属于curve类
    # Plot the interpolated curve
    temp = 0
    for i in range(1, len(curve.evalpts)):
        temp = temp + dis(curve.evalpts[i], curve.evalpts[i - 1], degree)
    curve.sample_size = 1 + int(temp / step_size + 0.5)
    """#可视化生成曲线
    curve.vis = vis.VisCurve2D()
    curve.render()
    x = []
    y = []
    for i in curve.evalpts:
        x.append(i[0])
        y.append(i[1])
        plt.axis([-10,10,-10,10])
        plt.plot(x, y)
        plt.show()"""
    print(type(curve.evalpts))
    if len(curve.evalpts) <= num_action:
        print("the num of act node is not enough")
    return np.array(curve.evalpts[0:num_action+10])
if __name__ == "__main__":
    #print(curve.delta)
    a = get_node()
    print(len(a))
    #print((get_node()))