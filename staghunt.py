import random
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

# Payoff matrix
payoffs = {
    ("S", "S"): (4, 4),
    ("S", "H"): (0, 2),
    ("H", "S"): (2, 0),
    ("H", "H"): (2, 2)
}

class StagHuntGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Stag Hunt")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.player_score = 0
        self.ai_score = 0
        self.round = 0
        self.history = []
        self.max_rounds = 0
        self.score_history = {"player": [], "ai": []}
        self.ai_trust = 0.5
        self.ai_trust_threshold = 0.4  # AI needs trust above this to hunt Stag
        self.ai_personality = "Neutral"
        
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Modern theme
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#eceff1", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(self.main_frame, text="Stag Hunt", font=("Arial", 18, "bold"), bg="#eceff1", fg="#263238").grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Instructions
        tk.Label(self.main_frame, text="Hunt Stag (S) together for 4 points or Hare (H) alone for 2.\nPayoffs: (S,S)=4,4 | (S,H)=0,2 | (H,S)=2,0 | (H,H)=2,2",
                 bg="#eceff1", fg="#37474f", font=("Arial", 10), wraplength=400, justify="center").grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Rounds input
        tk.Label(self.main_frame, text="Rounds:", bg="#eceff1", fg="#37474f", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=5)
        self.rounds_entry = tk.Entry(self.main_frame, width=10, font=("Arial", 10), fg="black", bg="white", insertbackground="black", borderwidth=2, relief="flat")
        self.rounds_entry.grid(row=2, column=1, sticky="w")

        # AI personality
        tk.Label(self.main_frame, text="AI Personality:", bg="#eceff1", fg="#37474f", font=("Arial", 10)).grid(row=3, column=0, sticky="e", pady=5)
        self.personality_var = tk.StringVar(value="Neutral")
        personality_frame = tk.Frame(self.main_frame, bg="#eceff1")
        personality_frame.grid(row=3, column=1, sticky="w")
        for text, value in [("Trusting (75%)", "Trusting"), ("Neutral (50%)", "Neutral"), ("Skeptical (25%)", "Skeptical")]:
            rb = tk.Radiobutton(personality_frame, text=text, variable=self.personality_var, value=value, bg="#eceff1", fg="#37474f", font=("Arial", 10), relief="flat")
            rb.pack(side=tk.LEFT, padx=5)
            rb.config(activebackground="#eceff1", selectcolor="#b0bec5")

        # Start button
        self.start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game, style="TButton")
        self.start_button.grid(row=4, column=0, columnspan=2, pady=20)
        self.start_button.configure(style="Start.TButton")
        self.style.configure("Start.TButton", background="#4CAF50", foreground="white")
        self.style.map("Start.TButton", background=[("active", "#4CAF50"), ("disabled", "#a5d6a7")], foreground=[("active", "white")])

    def ai_move(self):
        # AI hunts Stag only if trust exceeds threshold, otherwise Hare
        if self.ai_trust > self.ai_trust_threshold:
            return "S"
        return "H"

    def update_trust(self, player_move, ai_move):
        if player_move == "S" and ai_move == "S":
            self.ai_trust = min(1.0, self.ai_trust + 0.1)
            self.ai_trust_threshold = max(0.2, self.ai_trust_threshold - 0.05)  # Lower threshold with success
        elif player_move == "H" and ai_move == "S":
            self.ai_trust = max(0.0, self.ai_trust - 0.1)
            self.ai_trust_threshold = min(0.6, self.ai_trust_threshold + 0.05)  # Raise threshold with betrayal
        self.ai_trust += random.uniform(-0.02, 0.02)
        self.ai_trust = max(0.0, min(1.0, self.ai_trust))

    def start_game(self):
        try:
            self.max_rounds = int(self.rounds_entry.get())
            if self.max_rounds <= 0:
                raise ValueError
        except ValueError:
            error_window = tk.Toplevel(self.root)
            error_window.title("Error")
            error_window.geometry("300x100")
            error_window.transient(self.root)
            error_window.grab_set()
            tk.Label(error_window, text="Enter a positive number of rounds!", font=("Arial", 12), fg="black", bg="white").pack(pady=10)
            tk.Button(error_window, text="OK", command=error_window.destroy, font=("Arial", 10), bg="#4CAF50", fg="white").pack(pady=5)
            return
        
        self.player_score = 0
        self.ai_score = 0
        self.round = 0
        self.history = []
        self.score_history = {"player": [], "ai": []}
        self.ai_personality = self.personality_var.get()
        self.ai_trust = {"Trusting": 0.75, "Neutral": 0.5, "Skeptical": 0.25}[self.ai_personality]
        self.ai_trust_threshold = 0.4
        
        self.start_button.grid_forget()  # Hide start button
        self.game_frame = tk.Frame(self.main_frame, bg="#eceff1")
        tk.Label(self.game_frame, text="Your Choice:", bg="#eceff1", fg="#37474f", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.stag_button = ttk.Button(self.game_frame, text="Hunt Stag (S)", command=lambda: self.make_move("S"), style="Game.TButton")
        self.stag_button.grid(row=1, column=0, padx=10, pady=5)
        self.hare_button = ttk.Button(self.game_frame, text="Hunt Hare (H)", command=lambda: self.make_move("H"), style="Game.TButton")
        self.hare_button.grid(row=1, column=1, padx=10, pady=5)
        self.style.configure("Game.TButton", background="#0288d1", foreground="white")
        self.style.map("Game.TButton", background=[("active", "#0277bd")], foreground=[("active", "white")])
        
        self.round_label = tk.Label(self.game_frame, text=f"Round: {self.round} / {self.max_rounds}", bg="#eceff1", fg="#37474f", font=("Arial", 10))
        self.round_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.result_label = tk.Label(self.game_frame, text="Make your move!", bg="#eceff1", fg="#37474f", font=("Arial", 10), wraplength=400)
        self.result_label.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Label(self.game_frame, text="Scores:", bg="#eceff1", fg="#37474f", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=(10, 5))
        self.player_bar = ttk.Progressbar(self.game_frame, length=200, maximum=50, style="blue.Horizontal.TProgressbar")
        self.player_bar.grid(row=5, column=0, columnspan=2)
        self.player_score_label = tk.Label(self.game_frame, text="You: 0", bg="#eceff1", fg="#37474f", font=("Arial", 10))
        self.player_score_label.grid(row=6, column=0, columnspan=2)
        self.ai_bar = ttk.Progressbar(self.game_frame, length=200, maximum=50, style="orange.Horizontal.TProgressbar")
        self.ai_bar.grid(row=7, column=0, columnspan=2)
        self.ai_score_label = tk.Label(self.game_frame, text=f"AI ({self.ai_personality}): 0", bg="#eceff1", fg="#37474f", font=("Arial", 10))
        self.ai_score_label.grid(row=8, column=0, columnspan=2)
        self.style.configure("blue.Horizontal.TProgressbar", troughcolor="#eceff1", background="#0288d1")
        self.style.configure("orange.Horizontal.TProgressbar", troughcolor="#eceff1", background="#f57c00")
        
        self.trust_label = tk.Label(self.game_frame, text=f"AI Trust: {int(self.ai_trust * 100)}% (Threshold: {int(self.ai_trust_threshold * 100)}%)", 
                                   bg="#eceff1", fg="#37474f", font=("Arial", 10))
        self.trust_label.grid(row=9, column=0, columnspan=2, pady=10)
        
        self.game_frame.grid(row=5, column=0, columnspan=2, pady=10)

    def make_move(self, player_move):
        if self.round >= self.max_rounds:
            self.end_game()
            return
        
        self.round += 1
        ai_move = self.ai_move()
        player_payoff, ai_payoff = payoffs[(player_move, ai_move)]
        
        self.player_score += player_payoff
        self.ai_score += ai_payoff
        self.history.append((player_move, ai_move))
        self.score_history["player"].append(self.player_score)
        self.score_history["ai"].append(self.ai_score)
        
        self.update_trust(player_move, ai_move)
        self.update_ui(player_move, ai_move, player_payoff, ai_payoff)

    def update_ui(self, player_move=None, ai_move=None, player_payoff=None, ai_payoff=None):
        self.round_label.config(text=f"Round: {self.round} / {self.max_rounds}")
        if player_move:
            self.result_label.config(text=f"You: {player_move} | AI: {ai_move}\nPayoff - You: {player_payoff} | AI: {ai_payoff}")
            if self.round == self.max_rounds:
                self.end_game()
        self.player_bar["value"] = min(self.player_score, 50)
        self.ai_bar["value"] = min(self.ai_score, 50)
        self.player_score_label.config(text=f"You: {self.player_score}")
        self.ai_score_label.config(text=f"AI ({self.ai_personality}): {self.ai_score}")
        self.trust_label.config(text=f"AI Trust: {int(self.ai_trust * 100)}% (Threshold: {int(self.ai_trust_threshold * 100)}%)")

    def plot_scores(self):
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, self.max_rounds + 1), self.score_history["player"], label="You", color="#0288d1", linewidth=2, linestyle="-", alpha=0.8)
        plt.plot(range(1, self.max_rounds + 1), self.score_history["ai"], label="AI", color="#f57c00", linewidth=2, linestyle="--", alpha=0.8)
        plt.xlabel("Round")
        plt.ylabel("Cumulative Score")
        plt.title("Stag Hunt Score Progression")
        plt.legend(loc="upper left")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def end_game(self):
        self.game_frame.grid_forget()
        self.start_button.grid(row=4, column=0, columnspan=2, pady=20)  # Show start button again
        
        end_window = tk.Toplevel(self.root)
        end_window.title("Game Over")
        end_window.geometry("300x200")
        end_window.configure(bg="white")
        end_window.transient(self.root)
        end_window.grab_set()
        
        result = "You win!" if self.player_score > self.ai_score else "AI wins!" if self.ai_score > self.player_score else "Tie!"
        tk.Label(end_window, text="Game Over", font=("Arial", 14, "bold"), fg="#263238", bg="white").pack(pady=10)
        tk.Label(end_window, text=f"Final Scores:\nYou: {self.player_score}\nAI: {self.ai_score}\n{result}", 
                 font=("Arial", 12), fg="#37474f", bg="white", justify="center").pack(pady=10)
        tk.Button(end_window, text="OK", command=end_window.destroy, font=("Arial", 10), bg="#4CAF50", fg="white").pack(pady=10)
        
        insights_window = tk.Toplevel(self.root)
        insights_window.title("Game Insights")
        insights_window.geometry("300x220")
        insights_window.configure(bg="white")
        insights_window.transient(self.root)
        insights_window.grab_set()
        
        player_stags = sum(1 for p, _ in self.history if p == "S")
        ai_stags = sum(1 for _, a in self.history if a == "S")
        insights = (f"Insights:\nYou hunted Stag {player_stags}/{self.max_rounds} times.\n"
                    f"AI hunted Stag {ai_stags}/{self.max_rounds} times.\n"
                    f"Final AI Trust: {int(self.ai_trust * 100)}%\nThreshold: {int(self.ai_trust_threshold * 100)}%")
        tk.Label(insights_window, text="Game Insights", font=("Arial", 14, "bold"), fg="#263238", bg="white").pack(pady=10)
        tk.Label(insights_window, text=insights, font=("Arial", 12), fg="#37474f", bg="white", justify="center").pack(pady=10)
        tk.Button(insights_window, text="OK", command=insights_window.destroy, font=("Arial", 10), bg="#4CAF50", fg="white").pack(pady=10)
        
        self.plot_scores()

    def run(self):
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = StagHuntGame(root)
    game.run()