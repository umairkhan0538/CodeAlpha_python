import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

class Chatbot:
    def __init__(self, name="GrokBot"):
        self.name = name
        self.sid = SentimentIntensityAnalyzer()
        self.responses = {
            "greeting": [
                "Hey there! How's it going?",
                "Hi! Nice to chat with you!",
                "Hello! What's on your mind?"
            ],
            "farewell": [
                "Catch you later!",
                "Bye for now!",
                "See ya!"
            ],
            "question": [
                "Hmm, that's a good one! Can you tell me more?",
                "Interesting question! What's the context?",
                "Let me think... Could you clarify that a bit?"
            ],
            "positive": [
                "That's awesome to hear!",
                "Love the positivity!",
                "You're killing it!"
            ],
            "negative": [
                "Oh no, sorry to hear that. Want to talk about it?",
                "That sounds tough. I'm here for you!",
                "Hang in there, things will get better."
            ],
            "default": [
                "Cool, tell me more!",
                "That's interesting! What's next?",
                "Nice, what's on your mind now?"
            ]
        }
        self.patterns = {
            r"hi|hello|hey": "greeting",
            r"bye|goodbye|see you": "farewell",
            r"\?|what|why|how|when|where": "question"
        }

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the input text."""
        scores = self.sid.polarity_scores(text)
        if scores['compound'] > 0.3:
            return "positive"
        elif scores['compound'] < -0.3:
            return "negative"
        return None

    def get_response(self, user_input):
        """Generate a response based on input patterns and sentiment."""
        user_input = user_input.lower().strip()
        tokens = word_tokenize(user_input)

        # Check for specific patterns
        for pattern, response_type in self.patterns.items():
            if re.search(pattern, user_input):
                return random.choice(self.responses[response_type])

        # Check sentiment
        sentiment = self.analyze_sentiment(user_input)
        if sentiment:
            return random.choice(self.responses[sentiment])

        # Fallback to default response
        return random.choice(self.responses["default"])

    def chat(self):
        """Run the chatbot conversation loop."""
        print(f"{self.name}: Hi! I'm {self.name}, your chat buddy. What's up? (Type 'quit' to exit)")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() == 'quit':
                    print(f"{self.name}: {random.choice(self.responses['farewell'])}")
                    break
                if not user_input.strip():
                    print(f"{self.name}: Don't be shy, say something!")
                    continue
                response = self.get_response(user_input)
                print(f"{self.name}: {response}")
            except KeyboardInterrupt:
                print(f"\n{self.name}: Interrupted? No worries, bye!")
                break
            except EOFError:
                print(f"\n{self.name}: Input ended? Catch you later!")
                break

if __name__ == "__main__":
    # Download required NLTK data (run once)
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('punkt')
        nltk.download('vader_lexicon')
    
    # Start the chatbot
    bot = Chatbot()
    bot.chat()