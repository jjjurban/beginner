import random
import json
from collections import defaultdict

class BasicChatbot:
    def __init__(self):
        # Memory: {input: {category: count}}
        self.memory = defaultdict(lambda: defaultdict(int))
        # Response templates by category
        self.response_templates = {
            "question": ["What’s up with {key}?", "Why {key}?", "{key}—tell me more?"],
            "complaint": ["Ouch, {key} sounds rough.", "Ugh, {key} again?", "Sorry about {key}."],
            "happy": ["Nice, {key} is great!", "Cool, {key} huh?", "{key}—awesome!"],
            "default": ["Okay, {key}.", "Got {key}.", "Huh, {key}?"]
        }
        # Feedback: {(input, response): score}
        self.feedback = {}
        self.last_input = None
        self.last_response = None
        # Context: last few inputs
        self.context = []

    def categorize(self, user_input):
        """Guess the category of the input."""
        user_input = user_input.lower()
        if "?" in user_input or any(w in user_input for w in ["how", "what", "why", "who"]):
            return "question"
        elif any(word in user_input for word in ["bad", "sucks", "bullshit", "tired", "ugh"]):
            return "complaint"
        elif any(word in user_input for word in ["good", "great", "happy", "awesome", "cool"]):
            return "happy"
        else:
            return "default"

    def extract_key(self, user_input):
        """Pick a key word/phrase to mirror."""
        words = user_input.lower().split()
        stop_words = {"is", "are", "you", "the", "a", "doing"}
        for word in words:
            if word not in stop_words:
                return word
        return words[0] if words else user_input

    def handle_question(self, user_input):
        """Try to answer specific questions."""
        user_input = user_input.lower()
        if "how are you" in user_input or "how you doing" in user_input:
            return random.choice(["I’m good, how about you?", "Doing fine, you?"])
        elif any(op in user_input for op in ["+", "-", "*", "/"]) and any(c.isdigit() for c in user_input):
            # Simple math detection
            words = user_input.split()
            try:
                for i, w in enumerate(words):
                    if w in ["+", "-", "*", "/"]:
                        num1 = int(words[i-1])
                        num2 = int(words[i+1])
                        if w == "+":
                            return f"{num1 + num2}"
                        elif w == "-":
                            return f"{num1 - num2}"
                        elif w == "*":
                            return f"{num1 * num2}"
                        elif w == "/" and num2 != 0:
                            return f"{num1 / num2}"
            except (ValueError, IndexError):
                pass
        return None  # Fallback to normal response if no specific answer

    def learn(self, user_input, feedback=None):
        """Store input and update based on feedback."""
        category = self.categorize(user_input)
        self.memory[user_input][category] += 1
        if feedback and self.last_response:
            pair = (self.last_input, self.last_response)
            self.feedback[pair] = self.feedback.get(pair, 0) + (1 if feedback == "good" else -1)

    def respond(self, user_input):
        """Generate a response with mirroring, context, and question handling."""
        # Check for specific question answers first
        specific_answer = self.handle_question(user_input)
        if specific_answer:
            response = specific_answer
        else:
            category = self.categorize(user_input)
            key = self.extract_key(user_input)
            possible_responses = self.response_templates.get(category, self.response_templates["default"])
            
            if user_input in [pair[0] for pair in self.feedback.keys()]:
                scored = [(resp.format(key=key), self.feedback.get((user_input, resp.format(key=key)), 0)) 
                          for resp in possible_responses]
                response = max(scored, key=lambda x: x[1])[0]
            else:
                response = random.choice(possible_responses).format(key=key)

            # Ask back (20% chance for questions)
            if category == "question" and random.random() < 0.2:
                response += " What do you think?"

        # Add to context
        self.context.append(user_input)
        if len(self.context) > 3:
            self.context.pop(0)

        # Reference context (30% chance)
        if len(self.context) > 1 and random.random() < 0.3:
            prev_key = self.extract_key(self.context[-2])
            response += f" Tied to {prev_key}?"

        # Add natural filler (10% chance)
        if random.random() < 0.1:
            fillers = ["Hmm… ", "Well, ", "Oh, "]
            response = random.choice(fillers) + response

        self.last_input = user_input
        self.last_response = response
        return response

    def save_memory(self, filename="chatbot_memory.json"):
        """Save learned data to a file."""
        with open(filename, "w") as f:
            json.dump({"memory": dict(self.memory), "feedback": self.feedback, "context": self.context}, f)

    def load_memory(self, filename="chatbot_memory.json"):
        """Load learned data from a file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.memory = defaultdict(lambda: defaultdict(int), data["memory"])
                self.feedback = data["feedback"]
                self.context = data.get("context", [])
        except FileNotFoundError:
            pass

def main():
    chatbot = BasicChatbot()
    chatbot.load_memory()
    
    print("Chat with BasicChatbot! Say 'exit' to quit, 'good' or 'wrong' to train me.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            chatbot.save_memory()
            print("AI: Catch you later!")
            break
        
        if user_input.lower() in ["good", "wrong"]:
            chatbot.learn(chatbot.last_input, user_input.lower())
            print("AI: Thanks for the feedback!")
        elif user_input:
            response = chatbot.respond(user_input)
            print(f"AI: {response}")

if __name__ == "__main__":
    main()