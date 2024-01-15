# Author: Larnell Moore
# Creation Date: December 26, 2023
# Date Modified: Jan 14, 2024
# Purpose: This file contains the implementation of each the tools the RagAgent can invoke. Moreover, it also contains
# the implementation of helper functions associated with file and vector database management.
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from feedbackModel import FeedbackAgent
from FileUpload import FileUpload
from w3c_validator import validate
import tempfile
import tiktoken
import os
import subprocess
import shlex
from PIL import Image
import io
from ColorTheoryAgent import ColorAgent

############################################
#              File Management             #
############################################
# Class that manages the files uploaded by the user or AI
USER_UPLOAD = FileUpload()

def setFileUpload(name, ext, content):
    """Saves the most recent SQL, PHP, or HTML file saved by the user"""
    global USER_UPLOAD
    try:
     USER_UPLOAD.set_prevUpload(name,ext,content)
    except Exception as e:
     raise "An error occurred while saving the file uploaded by the user in setFileUpload:" + str(e)
    
def setImage(name, ext, content):
    """Saves the most recent image file saved by the user"""
    global USER_UPLOAD
    try:
     USER_UPLOAD.image = (name, ext, content)
    except Exception as e:
      raise "An error occurred while saving the image uploaded by the user in setImage:" + str(e)
    
def sendFile():
    """Returns the most recent SQL, PHP, or HTML code written by the AI"""
    try:
     return (USER_UPLOAD.sendFile)
    except Exception as e:
     return "No recent SQL, PHP, or HTML has been found in the sendFile() function. " + str(e)

def setFile():
    """Sets USER_UPLOAD.send file to indicate the AI currently has no files it needs to send."""
    global USER_UPLOAD
    USER_UPLOAD.sendFile = None

def createRetrievalChains(llm, memory):
    """
    Creates a retrieval chain with all the vector databases stored in the 'db' folder
    Precondition: There exists a 'db' directory with folders representing the checkpoint. Each of these checkpoint folders
    must contain one 'chroma.sqlite3' file.
    Postcondition: Returns a dict where the key is the folder name, and the value is the corresponding RetrievalQA object.
    """
    db_dir = 'db'
    embedding = OpenAIEmbeddings()
    retriever_dict = {}
    
    try:
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
    except Exception as e:
         raise Exception("An error occurred creating the vector database retrieval chains", e)

    if not retriever_dict:
        raise Exception("No valid folders found in 'db' directory.")

    return retriever_dict

############################################
#              RAG TOOLS                   #
############################################

def dummy_func(*args, **kwargs):
    """Simple function that does nothing. This allows the LLM use GPT-4's internal knowledge for questions 
    that cannot be solved with the external data in this project"""
    pass

def getFileUploadInfo(input = " "):
    """Returns the name and extension of the previous upload (sql, php, html) made by the user to the
    RAG Agent, so it can identify if the requested action is possible.
    """
    global USER_UPLOAD
    try:
     return (USER_UPLOAD.prevUpload[0],USER_UPLOAD.prevUpload[1])
    except:
     return "The user did not upload any code. Check getImageInfo if their request is related to an image."

def getImageInfo(input = " "):
    """Returns the previous upload made by the user (png, jpg, .etc) to the RAG Agent, so it can identify if the requested action is possible."""
    global USER_UPLOAD
    try:
     return (USER_UPLOAD.image[0],USER_UPLOAD.image[1])
    except:
     return "The user did not upload any image. If their request relates to code, check getFileUploadInfo."

def finetuned_feedback(input = " "):
    """Prompts a GPT 3.5 Turbo model finetuned on previous semester TA feedback to provide
    feedback on the user's HTML code. Returns its response."""
    global USER_UPLOAD
    if USER_UPLOAD.didUserUploadFile() == False:
        return "User must upload the code snippet through the Chainlit UI. Please tell them to upload a file first."
    
    try:
            input = USER_UPLOAD.prevUpload[2]
            MAX_TOKENS = 1000
            
            # Calculate the token count of the input to ensure the GPT 3.5-turbo context window of 4096 tokens can process it.
            input_token_count = count_tokens(input)
            
            if input_token_count <= MAX_TOKENS:
                # If the input is within the limit, send it for feedback.
                FB = FeedbackAgent()
                response = FB.chat("Please provide feedback and suggestions: " + input)
                return response
            else:
                # If the input is not within the limit, chunk the input into individual slices
                # and send them individually.
                HTML_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.HTML, chunk_size=1000, chunk_overlap=100)
                HTML_CHUNKS = HTML_splitter.split_text(input)
                
                # Send each chunk for feedback and accumulate the responses
                accumulated_response = ""
                
                # Creates temp buffer memory to remember previous code segments
                FB = FeedbackAgent()
                for chunk in HTML_CHUNKS:
                        FB = FeedbackAgent()
                        response = FB.chat("Please provide feedback and suggestions: " + chunk)
                        accumulated_response += "\n" + response
                return accumulated_response
    except Exception as e:
        return "An issue occurred communicating with the Feedback Agent " + str(e)


def html_validation(input= " "):
    """Validates HTML code using the W3C HTML Code Validator"""
    global USER_UPLOAD
    
    if USER_UPLOAD.didUserUploadFile() == False:
         return "User must upload the code snippet through the Chainlit UI. Please tell them to upload a file first."

    input = USER_UPLOAD.prevUpload[2]
    results = []
    
    try:
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
    except Exception as e:
        return "An issue occurred while using the html_validation function:  " + str(e)


