import streamlit as st
import pandas as pd
import numpy as np
from langchain.chains import RetrievalQA

import main

st.title("NSF Proposal Requirements Checker [DEMO]")
file_path = './src/formatted_nsf.txt'
main.create_retrievalqa(file_path)

#@st.cache_data
#def send_to_frontend(print_this: str):
    
#    text_load_state = st.text(print_this)
    
my_query = st.text_input("What is your question?")

if my_query:
    st.write("Question: ", my_query)
    answer = main.main_driver(my_query)
    st.write("Response: ", answer)