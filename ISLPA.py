import collections
import numpy as np
import networkx as nx

# SLPA 改进第一版本，度顺序邻接序列排序，使用jaccard相似性进行选择
class ISLPA:
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
        for i in range(len(self._G)):
            node_memory.append({i: 1})
        # print(node_memory)

        # 算法迭代过程
        for t in range(self._T):
            # 任意选择一个监听器
            # np.random.permutation()：随机排列序列
            # source = list(nx.degree(self._G))[0][0]
            # listenerslist = nx.bfs_tree(self._G,source)

            # listenerslist = [c[0] for c in sorted(nx.degree(self._G), key=lambda x: x[1], reverse=False)]

            listenerslist = [c[0] for c in sorted(nx.degree(self._G),key=lambda x:x[1],reverse=True)]
            # 遍历节点序列，
            for i in listenerslist:
                label_list = {}
                # 从speaker中选择一个标签传播到listener
                # 遍历它的邻居
                for j in self._G.neighbors(i):
                    # 数一数邻居内存中的标签数量，单个标签可能出现多次
                    sum_label = sum(node_memory[j].values())
                    # 对内存中标签出现的概率进行多项式抽样，抽样次数为1，获得出现次数最多的标签的下标k，k作为node_memory的第j个字典的第k个字典的键值

                    label = list(node_memory[j].keys())[
                        np.random.multinomial(1, [float(c) / sum_label for c in node_memory[j].values()]).argmax()]
                    # label = list(node_memory[j].keys())[
                    #     np.random.multinomial(1, [float(c) / sum_label for c in node_memory[j].values()]).argmax()]
                    label_list[label] = label_list.setdefault(label, 0) + 1

                # listener选择一个最流行的标签添加到内存中
                max_v = max(label_list.values())
                # selected_label = max(label_list, key=label_list.get)
                # 如果流行程度相同，使用jaccad进行判断
                candidate_list = [item[0] for item in label_list.items() if item[1] == max_v]
                max_index = self.jaccard_index(i, candidate_list)
                # selected_label = random.choice([item[0] for item in label_list.items() if item[1] == max_v])
                selected_label = candidate_list[max_index]
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

        # 返回值是个数据字典，value以集合的形式存在
        return C

    def ra_index(self, n, l):
        index = 0
        max_ra = 0
        for i in range(len(l)):
            a = set(nx.neighbors(self._G, n))
            b = set(nx.neighbors(self._G, l[i]))
            ra = 0
            for j in a.intersection(b):
                ra += 1 / nx.degree(self._G, j)
            if ra > max_ra:
                max_ra = ra
                index = i
        return index

    def jaccard_index(self, n, l):
        index = 0
        max_jarccard = 0
        for i in range(len(l)):
            a = set(nx.neighbors(self._G, n))
            b = set(nx.neighbors(self._G, l[i]))
            jarccard = len(a.intersection(b)) / len(a.union(b))
            if jarccard > max_jarccard:
                max_jarccard = jarccard
                index = i
        return index






