#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy
from numpy import random
from maze_algo.cell_dset import MazeCellDSet

"""
C for cell,0
S for space(remove from the init_walls),0
W for walls(not remove form the init_walls),1
w for walls(has no effect to the path of maze,can randomly change to space.),1 or 0
A 5X5 maze look like this:
CSCWC
WwSwS
CWCSC
SwSwW
CSCSC

The maze above is equivalent as 3X3 maze in some other docs which their wall's width/height is 0.
The w(little W) is only a dot in such 3X3 maze.
"""


class KruskalMaze(object):
    def __init__(self, width: int, height: int, ):
        """
        Init a maze.

        :param width: the width of the maze
        :param height: the height of the maze
        """
        if height % 2 == 0 or height < 3:
            raise Exception("illegal height because each wall's height is one.")
        if width % 2 == 0 or width < 3:
            raise Exception("illegal width because each wall's width is one.")
        self.height = height
        self.width = width
        count = self.height * self.width
        self.index_ls = list(range(1, count))
        self.grid = numpy.ones((width, height))
        cell_ls = [(x, y) for x in range(0, width, 2) for y in range(0, height, 2)]
        not_care_ls = [(x, y) for x in range(1, width, 2) for y in range(1, height, 2)]
        wall_ls = [(x, y) for x in range(1, width, 2) for y in range(0, height, 2)] + [
            (x, y) for x in range(0, width, 2) for y in range(1, height, 2)
        ]
        for x, y in cell_ls:
            self.grid[x][y] = 0
        cell_dset = MazeCellDSet(cell_ls, width, height)
        random.shuffle(wall_ls)
        for x, y in wall_ls:
            if cell_dset.count() == 1:
                break
            if x % 2 == 1:
                x1 = x - 1
                x2 = x + 1
                if not cell_dset.is_connected(x1, y, x2, y):
                    cell_dset.union(x1, y, x2, y)
                    self.grid[x][y] = 0
            else:
                y1 = y - 1
                y2 = y + 1
                if not cell_dset.is_connected(x, y1, x, y2):
                    self.grid[x][y] = 0
                    cell_dset.union(x, y1, x, y2)
        additional_wall = random.randint(0, len(not_care_ls))
        for i in random.choice(len(not_care_ls), additional_wall, False):
            x, y = not_care_ls[i]
            self.grid[x][y] = 0

    def __str__(self):
        return str(self.grid)


def main():
    maze = KruskalMaze(9, 7)
    print(maze)


if __name__ == '__main__':
    main()
