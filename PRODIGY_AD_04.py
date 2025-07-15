import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful Tic Tac Toe")
        self.root.geometry("500x645")
        self.root.resizable(False, True)
        
        # Game variables
        self.board = [""] * 9
        self.current_player = "X"
        self.game_mode = "human"  # Default to human vs human
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0
        self.game_active = True
        
        # Colors
        self.bg_color = "#2c3e50"
        self.button_bg = "#34495e"
        self.x_color = "#e74c3c"
        self.o_color = "#3498db"
        self.hover_color = "#7f8c8d"
        self.text_color = "#ecf0f1"
        self.current_player_color = "#f1c40f"
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Game mode selection
        self.mode_frame = tk.Frame(self.root, bg=self.bg_color)
        self.mode_frame.pack(pady=10)
        
        self.mode_label = tk.Label(
            self.mode_frame, 
            text="Game Mode:", 
            bg=self.bg_color, 
            fg=self.text_color,
            font=("Arial", 12)
        )
        self.mode_label.pack(side=tk.LEFT)
        
        self.mode_var = tk.StringVar(value="human")
        
        self.human_mode = tk.Radiobutton(
            self.mode_frame,
            text="Player vs Player",
            variable=self.mode_var,
            value="human",
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor=self.bg_color,
            command=self.change_mode,
            font=("Arial", 10)
        )
        self.human_mode.pack(side=tk.LEFT, padx=5)
        
        self.ai_mode = tk.Radiobutton(
            self.mode_frame,
            text="Player vs AI",
            variable=self.mode_var,
            value="ai",
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor=self.bg_color,
            command=self.change_mode,
            font=("Arial", 10)
        )
        self.ai_mode.pack(side=tk.LEFT, padx=5)
        
        # Current player display
        self.player_frame = tk.Frame(self.root, bg=self.bg_color)
        self.player_frame.pack(pady=5)
        
        self.player_label = tk.Label(
            self.player_frame,
            text="Current Player:",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 12)
        )
        self.player_label.pack(side=tk.LEFT)
        
        self.current_player_display = tk.Label(
            self.player_frame,
            text="X",
            bg=self.bg_color,
            fg=self.current_player_color,
            font=("Arial", 12, "bold")
        )
        self.current_player_display.pack(side=tk.LEFT, padx=5)
        
        # Scoreboard
        self.score_frame = tk.Frame(self.root, bg=self.bg_color)
        self.score_frame.pack(pady=10)
        
        self.x_score = tk.Label(
            self.score_frame,
            text="X: 0",
            bg=self.bg_color,
            fg=self.x_color,
            font=("Arial", 12)
        )
        self.x_score.pack(side=tk.LEFT, padx=10)
        
        self.o_score = tk.Label(
            self.score_frame,
            text="O: 0",
            bg=self.bg_color,
            fg=self.o_color,
            font=("Arial", 12)
        )
        self.o_score.pack(side=tk.LEFT, padx=10)
        
        self.tie_score = tk.Label(
            self.score_frame,
            text="Ties: 0",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 12)
        )
        self.tie_score.pack(side=tk.LEFT, padx=10)
        
        # Game board
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 30, "bold"),
                width=4,
                height=2,
                bg=self.button_bg,
                fg=self.text_color,
                activebackground=self.hover_color,
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            # Add hover effects
            btn.bind("<Enter>", lambda event, b=btn: self.on_enter(event, b))
            btn.bind("<Leave>", lambda event, b=btn: self.on_leave(event, b))
            
            self.buttons.append(btn)
        
        # Reset button
# Reset button
            self.reset_button = tk.Button(
                self.root,
                text="New Game",
                font=("Arial", 12),
                bg="#27ae60",
                fg=self.text_color,
                activebackground="#2ecc71",
                command=self.reset_game
            )
            self.reset_button.pack(pady=10)

    
    def on_enter(self, event, button):
        if button["text"] == "" and self.game_active:
            button["bg"] = self.hover_color
    
    def on_leave(self, event, button):
        if button["text"] == "":
            button["bg"] = self.button_bg
    
    def change_mode(self):
        self.game_mode = self.mode_var.get()
        self.reset_game()
    
    def make_move(self, position):
        if not self.game_active or self.board[position] != "":
            return
        
        # Human move
        self.board[position] = self.current_player
        self.buttons[position]["text"] = self.current_player
        self.buttons[position]["fg"] = self.x_color if self.current_player == "X" else self.o_color
        
        if self.check_winner():
            self.handle_win()
            return
        elif self.check_draw():
            self.handle_draw()
            return
            
        self.switch_player()
        
        # AI move if in AI mode and it's O's turn
        if self.game_mode == "ai" and self.current_player == "O" and self.game_active:
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        # Simple AI - first tries to win, then blocks, then random
        available_moves = [i for i, val in enumerate(self.board) if val == ""]
        
        # Check for winning move
        for move in available_moves:
            self.board[move] = "O"
            if self.check_winner(silent=True):
                self.board[move] = ""
                self.make_move(move)
                return
            self.board[move] = ""
        
        # Check for blocking move
        for move in available_moves:
            self.board[move] = "X"
            if self.check_winner(silent=True):
                self.board[move] = ""
                self.make_move(move)
                return
            self.board[move] = ""
        
        # Otherwise make a random move
        if available_moves:
            move = random.choice(available_moves)
            self.make_move(move)
    
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.current_player_display["text"] = self.current_player
        self.current_player_display["fg"] = self.o_color if self.current_player == "O" else self.x_color
    
    def check_winner(self, silent=False):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != "":
                if not silent:
                    # Highlight winning cells
                    for idx in combo:
                        self.buttons[idx]["bg"] = "#f1c40f"
                return True
        return False
    
    def check_draw(self):
        return "" not in self.board
    
    def handle_win(self):
        self.game_active = False
        winner = self.current_player
        if winner == "X":
            self.x_wins += 1
            self.x_score["text"] = f"X: {self.x_wins}"
        else:
            self.o_wins += 1
            self.o_score["text"] = f"O: {self.o_wins}"
        
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
    
    def handle_draw(self):
        self.game_active = False
        self.ties += 1
        self.tie_score["text"] = f"Ties: {self.ties}"
        messagebox.showinfo("Game Over", "It's a draw!")
    
    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        
        self.current_player_display["text"] = "X"
        self.current_player_display["fg"] = self.x_color
        
        for button in self.buttons:
            button["text"] = ""
            button["bg"] = self.button_bg
            button["fg"] = self.text_color

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()