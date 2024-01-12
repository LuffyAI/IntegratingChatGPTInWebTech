from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory, ReadOnlySharedMemory
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from helperFunctions import createRetrievalChains, dummy_func, html_feedback, html_validation
from dotenv import load_dotenv

class RAGAgent:
    def __init__(self):
        load_dotenv()

        # Model
        self.llm = ChatOpenAI(temperature=0.5, model="gpt-4-1106-preview", streaming=True)

        # Memory
        self.memory = ConversationTokenBufferMemory(memory_key="chat_history", llm=self.llm, max_token_limit=1000)
        self.readonly = ReadOnlySharedMemory(memory=self.memory)

        # Tools
        retrievalChains = createRetrievalChains(self.llm, self.memory)

        self.tools = [
            Tool(
                name="Web Technology project proposal and feedback",
                func=retrievalChains['checkpoint1'].run,
                description="Useful for when you need to answer questions about Checkpoint1. Input should be fully formed question."
            ),
            Tool(
                name="University of Michigan Faculty Information QA system",
                func=retrievalChains['checkpoint2'].run,
                description="Useful for when you need to answer questions about Checkpoint2."
            ),
            Tool(
                name="University of Michigan Faculty Research QA system",
                func=retrievalChains['checkpoint3'].run,
                description="Useful for when you need to answer questions about checkpoint3."
            ),
            Tool(
                name = "General LLM Query",
                func = dummy_func,
                description="Useful for answering general questions not related to the University of Michigan-Dearborn. This tool does not have a specific function and sends queries directly to the LLM for a wide range of topics and inquiries."
            ),
            Tool(
                name = "Code Analysis",
                func = html_feedback,
                description="Useful for when you the user asks to analyze code or provide code. Pass in the code or file uploaded to the user as input. The input is sent to be a finetuned GPT 3.5 model, so be mindful of its token count."
            ),
             Tool(
                name = "HTML code validation using W3C",
                func = html_validation,
                description="Use full for answering code smell detection and code vulnerabilities and syntax errors of html code"
            )
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
        return self.chain.arun(input_text,callbacks)
    
    def chat(self, input_text):
        return self.chain.run(input_text)


