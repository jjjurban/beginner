import random

# Payoff matrix for Prisoner's Dilemma (Player, Opponent)
# (Cooperate, Cooperate), (Cooperate, Defect), (Defect, Cooperate), (Defect, Defect)
payoffs = {
    ("C", "C"): (3, 3),  # Both cooperate: moderate reward
    ("C", "D"): (0, 5),  # You cooperate, they defect: you lose big
    ("D", "C"): (5, 0),  # You defect, they cooperate: you win big
    ("D", "D"): (1, 1)   # Both defect: small reward
}

# AI strategies
def ai_random(history):
    return random.choice(["C", "D"])

def ai_always_cooperate(history):
    return "C"

def ai_always_defect(history):
    return "D"

def ai_tit_for_tat(history):
    if not history:  # First move, cooperate
        return "C"
    return history[-1][0]  # Mirror player's last move

# Game setup
strategies = {
    "1": ("Random", ai_random),
    "2": ("Always Cooperate", ai_always_cooperate),
    "3": ("Always Defect", ai_always_defect),
    "4": ("Tit-for-Tat", ai_tit_for_tat)
}

def play_round(player_choice, ai_choice):
    return payoffs[(player_choice, ai_choice)]

def game():
    print("Welcome to the Prisoner's Dilemma!")
    print("You and your AI opponent can Cooperate (C) or Defect (D).")
    print("Payoffs: (C,C) = 3,3 | (C,D) = 0,5 | (D,C) = 5,0 | (D,D) = 1,1")
    
    # Choose AI strategy
    print("\nChoose your opponent's strategy:")
    for key, (name, _) in strategies.items():
        print(f"{key}: {name}")
    choice = input("Enter 1-4: ")
    ai_name, ai_strategy = strategies.get(choice, strategies["1"])
    print(f"You're playing against: {ai_name}\n")
    
    rounds = int(input("How many rounds do you want to play? "))
    player_score, ai_score = 0, 0
    history = []  # Tracks (player_move, ai_move) pairs

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}:")
        player_move = input("Enter your move (C or D): ").upper()
        while player_move not in ["C", "D"]:
            player_move = input("Invalid move! Enter C or D: ").upper()
        
        ai_move = ai_strategy(history)
        player_payoff, ai_payoff = play_round(player_move, ai_move)
        
        player_score += player_payoff
        ai_score += ai_payoff
        history.append((player_move, ai_move))
        
        print(f"You chose: {player_move} | AI chose: {ai_move}")
        print(f"Payoffs - You: {player_payoff} | AI: {ai_payoff}")
        print(f"Total Scores - You: {player_score} | AI: {ai_score}")

    print("\nGame Over!")
    print(f"Final Scores - You: {player_score} | AI: {ai_score}")
    if player_score > ai_score:
        print("You win!")
    elif ai_score > player_score:
        print("AI wins!")
    else:
        print("It's a tie!")

# Start the game
if __name__ == "__main__":
    game()