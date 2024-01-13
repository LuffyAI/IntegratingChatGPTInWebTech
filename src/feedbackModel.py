import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

class FeedbackAgent:

 def __init__(self):
      
    load_dotenv()
    
    # Model
    self.fine_tuned_model = os.getenv("FINETUNED_FEEDBACK_MODEL")  
    openai.api_key = os.getenv("OPENAI_API_KEY")
    self.llm = ChatOpenAI(temperature=0.5, model=self.fine_tuned_model, streaming=True)
    self.conversation = ConversationChain(
    llm=self.llm,
    memory=ConversationBufferMemory(
        llm=ChatOpenAI(), max_token_limit=3000
    ),
    verbose=False,
)
     
    
 def chat(self, input_text):
    response = self.conversation.predict(input = input_text)
    return response

