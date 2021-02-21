import random
import sys
from PySide2.QtWidgets import *
# 导入界面
from NightWindGameLib.Chess.ui_isolation import Ui_Isolation

# 导入基类和基础方法
from NightWindGameLib.Chess.chess import (
    Game, GameState, Board,
    strategic_player, random_player
)

# 修复Qt
from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class Isolation(Game):
    def __init__(self, width=8, height=8, players=('X', 'O'), to_move='X'):
        self.players = players
        player_squares = {players[0]: (0, 0),
                          players[1]: (width - 1, height - 1)}
        board = IsolationBoard(width, height)
        for player, square in player_squares.items():
            board[square] = player
        self.initial = IsolationState(board=board,
                                      player_squares=player_squares,
                                      to_move=to_move)
        super().__init__(initial=self.initial, players=self.players)

    def moves(self, state):
        return state.open_moves(state.to_move)

    def transition(self, state, move):
        if move not in self.moves(state):
            return state

        player = state.to_move
        board = state.board.new()
        board.update({move: player, state.player_squares[player]: '*'})
        player_squares = state.player_squares.copy()
        player_squares.update({player: move})
        to_move = self.opponent(player)
        return IsolationState(board=board,
                              player_squares=player_squares,
                              to_move=to_move)

    def utility(self, state, player):
        if player == state.to_move:
            return -1
        else:
            return 1


class IsolationState(GameState):
    def __init__(self, board, player_squares, to_move):
        self.board = board
        self.player_squares = player_squares
        self.to_move = to_move
        super().__init__(board=self.board, to_move=self.to_move)

    def open_moves(self, player):
        return self.board.open_squares(self.player_squares[player])


class IsolationBoard(Board):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = {(x, y) for x in range(width)
                        for y in range(height)}
        self.rows = []
        super().__init__(width=self.width, height=self.height)

    def open_squares(self, square):
        open_squares = []
        for delta in ((0, 1), (1, 0), (1, 1), (1, -1)):
            (delta_x, delta_y) = delta
            x, y = square
            x, y = x + delta_x, y + delta_y
            if self.in_board((x, y)) and not self.get((x, y)):
                open_squares.append((x, y))

            x, y = square
            x, y = x - delta_x, y - delta_y
            if self.in_board((x, y)) and not self.get((x, y)):
                open_squares.append((x, y))

        return open_squares

    def in_board(self, square):
        x, y = square
        return 1 <= x <= self.width and 1 <= y <= self.height

    def __repr__(self):
        for x in range(self.height):
            row = []
            for y in range(self.width):
                row.append(self.get((x, y), "·"))
            self.rows.append(row)
        return self.rows


def center_evaluation(game, state, player):
    # 占中策略，尽可能往棋盘中间走
    square = state.player_squares[player]
    board = state.board
    center_x, center_y = (board.width + 1) / 2, (board.height + 1) / 2
    return 2 - abs(square[0] - center_x) - abs(square[1] - center_y)


def open_evaluation(game, state, player):
    # 开放策略，往自己周围空格子更多的地方走
    own_moves = len(state.open_moves(player))
    opp_moves = len(state.open_moves(game.opponent(player)))
    return own_moves - opp_moves


def mixed_evaluation(game, state, player):
    # 综合策略，前期使用占中策略，后期使用开放策略
    if len(state.board.blank_squares()) / len(state.board.squares) >= 0.6:
        return center_evaluation(game, state, player)
    else:
        return open_evaluation(game, state, player)


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


class Main(QMainWindow, Ui_Isolation, Isolation):
    def __init__(self, width=8, height=8, players=('X', 'O'), to_move='X'):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pbtn_start.clicked.connect(self.Start)
        self.pbtn_rule.clicked.connect(self.get_rule)
        self.info = "游戏规则\n双方位于棋盘对角，由X玩家先手下棋，双方可以移动到" \
                    "和自己当前格子有公共边或公共点的格子中，某一方走过的地方双方都不允许再次被踏足，" \
                    "直到有一方所处格子有公共边或有公共点的格子全部被某一方踏足过，无法移动，游戏结束"

        self.players = players
        player_squares = {players[0]: (0, 0),
                          players[1]: (width - 1, height - 1)}
        board = IsolationBoard(width, height)
        for player, square in player_squares.items():
            board[square] = player
        self.initial = IsolationState(board=board,
                                      player_squares=player_squares,
                                      to_move=to_move)

        pbtn = [j for i in self.pbtn_list for j in i]
        row = [j for i in board.rows for j in i]
        self.board = dict(zip(row, pbtn))
        self.center_player = strategic_player(minimax_search,
                                              depth_limit=4,
                                              eval_fn=center_evaluation)
        self.open_player = strategic_player(minimax_search,
                                            depth_limit=4,
                                            eval_fn=open_evaluation)
        self.mixed_player = strategic_player(minimax_search,
                                             depth_limit=4,
                                             eval_fn=mixed_evaluation)

    def get_rule(self):
        QMessageBox.about(self, "游戏规则", self.info)

    def play_game(self, strategies: dict, verbose=False):
        QApplication.processEvents()
        state = self.initial
        if verbose:
            self.label_moves.setText("初始状态:")

        while not self.terminal_test(state):
            player = state.to_move
            move = strategies[player](self, state)
            state = self.transition(state, move)
            if verbose:
                self.label_moves.setText(f"玩家{player}\n行动:{move}")
                for i, j in self.board.items():
                    i.setText(j)
        return state

    def human_player(self, game, state: IsolationState):
        QApplication.processEvents()
        open_squares = state.open_moves(state.to_move)
        for i in range(8):
            for j in range(8):
                if (j, i) not in open_squares:
                    self.pbtn_list[i][j].setEnabled(True)
                else:
                    self.pbtn_list[i][j].setCheckable(True)

    def Start(self):
        level = self.cb_level.currentText()
        first = self.cb_first.currentText()

        if first == "先手":
            self.label_status.setText("你是X玩家")
            if level == "简单":
                end = self.play_game(
                    dict(X=self.human_player, O=random_player), verbose=True)
            elif level == "中等":
                end = self.play_game(
                    dict(X=self.human_player,
                         O=random.choice([self.open_player, self.center_player])),
                    verbose=True)
            else:
                end = self.play_game(
                    dict(X=self.human_player, O=self.mixed_player), verbose=True)

            result = self.utility(state=end, player='X')
            if result == 1:
                self.label_status.setText("你赢了！")
            elif result == 0:
                self.label_status.setText("平局！")
            elif result == -1:
                self.label_status.setText("你输了！")

        else:
            self.label_status.setText("你是O玩家")
            if level == "简单":
                end = self.play_game(
                    dict(X=self.center_player, O=self.human_player), verbose=True)
            elif level == "中等":
                end = self.play_game(
                    dict(X=self.open_player, O=self.human_player), verbose=True)
            else:
                end = self.play_game(
                    dict(X=self.mixed_player, O=self.human_player), verbose=True)

            result = self.utility(state=end, player='O')
            if result == 1:
                self.label_status.setText("你赢了！")
            elif result == 0:
                self.label_status.setText("平局！")
            elif result == -1:
                self.label_status.setText("你输了！")


def main():
    app = QApplication(sys.argv)
    game = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
