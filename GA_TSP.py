import random

import pandas as pd
import logging
import numpy as np
import matplotlib.pyplot as plt
import copy
#定义中文字体格式
plt.rcParams['font.sans-serif'] = ["SimHei"]
def load():
    df = pd.read_csv("./TSP问题测试数据集/oliver30.tsp",skiprows=6,header=None,sep=" ")
    city_num = len(df[0])
    city_name = df[0][0:city_num-1].tolist() #最后一行EOF不读入  这里数字仅代表城市名字 与下面的距离矩阵的ij不相关
    x = df[1][0:city_num - 1]
    y = df[2][0:city_num - 1]#获取城市平面坐标
    city_location = list(zip(x,y))
    return city_name,city_location


def dict_cal(loca1, loca2):
    return ((loca1[0] - loca2[0])**2 + (loca1[1] - loca2[1])**2 )**0.5


def martix_dis(city_name, city_location):#待改进
    city_num = len(city_name)

    martix_distance = np.zeros((city_num,city_num))#初始化矩阵 都为0
    for i in range(city_num):

        for j in range(i+1,city_num):#i+1 为了保持对角线全为0
            martix_distance[i][j] = dict_cal(city_location[i],city_location[j]) #城市i到城市j的距离
            martix_distance[j][i] = martix_distance[i][j]

    return martix_distance


def com_dist(rand_pop, martix_distance):
    dist = 0
    num = len(rand_pop)-1
    for i in range(num):
        dist+=martix_distance[rand_pop[i]][rand_pop[i+1]]
    dist+= martix_distance[rand_pop[-1]][rand_pop[0]]

    return dist


def rand_pop(city_num, pop_num, pop, distance, martix_distance):
    rand_pop = [i for i in range(city_num)]#待修改

    pop_sub =[] #新种群
    for i in range(pop_num):
        random.shuffle(rand_pop)
        pop[i][:] = rand_pop
        distance[i] = com_dist(rand_pop,martix_distance)#计算每个个体的路径




#轮盘赌法，选择个体
def select_sub(pop_num, pop, distance):
    next_sub=[]
    # distance_copy = copy.deepcopy(distance)
    # #归一化
    # distance_copy =[1.0/item for item in distance_copy]
    # total = sum(distance_copy)
    # for i in range(len(distance)):
    #     distance_copy[i] = distance_copy[i]/total
    # #求解概率
    # for i in range(1,len(distance_copy)):
    #     distance_copy[i]+=distance_copy[i-1]
    fit = 1.0 / distance
    p = fit / sum(fit)
    q = p.cumsum()#累积概率

    for i in range(pop_num):
        rand = random.uniform(0,1)#随机概率
        for j in range(len(distance)-1):
            if rand<=q[0]:
                next_sub.append(pop[0])
                break
            elif rand>q[j] and rand<=q[j+1]:
                next_sub.append(pop[j+1])
                break


    return next_sub


def intercross(a, b):
    a1 = a.copy()
    b1 = b.copy()
    index1,index2 = random.randint(0,len(a)-1),random.randint(0,len(a)-1)
    while index1==index2:
        index2 = random.randint(0,len(a)-1) #这里包含len(a)
    l,r = min(index1,index2),max(index1,index2)
    for i in range(l,r+1):
        a2 = a.copy()
        b2 = b.copy()#这里的a2，b2表示为在这次循环中替换前的a,b

        a[i] = b1[i]
        b[i] = a1[i]
        x = np.argwhere(a==a[i])#这里检查换后重复的索引，而不能a==a1p[i],
        y = np.argwhere(b==b[i])

        if(len(x)==2):
            a[x[x!=i]] = a2[i]#将在其他索引的重复处，替换为最开始替换出的数
        if(len(y)==2):
            b[y[y!=i]] = b2[i]
    return a,b

'''
a: 0 1 3 4 2       a2: 0 1 3 4 2
b: 2 4 1 0 3       b2: 2 4 1 0 3 
对index为1交换为
a: 0 4 3 4 2 
b: 2 1 1 0 3
将在其他索引的重复处，替换为最开始替换出的数
a: 0 4 3 1 2 
b: 2 1 4 0 3

'''
def cross_sub(city_num, pop_num, next_gen, cross_prob, evbest_path):
    for i in range(pop_num):
        rand = random.uniform(0,1)
        if rand <= cross_prob:
            next_gen[i][:] ,evbest_path = intercross(next_gen[i][:],evbest_path)


