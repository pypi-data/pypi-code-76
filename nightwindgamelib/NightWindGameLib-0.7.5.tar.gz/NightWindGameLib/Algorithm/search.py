class Problem:
    def __init__(self, initial, goal=None):
        # 指定搜索问题的初始状态和目标状态
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        # 返回在给定状态下可以采取的动作
        raise NotImplementedError

    def transition(self, state, action):
        # 执行给定动作后达到的状态
        raise NotImplementedError

    def goal_test(self, state):
        # 给定状态是目标状态则返回True
        return state == self.goal


class Node:
    def __init__(self, state, parent=None, action=None):
        # 构造节点，记录当前状态、父节点和采取的动作
        self.state = state
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def expand(self, problem: Problem):
        # 展开当前问题可以到达的所有子节点
        child = []
        for action in problem.actions(self.state):
            next_state = problem.transition(self.state, action)
            child.append(Node(next_state, self, action))
        return child

    def path(self):
        # 返回从根节点到该节点的路径
        if self.parent is None:
            return [self]
        return self.parent.path() + [self]


def TreeSearch(problem: Problem):
    # 实现树搜索算法
    frontier = [Node(problem.initial)]
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(n for n in node.expand(problem) if n.state not in explored)
    return None
