from NightWindGameLib.Algorithm.search import (
    Problem, TreeSearch
)


class RiverCrossing(Problem):
    def __init__(self, forbidden_states=None):
        super().__init__(initial=(1, 1, 1, 1), goal=(-1, -1, -1, -1))
        if forbidden_states is None:
            forbidden_states = set()
        self.forbidden_states = set(forbidden_states)

    def actions(self, state):
        if state in self.forbidden_states:
            return []
        allowed_actions = [(-1, 1, 1, 1)]
        for n in range(1, len(state)):
            if state[n] == state[0]:
                action = tuple([-1 if i in [0, n] else 1 for i in range(4)])
                allowed_actions.append(action)

        return allowed_actions

    def transition(self, state, action):
        return tuple(s * a for s, a in zip(state, action))


def riverCrossing():
    forbidden_states = {
        (1, 1, -1, -1),
        (1, -1, -1, 1),
        (1, -1, -1, -1),
        (-1, -1, 1, 1),
        (-1, 1, 1, -1),
        (-1, 1, 1, 1)
    }
    river_crossing = RiverCrossing(forbidden_states=forbidden_states)
    result = TreeSearch(river_crossing)
    if result:
        for node in result.path():
            print("".join(["N" if s == 1 else "F" for s in node.state]))
    else:
        print("未找到可行路径")


if __name__ == "__main__":
    riverCrossing()
