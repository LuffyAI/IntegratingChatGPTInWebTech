# Author: Larnell Moore
# Creation Date: Jan 14, 2023
# Date Modified: Jan 14, 2024
# Purpose: This file communicates with a GPT 4-Vision model that examines an image uploaded by the user and provide color theory feedback.
import base64
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser

class ColorAgent:
 def __init__(self):
      
    load_dotenv()
    
    # Model
    self.llm = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
    
 def chat(self, image, user_request):
    try:
        msg = self.llm.invoke(
            [   AIMessage(
                content="You are a useful bot that describes the given webpage and color scheme and is knowledgable about Color Theory."
            ),
                HumanMessage(
                    content=[
                        {"type": "text", "text": "{user_request}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image}"
                            },
                        },
                    ]
                )
            ]
        )
        return msg
    except Exception as e:
        return "An error occurred communicating with the Color Theory Agent in the chat function: " + str(e)

 def encode_image(self, image_bytes):
    try:
     return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        raise "A error occurred converting the image bytes into base64 in the ColorTheory Agent encode function: " + str(e)
    
 

