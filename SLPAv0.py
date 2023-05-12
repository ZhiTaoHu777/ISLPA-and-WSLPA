import collections
import random
import numpy as np
import networkx as nx
import ONMI_Calc


# SLPA最初原版本，两次随机选择
class SLPAv0:
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
        # 节点存储器初始化
        node_memory = []
        # 节点编号0-1000，共一千个节点，
        for i in self._G.nodes:
            node_memory.append({i: 1})

        # 算法迭代过程
        for t in range(self._T):
            # 任意选择一个监听器
            # np.random.permutation()：随机排列序列
            listenerslist = [x for x in np.random.permutation(self._n)]
            # rank = sorted(nx.pagerank(self._G).items(), key=lambda x: x[1], reverse=False)
            # listenerslist = []
            # for item in order:
            #     listenerslist.append(item[0])
            # 遍历节点序列，
            for i in listenerslist:
                label_list = {}
                # 从speaker中选择一个标签传播到listener
                # 遍历它的邻居
                for j in self._G.neighbors(i):
                    # 将j作为角标的时候要减去1
                    # 数一数邻居内存中的标签数量，单个标签可能出现多次

                    # 标签出现的总次数
                    total = sum(node_memory[j].values())
                    # 查看speaker中node_memory中出现概率最大的标签并记录，key是标签名，value是Listener与speaker之间的权
                    # 对内存中标签出现的概率进行多项式抽样，抽样次数为1，获得出现次数最多的标签的下标k，k作为node_memory的第j个字典的第k个字典的键值
                    prob = [float(c) / total for c in node_memory[j].values()]
                    index = np.random.multinomial(1, prob)
                    label = list(node_memory[j].keys())[index.argmax()]
                    label_list[label] = label_list.setdefault(label, 0) + 1

                # listener选择一个最流行的标签添加到内存中
                max_v = max(label_list.values())
                # selected_label = max(label_list, key=label_list.get)
                # 如果流行程度相同，选择第一个作为标签
                selected_label = random.choice([item[0] for item in label_list.items() if item[1] == max_v])
                # setdefault如果键不存在于字典中，将会添加键并将值设为默认值。
                node_memory[i][selected_label] = node_memory[i].setdefault(selected_label, 0) + 1

        # 根据阈值threshold删除不符合条件的标签，遍历每一个节点的内存
        for memory in node_memory:
            # 标签总数计数
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
        return communities.values()





