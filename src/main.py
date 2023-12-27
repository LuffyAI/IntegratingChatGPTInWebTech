#Author: Larnell Moore
#Creation Date: December 26, 2023
#Date Modified: December 26, 2023
#Purpose: This file runs the chainlit client and allows the user to interact with the model.

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
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import ratemyprofessor
from scholarly import scholarly


# Directories that contain the chroma databases
c1_dir = 'db/checkpoint1'
c2_dir = 'db/checkpoint2'
c3_dir = 'db/checkpoint3'
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

# OpenAI Model Settings
llm = ChatOpenAI(temperature=0.5, model = "gpt-4-1106-preview", streaming=True)

# Chat Memory
memory = ConversationBufferMemory(memory_key="chat_history")
readonly = ReadOnlySharedMemory(memory=memory)

# Chains
c1_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=c1_retriever, memory=readonly)
c2_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=c2_retriever, memory=readonly)
c3_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=c3_retriever, memory=readonly)

def dummy_func(*args, **kwargs):
    # This function might log the query, send it to the LLM, or just do nothing.
    pass

def google_scholar_search(input= " "):
    search_query = scholarly.search_author(input)
    author = scholarly.fill(next(search_query))
    publications = [pub['bib']['title'] for pub in author['publications']]
    return publications

def rateMyProfessor(input=" "):
    professor = ratemyprofessor.get_professor_by_school_and_name(
        ratemyprofessor.get_school_by_name("University of Michigan-Dearborn"), input)
    
    if professor is not None:
        would_take_again = f"{round(professor.would_take_again, 1)}%" if professor.would_take_again is not None else "N/A"
        context = (
            f"{professor.name} works in the {professor.department} Department of {professor.school.name}. "
            f"Rating: {professor.rating} / 5.0. "
            f"Difficulty: {professor.difficulty} / 5.0. "
            f"Total Ratings: {professor.num_ratings}. "
            f"Would Take Again: {would_take_again}"
        )
    else:
        context = "Professor not found."
    
    return context

  


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
    ),
        Tool(
        name = "Rate My Professor",
        func = rateMyProfessor,
        description="Use this when the student asks for the rating or quality of the Professor's teaching. Pass in the Professor's name as input into the function."
    ),
    Tool(
        name = "Google Scholar Search",
        func = google_scholar_search,
        description = "Useful for when you need to find research and publications from a professor but only when the University of Michigan Faculty and Course QA system could not answer the query. Pass in the Professor's name as input into the function."
    ),
]
    
prefix = """You are a helpful AI assistant having a conversation with a a student. Your objective is answer their questions about University of Michigan's Dearborn
Web Technology class and provide feedback on their work. If you do not know the answer to a question, take your best educated guess and simply tell them you are unsure about your answer. You have access to the following tools:"""

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
        agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True,memory=memory, handle_parsing_errors=True)
        
        #Session state chain
        cl.user_session.set("llm_chain", agent_chain)
    except Exception as e:
        print("An error occurred in the on_chat_start function:")
        traceback.print_exc()
    
    
@cl.on_message
async def main(message: cl.Message):
    
    ## Message sent by the user has nothing attached
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
        
    ## Message sent by user has something attached
    if message.elements:
        
        images = [file for file in message.elements if "image" in file.mime]
        pdfs = [file for file in message.elements if "pdf" in file.mime]

        if images:
          print(" images yes")
          
        if pdfs:
            print("pdf yes")
            
            
        

   