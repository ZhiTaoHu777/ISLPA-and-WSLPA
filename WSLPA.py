import collections
import numpy as np
import networkx as nx
import pandas as pd

"""加权SLPA
"""

class WSLPA:
    def __init__(self, G, T, r):
        """
        :param G:图本身
        :param T: 迭代次数T
        :param r:满足社区次数要求的阈值r
        """
        self._G = G
        self._n = len(G.nodes(False))  # 节点数目
        self._T = T
        self._r = r

    def execute(self):
        # 新建节点标签内存
        weight = {j: {} for j in self._G.nodes()}
        # 初始化内存
        for q in weight.keys():
            for m in self._G[q].keys():
                weight[q][m] = self._G[q][m]['weight']
        # 建立成员标签记录
        node_memory = []
        # 节点编号0-1000，共一千个节点，
        for i in self._G.nodes:
            node_memory.append({i: 1})
        # 开始遍历self._T次所有节点
        for t in range(self._T):
            # listenerslist = list(reversed(nx.pagerank(self._G).keys()))
            listenerslist = [x for x in np.random.permutation(self._n)]
            # 开始遍历节点
            for i in listenerslist:
                labels = {}
                # 遍历所有与其相关联的节点
                for j in self._G.neighbors(i):
                    # 标签出现的总次数
                    total = sum(node_memory[j].values())
                    # 查看speaker中node_memory中出现概率最大的标签并记录，key是标签名，value是Listener与speaker之间的权

                    # 对内存中标签出现的概率进行多项式抽样，抽样次数为1，获得出现次数最多的标签的下标k，k作为node_memory的第j个字典的第k个字典的键值
                    prob = [float(c) / total for c in node_memory[j].values()]
                    index = np.random.multinomial(1,prob)
                    label = list(node_memory[j].keys())[index.argmax()]
                    labels[label] = labels.setdefault(label, 0) + weight[i][j]
                # 查看labels中值最大的标签，让其成为当前listener的一个记录
                selected_label = max(labels, key=labels.get)
                # 如果最大标签当前节点的node_memory中,node_memory加一；如果没在，加入置为1
                node_memory[i][selected_label] = node_memory[i].setdefault(selected_label, 0) + 1

        # 根据阈值threshold删除不符合条件的标签，遍历每一个节点的内存
        for memory in node_memory:
            # 标签总数计数++++++++++++
            sum_label = sum(memory.values())
            # 标签出现的频数等于标签总数乘以阈值
            threshold_num = sum_label * self._r
            # 遍历每一个标签，如果标签出现的概率小于阈值，则删除这个标签
            for k, v in list(memory.items()):
                if v < threshold_num:
                    del memory[k]
        # 还原社区划分
        communities = collections.defaultdict(lambda: list())
        # 扫描memory中的记录标签，相同标签的节点加入同一个社区中
        for primary, change in enumerate(node_memory):
            for label in change.keys():
                communities[label].append(primary)

        # 排除相互包含的社区（上面那段注释代码不加这段也可以不加）
        # 去除重叠包含的社区
        del_list = []
        add_list = []
        C = list(communities.values())
        for i in range(len(C)):
            for j in range(i + 1, len(C)):
                if C[i] == C[j]:
                    if C[i] not in del_list:
                        del_list.append(C[i])
                    if C[i] not in add_list:
                        add_list.append(C[i])
                    continue
                if set(C[i]).issubset(set(C[j])):
                    del_list.append(C[i])
                if set(C[i]).issuperset(set(C[j])):
                    del_list.append(C[j])
        add = []
        C = [c for c in C if c not in del_list]
        for c in add_list:
            flag = True
            for item in C:
                if set(c).issubset(item):
                    flag = False
                    break
            if flag:
                add.append(c)
        for c in add:
            C.append(c)
        return C
