from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.document import Document
from langchain.document_loaders import UnstructuredURLLoader
from langchain.retrievers import BM25Retriever
from langchain.retrievers.merger_retriever import MergerRetriever
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain.document_loaders import PyPDFLoader
from bs4 import BeautifulSoup
from langchain.text_splitter import TokenTextSplitter
import requests
import re
import tiktoken

from const import OPEN_API_KEY, COHERE_API_KEY, prompt_template

# import frontend
#import webapp_demo
import os
#print(os.getcwd())
# RetrievalQA object containing chat memory
# Use create_retrievalqa() to un-null this
qa_with_memory = None

def combine_chunks(chunks, max_tokens, model="gpt-3.5-turbo"):
    """
    Combine chunks by token count

    Note: This does not handle the case where the chunks provided already contain too many tokens
    Note: This currently only works for OpenAI models because it uses tiktoken to count tokens
    :param chunks: list containing text chunks
    :param max_tokens: max number of tokens in a chunk
    :param model: GPT model being used
    :return: list of combined text chunks
    """
    encoder = tiktoken.encoding_for_model(model)
    # count the number of tokens in each chunk
    num_tokens = [len(encoder.encode(chunk)) for chunk in chunks]
    # this will contain the combined chunks
    combined_chunks = []
    # this will hold the length of the chunk being combined
    combined_chunk_length = 0
    # this will be the combined chunk
    combined_chunk = ""
    for i in range(len(num_tokens)):
        combined_chunk_length += num_tokens[i]
        combined_chunk += chunks[i]
        if i < len(num_tokens) - 1:
            next_chunk_length = num_tokens[i + 1]
            # if combining the next chunk would go over the max token limit, then start a new combined chunk
            if combined_chunk_length + next_chunk_length > max_tokens:
                combined_chunks.append(combined_chunk)
                combined_chunk_length = 0
                combined_chunk = ""
        else:
            # the chunk at the end needs to be handled
            combined_chunks.append(chunks[i])

    return combined_chunks

def create_retrievalqa(file_path: str) -> RetrievalQA.from_chain_type:
    '''
    [documentation]
    '''
    
    #webapp_demo.send_to_frontend(my_query)
    #print(my_query)
    
    # Read the contents of the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        formatted_nsf = file.read()

    # Split by double newlines (This is the contextual split)
    chunks = formatted_nsf.split('\n\n')
    
    max_size = 2000
    chunks = [Document(page_content=chunk) for chunk in combine_chunks(chunks, max_size)]

    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
    db = Chroma.from_documents(chunks, embeddings)
    
    # limit number of chunks passed to avoid passing token limit
    search = len(chunks)
    while (search*2)*max_size > 16000:
        search -= 1
    #print(search)
    semantic_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": search})
    bm25_retriever = BM25Retriever.from_documents(chunks, k=search)
    merged_retriever = MergerRetriever(retrievers=[semantic_retriever, bm25_retriever])
    """
    compressor = CohereRerank(top_n=3)
    # it will use the compress the output of the merged retriever to only 3 docs
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=merged_retriever)
    """
    
    model_name = 'gpt-3.5-turbo-16k'
    #model_name = "gpt-4-32k"  # ChatGPT
    #
    # CHANGE AMOUNT OF CHUNKS IF TOKENS EXCEED LIMIT
    #
    llm = ChatOpenAI(openai_api_key=OPEN_API_KEY, model_name=model_name)

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question", "chat_history"]
    )

    chain_type_kwargs = {"prompt": PROMPT, "memory": ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question")}
    # k is the number of relevant text chunks to return
    qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 chain_type_kwargs=chain_type_kwargs,
                                 retriever=merged_retriever)
    
    #answer = str(qa.run(my_query))
    #print(answer)
    
    #webapp_demo.send_to_frontend(answer)
    global qa_with_memory
    qa_with_memory = qa
    
def main_driver(my_query):
    
    #print(os.getcwd())
    file_path = './src/temp/formatted_nsf.txt'
    #print(os.path.abspath(file_path))
    
    #my_query = "Who can be PI on this proposal and is there a limit to how many I can have?"

    #os.system('streamlit run Home.py')
    #if qa_with_memory == None:
    #    create_retrievalqa(file_path, my_query)
    
    return str(qa_with_memory.run(my_query))

    #my_query = "What happens if I exceed this limit?"


    # this is random and funny so let's keep it
    print('PyCharm')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/

if __name__ == '__main__':
    
    file_path = './formatted_nsf.txt'
    prompt_template = """
    <CONTEXT START>
    {context}
    <CONTEXT END>
    
    Chat History:
    {chat_history}
    
    You are an expert in NSF grant proposals and are tasked with answering questions about opportunities to receive an NSF grant. The context above contains portions of the NSF proposal guidelines. Using the context and chat history provided above, try to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. You are allowed to change the language of the response if doing so will make the response more clear and as long as the underlying meaning or facts do not change.
    Question: {question}
    """
    my_query = "Who can be PI on this proposal and is there a limit to how many I can have?"

    os.system('streamlit run ChatMode.py')
    create_retrievalqa(file_path)

    #my_query = "What happens if I exceed this limit?"


    # this is random and funny so let's keep it
    print('PyCharm')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
