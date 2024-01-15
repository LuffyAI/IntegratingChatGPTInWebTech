# Author: Larnell Moore
# Creation Date: December 26, 2023
# Date Modified: Jan 12, 2024
# Purpose: This file communicates with a GPT 3.5-Turbo model finetuned on TA feedback from the Web Technology course.
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

class FeedbackAgent:

 def __init__(self):
      
    # Loads the API key  
    load_dotenv()
    
    # Model
    self.fine_tuned_model = os.getenv("FINETUNED_FEEDBACK_MODEL")  
    openai.api_key = os.getenv("OPENAI_API_KEY")
    self.llm = ChatOpenAI(temperature=0.5, model=self.fine_tuned_model, streaming=True)
    
    # Prompt
    template = """You are an an AI assistant that reads code and provides a numbered list of suggestions to the user. 

    Current conversation:
    {history}
    Human: {input}
    AI Assistant:"""
    
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    
    # Conversation Chain with memory
    self.conversation = ConversationChain(
    prompt=PROMPT,
    llm=self.llm,
    memory=ConversationBufferMemory(
        llm=ChatOpenAI(), max_token_limit=3000
    ),
    verbose=False,
)
     
    
 def chat(self, input_text):
    try:
      response = self.conversation.predict(input = input_text)
      return response
    except Exception as e:
      return "An error occurred while communicating with the Feedback Agent: " + str(e)  

