import pygame, sys, os
from pygame.locals import *
from collections import deque
import heapq
import time
import numpy as np


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = state.g
        self.f = self.g + state.h

    def __lt__(self, other):
        return self.f < other.f

    def getSolution(self):
        node = self
        solution = []
        while node:
            solution.append(node.action)
            node = node.parent
        return solution[::-1]
