from NightWindGameLib.Chess.chess import (
    Game, GameState,
    Board, human_player,
    strategic_player,
)


def minimax_search(game: Game, state: GameState):
    player = state.to_move

    def max_value(state):
        # 计算子状态中的最大效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        v = -float('inf')
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m)))
        return v

    def min_value(state):
        # 计算子状态中的最小效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        v = float('inf')
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m)))
        return v

    return max(game.moves(state),
               key=lambda m: min_value(game.transition(state, m)))


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


def ticTacToe():
    minimax_player = strategic_player(minimax_search)
    tic_tac_toe = TicTacToe(players=('X', 'O'), to_move='X')
    first = input("你想先手还是后手？")
    if first == "先手":
        end = tic_tac_toe.play_game(dict(X=human_player, O=minimax_player),
                                    verbose=True)
        result = tic_tac_toe.utility(end, 'X')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")
    else:
        end = tic_tac_toe.play_game(dict(X=minimax_player, O=human_player),
                                    verbose=True)
        result = tic_tac_toe.utility(end, 'O')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")


if __name__ == "__main__":
    ticTacToe()
