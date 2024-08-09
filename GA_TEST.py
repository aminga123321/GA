
#问题：在一个长度为n的数组nums中选中10个元素，使得10个元素的和
#与原数组的元素之和的1/10无限接近
'''
遗传算法思路
1.随机生成种群：在n个数中取10个数作为一个数组，随机生成10个
2.选择优秀个体并进行基因片段交换
2.1选择优秀个体：构造每个个体与正确值之间的误差，归一化，进而构造概率分布
2.2基因片段交换：随机函数random,确定交换片段
3.突变：当随机数小于突变因子，随机对个体上随机位置进行数字更换，有利于避免局部最优解
4.迭代：在每次片段交换和突变后的优秀种群上进行迭代，每次迭代存储最优解，最后排序输出最最优解
'''

import random

# 在原始数组中随机生成n组数组
#random.sample(arr,n) 在set数组中随机选n个元素组成数组
#arr.append(set)添加数组到arr末尾
def creat_answer(numbers_set, n): #numbers_set是一个数组，每一个元素都是数组
    result = []
    for i in range(n):
         result.append(random.sample(numbers_set,10))
    return result
#误差函数
def error_level(new_answer,numbers_set):
    error = [] #存储选中对应随机个体与正确解的误差的概率
    right_answer = sum(numbers_set) / 10
    for item in new_answer:
        value = abs( right_answer - sum(item)) #个体与正确解的误差的绝对值
        if value == 0:
            error.append(10) #如果误差 为0  添加10 表示选中的概率很大  添加10 是因为 最小精度为0.1 倒数为10
        else:
            error.append(1 / value) #用1/value 表示选中的概率 value越大 被选中的概率越小
    return error
#选择误差较小的片段进行交换
def choice_selected(old_answer , numbers_set):
    result = []
    error = error_level(old_answer , numbers_set) #对上一次迭代的结果 求取对应的误差概率
    error_one = [item/sum(error) for item in error ] #对 error中的元素归一化
    for i in range( 1 , len(error_one)):
        error_one[i] += error_one[i - 1] # 概率分布 有点前缀和的意思
    for i in range ( len(old_answer)//2): #len//2得出整数解
        temp = [] #存储两个个体
        for j in range(2): #选择两个个体，进行数据交换
            rand = random.uniform(0,1) #这里的rand用于随机选择old_answer数组的个体
            for k in range( len(error_one)):
                if k == 0:
                    if rand < error_one[k]:
                        temp.append(old_answer[k])
                else:
                    if rand >= error_one[k-1] and rand < error_one[k]:
                        temp.append(old_answer[k])
        rand = random.randint(0,6) #这里的rand用于个体中从哪开始交换片段
        temp_1 = temp[0][:rand] + temp[1][rand:rand+3] + temp[0][rand+3:] #交换片段
        temp_2 = temp[1][:rand] + temp[0][rand:rand+3] + temp[1][rand+3:]
        result.append(temp_1)
        result.append(temp_2)
    return  result #每个循环交换片段，生成两个新的个体，循环len//2次
#突变操作
def variation(old_answer,nummber_set,pro):
    for i in range(len(old_answer)):
        rand = random.uniform(0,1)
        if rand < pro:
            rand_num = random.randint(0,9)
            old_answer[i] =  old_answer[i][:rand_num] + random.sample(numbers_set,1) +old_answer[i][rand_num+1:]
    return old_answer


numbers_set = random.sample(range(0, 1000), 50)  # 0-1000里随机生成50个数组 组成一个集合
middle_answer = creat_answer(numbers_set, 10)  #创造100个解的初始解集，每个解10个1000以内的随机整数
first_answer = middle_answer[0]
great_answer = []
#print(middle_answer)
#print(numbers_set)


for i in range(1000):
    middle_answer = choice_selected(middle_answer , numbers_set)
    middle_answer = variation(middle_answer,numbers_set,0.1)
    error = error_level(middle_answer,numbers_set)
    index = error.index(max(error)) #找到误差最小的下标
    great_answer.append([middle_answer[index],error[index]])#存储起来
great_answer.sort(key = lambda x : x[1],reverse=True)
print("原数组",numbers_set)
print("正确答案为",sum(numbers_set)/10)
print("给出的最优解为",great_answer[0][0])
print("该和为",sum(great_answer[0][0]))
print("选择系数为",great_answer[0][1])
print("最初解的和为",sum(first_answer))
#print("最好的解",great_answer)