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

# Directories that contain the chroma databases
c1_dir = 'db/checkpoint1'
c2_dir = 'db/checkpoint2'
c3_dir = 'db/checkpoint3'
c4_dir = 'db/checkpoint4'
pdf_dir= 'db/vectordb'
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

# Tools
tools = [
    Tool (
        name = "Web Tech Checkpoint",
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

@on_chat_start
async def main(): 
    try:
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True)
        
        # Session state chain
        cl.user_session.set("llm_chain", agent_chain)
    except Exception as e:
        print("An error occurred in the on_chat_start function:")
        traceback.print_exc()

@cl.on_message
async def main(message: cl.Message):
    
    # Message sent by the user has nothing attached
    if not message.elements:
        try:
            answer_prefix_tokens=["FINAL", "ANSWER"]
            content = message.content
            agent_chain = cl.user_session.get("llm_chain")
            res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])


            await cl.Message(content=res, author="BlueBot").send()
        except Exception as e:
            print("An error occurred in the on_message function:")
            traceback.print_exc()

    # Message sent by user has something attached
    if message.elements:
        
        images = [file for file in message.elements if "image" in file.mime]
        pdfs = [file for file in message.elements if "pdf" in file.mime]
        content = message.content
        if images:
            print("images yes")
        if pdfs:
         try:
           for pdf_file in pdfs:
            # Handling the attached PDF file
            if hasattr(pdf_file, 'content'):  # If the PDF content is provided as bytes
                with BytesIO(pdf_file.content) as pdf_buffer:
                    with pdfplumber.open(pdf_buffer) as pdf:
                        pdf_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
                content += '\n' + pdf_text
            else:
                print(f"Unsupported PDF file type or missing content: {type(pdf_file)}")
                continue

            # Append the extracted text to the message content
            

    # Now proceed with your langchain processing using the updated content
           answer_prefix_tokens = ["FINAL", "ANSWER"]
           agent_chain = cl.user_session.get("llm_chain")
           res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])

           await cl.Message(content=res, author="BlueBot").send()
         except Exception as e:
          print("An error occurred in the on_message function:", e)


 

    

 


