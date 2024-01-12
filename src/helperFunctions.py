#Author: Larnell Moore
#Creation Date: December 26, 2023
#Date Modified: Jan 11, 2023
#Purpose: This file runs the chainlit client and allows the user to interact with the model.
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from feedbackModel import FeedbackAgent
from w3c_validator import validate
import tempfile
import traceback
import os

def createRetrievalChains(llm, memory):
    """
    Precondition: There exists a 'db' directory with folders representing the checkpoint. Each of these checkpoint folders
    must contain one 'chroma.sqlite3' file.
    Postcondition: Returns a dict where the key is the folder name, and the value is the corresponding RetrievalQA object.
    Purpose: Iterate through all subdirectories in the 'db' directory, create retrievers for each one, 
    and ensure the folder contains at least one 'chroma.sqlite3' file.
    """
    db_dir = 'db'
    embedding = OpenAIEmbeddings()
    retriever_dict = {}

    for dir_name in os.listdir(db_dir):
        dir_path = os.path.join(db_dir, dir_name)
        if os.path.isdir(dir_path):
            files = os.listdir(dir_path)
            chroma_files = [file for file in files if file == 'chroma.sqlite3']
            if chroma_files:
                db = Chroma(persist_directory=dir_path, embedding_function=embedding)
                retriever = db.as_retriever(search_kwargs={"k": 50})
                retriever.search_type = 'similarity'
                retriever_dict[dir_name] = (RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, memory=memory))
            else:
                raise Exception(f"Folder '{dir_name}' does not contain a 'chroma.sqlite3' file.")

    if not retriever_dict:
        raise Exception("No valid folders found in 'db' directory.")

    return retriever_dict

def dummy_func(*args, **kwargs):
    # This function might log the query, send it to the LLM, or just do nothing.
    pass

def html_feedback(input=" "):
    print(input)
    FB = FeedbackAgent()
    response = FB.chat(input)
    return response

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





