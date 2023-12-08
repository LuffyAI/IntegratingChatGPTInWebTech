import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import DirectoryLoader


os.environ["OPENAI_API_KEY"] = ""
print("test")


coursedb_dir = ('um_dearborn_courses', 'html_files/courses_db')
facultydb_dir = ('um_dearborn_faculty', 'html_files/faculty_db')
researchdb_dir = ('um_dearborn_research', 'html_files/research_db')

databases = [coursedb_dir, facultydb_dir, researchdb_dir]


def process_llm_response(llm_response):
    print(llm_response['result'])
    print('\n\nSources: ')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])
    
def createNewDB(db_dir, html_dir):
    loader = DirectoryLoader(html_dir, glob="./*.html", loader_cls=UnstructuredHTMLLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    dir = db_dir
    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, embedding = embedding, persist_directory=dir)
    vectordb.persist()
    vectordb = None
    

for db in databases:
    createNewDB(db[0], db[1])
    
    
print("FINISHED")
