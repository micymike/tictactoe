import random

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_winner = None

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, row, col, level):
        if self.board[row][col] == '':
            self.board[row][col] = 'X'  # Human move
            if self.check_winner('X'):
                return {'status': 'win', 'board': self.board}
            if self.is_board_full():
                return {'status': 'tie', 'board': self.board}
            
            self.ai_move(level)
            if self.check_winner('O'):
                return {'status': 'lose', 'board': self.board}
            if self.is_board_full():
                return {'status': 'tie', 'board': self.board}
            
            return {'status': 'continue', 'board': self.board}
        return {'status': 'invalid', 'board': self.board}

    def ai_move(self, level):
        if level == 'easy':
            self.random_move()
        elif level == 'medium':
            if not self.try_win_block('O'):  # Try to win
                if not self.try_win_block('X'):  # Try to block
                    self.random_move()
        elif level == 'hard':
            if not self.try_win_block('O'):  # Try to win
                if not self.try_win_block('X'):  # Try to block
                    self.best_move()

    def random_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 'O'

    def try_win_block(self, player):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    self.board[r][c] = player
                    if self.check_winner(player):
                        if player == 'O':
                            return True  # AI wins
                        self.board[r][c] = 'O'  # Block
                        return True
                    self.board[r][c] = ''
        return False

    def best_move(self):
        best_score = -float('inf')
        move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    self.board[r][c] = 'O'
                    score = self.minimax(False)
                    self.board[r][c] = ''
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        if move:
            self.board[move[0]][move[1]] = 'O'

    def minimax(self, is_maximizing):
        if self.check_winner('O'):
            return 1
        if self.check_winner('X'):
            return -1
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == '':
                        self.board[r][c] = 'O'
                        score = self.minimax(False)
                        self.board[r][c] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == '':
                        self.board[r][c] = 'X'
                        score = self.minimax(True)
                        self.board[r][c] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        # Check rows, columns and diagonals
        for row in self.board:
            if all([s == player for s in row]):
                self.current_winner = player
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                self.current_winner = player
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2-i] == player for i in range(3)]):
            self.current_winner = player
            return True
        return False

    def is_board_full(self):
        return all(all(row) for row in self.board)
