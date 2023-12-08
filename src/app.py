import chainlit as cl
from chainlit import user_session
from chainlit import AskUserMessage, Message, on_chat_start, on_message
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain, LLMMathChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.tools import BaseTool
from langchain.utilities import SerpAPIWrapper
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import chainlit as cl
import ratemyprofessor
from scholarly import scholarly


os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""

# Directories that contain the chroma databases
courses_dir = 'um_dearborn_courses'
faculty_dir = 'um_dearborn_faculty'
research_dir = 'um_dearborn_research'
embedding = OpenAIEmbeddings()

# Directories that contain
coursedb = Chroma(persist_directory=courses_dir, embedding_function = embedding)
course_retriever = coursedb.as_retriever(search_kwargs={"k":50})
course_retriever.search_type= 'similarity'

facultydb = Chroma(persist_directory=faculty_dir, embedding_function = embedding)
faculty_retriever = facultydb.as_retriever(search_kwargs={"k":50})
faculty_retriever.search_type= 'similarity'

researchdb = Chroma(persist_directory=research_dir, embedding_function = embedding)
research_retriever = researchdb.as_retriever(search_kwargs={"k":50})
research_retriever.search_type= 'similarity'

# OpenAI Model Settings
llm = ChatOpenAI(temperature=0.5, model = "gpt-4-1106-preview", streaming=True)

# Chat Memory
memory = ConversationBufferMemory(memory_key="chat_history")
readonly = ReadOnlySharedMemory(memory=memory)

# Chains
course_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=course_retriever, memory=readonly)
faculty_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=faculty_retriever, memory=readonly)
research_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=research_retriever, memory=readonly)
search = SerpAPIWrapper()

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
        name = "University of Michigan Course QA system",
        func = course_qa.run,
        description = "Useful for when you need to answer questions University of Michigan-Dearborn courses. Input should be fully formed question/"
    ),
     Tool (
        name = "University of Michigan Faculty Information QA system",
        func = faculty_qa.run,
        description = "Useful for when you need to answer questions about faculty. It should also be able to answer question about professor contact information and interests. Input should be fully formed question/"
    ),
    Tool (
        name = "University of Michigan Faculty Research QA system",
        func = research_qa.run,
        description = "Useful for when you need to answer questions about publications from University of Michigan Dearborn faculty. Input should be a fully formed question/"
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
faculty and courses. If you do not know the answer to a question, take your best educated guess and simply tell them you are unsure about your answer. You have access to the following tools:"""

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
    # Chain for the user session
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True,memory=memory, handle_parsing_errors=True)
    
    #Session state chain
    cl.user_session.set("llm_chain", agent_chain)
    
    
@cl.on_message
async def main(message: cl.Message):
    answer_prefix_tokens=["FINAL", "ANSWER"]
    content = message.content
    agent_chain = cl.user_session.get("llm_chain")
    res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
    await cl.Message(content=res, author="BlueBot").send()
    



