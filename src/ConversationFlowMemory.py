from nltk.sentiment import SentimentIntensityAnalyzer

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