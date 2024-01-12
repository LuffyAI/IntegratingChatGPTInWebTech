#Author: Larnell Moore
#Creation Date: December 26, 2023
#Date Modified: December 29, 2023
#Purpose: This file runs the chainlit client and allows the user to interact with the model.

import PyPDF2
import chainlit as cl
from chainlit import user_session
from chainlit import AskUserMessage, Message, on_chat_start, on_message
import os
import traceback
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain, LLMMathChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.tools import BaseTool
from langchain.memory import ConversationTokenBufferMemory, ReadOnlySharedMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import cv2
import numpy as np
from PyPDF2 import PdfReader
from io import BytesIO
import pdfplumber
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import random
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredPDFLoader,UnstructuredHTMLLoader
from langchain.document_loaders import DirectoryLoader
import sqlparse
# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')
from w3c_validator import validate
import tempfile



# Directories that contain the chroma databases
c1_dir = 'db/checkpoint1'
c2_dir = 'db/checkpoint2'
c3_dir = 'db/checkpoint3'
c4_dir = 'db/checkpoint4'
pdf_dir= 'db/vectordb'
c1_f23_dir = 'db/checkpoint1_f23'
embedding = OpenAIEmbeddings()


# Directories that contain
c1db = Chroma(persist_directory=c1_dir, embedding_function = embedding)
c1_retriever = c1db.as_retriever(search_kwargs={"k":50})
c1_retriever.search_type= 'similarity'

c2db = Chroma(persist_directory=c2_dir, embedding_function = embedding)
c2_retriever = c2db.as_retriever(search_kwargs={"k":50})
c2_retriever.search_type= 'similarity'

c3db = Chroma(persist_directory=c3_dir, embedding_function = embedding)
c3_retriever = c3db.as_retriever(search_kwargs={"k":50})
c3_retriever.search_type= 'similarity'

c3db = Chroma(persist_directory=c3_dir, embedding_function = embedding)
c3_retriever = c3db.as_retriever(search_kwargs={"k":50})
c3_retriever.search_type= 'similarity'

vectordb = Chroma(persist_directory=pdf_dir, embedding_function=embedding)
pdf_retriever = vectordb.as_retriever(search_kwargs={"k": 50})
pdf_retriever.search_type = 'similarity'

checkpoint1_f23db = Chroma(persist_directory=pdf_dir, embedding_function=embedding)
checkpoint1_f23_retriever = checkpoint1_f23db.as_retriever(search_kwargs={"k": 50})
checkpoint1_f23_retriever.search_type = 'similarity'

# OpenAI Model Settings
llm = ChatOpenAI(temperature=0.5, model = "gpt-4-1106-preview", streaming=True)


# Chat Memory with Token Buffer
memory = ConversationTokenBufferMemory(memory_key="chat_history", llm=llm,max_token_limit=1000)
readonly = ReadOnlySharedMemory(memory=memory)

# Chains
c1_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=c1_retriever, memory=readonly)
c2_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=c2_retriever, memory=readonly)
c3_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=c3_retriever, memory=readonly)
pdf_qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=pdf_retriever,verbose=True)

def dummy_func(*args, **kwargs):
    # This function might log the query, send it to the LLM, or just do nothing.
    pass


def html_validation(input= " "):
    results = []

    # Check if html_input is a file path
    if os.path.isfile(input):
        results = validate(input)["messages"]
    else:
        # Create a temporary file for the HTML content
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html', encoding='utf-8') as tmp_file:
            tmp_file.write(input)
            tmp_file_path = tmp_file.name
        
        # Validate the temporary file
        results = validate(tmp_file_path)["messages"]

        # Clean up the temporary file
        os.remove(tmp_file_path)

    # Format the results
    formatted_results = []
    for m in results:
        formatted_result = f"Type: {m['type']}, Line: {m.get('lastLine', 'N/A')}, Description: {m['message']}"
        formatted_results.append(formatted_result)

    return "\n".join(formatted_results) if formatted_results else "No issues found."


    
# Tools
tools = [
    Tool (
        name = "Web Technology project proposal and feedback",
        func = c1_qa.run,
        description = "Useful for when you need to answer questions about Checkpoint1. Input should be fully formed question."
    ),
    Tool (
        name = "University of Michigan Faculty Information QA system",
        func = c2_qa.run,
        description = "Useful for when you need to answer questions about Checkpoint2."
    ),
    Tool (
        name = "University of Michigan Faculty Research QA system",
        func = c3_qa.run,
        description = "Useful for when you need to answer questions about checkpoint3."
    ),
    Tool(
        name = "General LLM Query",
        func = dummy_func,
        description="Useful for answering general questions not related to the University of Michigan-Dearborn. This tool does not have a specific function and sends queries directly to the LLM for a wide range of topics and inquiries."
    ),
    Tool(
        name = "HTML code validation using W3C",
        func = html_validation,
        description="Use full for answering code smell detection and code vulnerabilities and syntax errors of html code"
    )
]

