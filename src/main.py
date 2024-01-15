# Authors: Larnell Moore and Venkata Alekhya Kusam
# Creation Date: December 26, 2023
# Date Modified: Jan 14, 2024
# Purpose: This file runs the chainlit client and allows the user to interact with the LLM Agent.
from ConversationFlowMemory import ConversationFlowMemory
import chainlit as cl
from RAGAgent import RAGAgent
import traceback
from io import BytesIO
import pdfplumber
from RagTools import sendFile, setFile, setImage
from UIHelper import setProfilePictureViaPath, setProfilePictureViaURL, isFileValid, convertScriptToString

## Conversational Flow Memory
conversation_memory = ConversationFlowMemory()

## Variables to keep track of the names assigned to AI Assistant and user
AI_ASSISTANT_NAME = "Web Tech"
STUDENT_NAME = "User"

## ERROR MESSAGES
UNKNOWN_ERROR = "Oops, something went wrong. Could you please try again?"
FILE_ERROR = lambda ext: f"I encountered an issue processing the {ext.upper()}. Could you please try again?"

@cl.on_chat_start
async def main(): 
    """Defines a hook that is called when a new chat session is created."""
    session_id = cl.user_session.get(id)
    conversation_memory.update_conversation(session_id, "Session started")
    
    ## Profile Pictures for the AI Assistant and User
    await cl.Avatar(**setProfilePictureViaPath(name=AI_ASSISTANT_NAME)).send()
    await cl.Avatar(**setProfilePictureViaURL(name=STUDENT_NAME)).send()
    try:
        ## Initializes the main LLM Agent used throughout the program
        LLMAgent = RAGAgent()
        cl.user_session.set("llm_chain", LLMAgent.chain)
    except Exception as e:
        print("An error occurred in the on_chat_start function:")
        traceback.print_exc()
        

@cl.on_message
async def main(message: cl.Message):
    """Defines a hook that is called when a new message is received from the user."""
    session_id = cl.user_session.get(id)
    content = message.content
    conversation_memory.update_conversation(session_id, content)
            
    ## Retrieves a response intro and prefix for the upcoming message
    response_intro = conversation_memory.selectResponseStarter()
    response_prefix = conversation_memory.personalizeResponseStyle(session_id)

    ## Invoked when the message sent by the user has nothing attached
    if not message.elements:
        answer_prefix_tokens=["FINAL", "ANSWER"]
        try:
            content = response_intro + " " + response_prefix + content
            agent_chain = cl.user_session.get("llm_chain")
            res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
            if sendFile() is not None:
               newFileName, newFileContent = sendFile()
               attachment = [cl.Text(name=newFileName, content= newFileContent, language="php", display = "inline")]
               await cl.Message(content=res, author=AI_ASSISTANT_NAME, elements=attachment).send()  
               setFile()
            else:
             await cl.Message(content=res, author=AI_ASSISTANT_NAME).send()
        except Exception as e:
            await cl.Message(content=UNKNOWN_ERROR, author=AI_ASSISTANT_NAME).send()
            print("An error occurred while processing a message with nothing attached:", e)

    ## Invoked when message sent by the user has something attached
    if message.elements is not None:
     try:
        images, pdfs, html, sql ,php, pdfs = await isFileValid(message)
        answer_prefix_tokens=["FINAL", "ANSWER"]
        
        ## User uploaded an SQL file.
        if sql:
            try:
              combined_sql = await convertScriptToString(message, sql, "sql")
              agent_chain = cl.user_session.get("llm_chain")
              content = response_intro + " " + response_prefix + content + '\n' + combined_sql
              res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
              if sendFile() == None:
               await cl.Message(content=res, author=AI_ASSISTANT_NAME).send()
              else:
               newFileName, newFileContent = sendFile()
               attachment = [cl.Text(name=newFileName, content= newFileContent, language="sql", display = "inline")]
               await cl.Message(content=res, author=AI_ASSISTANT_NAME, elements=attachment).send()  
               setFile()
            except Exception as e:
                await cl.Message(content=FILE_ERROR("sql"), author=AI_ASSISTANT_NAME).send()
                print("An error occurred while processing an SQL File:", e)
        
        ## User uploaded a php file.
        if php:
            try:
              combined_php = await convertScriptToString(message, php, "php")
              agent_chain = cl.user_session.get("llm_chain")
              content = response_intro + " " + response_prefix + content + '\n' + combined_php
              res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
              if sendFile() == None:
               await cl.Message(content=res, author=AI_ASSISTANT_NAME).send()
              else:
               newFileName, newFileContent = sendFile()
               attachment = [cl.Text(name=newFileName, content= newFileContent, language="php", display = "inline")]
               await cl.Message(content=res, author=AI_ASSISTANT_NAME, elements=attachment).send()  
               setFile()
            except Exception as e:
                await cl.Message(content=FILE_ERROR("php"), author=AI_ASSISTANT_NAME).send()
                print("An error occurred while processing a php file:", e)
        
        ## User uploaded an image.
        if images:
            try:
             get_extension = lambda file_name: file_name.split('.')[-1] if '.' in file_name else ''
             file_name, file_content = message.elements[0].name, message.elements[0].content,
             setImage(file_name,get_extension(file_name), file_content)
             agent_chain = cl.user_session.get("llm_chain")
             res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
             await cl.Message(content=res, author="Web Tech").send() 
            except Exception as e:
                await cl.Message(content=FILE_ERROR("png/jpg/etc."), author=AI_ASSISTANT_NAME).send()
                print("An error occurred while processing an image:", e)
        
        ## User uploaded a pdf.
        if pdfs:
            file_name = message.elements[0].name
            try:
                for pdf_file in pdfs:
                    if hasattr(pdf_file, 'content'): 
                        with BytesIO(pdf_file.content) as pdf_buffer:
                            with pdfplumber.open(pdf_buffer) as pdf:
                                pdf_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
                        content = response_intro + " " + response_prefix + content + '\n' + pdf_text
                    else:
                        print(f"Unsupported PDF file type or missing content: {type(pdf_file)}")
                        continue
                agent_chain = cl.user_session.get("llm_chain")
                res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
                await cl.Message(content=res, author="Web Tech").send()
            except Exception as e:
                await cl.Message(content=FILE_ERROR("pdf"), author=AI_ASSISTANT_NAME).send()
                print("An error occurred while processing a pdf:", e)
        
        ## User uploaded a html file. 
        if html:
            try:
              combined_html = await convertScriptToString(message, html, "html")
              agent_chain = cl.user_session.get("llm_chain")
              content = response_intro + " " + response_prefix + content + '\n' + combined_html
              res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
              await cl.Message(content=res, author="Web Tech").send()
            except Exception as e:
                await cl.Message(content=FILE_ERROR("html"), author=AI_ASSISTANT_NAME).send()
                print("An error occurred while processing a HTML file:", e)
     except Exception as e:
            await cl.Message(content=UNKNOWN_ERROR, author=AI_ASSISTANT_NAME).send()
            print("An error occurred processing a message with an attachment:", e)