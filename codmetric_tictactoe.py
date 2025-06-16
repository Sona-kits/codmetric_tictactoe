import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Minimax AI")
        self.current_player = "X"  # Human is X, AI is O
        self.board = [" " for _ in range(9)]
        self.buttons = []
        
        # Create GUI
        self.create_board()
        self.status_label = tk.Label(root, text="Your turn (X)", font=('Arial', 14))
        self.status_label.grid(row=3, column=0, columnspan=3)
        
        # Add restart button
        restart_btn = tk.Button(root, text="Restart Game", command=self.restart_game)
        restart_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=('Arial', 30), width=5, height=2,
                                 command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)
    
    def on_click(self, row, col):
        index = 3 * row + col
        
        if self.board[index] == " " and self.current_player == "X":
            self.make_move(index, "X")
            
            if not self.check_game_over():
                self.current_player = "O"
                self.status_label.config(text="AI is thinking...")
                self.root.after(500, self.ai_move)  # Small delay for better UX
    
    def ai_move(self):
        if " " in self.board and self.current_player == "O":
            # AI makes move using minimax
            best_score = -float('inf')
            best_move = None
            
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(self.board, False)
                    self.board[i] = " "
                    
                    if score > best_score:
                        best_score = score
                        best_move = i
            
            if best_move is not None:
                self.make_move(best_move, "O")
                self.current_player = "X"
                self.status_label.config(text="Your turn (X)")
                self.check_game_over()
    
    def minimax(self, board, is_maximizing):
        # Check terminal states
        winner = self.check_winner(board)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif " " not in board:
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score
    
    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)
        self.buttons[index].config(state=tk.DISABLED)
    
    def check_winner(self, board):
        # Check rows
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] != " ":
                return board[i]
        
        # Check columns
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] != " ":
                return board[i]
        
        # Check diagonals
        if board[0] == board[4] == board[8] != " ":
            return board[0]
        if board[2] == board[4] == board[6] != " ":
            return board[2]
        
        return None
    
    def check_game_over(self):
        winner = self.check_winner(self.board)
        
        if winner:
            self.disable_all_buttons()
            if winner == "X":
                messagebox.showinfo("Game Over", "Congratulations! You win!")
            else:
                messagebox.showinfo("Game Over", "AI wins!")
            self.status_label.config(text=f"Game Over - {'You' if winner == 'X' else 'AI'} wins!")
            return True
        elif " " not in self.board:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.status_label.config(text="Game Over - It's a tie!")
            return True
        return False
    
    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
    
    def restart_game(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", state=tk.NORMAL)
        self.status_label.config(text="Your turn (X)")

# Create and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()