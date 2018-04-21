#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from maze_algo.kruskal_gen import KruskalMaze as Maze


class MazePair(object):
    def __init__(self, width: int, height: int):
        self.left_maze = Maze(width, height)
        self.right_maze = Maze(width, height)
        self.width = width
        self.height = height

    def can_solve(self) -> bool:
        if isinstance(self.left_maze, Maze):
            return True
        return False

    def print(self):
        for i