prefix = """You are a helpful AI assistant having a conversation with a student. Your objective is to answer their questions about the University of Michigan's Dearborn Web Technology class and provide feedback on their work. If you do not know the answer to a question, take your best educated guess and simply tell them you are unsure about your answer. You have access to the following tools:"""

suffix = """Begin!"
{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"]
)
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

conversation_memory = ConversationFlowMemory()

@on_chat_start
async def main(): 
    session_id = cl.user_session.get(id)
    conversation_memory.update_conversation(session_id, "Session started")
    try:
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True)
        
        # Session state chain
        cl.user_session.set("llm_chain", agent_chain)
    except Exception as e:
        print("An error occurred in the on_chat_start function:")
        traceback.print_exc()

    history = conversation_memory.get_conversation_history(session_id)

@cl.on_message
async def main(message: cl.Message):
    session_id = cl.user_session.get(id)
    content = message.content
    conversation_memory.update_conversation(session_id, content)

    last_sentiment = conversation_memory.get_last_sentiment(session_id)

    response_starters = ["That's an interesting question.", "Let me think about that.", "Good point!"]
    response_intro = random.choice(response_starters)

    # Personalize the response style based on sentiment
    response_style = "neutral"
    response_prefix = ""
    if last_sentiment:
        if last_sentiment['compound'] < -0.5:
            response_prefix = "I understand this might be frustrating. "
        elif last_sentiment['compound'] > 0.5:
            response_prefix = "That's great to hear!"

    # Message sent by the user has nothing attached
    if not message.elements:
        try:
            answer_prefix_tokens=["FINAL", "ANSWER"]
            content = response_intro + " " + response_prefix + content
            agent_chain = cl.user_session.get("llm_chain")
            res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])

            await cl.Message(content=res, author="BlueBot").send()
        except Exception as e:
            friendly_message = "Oops, something went wrong. Could you please try again?"
            await cl.Message(content=friendly_message, author="BlueBot").send()
            print("An error occurred in the on_message function:", e)

    # Message sent by user has something attached
    if message.elements is not None:
        images = [file for file in message.elements if "image" in file.mime]
        pdfs = [file for file in message.elements if "pdf" in file.mime]
        html =[file for file in message.elements if "html" in file.mime]
        sql = [file for file in message.elements if "sql" in file.mime]
        if images:
          print("image yes")
        if pdfs:
            try:
                for pdf_file in pdfs:
                    if hasattr(pdf_file, 'content'):  # If the PDF content is provided as bytes
                        with BytesIO(pdf_file.content) as pdf_buffer:
                            with pdfplumber.open(pdf_buffer) as pdf:
                                pdf_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
                        content = response_intro + " " + response_prefix + content + '\n' + pdf_text
                    else:
                        print(f"Unsupported PDF file type or missing content: {type(pdf_file)}")
                        continue

                answer_prefix_tokens = ["FINAL", "ANSWER"]
                agent_chain = cl.user_session.get("llm_chain")
                res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
                await cl.Message(content=res, author="BlueBot").send()
            except Exception as e:
                friendly_message = "I encountered an issue processing the PDF. Could you please try again?"
                await cl.Message(content=friendly_message, author="BlueBot").send()
                print("An error occurred in the on_message function:", e)
        if html:
            print("HTML yes")
            try:
              for html_file in html:
                if hasattr(html_file, 'content') and html_file.content: # If the HTML content is provided as bytes
                     html_content = BytesIO(html_file.content).read().decode('utf-8')
                     soup = BeautifulSoup(html_content, 'html.parser')
                     html_text = soup.get_text(separator='\n')
            # Combine with your existing content
                     content = response_intro + " " + response_prefix + content + '\n' + html_text
            # Now, soup contains the parsed HTML
                else:
                 print(f"Unsupported HTML file type or missing content: {type(html_file)}")
              validation_results = html_validation(html_content)
              print(validation_results) 
              answer_prefix_tokens = ["FINAL", "ANSWER"]
              agent_chain = cl.user_session.get("llm_chain")
              res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
              await cl.Message(content=res, author="BlueBot").send()
            except Exception as e:
                friendly_message = "I encountered an issue processing the html. Could you please try again?"
                await cl.Message(content=friendly_message, author="BlueBot").send()
                print("An error occurred in the on_message function:", e)



                

        
    

 


