from functools import lru_cache
BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0]
LIST_OF_POSITION = list(range(0, 9))


class TieTacToe:
    def __init__(self) -> None:
        self.board = [x for x in BOARD]
        self.state = {
            "gameWonBy": 0,
            "movePlayedCount": 0,
            "currentPlayer": 1
        }

    def change_player(self):
        self.state["currentPlayer"] = 1 if self.state["currentPlayer"] == -1 else -1

    def increment_played_count(self):
        self.state["movePlayedCount"] += 1

    def is_game_over(self):
        return True if (self.state["gameWonBy"] != 0 or self.state["movePlayedCount"] >= 9) else False

    def get_current_player(self):
        return self.state["currentPlayer"]

    def check_game_win(self, current_player, game):
        if (game[0] == current_player and game[4] == current_player and game[8] == current_player):
            return True
        if (game[2] == current_player and game[4] == current_player and game[6] == current_player):
            return True
        list_of_rows = [[game[0], game[1], game[2]],
                        [game[3], game[4], game[5]],
                        [game[6], game[7], game[8]]
                        ]
        list_of_columns = [[game[0], game[3], game[6]],
                           [game[1], game[4], game[7]],
                           [game[2], game[5], game[8]]
                           ]
        for item in list_of_rows:
            result = all(current_player == x for x in item)
            if result:
                return True
        for item in list_of_columns:
            result = all(current_player == x for x in item)
            if result:
                return True
        return False

    def isAllPlacesPlayed(self, game):
        for item in game:
            if item == 0:
                return False
        return True

    def print_state(self):
        if self.state["gameWonBy"] != 0:
            print(
                f'game is won by {"X" if self.state["gameWonBy"] == 1 else "O"}')
        elif self.state["movePlayedCount"] >= 9:
            print('The game was a draw')

        counter = 0
        for index in range(len(self.board)):
            if counter == 2:
                counter = 0
                print(self.board[index])
            else:
                counter += 1
                print(self.board[index], end=" ")

    def score(self, game, depth, current_player):
        if self.check_game_win(current_player, game):
            return 10 - depth
        elif self.check_game_win(self.get_current_opposite(current_player), game):
            return depth - 10
        else:
            return 0

    def get_current_opposite(self, current_player):
        return 1 if current_player == -1 else -1

    @lru_cache(maxsize=4000)
    def alpha_beta_pruning(self, game, depth, current_player, alpha, beta):
        game = list(game)
        if self.check_game_win(current_player, game) or self.check_game_win(self.get_current_opposite(current_player), game) or self.isAllPlacesPlayed(game):
            return self.score(game, depth, self.get_current_player())
        local_depth = depth + 1
        if current_player == self.get_current_player():
            # alpha
            value = -float('inf')
            _ans = -float('inf')
            _ans_index = 0
            for index in range(len(game)):
                if game[index] == 0:
                    game[index] = current_player
                    value = self.alpha_beta_pruning(tuple(game), local_depth,
                                                    self.get_current_opposite(current_player), alpha, beta)
                    game[index] = 0
                    if value > _ans:
                        _ans = value
                        _ans_index = index
                    if value >= beta:
                        break
                    alpha = max(alpha, value)
            if depth == 0:
                return _ans_index
            return _ans
        else:
            # beta
            value = float('inf')
            _ans = float('inf')
            _ans_index = 0
            for index in range(len(game)):
                if game[index] == 0:
                    game[index] = current_player
                    value = self.alpha_beta_pruning(tuple(game), local_depth,
                                                    self.get_current_opposite(current_player), alpha, beta)
                    game[index] = 0
                    if value < _ans:
                        _ans = value
                    if value <= alpha:
                        break
                    beta = min(beta, value)
            return _ans

    def bot_play(self):
        if self.is_game_over() == True:
            self.print_state()
            return
        best_pick = self.alpha_beta_pruning(tuple(self.board), 0,
                                            self.get_current_player(), -float('inf'), float('inf'))
        self.play(best_pick)

    def play(self, board_position):
        if board_position not in LIST_OF_POSITION:
            print('wrong position choose between 0-8')
            return
        if self.is_game_over() == True:
            self.print_state()
            return
        current_player = self.get_current_player()
        self.board[board_position] = current_player
        is_gameOver = self.check_game_win(current_player, self.board)
        if is_gameOver:
            self.state["gameWonBy"] = current_player
        self.increment_played_count()
        self.change_player()
        self.print_state()


if __name__ == "__main__":
    pass
