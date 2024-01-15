# Author: Larnell Moore
# Creation Date: December 26, 2023
# Date Modified: Jan 14, 2024
# Purpose: This file defines the RAGAgent class, which acts as the primary Large Language Model (LLM) agent in this project. 
# The RAGAgent class is responsible for understanding the user's request and choosing the appropriate functionality to 
# to gather external knowledge, enhancing the quality of its answers. It retrieves additional context from vector databases and/or LangChain tools.
# Through Retrieval Augmented Generation (RAG), it allows the agent to better understand the user's queries without fully relying on its
# pretrained internal knowledge. 
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory, ReadOnlySharedMemory
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from RagTools import createRetrievalChains, dummy_func, finetuned_feedback, html_validation, getFileUploadInfo,php_code_sniffer, php_code_beautifier, php_code_fixer, lint_sql, getImageInfo, color_theory_analysis
from dotenv import load_dotenv

class RAGAgent:
    def __init__(self):
        
        # Loads the OpenAI API key from .env file
        load_dotenv()

        # Model
        self.llm = ChatOpenAI(temperature=0.5, model="gpt-4-1106-preview", streaming=True)

        # Memory
        self.memory = ConversationTokenBufferMemory(memory_key="chat_history", llm=self.llm, max_token_limit=1000)
        self.readonly = ReadOnlySharedMemory(memory=self.memory)

        # Establishes Retrieval Chains with the vector databases that contain external knowledge about
        # the Web Technology course
        retrievalChains = createRetrievalChains(self.llm, self.memory)
        
        # Tools
        self.tools = [
            Tool(
               name = "Did the user upload a file?",
               func = getFileUploadInfo,
               description = "Checks if the user uploaded a file for examination. If it returns (file_ext, file_name), then tell the user to upload a file if they wish to proceed." 
            ),
             Tool(
               name = "Did the user upload a picture?",
               func = getImageInfo,
               description = "Checks if the user uploaded a picture for examination. If it returns (file_ext, file_name), then tell the user to upload an image if they wish to proceed." 
            ),
            Tool(
                name="Checkpoint 1: Web Technology Project Proposal",
                func=retrievalChains['checkpoint1'].run,
                description="Useful for when you need to answer questions about Checkpoint1. Input should be fully formed question."
            ),
            Tool(
                name="Checkpoint 2: HTML Pages",
                func=retrievalChains['checkpoint2'].run,
                description="Useful for when you need to answer questions about Checkpoint2."
            ),
            Tool(
                name="Checkpoint 3: Database Design",
                func=retrievalChains['checkpoint3'].run,
                description="Useful for when you need to answer questions about checkpoint3."
            ),
            Tool(
                name = "Code Feedback",
                func = finetuned_feedback,
                description="Useful for when the user asks for feedback or code analysis. First check if they uploaded a programming file. If so, pass in the name of the file as input. Else, tell them to upload a file."
            ),
              Tool(
                name = "Color Theory Analysis",
                func = color_theory_analysis,
                description="Useful for when the user uploads a picture. First check if they uploaded an image. If so, pass in their specific color theory request into the function. If no request is made, pass in 'Please provide a color theory analysis on my website and offer suggestions'."
            ),
             Tool(
                name = "W3C HTML Code Validator",
                func = html_validation,
                description="Useful for identifying code smell detection, vulnerabilities, and syntax errors in html code. First check if they uploaded a html file. If so, pass in the name of the file as input. Else, tell them to upload a HTML file."
            ),
            Tool(
                name = "PHP Code Validator",
                func = php_code_sniffer,
                description="Useful for identifying code smell detection, vulnerabilities, and syntax errors in html code. First check if they uploaded a PHP file. If so, pass in the name of the file as input. Else, tell them to upload a PHP file and pass in none."
            ),
             Tool(
                name = "PHP Code Fixer",
                func = php_code_fixer,
                description="Useful for fixing issues in a PHP file to ensure it adheres to coding standards. First check if they uploaded a PHP file. If so, pass in the name of the file as input. Else, tell them to upload a PHP file and pass in none."
            ),
            Tool(
                name = "PHP Code Beautifier",
                func = php_code_beautifier,
                description="Useful for beautifying php code. First check if they uploaded a PHP file. If so, pass in the name of the file as input. Else, tell them to upload a PHP file and pass in none."
            ),
             Tool(
                name = "SQL Validator",
                func = lint_sql,
                description="Useful when the user asks to validate SQL code. First check if they uploaded a SQL file. If so, pass in the name of the file as input. Else, tell them to upload a SQL file and pass in none."
            ),
            Tool(
                name = "General LLM Query",
                func = dummy_func,
                description="Useful for answering general questions not related to the University of Michigan-Dearborn. This tool does not have a specific function and sends queries directly to the LLM for a wide range of topics and inquiries."
            ),
            
        ]

        # Prefix and Suffix
        self.prefix = """You are a helpful AI assistant having a conversation with a student. Your objective is to answer their questions about the University of Michigan's Dearborn Web Technology class and provide feedback on their work. If you do not know the answer to a question, take your best-educated guess and simply tell them you are unsure about your answer. You have access to the following tools:"""
        self.suffix = """Begin!"
        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        # Prompt
        self.prompt = ZeroShotAgent.create_prompt(
            self.tools,
            prefix=self.prefix,
            suffix=self.suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"]
        )

        # LLM Chain and Agent
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        self.agent = ZeroShotAgent(llm_chain=self.llm_chain, tools=self.tools, verbose=True)
        self.chain = AgentExecutor.from_agent_and_tools(agent=self.agent, tools=self.tools, verbose=True, memory=self.memory, handle_parsing_errors=True)

    async def asyncChat(self, input_text, callbacks):
        """Given a prompt from the user, it asynchronously invokes the RAGAgent's chain."""
        try:
         return self.chain.arun(input_text,callbacks)
        except Exception as e:
           return "An error occurred communicating with the RAGAgent in asyncChat function:" + str(e)
    
    def chat(self, input_text):
        """Given a prompt from the user, it synchronously invokes the RAGAgent's chain."""
        try:
         return self.chain.run(input_text)
        except Exception as e:
           return "An error occurred communicating with the RAGAgent in the chat function:" + str(e)


