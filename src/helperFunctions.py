#Author: Larnell Moore
#Creation Date: December 26, 2023
#Date Modified: Jan 11, 2023
#Purpose: This file runs the chainlit client and allows the user to interact with the model.
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from feedbackModel import FeedbackAgent
from w3c_validator import validate
import tempfile
import tiktoken
import os
import subprocess

prevUpload="testValue"

def get_prevUpload():
    return prevUpload

def set_prevUpload(new_value):
    global prevUpload
    prevUpload = new_value
    
def estimate_token_count(text):
    # Rough estimation of token count
    return len(text) // 4

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

def finetuned_feedback(input = " "):
    """Chunks the document"""
    input = prevUpload
    MAX_TOKENS = 1000
    # Calculate the token count of the input
    input_token_count = count_tokens(input)
    print("This is the estimated token count" + str(input_token_count))
    
    if input_token_count <= MAX_TOKENS:
        # If the input is within the limit, send it for feedback
        FB = FeedbackAgent()
        response = FB.chat("Please provide code analysis on following code: " + input)
        return response
    else:
       HTML_splitter = RecursiveCharacterTextSplitter.from_language(
       language=Language.HTML, chunk_size=50, chunk_overlap=0)
       HTML_CHUNKS = HTML_splitter.create_documents([input])
       print(HTML_CHUNKS)
       return "Everything looks good"

def count_tokens(input):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = len(encoding.encode(input))
    return tokens

def html_validation(input= " "):
    print("This is what the AI AGENT PASSED INTO THIS FUNCTION:" + input)
    print("prev:" + prevUpload)
    input = prevUpload
    
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


def php_code_sniffer(input= " ", standard='PSR2'):
    print("This is what the AI AGENT PASSED INTO THIS FUNCTION:" + input)
    print("prev:" + prevUpload)
    input = prevUpload
    
    # Save the PHP code to a temporary file
    with open('temp_php_file.php', 'w') as temp_file:
        temp_file.write(input)

    # Run PHP CodeSniffer command
    cmd = ['phpcs', '--standard=' + standard, 'temp_php_file.php']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Delete the temporary PHP file
    subprocess.run(['rm', 'temp_php_file.php'])

    output_message = result.stdout + result.stderr  # Capture both standard output and error

    if result.returncode == 0:
        return True, "PHP code follows coding standards", output_message
    else:
        error_message = result.stderr
        return False, error_message, output_message
    
    

