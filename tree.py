from typing import Tuple
import numpy as np

class Tree:
    def __init__(self, string: str, left=None, right=None) -> None:
        self.string: str = string
        self.left: Tree = left
        self.right: Tree = right
    
    def is_leaf(self) -> bool:
        return self.left == None and self.right == None
    
    def get_leaves(self, path: list = []) -> list:
        if self.is_leaf():
            return [(path, self)]

        # is this necessary bc of structure?
        # if self.left == None:
        #     return self.right.get_leaves(1)
        # if self.right == None:
        #     return self.left.get_leaves(0)

        return self.left.get_leaves(path + [0]) + self.right.get_leaves(path + [1])

    def find_leaf(self, s: str) -> list:
        for path, leaf in self.get_leaves():
            if leaf.string == s:
                return path
        return []

    
    # finds the least common ancestor of two leaf nodes in the tree
    def closest_ancestor(self, s1: str, s2: str, path: list = []) -> Tuple[str, list]:
        if self.is_leaf():
            # if leaf is s1: set left bit, if s2: set right bit
            if self.string == s1:
                return '', 2  # 10 = 2
            
            if self.string == s2:
                return '', 1  # 01 = 1

            # otherwise if leaf is neither, return 0 for both bitss
            return '', 0      # 00 = 0


        left, l = self.left.closest_ancestor(s1, s2, path + [0])
        if l == 3: # 11
            return left, l # if left is closest ancestor 

        right, r = self.right.closest_ancestor(s1, s2, path + [1])
        if r == 3: # 11
            return right, r # if right is closest ancestor

        # if this case is optimal (for example: left was 10 and right was 01)
        # return their sum, and note that this differentiating string

        # if this is not optimal, (l+r != 11) but l+r is the best we have seen in this branch
        return self.string, l + r # if self is closest ancestor
