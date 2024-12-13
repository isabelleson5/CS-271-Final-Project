import numpy as np
import matplotlib.pyplot as plt

class TreeNode(object):
    def __init__(self, start, end, label="", value=0, is_selected=False, branch=False):
        """
        Initialize tree node

        Parameters
        ----------
        start: int
            starting index of node
        end: int
            ending index of node
        value: int
            given value, default is 0
        label: string
            if leaf node then given label, default is None
        is_selected: boolean
            For demonstrative purposes, will bold text if True
        branch: boolean
            For demonstrative purposes, will bold line connecting node
        """
        self.start = start
        self.end = end
        self.label = label
        self.value = value
        self.is_selected = is_selected
        self.branch = branch
        self.left = None
        self.right = None

    def update(self, idx, value):
        if self.start == self.end:
            self.value = value
        else:
            mid = (self.start + self.end) // 2
            if idx <= mid:
                self.left.update(idx, value)
            else:
                self.right.update(idx, value)

            if self.left.value > self.right.value:
                self.value = self.left.value
                # self.label = "<-"
            else:
                self.value = self.right.value
                # self.label = "->"

    def query(self, start, end):
        ret = None
        if self.start == start and self.end == end:
            ret = self.value
        else:
            mid = (self.start + self.end) // 2
            if end <= mid:
                ret = self.left.query(start, end)
            elif start > mid:
                ret = self.right.query(start, end)
            else:
                left_max = self.left.query(start, mid)
                right_max = self.right.query(mid + 1, end)
                ret = max(left_max, right_max)
        return ret
    
    def inorder(self, num, key_list):
        """
        Parameters
        ----------
        num: list
            List of a single element which keeps 
            track of the number I'm at
        """
        # taken from AVL lab
        if self.left:
            self.left.inorder(num, key_list)
        self.inorder_pos = num[0]
        key_list.append(self.label)
        num[0] += 1
        if self.right:
            self.right.inorder(num, key_list)

    def draw(self, y):
        # taken from AVL lab, modified to support highlighting of nodes and their branches
        x = self.inorder_pos
        plt.scatter([x], [y], 50, 'k')
        # line that applies label and value to node
        s = "(" + (str)(self.value) + ") " + self.label + " [" + (str)(self.start) + ":" + (str)(self.end) + "]"
        if self.is_selected:
            plt.text(x+0.1, y, "{}".format(s),fontsize='x-small',weight='bold',backgroundcolor="#f7ff00")
        else:
            plt.text(x+0.1, y, "{}".format(s),fontsize='x-small')
        y_next = y-1
        if self.left:
            x_next = self.left.inorder_pos
            line_width = 1.5
            if self.left.branch:
                line_width = 4
            plt.plot([x, x_next], [y, y_next], lw=line_width)
            self.left.draw(y_next)
        if self.right:
            x_next = self.right.inorder_pos
            line_width = 1.5
            if self.right.branch:
                line_width = 4
            plt.plot([x, x_next], [y, y_next], lw=line_width)
            self.right.draw(y_next)

class SegmentTree:
    def __init__(self, values, labels, selected_idx=-1, branch_idx=-1):
        """
        Initialize tree

        Parameters
        ----------
        values: list
            values to be set as leaf nodes
        labels: list
            parallel list to values, labels for the leaf nodes
        selected_idx: int
            For demonstrative purposes, will bold text of a node at index
        branch_idx: int
            For demonstrative purposes, will make the branch of a node at index thicker
        """
        self.values = values
        self.labels = labels
        self.selected_idx = selected_idx
        self.branch_idx = branch_idx
        self.root = self.build_tree(0, len(values) - 1)

    def build_tree(self, start, end):
        """
        Builds the tree recursively

        Parameters
        ----------
        start: int
            starting index
        end: int
            ending index
        """
        ret = None
        if start == end:
            label = self.labels[start]
            selected_var = False
            branch_var = False
            if self.selected_idx == start:
                selected_var = True
            if self.branch_idx == start:
                branch_var = True
            ret = TreeNode(start, end, label, self.values[start], selected_var, branch_var)
        else:
            mid = (start + end) // 2
            root = TreeNode(start, end)
            root.left = self.build_tree(start, mid)
            root.right = self.build_tree(mid + 1, end)
            if root.left.value > root.right.value:
                root.value = root.left.value
                # root.label = "<-"
            else:
                root.value = root.right.value
                # root.label = "->"
            root.branch = root.right.branch or root.left.branch
            ret = root
        return ret
    
    def update(self, idx, value):
        """
        Updates the tree at a given index recursively starting from the root
        Entry point into TreeNode class's method of the same name

        Parameters
        ----------
        idx: int
            index of value that will be updated
        value: int
            new value to be put at idx
        """
        self.root.update(idx, value)

    def query(self, start, end):
        """
        Queries the maximum of a range, returns the maximum
        Entry point into TreeNode class's method of the same name

        Parameters
        ----------
        start: int
            starting index of the range
        end: int
            ending index of the range (inclusive)
        """
        return self.root.query(start, end)
    
    def inorder(self):
        # taken from AVL lab
        key_list = []
        if self.root:
            self.root.inorder([0], key_list)
        return key_list
    
    def draw(self):
        # taken from AVL lab
        self.inorder()
        if self.root:
            self.root.draw(0)

if __name__ == "__main__":
    np.random.seed(0)

    # 1 darkest, 100 brightest
    # random multiples of 10, 1 to 100
    light_levels = np.random.randint(1, 11, 10)
    light_levels *= 10
    print(light_levels)

    city_names = ["Intejersey","Binopolis","Pennsylstringia","Florida","North Charolina","Arrayzona","South Charolina","Dataware","North Dacode-a","Alascii"]

    # generate tree
    # tree = SegmentTree(light_levels, city_names, 5, 5)
    tree = SegmentTree(light_levels, city_names)

    # tree once built
    plt.figure(figsize=(20, 20))
    tree.draw()
    plt.show()

    # # update tree at index 5, replace value with 10
    # tree.update(5,10)
    # plt.figure(figsize=(20, 20))
    # tree.draw()
    # plt.show()

    # query tree to find max value from 0 to 5 inclusive
    print(tree.query(0,5))
