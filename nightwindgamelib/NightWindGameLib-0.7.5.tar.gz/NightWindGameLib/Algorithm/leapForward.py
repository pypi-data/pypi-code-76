from NightWindGameLib.Algorithm.search import (
    Problem, TreeSearch
)


class LeapForward(Problem):
    def __init__(self, road=(), allowed_steps=()):
        self.road = road
        self.allowed_steps = allowed_steps
        super().__init__(initial=1, goal=len(self.road))

    def actions(self, state):
        if self.road[state - 1] == 0:
            return []
        return [s for s in self.allowed_steps if state + s <= self.goal]

    def transition(self, state, action):
        return state + action


def leapForward():
    import random
    allowed_steps = (2, 3, 4)
    road = [1]
    for _ in range(11):
        road.append(random.randint(0, 1))
    road.append(1)

    display_road = ["_" if s == 1 else "^" for s in road]
    print(" ".join(display_road))
    print("\n")

    leap_forward = LeapForward(road, allowed_steps)
    result = TreeSearch(leap_forward)
    if result:
        # print([node.action for node in result.path() if node.action])
        for node in result.path():
            copy = display_road.copy()
            copy[node.state - 1] = "@"
            print(" ".join(copy))
            print("\n")
    else:
        print("未找到有效路径")


if __name__ == "__main__":
    leapForward()
