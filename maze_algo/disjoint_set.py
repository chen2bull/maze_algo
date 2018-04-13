#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
In computer science, a disjoint-set data structure (also called a union–find data structure or merge–find set) is a
data structure that tracks a set of elements partitioned into a number of disjoint (non-overlapping) subsets.
It provides near-constant-time operations (bounded by the inverse Ackermann function) to add new sets, to merge
existing sets, and to determine whether elements are in the same set. In addition to many other uses (see the
Applications section), disjoint-sets play a key role in Kruskal's algorithm for finding the minimum spanning
tree of a graph.

Note that the implementation as disjoint-set forests doesn't allow the deletion of edges, even without path compression
or the rank heuristic.
"""
from abc import ABC, abstractmethod


class AbstractDisjointSet(ABC):
    @abstractmethod
    def union(self, p: int, q: int) -> None:
        """
        在p和q之间添加一条连接
        """
        pass

    @abstractmethod
    def find(self, p: int) -> int:
        """
        返回p所在的分量的标识符
        """
        pass

    @abstractmethod
    def is_connected(self, p: int, q: int) -> bool:
        """
        判断p和q两点是否连通
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        返回连通分量的数量
        """
        pass


class QuickUnionDisjointSet(AbstractDisjointSet):
    """
    union时间复杂度为树的高度，find时间复杂度为树的高度,然而都不是lgN
    任何时候都不该使用这个实现，用WeightQuickUnionDisjointSet代替
    """

    def __init__(self, n: int):
        self._count = n
        self.parent_map = {}
        for i in range(n):
            self.parent_map[i] = i

    def union(self, p: int, q: int) -> None:
        p_root = self.find(p)
        q_root = self.find(q)
        if q_root == p_root:
            return
        self.parent_map[p_root] = q_root
        self._count = self._count - 1

    def find(self, p: int) -> int:
        while p != self.parent_map[p]:
            p = self.parent_map[p]
        return p

    def is_connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)

    def count(self) -> int:
        return self._count

    def __repr__(self):
        return str({
            "parent_map": self.parent_map,
            "count": self._count,
        })


class QuickFindDisjointSet(AbstractDisjointSet):
    """
    union时间复杂度为N，find时间复杂度为1
    查找高效,但 union低效的实现，不适用于需要动态给两个节点建立连接的情况
    """

    def __init__(self, n: int):
        self._count = n
        self.parent_map = {}
        for i in range(1, n):
            self.parent_map[i] = i

    def union(self, p: int, q: int) -> None:
        p_id = self.find(p)
        q_id = self.find(q)
        if q_id == p_id:
            return
        for i in self.parent_map.items():
            if self.parent_map[i] == p_id:
                self.parent_map[i] = q_id
        self._count = self._count - 1

    def find(self, p: int) -> int:
        return self.parent_map[p]

    def is_connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)

    def count(self) -> int:
        return self._count


class WeightQuickUnionDisjointSet(AbstractDisjointSet):
    def __init__(self, n: int):
        """`
        union时间复杂度为logN，find时间复杂度为logN
        加了路径压缩以后，union和find时间复杂度接近1（有均摊成本）
        """
        self._count = n
        self.parent_map = {}
        self.sz_map = {}
        for i in range(n):
            self.parent_map[i] = i
            self.sz_map[i] = 1

    def union(self, p: int, q: int) -> None:
        p_root = self.find(p)
        q_root = self.find(q)
        if q_root == p_root:
            return
        # 总是把小树的根节点连接到大树的根节点
        if self.sz_map[p_root] < self.sz_map[q_root]:
            self.parent_map[p_root] = q_root
            self.sz_map[q_root] = self.sz_map[p_root] + self.sz_map[q_root]
        else:
            self.parent_map[q_root] = p_root
            self.sz_map[p_root] = self.sz_map[p_root] + self.sz_map[q_root]
        self._count = self._count - 1

    def find(self, p: int) -> int:
        q = p
        while q != self.parent_map[q]:
            q = self.parent_map[q]
        # # 路径压缩,压缩以后高度为2了
        while p != self.parent_map[p]:
            p_last = p
            p = self.parent_map[p]
            self.parent_map[p_last] = q
            self.sz_map[p_last] = 2
        return q

    def __repr__(self):
        return str({
            "parent_map": self.parent_map,
            # "sz_map": self.sz_map,
            "count": self._count,
        })

    def is_connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)

    def count(self) -> int:
        return self._count


def test_tiny_quick_union():
    with open("tinyUF.txt") as f:
        array_len = int(next(f))
        uf = QuickUnionDisjointSet(array_len)
        for line in f:
            p, q = [int(x) for x in line.split()]
            if uf.is_connected(p, q):
                continue
            uf.union(p, q)
            print("%s %s" % (p, q))
        print("%s components" % uf.count())
        print(uf)


def test_tiny_weight_quick_union():
    with open("tinyUF.txt") as f:
        array_len = int(next(f))
        uf = WeightQuickUnionDisjointSet(array_len)
        for line in f:
            p, q = [int(x) for x in line.split()]
            if uf.is_connected(p, q):
                continue
            uf.union(p, q)
            print("%s %s" % (p, q))
        # 便利一次执行find，把说有路径都压缩了
        for i in range(array_len):
            uf.find(i)
        print("%s components" % uf.count())
        print(uf)


def test_medium_quick_union():
    with open("mediumUF.txt") as f:
        array_len = int(next(f))
        uf = QuickUnionDisjointSet(array_len)
        for line in f:
            p, q = [int(x) for x in line.split()]
            if uf.is_connected(p, q):
                continue
            uf.union(p, q)
            print("%s %s" % (p, q))
        print("%s components" % uf.count())


def test_test_medium_weight_quick_union():
    with open("mediumUF.txt") as f:
        array_len = int(next(f))
        uf = WeightQuickUnionDisjointSet(array_len)
        for line in f:
            p, q = [int(x) for x in line.split()]
            if uf.is_connected(p, q):
                continue
            uf.union(p, q)
            print("%s %s" % (p, q))
        for i in range(array_len):
            uf.find(i)
        value_map = {}
        for value in uf.parent_map.values():
            value_map[value] = True
        print("%s components" % uf.count())
        print("value_map:%s" % value_map)


if __name__ == '__main__':
    # test_tiny()
    # test_tiny_quick_union()
    # test_tiny_weight_quick_union()
    # test_medium_quick_union()
    test_test_medium_weight_quick_union()
    pass
