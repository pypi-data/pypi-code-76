from NightWindGameLib.Algorithm.search import (
    Problem, TreeSearch
)


class JumpingFrogs(Problem):
    def __init__(self, n=3):
        self.initial = n*'L' + '.' + n*'R'
        self.goal = self.initial[::-1]
        super().__init__(initial=self.initial, goal=self.goal)

    def actions(self, state):
        ids = range(len(state))
        return ({(i, i + 1) for i in ids if state[i: i + 2] == "L."}
                | {(i, i + 2) for i in ids if state[i: i + 3] == "LR."}
                | {(i + 1, i) for i in ids if state[i: i + 2] == ".R"}
                | {(i + 2, i) for i in ids if state[i: i + 3] == ".LR"})

    def transition(self, state, action):
        i, j = action
        result = list(state)
        result[i], result[j] = state[j], state[i]
        return "".join(result)


def jumpingFrogs():
    jumping_frogs = JumpingFrogs()
    result = TreeSearch(jumping_frogs)
    if result:
        for node in result.path():
            print(node.state)
    else:
        print("未找到有效路径")


if __name__ == "__main__":
    jumpingFrogs()
