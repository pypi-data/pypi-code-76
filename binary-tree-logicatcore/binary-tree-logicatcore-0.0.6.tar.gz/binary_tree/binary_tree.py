from typing import TypeVar, Generic
from binary_tree import heapify
from binary_tree import heap_sort

Node = TypeVar('Node')


class Node(Generic[Node]):

    def __init__(self, v: float, l: Node = None, r: Node = None) -> None:
        """
        Initialises a node with a value and assigns it left and/or right childs

        :param v: Value of the Node in the tree
        :param l: left child node if present
        :param r: right child node if present
        """
        self.value = v
        self.left = l
        self.right = r

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, l):
        if hasattr(l, 'value') or l is None:
            self._left = l
        else:
            raise TypeError('Left child accepts only a "Node" type object')

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, r):
        if hasattr(r, 'value') or r is None:
            self._right = r
        else:
            raise TypeError('Right child accepts only a "Node" type object')

    def __repr__(self):
        """
        Prints the node value and it's childs values in ASCII style

        ##a##    ##a##    ##a##
        #/ \# or #/    or
        b###c    b

        :return: ASCII representation of the node and it's childs
        """
        if self.left and self.right:
            return f'  {self.value}  \n' \
                   f' / \\ \n' \
                   f'{self.left.value}   {self.right.value}'
        elif self.right is None and self.left is not None:
            return f'  {self.value}  \n' \
                   f' /   \n' \
                   f'{self.left.value}    '
        else:
            return f'  {self.value}  '


