from typing import List, Tuple
from maze_algo.disjoint_set import WeightQuickUnionDisjointSet as DSet


class MazeCellDSet(object):
    def __init__(self, point_ls: List[Tuple[int, int]], width: int, height: int):
        self.width = width
        self.height = height
        self.index_map = {}
        self.dset = DSet(len(point_ls))
        for i, (x, y) in enumerate(point_ls):
            index = x + y * self.width
            self.index_map[index] = i

    def _find(self, x, y):
        index = x + y * self.width
        # !! if self.index_map[index] is not int, you finding the illegal point
        return self.dset.find(self.index_map[index])

    def is_connected(self, x1, y1, x2, y2):
        return self._find(x1, y1) == self._find(x2, y2)

    def union(self, x1, y1, x2, y2):
        index1 = x1 + y1 * self.width
        index2 = x2 + y2 * self.width
        # print(f"union ({x1},{y1}) ({x2},{y2}) index1:{index1} index2:{index2}")
        self.dset.union(self.index_map[index1], self.index_map[index2])

    def count(self):
        return self.dset.count()
