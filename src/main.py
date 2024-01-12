#Author: Larnell Moore
#Creation Date: December 26, 2023
#Date Modified: Jan 11, 2023
#Purpose: This file runs the chainlit client and allows the user to interact with the model.
from ConversationFlowMemory import ConversationFlowMemory
import chainlit as cl
from RAGAgent import RAGAgent
import traceback
import random
from io import BytesIO
import pdfplumber
from bs4 import BeautifulSoup
from helperFunctions import set_prevUpload

conversation_memory = ConversationFlowMemory()

@cl.on_chat_start
async def main(): 
    session_id = cl.user_session.get(id)
    conversation_memory.update_conversation(session_id, "Session started")
    try:
        LLMAgent = RAGAgent()
        
        # Session state chain
        cl.user_session.set("llm_chain", LLMAgent.chain)
    except Exception as e:
        print("An error occurred in the on_chat_start function:")
        traceback.print_exc()
        

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
            combined_html = ""
            try:
              for html_file in html:
                if hasattr(html_file, 'content'):  # If the HTML content is provided as bytes
                  html_content = html_file.content.decode()
                  combined_html += html_content + '\n'
                  set_prevUpload(combined_html)
                else:
                 print(f"Unsupported HTML file type or missing content: {type(html_file)}")
              print(combined_html)
              answer_prefix_tokens = ["FINAL", "ANSWER"]
              agent_chain = cl.user_session.get("llm_chain")
              content = response_intro + " " + response_prefix + content + '\n' + combined_html
              res = await agent_chain.arun(content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=answer_prefix_tokens)])
              await cl.Message(content=res, author="BlueBot").send()
            except Exception as e:
                friendly_message = "I encountered an issue processing the html. Could you please try again?"
                await cl.Message(content=friendly_message, author="BlueBot").send()
                print("An error occurred in the on_message function:", e)