class BT:

    def __init__(self, norl) -> None:
        """
        The init initialiser accepts either a single root node or a list to create a binary tree from the list
        :param norl: An object of type Node or type python list
        """
        self.root = norl
        self.depth = self.__depth__(self.root)
        self.nodes, self.leafs = self.__countnl__(self.root, self.depth)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, norl):
        if isinstance(norl, Node):
            self._root = norl
            self.elements = self.to_list()
        elif isinstance(norl, list):
            self.elements = norl

            def recur(i):
                if 2 * i + 2 < len(norl):
                    return Node(norl[i], recur(2 * i + 1), recur(2 * i + 2))
                elif 2 * i + 1 < len(norl):
                    return Node(norl[i], recur(2 * i + 1))
                else:
                    return Node(norl[i])

            self._root = recur(0)

    def to_list(self):
        elements = [self.root]
        values = [self.root.value]
        n, l = 0, 0
        while len(elements) > 0:
            tmp = []
            for e in elements:
                if e.left and e.right:
                    tmp += [e.left, e.right]
                elif e.left is None and e.right:
                    tmp += [e.right]
                elif e.right is None and e.left:
                    tmp += [e.left]
            elements = tmp
            values += [x.value for x in elements]
        return values

    @staticmethod
    def __depth__(root):
        """
        Calculates the maximum depth/height of the tree
        :param root: root node of the tree
        :return: maximum depth/height of the tree
        """

        def recur(n):
            if n is None:
                return 1
            return max(1 + recur(n.left), 1 + recur(n.right))

        return max(1 + recur(root.left), 1 + recur(root.right)) - 2

    @staticmethod
    def __countnl__(root, depth):
        """
        Counts the number of nodes and leafs in the tree
        :param root: root node of the tree
        :return: count of nodes and count of leafs
        """
        elements = [root]
        n, l = 0, 0
        while depth > 0:
            for e in elements:
                if e.left or e.right:
                    n += 1
                else:
                    l += 1
            elements = [e.left for e in elements if e.left is not None] + [e.right for e in elements if
                                                                           e.right is not None]
            depth -= 1
        # the elements in last level are indefinitely leafs, so no checking needed
        l += len(elements)
        return n, l

    def graphviz(self):
        try:
            import graphviz as G

            dot = G.Digraph(comment='Binary Tree',
                            graph_attr={'nodesep': '0.04', 'ranksep': '0.05', 'bgcolor': 'white', 'splines': 'line',
                                        'rankdir': 'TB', 'fontname': 'Hilda 10', 'color': 'transparent'},
                            node_attr={'fixedsize': 'true', 'shape': 'circle', 'penwidth': '1', 'width': '0.4',
                                       'height': '0.4', 'fontcolor': 'black'},
                            edge_attr={'color': 'black', 'arrowsize': '.4'})
            mapping = []
            depth = self.depth
            while depth >= 0:
                with dot.subgraph(name='cluster_' + str(depth)) as c:
                    # c.attr(color='transparent', rankdir='LR')
                    if depth == self.depth:
                        c.node(str(depth) + str(0), str(self.root.value))

                        if self.root.left and self.root.right:
                            mapping += [{str(depth) + str(0): [self.root.left, self.root.right]}]
                        elif self.root.right is None:
                            mapping += [{str(depth) + str(0): [self.root.left]}]
                        elif self.root.right is None:
                            mapping += [{str(depth) + str(0): [self.root.right]}]
                    else:
                        tmp = []
                        i = 0
                        # list of dicts
                        for subtree in mapping:
                            # dict with list as value
                            for key, value in subtree.items():
                                # value list contains the childs of a node, here key
                                for e in reversed(value):
                                    c.node(str(depth) + str(i), str(e.value))
                                    dot.edge(key, str(depth) + str(i))

                                    if e.left or e.right:
                                        if e.left and e.right:
                                            tmp += [{str(depth) + str(i): [e.left, e.right]}]
                                        elif e.right is None:
                                            tmp += [{str(depth) + str(i): [e.left]}]
                                        elif e.left is None:
                                            tmp += [{str(depth) + str(i): [e.right]}]
                                    i += 1
                        mapping = tmp
                depth -= 1
            return dot
        except ImportError as e:
            print('ModuleNotFoundError: "graphviz" package not available')

    def max_heapify(self):
        """
        This is wrap to the general max_heapify algorithm
        :return: None
        """
        self.root = heapify.max_heapify(self.elements)

    def min_heapify(self):
        """
        This is wrap to the general min_heapify algorithm
        :return: None
        """
        self.root = heapify.min_heapify(self.elements)

    def ASCII(self):
        """
        This method prints a ASCII representation of the binary tree
        :return: None
        """
        import textwrap

        def split_tree_lr(width):
            if width % 2:
                return "_" * (width // 2) + "|" + "_" * (width // 2) + "\n" + "|" + " " * (width - 2) + "|"
            else:
                return "_" * (width // 2) + "|" + "_" * (width // 2 - 1) + "\n" + "|" + " " * (width - 2) + "|"

        def split_tree_r(width):
            if width % 2:
                return " " * (width // 2) + "|" + "_" * (width // 2) + "\n" + " " * (width - 1) + "|"
            else:
                return " " * (width // 2) + "|" + "_" * (width // 2 - 1) + "\n" + " " * (width - 1) + "|"

        def split_tree_l(width):
            if width % 2:
                return "_" * (width // 2) + "|" + " " * (width // 2) + "\n" + "|" + " " * (width - 1)
            else:
                return "_" * (width // 2) + "|" + " " * (width // 2 - 1) + "\n" + "|" + " " * (width - 1)

        def join_ml(s1, s2):
            """
            Joins a multiline string
            """
            joined = ''
            for l, r in zip(s1.splitlines(), s2.splitlines()):
                joined += l + r + "\n"
            return joined

        WIDTH = 7
        MARGIN = 4

        elements = [[self.root]]
        depth = self.depth
        # Nested list of elements level wise
        while depth > 0:
            tmp = []
            for e in elements[-1]:
                if e is None:
                    tmp += [None, None]
                else:
                    tmp += [e.left, e.right]
            elements.append(tmp)
            depth -= 1

        output = ''
        inbtw_len = 0  # not used for root level
        for i, level_elements in enumerate(elements):
            prefix_suffix_len = max(int(2 ** (self.depth - i - 1)) * WIDTH, MARGIN)

            # string with elements values are prepared
            tmp = ' ' * prefix_suffix_len
            for j, e in enumerate(level_elements):
                if j == 0:
                    tmp += str(e.value) if e is not None else " "
                else:
                    if e is not None:
                        tmp += " " * (inbtw_len - len(str(e.value))) + str(e.value)
                    else:
                        tmp += " " * (inbtw_len)

            tmp += ' ' * prefix_suffix_len + '\n'
            output += tmp

            inbtw_len = prefix_suffix_len
            if i != self.depth:  # skip trees for the last level which are all leaves
                # 3 line string the tree's
                for k, e in enumerate(level_elements):
                    if k == 0:
                        if e is not None:
                            if e.left and e.right:
                                tmp = textwrap.indent(split_tree_lr(inbtw_len),
                                                      " " * (prefix_suffix_len - inbtw_len // 2))
                            elif e.left and e.right is None:
                                tmp = textwrap.indent(split_tree_l(inbtw_len),
                                                      " " * (prefix_suffix_len - inbtw_len // 2))
                            elif e.left is None and e.right:
                                tmp = textwrap.indent(split_tree_r(inbtw_len),
                                                      " " * (prefix_suffix_len - inbtw_len // 2))
                        else:
                            tmp = " " * (inbtw_len // 2 + prefix_suffix_len) + "\n" + " " * (
                                        inbtw_len // 2 + prefix_suffix_len) \
                                  + "\n" + " " * (inbtw_len // 2 + prefix_suffix_len) + "\n"
                    else:
                        if e is not None:
                            if e.left and e.right:
                                tmp = join_ml(tmp, textwrap.indent(split_tree_lr(inbtw_len), " " * inbtw_len))
                            elif e.left and e.right is None:
                                tmp = join_ml(tmp, textwrap.indent(split_tree_l(inbtw_len), " " * inbtw_len))
                            elif e.left is None and e.right:
                                tmp = join_ml(tmp, textwrap.indent(split_tree_r(inbtw_len), " " * inbtw_len))
                            else:
                                tmp = join_ml(tmp,
                                              " " * 2 * inbtw_len + "\n" + " " * 2 * inbtw_len + "\n" + " " * 2 * inbtw_len + "\n")
                        else:
                            tmp = join_ml(tmp,
                                          " " * 2 * inbtw_len + "\n" + " " * 2 * inbtw_len + "\n" + " " * 2 * inbtw_len + "\n")
                tmp = join_ml(tmp,
                              " " * prefix_suffix_len + "\n" + " " * prefix_suffix_len + "\n" + " " * prefix_suffix_len + "\n")
                output += tmp
        print(output)

    def heap_sort(self, order='ascending'):
        """
        Performs a heapfort on the elements of the binary tree in either ascending or descending order
        :param order: decides the sorting order, acceptable values are 'ascending' or 'descending'
        :return Sorted list of tree elements
        """
        if order == 'ascending':
            sorted = heap_sort.heap_sort_asc(self.elements)
        elif order == 'descending':
            sorted = heap_sort.heap_sort_desc(self.elements)
        return sorted

    def properties(self):
        """
        Prints a summary of the tree properties and an ASCII representation of the tree
        :return: None
        """
        print(f"Total number of elements in the tree are: {self.nodes + self.leafs}")
        print(f"Total number of nodes are: {self.nodes}")
        print(f"Total number of leafs are: {self.leafs}")
        print(f"The depth of the tree is: {self.depth}")

        sorted = heap_sort.heap_sort_asc(self.elements)
        print(f"The maximum value in the tree is: {sorted[-1]}")
        print(f"The minimum value in the tree is: {sorted[0]}")

        print("")
        self.ASCII()