def mutation_sub(city_num, pop_num, next_gen, mut_prob):
    for i in range(pop_num):
        rand = random.uniform(0,1)
        if rand <= mut_prob:
            index1,index2 = np.random.randint(city_num),np.random.randint(city_num)#不包含右边
            while index1==index2:
                index2 = np.random.randint(city_num)
            l,r = min(index1,index2),max(index1,index2)
            next_gen[i][l:r] = next_gen[i][l:r][::-1]


def draw_iter(iterate, best_distance_list):
    iteration = np.linspace(1,iterate,iterate)#x轴 间距为1
    plt.plot(iteration,best_distance_list)
    plt.xlabel("迭代次数")
    plt.ylabel("最短路径长度")
    plt.savefig("figure.png")
    plt.show()



def print_path(city_num, path):
    res = str(path[0]+1)+'--->' #+1是之前城市从0开始的
    for i in range(1,len(path)):
        res += str(path[i]+1)+'--->'
    res += str(path[0]+1)
    print("最佳路径为：")
    print(res)


def draw_path(city_num, city_location, path, distance):
    fig,ax = plt.subplots()
    x,y = zip(*city_location)
    ax.scatter(x,y,linewidths=0.1)#绘制坐标
    for i,txt in enumerate(range(1,len(city_location)+1)):
        ax.annotate(txt,(x[i],y[i]))#写标签
    res = path
    x0 = [x[i] for i in res]
    y0 = [y[i] for i in res]
    ax.annotate("起点",(x0[0],y0[0]))
    ax.annotate("终点",(x0[-1],y0[-1]))
    #绘制箭头图
    for i in range(city_num-1):
        plt.quiver(x0[i],y0[i],x0[i+1]-x0[i],y0[i+1]-y0[i],color ='b',width=0.005,angles='xy',scale=1,scale_units='xy')
    plt.quiver(x0[-1], y0[-1], x0[ 0] - x0[-1], y0[0] - y0[-1], color='b', width=0.005, angles='xy', scale=1,
               scale_units='xy')
    plt.title("遗传算法优化路径-最短路径："+str(distance))
    plt.xlabel("城市位置横坐标")
    plt.ylabel("城市位置纵坐标")
    plt.savefig("map.png")
    plt.show()



def main():
    city_name,city_location = load() #都是list
    #创建城市映射表 键值对 城市：坐标
    city_table = dict(zip(city_name,city_location))
    #城市距离矩阵
    martix_distance = martix_dis(city_name,city_location)
    city_num = len(city_name)
    pop_num = 300 #种群个数
    cross_prob = 0.9 #交叉概率
    mut_prob = 0.5 #变异概率
    iterate = 1000 #迭代次数

    #初始化初代种群 和 每个个体的 个体为整数 距离为浮点数
    pop = np.zeros((pop_num,city_num),dtype=int)
    distance = np.zeros(pop_num)

    #初始化种群 和个体距离
    rand_pop(city_num,pop_num,pop,distance,martix_distance)

    #初始化最好的个体，最好的距离，以及对应的列表
    evbest_path = pop[0]
    evbest_distance = float('inf') #正无穷大的浮点数
    best_path_list = []
    best_distance_list =[]

    #循环迭代遗传过程
    for i in range(iterate):
        #选择
        next_gen = select_sub(pop_num,pop,distance)
        #交叉
        cross_sub(city_num,pop_num,next_gen,cross_prob,evbest_path)
        #变异
        mutation_sub(city_num,pop_num,next_gen,mut_prob)

        #更新每个个体的路程
        for j in range(pop_num):
            distance[j] = com_dist(next_gen[j][:],martix_distance)

        index = distance.argmin()#获取最小个体的下标
        #记录每次迭代的最短路径以及距离
        if evbest_distance>distance[index]:
            evbest_distance = distance[index]
            evbest_path = next_gen[index][:]
        else:
            distance[index] = evbest_distance
            next_gen[index][:] = evbest_path
        best_distance_list.append(evbest_distance)
        best_path_list.append(evbest_path)

    #绘制迭代次数与最优解的关系曲线图
    print(best_distance_list)
    draw_iter(iterate,best_distance_list)

    best_path = evbest_path
    best_distance = evbest_distance

    #迭代完成打印最佳路径
    print_path(city_num,best_path)

    #绘制路径图
    draw_path(city_num,city_location,best_path,best_distance)




if __name__ =='__main__':
    main()