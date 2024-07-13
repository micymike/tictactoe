from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_winner = None

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
            self.easy_move()
        elif level == 'medium':
            self.medium_move()
        elif level == 'hard':
            self.hard_move()

    def easy_move(self):
        empty_cells = self.get_empty_cells()
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 'O'

    def medium_move(self):
        # Try to win, then block, then random
        if not self.try_win_or_block('O') and not self.try_win_or_block('X'):
            self.easy_move()

    def hard_move(self):
        # Try to win, then block, then play strategically
        if not self.try_win_or_block('O') and not self.try_win_or_block('X'):
            if self.board[1][1] == '':
                self.board[1][1] = 'O'  # Take center if available
            else:
                corners = [(0,0), (0,2), (2,0), (2,2)]
                empty_corners = [corner for corner in corners if self.board[corner[0]][corner[1]] == '']
                if empty_corners:
                    row, col = random.choice(empty_corners)
                    self.board[row][col] = 'O'
                else:
                    self.easy_move()  # If no strategic move, play randomly

    def try_win_or_block(self, player):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = player
                    if self.check_winner(player):
                        self.board[row][col] = 'O'
                        return True
                    self.board[row][col] = ''
        return False

    def check_winner(self, player):
        # Check rows, columns, and diagonals for a winner
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def get_empty_cells(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_winner = None

game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    game.reset_board()
    return jsonify({'board': game.board})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    row = int(data['row'])
    col = int(data['col'])
    level = data['level']
    
    result = game.make_move(row, col, level)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)