def php_code_sniffer(input= " ", standard='PSR2'):
    """Validates PHP code using the php code sniffer through the client's terminal"""
    global USER_UPLOAD
    
    if USER_UPLOAD.didUserUploadFile() == False:
        return "User must upload the code snippet through the Chainlit UI"
    
    try:
        input = USER_UPLOAD.prevUpload[2]
        
        # Save the PHP code to a temporary file
        with open('temp_php_file.php', 'w') as temp_file:
            temp_file.write(input)

        # Run PHP CodeSniffer command
        cmd = ['phpcs', '--standard=' + standard, 'temp_php_file.php']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Delete the temporary PHP file
        subprocess.run(['rm', 'temp_php_file.php'])

        # Capture both standard output and error
        output_message = result.stdout + result.stderr 

        if result.returncode == 0:
            return True, "PHP code follows coding standards", output_message
        else:
            error_message = result.stderr
            return False, error_message, output_message
    except Exception as e:
        return False, "An issse occurred while attempting to use the PHPCS on the user's machine", str(e)
    
    
def php_code_beautifier(input=" ", standard='PSR2'):
    """Runs the phpcbf code beautifier command through the terminal. Returns its output."""
    global USER_UPLOAD
    
    if not USER_UPLOAD.didUserUploadFile():
        return "User must upload the code snippet through the Chainlit UI"
    
    try:
        input = USER_UPLOAD.prevUpload[2]
        # Save the PHP code to a temporary file
        with open('temp_php_file.php', 'w') as temp_file:
            temp_file.write(input)

        # Run PHP Code Beautifier
        cmd = ['phpcbf', '--standard=' + standard, 'temp_php_file.php']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the beautified code
        with open('temp_php_file.php', 'r') as beautified_file:
            beautified_code = beautified_file.read()
        
        # Sets the AI file-to-send as the beautified code
        # The fixed code will appear to the user through Chainlit with the title aifix.
        USER_UPLOAD.sendFile = ("aifix", beautified_code)

        # Delete the temporary PHP file
        subprocess.run(['rm', 'temp_php_file.php'])

        # Check if errors were fixed
        if "ERRORS WERE FIXED" in result.stdout:
            return True, "PHP code successfully beautified"
        else:
            error_message = result.stderr
            return False, error_message
    except Exception as e:
        return False, "There was an error on the user's machine attempting to use the PHPCBF Code beautifier" + str(e)
        


def php_code_fixer(input=" ", standard='PSR2'):
    """Runs the phpcbf code fixer command through the terminal. Returns its output."""
    global USER_UPLOAD
    
    if not USER_UPLOAD.didUserUploadFile():
        return "User must upload the code snippet through the Chainlit UI"
    
    try:
        input = USER_UPLOAD.prevUpload[2]
        
        # Save the PHP code to a temporary file
        with open('temp_php_file.php', 'w') as temp_file:
            temp_file.write(input)

        # Run phpcbf code fixer
        cmd = ['phpcbf', '--standard=' + standard, 'temp_php_file.php']
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Re-run PHP CodeSniffer to see if the applied fixes worked
        cmd = ['phpcs', '--standard=' + standard, 'temp_php_file.php']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the fixed code
        with open('temp_php_file.php', 'r') as fixed_file:
            fixed_code = fixed_file.read()
        
        # Sets the AI file-to-send as the fixed code
        # The fixed code will appear to the user through Chainlit with the title aifix.
        USER_UPLOAD.sendFile = ("aifix",fixed_code)
        
        # Delete the temporary PHP file
        subprocess.run(['rm', 'temp_php_file.php'])

        if result.returncode == 0:
            return True, "PHP code successfully fixed"
        else:
            error_message = result.stderr
            return False, error_message
    except Exception as e:
         return False, "There was an error on the user's machine attempting to use the PHPCBF Code Fixer" + str(e)
    
def lint_sql(input= " "):
    """Validates SQL code using lint_sql through the client's terminal"""
    if not USER_UPLOAD.didUserUploadFile():
        return "User must upload the code snippet through the Chainlit UI"
    
    try:
        sql_content = USER_UPLOAD.prevUpload[2]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.sql', mode='w+') as temp_file:
            # Write the SQL content to the temporary file
            temp_file.write(sql_content)
            temp_file_path = temp_file.name

        # Prepare the sqlfluff lint command
        command = f"sqlfluff lint --dialect mysql {temp_file_path}"

        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Delete the temporary file
        os.remove(temp_file_path)

        # Return the output
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
         return "There was an error on the user's machine attempting to use the lint sql application: " + str(e)
        

def color_theory_analysis(input = " "):
    """Prompts a GPT-4 Vision model to perform a color theory analysis. Returns the response of the model."""
    print("AI inputted: ", input)
    
    if USER_UPLOAD.image is None:
        return "User must upload their image through the Chainlit UI"
    
    try:
        # Stores the image bytes
        img_bytes = bytes(USER_UPLOAD.image[2])
        
        # Encodes the image then gives to GPT 4 Vision to perform its color theory analysis.
        CA = ColorAgent()
        encoded = CA.encode_image(img_bytes)
        msg = CA.chat(encoded, input)
        return msg
    except Exception as e:
         return "There was an error with communication to the GPT 4 vision model: " + str(e)
    
############################################
#             RAG HELPERS                  #
############################################
def count_tokens(input):
    """Returns the tokens given a prompt using the gpt-3.5-turbo encoding."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = len(encoding.encode(input))
    return tokens    
