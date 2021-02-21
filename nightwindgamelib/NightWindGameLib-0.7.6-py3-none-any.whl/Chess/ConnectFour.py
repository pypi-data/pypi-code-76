from NightWindGameLib.Chess.chess import (
    Game, GameState,
    Board, human_player,
    strategic_player,
)


def minimax_search(game: Game, state: GameState, depth_limit, eval_fn):
    player = state.to_move

    def max_value(state, depth):
        # 计算子状态中的最大效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        if depth > depth_limit:
            return eval_fn(game, state, player)

        v = -float('inf')
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m), depth + 1))
        return v

    def min_value(state, depth):
        # 计算子状态中的最小效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        if depth > depth_limit:
            return eval_fn(game, state, player)

        v = float('inf')
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m), depth + 1))
        return v

    return max(game.moves(state),
               key=lambda m: min_value(game.transition(state, m), 1))


class TicTacToe(Game):
    def __init__(self, width=3, height=3, k=3,
                 players=('X', 'O'), to_move='X'):
        self.k = k
        self.players = players
        self.initial = GameState(board=Board(width, height),
                                 to_move=to_move, score=0)
        super().__init__(initial=self.initial, players=self.players)

    def moves(self, state):
        return state.board.blank_squares()

    def transition(self, state, move):
        if move not in self.moves(state):
            return state

        player = state.to_move
        board = state.board.new()
        board[move] = player
        to_move = self.opponent(player)
        score = 0
        if board.k_in_line(self.k, player=player, move=move):
            score = 1 if player == self.initial.to_move else -1

        return GameState(board=board, to_move=to_move, score=score)

    def terminal_test(self, state):
        return not self.moves(state) or state.score != 0

    def utility(self, state, player):
        if player == self.initial.to_move:
            return state.score
        else:
            return -state.score


def novice_evaluation(game, state, player):
    import random
    return random.choice([float('inf'), -float('inf')])


def improved_evaluation(game, state: GameState, player):
    value = 0
    board = state.board
    center_x, center_y = (board.width + 1) / 2, (board.height + 1) / 2
    for s, p in board.items():
        distance = abs(s[0] - center_x) + abs(s[1] - center_y)
        if p == player:
            value -= distance
        else:
            value += distance

    return value


class ConnectFour(TicTacToe):
    def __init__(self, width=7, height=6, k=4,
                 players=('X', 'O'), to_move='X'):
        super().__init__(width=width, height=height, k=k,
                         players=players, to_move=to_move)

    def moves(self, state):
        return [(x, y) for (x, y) in state.board.blank_squares()
                if y == state.board.height or (x, y + 1) in state.board]


def connectFour():
    level = input("请选择难度：简单或较难")
    while level != "简单" and level != "较难":
        print("难度输入有误，请重新选择！")
        level = input("请选择难度：简单或较难")

    first = input("你想先手还是后手？")
    while first != "先手" and first != "后手":
        print("先后手输入有误，请重新选择！")
        first = input("你想先手还是后手？")

    novice_player = strategic_player(minimax_search,
                                     depth_limit=4,
                                     eval_fn=novice_evaluation)
    improved_player = strategic_player(minimax_search,
                                       depth_limit=4,
                                       eval_fn=improved_evaluation)

    if first == "先手":
        if level == "简单":
            connect_four = ConnectFour(players=('X', 'O'), to_move='X')
            end = connect_four.play_game(
                dict(X=human_player, O=novice_player), verbose=True)
        else:
            connect_four = ConnectFour(players=('X', 'O'), to_move='X')
            end = connect_four.play_game(
                dict(X=human_player, O=improved_player), verbose=True)

        result = connect_four.utility(end, 'X')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")

    else:
        if level == "简单":
            connect_four = ConnectFour(players=('X', 'O'), to_move='X')
            end = connect_four.play_game(
                dict(X=novice_player, O=human_player), verbose=True)
        else:
            connect_four = ConnectFour(players=('X', 'O'), to_move='X')
            end = connect_four.play_game(
                dict(X=improved_player, O=human_player), verbose=True)

        result = connect_four.utility(end, 'O')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")


if __name__ == "__main__":
    connectFour()
