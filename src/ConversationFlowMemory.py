# Authors: Venkata Alekhya Kusam
# Creation Date: December 26, 2023
# Date Modified: Jan 14, 2024
# Purpose: 

from nltk.sentiment import SentimentIntensityAnalyzer
import random

class ConversationFlowMemory:
    def __init__(self):
        self.session_history = {}
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def update_conversation(self, session_id, interaction):
        if session_id not in self.session_history:
            self.session_history[session_id] = []
        sentiment = self.sentiment_analyzer.polarity_scores(interaction)
        self.session_history[session_id].append((interaction, sentiment))

    def get_conversation_history(self, session_id):
        return self.session_history.get(session_id, [])

    def get_last_sentiment(self, session_id):
        if session_id in self.session_history and self.session_history[session_id]:
            return self.session_history[session_id][-1][1]
        return None
    
    def selectResponseStarter(self):
     response_starters = ["That's an interesting question.", "Let me think about that.", "Good point!"]
     return random.choice(response_starters)
    
    def personalizeResponseStyle(self, session_id):
        last_sentiment = self.get_last_sentiment(session_id)
        response_prefix = ""
        if last_sentiment:
            if last_sentiment['compound'] < -0.5:
                response_prefix = "I understand this might be frustrating. "
            elif last_sentiment['compound'] > 0.5:
                response_prefix = "That's great to hear!"
        return response_prefix