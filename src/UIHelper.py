
# This file consist of functions that manipulate the Chainlit UI elements and prepare them for usage with other parts of the code.
from RagTools import setFileUpload

def setProfilePictureViaPath(name="WebTechAI", path= "img/umichicon.png"):
  """Returns the **kwargs required to set the profile picture of a user given a path to an image"""
  return {"name": name, "path": path,}

def setProfilePictureViaURL(name="User", url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4"):
  """Returns the **kwargs required to set the profile picture of a user given an URL"""
  return {"name": name, "url": url,}

async def convertScriptToString(message, script, ext):
    """Reads a given SQL, PHP, or HTML file, reads its contents, and return its details in the form of a multi-line string"""
    file_name = message.elements[0].name
    combined_script = ""
    try:
      for script_file in script:
            if hasattr(script_file, 'content'):  
                  script_content = script_file.content.decode()
                  combined_script += script_content + '\n'
                  setFileUpload(file_name, ext, combined_script)
            else:
                 print(f"Unsupported file type or missing content: {type(script_file)}")
    except Exception as e:
        print("An error occurred in the ConvertScriptToString function:", e)
    return combined_script
  
async def isFileValid(message):
    """Verifies the user uploaded a file supported by the program. Only support jpg,png, pdf, html, sql and php."""
    try:
        images = [file for file in message.elements if file.mime and "image" in file.mime]
        pdfs = [file for file in message.elements if file.mime and "pdf" in file.mime]
        html =[file for file in message.elements if file.mime and "html" in file.mime]
        sql =[file for file in message.elements if ".sql" in file.name]
        php = [file for file in message.elements if file.mime and "php" in file.mime]
        
        if ((images or pdfs or html or sql or php) is False):
            raise("Unsupported File Extension uploaded!")
        else:
            return images, pdfs, html, sql ,php, pdfs
    except Exception as e:
            print("An error occurred in the isFileValid function:", e)