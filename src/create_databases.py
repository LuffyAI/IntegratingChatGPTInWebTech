#Author: Larnell Moore
#Creation Date: December 23, 2023
#Date Modified: December 23, 2023
#Purpose: Reads data from the 'kb' folder (shorthand for knowledge base) and creates chromadb vector databases that are for additional context in the RAG system.
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredPDFLoader,UnstructuredHTMLLoader
from langchain.document_loaders import DirectoryLoader
import pdf2image
import pdfminer


print("Creating VectorDatabases...")
load_dotenv('.env')

c1_dir =  ('db/checkpoint1', 'kb/checkpoint1')
c2_dir =  ('db/checkpoint2', 'kb/checkpoint2')
c3_dir =  ('db/checkpoint3', 'kb/checkpoint3')
c4_dir =  ('db/checkpoint4', 'kb/checkpoint4')
c5_dir =  ('db/checkpoint5', 'kb/checkpoint5')
c1_f23_dir = ('db/checkpoint1_f23', 'kb/checkpoint1_f23')
databases = [c1_dir, c2_dir, c3_dir, c4_dir, c5_dir, c1_f23_dir]

def createNewDB(db_dir, pdf_dir):
    """Scraps Information from given pdfs in the knowledgebase and transforms it into OpenAI Embeddings, storing them in a VectorDB."""
    loader = DirectoryLoader(pdf_dir, glob="./*.pdf", loader_cls=UnstructuredPDFLoader)
    documents = loader.load()
    if not documents:
        print(f"No documents found in {pdf_dir}. Skipping.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    if not texts:
        print(f"No texts extracted from documents in {pdf_dir}. Skipping.")
        return

    dir = db_dir
    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=dir)
    if vectordb is None:
        print(f"Failed to create VectorDB for {pdf_dir}.")
        return

    vectordb.persist()
    print("vector db created")
    vectordb = None

for db in databases:
    createNewDB(db[0], db[1])

    
print("JOB FINISHED!")
