import tkinter as tk
from tkinter import messagebox
import copy
from tkinter import font as tkFont

# AI algorithm
def minimax(board, depth, maximizingPlayer):
    if game_over(board):
        if winning(board, 'O'):
            return {'position': None, 'score': 1 * (depth + 1)}
        elif winning(board, 'X'):
            return {'position': None, 'score': -1 * (depth + 1)}
        else: # Game is over, no more valid moves
            return {'position': None, 'score': 0}

    if maximizingPlayer:
        best = {'position': None, 'score': -float('inf')}

        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    new_score = minimax(board, depth - 1, False)
                    board[i][j] = ''
                    new_score['position'] = (i, j)

                    if new_score['score'] > best['score']:
                        best = new_score

        return best

    else:
        best = {'position': None, 'score': float('inf')}

        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    new_score = minimax(board, depth - 1, True)
                    board[i][j] = ''
                    new_score['position'] = (i, j)

                    if new_score['score'] < best['score']:
                        best = new_score

        return best

# Check if game is over
def game_over(board):
    # Check for win
    if winning(board, 'O') or winning(board, 'X'):
        return True
    # Check for draw
    if len(available_moves(board)) == 0:
        return True
    # Game is not over
    return False

# Check if a player has won
def winning(board, player):
    # Check rows, columns and diagonals
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    if [player, player, player] in win_states:
        return True
    return False

# Check for available moves
def available_moves(board):
    moves = []
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == '':
                moves.append((i, j))
    return moves

# GUI
class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player_turn = 'X'

        # Create main window
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')

        # Create grid of buttons
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text='', command=lambda i=i, j=j: self.on_button_click(i, j), height=3, width=6)
                self.buttons[i][j].grid(row=i, column=j, sticky='nsew')

        # Create restart button
        self.restart_button = tk.Button(self.window, text='Restart', command=self.new_game)
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky='nsew')

        # Configure grid weights
        for i in range(4):  # Now there are 4 rows
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.window.grid_columnconfigure(i, weight=1)

        # Bind a function to window resize event
        self.window.bind('<Configure>', self.resize)

        # Create menu
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        
        # Game Menu
        self.game_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Game', menu=self.game_menu)
        self.game_menu.add_command(label='New Game', command=self.new_game)
        self.game_menu.add_command(label='Exit', command=self.window.quit)

        # Help Menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='How to Play', command=self.show_help)
        self.help_menu.add_command(label='About AI', command=self.show_ai_info)
    
    def resize(self, event):
        # Compute font size based on window size
        size = min(int(event.width / 15), int(event.height / 15))  # Adjust divisor to get the desired appearance
        btn_font = tkFont.Font(size=size)  # Create a font with the computed size

        # Set button font sizes
        for row in self.buttons:
            for button in row:
                button['font'] = btn_font

    def show_help(self):
        messagebox.showinfo('How to Play', 'The game is played on a grid that\'s 3 squares by 3 squares. '
                                'You are X, your friend (or the computer in this case) is O. '
                                'Players take turns putting their marks in empty squares. '
                                'The first player to get 3 of her marks in a row (up, down, across, or diagonally) is the winner. '
                                'When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.')

    def show_ai_info(self):
        messagebox.showinfo('About AI', 'The AI uses a strategy called Minimax to decide its next move. '
                                'Minimax is a decision-making algorithm for minimizing the worst case scenario in a game. '
                                'The AI evaluates all possible moves and chooses the one that is most likely to result in a victory.')
            
    def new_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ''
                self.buttons[i][j]['state'] = 'normal'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player_turn = 'X'

    def on_button_click(self, i, j):
        if self.buttons[i][j]['text'] == '' and self.player_turn == 'X':
            self.buttons[i][j]['text'] = 'X'
            self.board[i][j] = 'X'
            self.player_turn = 'O'

            if not self.check_game_over('X'):
                self.ai_move()

    def ai_move(self):
        if not game_over(self.board):
            move = minimax(self.board, len(available_moves(self.board)), True)['position']
            self.buttons[move[0]][move[1]]['text'] = 'O'
            self.board[move[0]][move[1]] = 'O'
            self.player_turn = 'X'
            self.check_game_over('O')

    def check_game_over(self, player):
        if game_over(self.board):
            if winning(self.board, player):
                messagebox.showinfo('Game Over', 'Player ' + player + ' wins!')
            else:
                messagebox.showinfo('Game Over', 'The game is a draw')
            self.new_game()
            return True
        return False

if __name__ == '__main__':
    game = TicTacToe()
    game.window.mainloop()