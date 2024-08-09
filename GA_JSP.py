'''
调度问题
题目：给出5个工件，4台机器，确定工件在每台机器上的最优工序，使得最大流程时间达到最小
（每台机器只能加工一个工件，一个工件不能同时在不同的机器上加工）
工件\机器    A    B    C     D
1          31   41   25    30
2          19   55   3     34
3          23   42   27    6
4          13   22   14    13
5          33   5    57    19
'''
import random
def test_008(nums):
    def random_answer(nums):
        fact_n = len(nums)#工件的数量
        fact = [1 for i in range(fact_n)]#对应工件的适应度
        machine_n = len(nums[0])#机器数量
        result = [[]for i in range(machine_n)]#初始化空列表
        while(True):
            if sum(fact) == 0:
                break
            choice = [i for i in range(fact_n)]
            for i in range(machine_n):
                val = random.choices(choice)[0]#随机从choice抽取工件，并移除
                choice.remove(val)
                if fact[val] == 0:
                    result[i].append('')
                    continue #如果一个工件被分配完毕【fact【val】为0】，就在结果列表中添加空字符，并进行下一次循环
                result[i].append(val)#否则工件被分配给机器i
                fact[val] -= 1/nums[val][i] #val工件的索引 i机器的索引 nums[val][i]工件val在机器i上的完成时间 倒数，理解为处理工件的效率
                if fact[val] < 0:
                    fact[val] = 0
        # for item in result:
        #     print(item)
        # print(fact)
        # print(len(result[0]))
        return result

    def start(answer, n, nums):
        res = [1 for i in range(len(nums))]
        for i in range(len(answer)):
            for j in range(n):
                if answer[i][j] == '':
                    continue
                res[answer[i][j]] -= 1/nums[answer[i][j]][i]
                if res[answer[i][j]] < 0:
                    res[answer[i][j]] = 0
        return res

    def end(answer, res, nums):
        n = -1
        while(True):
            if sum(res) == 0 or n == len(answer[0]) - 1:
                break
            n += 1
            for i in range(len(answer)):
                if answer[i][n] == '':
                    continue
                res[answer[i][n]] -= 1/nums[answer[i][n]][i]
                if res[answer[i][n]] < 0:
                    res[answer[i][n]] = 0
        return n + 2

    def change(x, y):
        length = len(x[0])
        x_left = []
        x_right = []
        y_left = []
        y_right = []
        for i in range(len(x)):
            x_left.append(x[i][:length // 2])
            x_right.append(x[i][length //2:])
            y_left.append(y[i][:length // 2])
            y_right.append(y[i][length //2:])
        res_x = start(x_left, length // 2, nums)
        n_x = end(y_right, res_x, nums)
        res_y = start(y_left, length // 2, nums)
        n_y = end(x_right, res_y, nums)
        x, y = [], []
        for i in range(len(x_left)):
            mid_x = x_left[i] + y_right[i][:n_x]
            mid_y = y_left[i] + x_right[i][:n_y]
            x.append(mid_x)
            y.append(mid_y)
        return [x, y]

    def variate(new_group):
        return new_group

    group_num = 1000
    times = 100
    group = []
    choice = []
    res_group = []
    for i in range(group_num):
        answer = random_answer(nums)
        group.append(answer)
        choice.append(1/len(answer[0]))
    choice = [item/sum(choice) for item in choice]
    for i in range(1, len(choice)):
        choice[i] += choice[i - 1]
    for i in range(times):
        new_group = []
        for j in range(group_num//2):
            team = []
            for t in range(2):
                y = random.random()
                if choice[0] >= y:
                    team.append(group[0])
                    continue
                for tt in range(1, len(choice)):
                    if choice[tt - 1] < y and y <= choice[tt]:
                        team.append(group[tt])
                        break
            new_group.extend(change(team[0], team[1]))
        new_group = variate(new_group)
        group = new_group
        mid_group = [len(item[0]) for item in new_group]
        min_index = mid_group.index(min(mid_group))
        res_group.append([new_group[min_index], min(mid_group)])

    res_group.sort(key = lambda x:x[1], reverse = False)
    for item in res_group:
        print(item[1])
    for item in res_group[0][0]:
        print(item)
    return

nums = [[31,41,25,30],
        [19,55,3,34],
        [23,42,27,6],
        [13,22,14,13],
        [33,5,57,19]]
test_008(nums)