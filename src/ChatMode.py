import streamlit
import pandas as pd
import numpy as np
from langchain.chains import RetrievalQA
import base64

import main as m
from process_data import *

# Change site title and add favicon
streamlit.set_page_config(
        layout='wide',
        page_title="Policy Pro",
        page_icon='./src/assets/policy_pro_icon.ico'
    )

# This reduces white space at the top of the page
streamlit.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 5rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

# This eliminates extra spacing being created due to change_label_style()
# Run it every couple of text components (after every component to be safe)
height_hack = '''
<script>
    var hide_me_list = window.parent.document.querySelectorAll('iframe');
    for (let i = 0; i < hide_me_list.length; i++) { 
        if (hide_me_list[i].height == 0) {
            hide_me_list[i].parentNode.style.height = 0;
            hide_me_list[i].parentNode.style.marginBottom = '-1rem';
        };
    };
</script>
'''
streamlit.components.v1.html(height_hack, height=0)

# Add logos + title
# Different logo sizes available in /src/assets
streamlit.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:60px !important;
        color: #000000 !important;
        padding-top: 0px !important;
        font-family: Arial Black;
        text-align: center;
    }
    .logo-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: auto;
        margin-bottom: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
streamlit.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open('./src/assets/policy_pro_128.png', "rb").read()).decode()}">
        <p class="logo-text">POLICY PRO</p>
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open('./src/assets/NSF_Official_logo_High_Res_128.png', "rb").read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True
)
    
streamlit.components.v1.html(height_hack, height=0)

def process(user_file):
    # URL to load in
    # url = "https://www.nsf.gov/pubs/2024/nsf24507/nsf24507.htm"
    url = user_file
    # scrape the HTML from th web
    html = requests.get(url).text
    # parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # save the parsed html to a file for debugging
    with open('./src/temp/nsf.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # Most of the document's information is inside a table that contains only one row and column.
    # The only thing we need outside of that one column is the title, which we can grab and process manually
    title = clean_text(soup.find('title').get_text())
    
    # for https://www.nsf.gov/pubs/2023/nsf23610/nsf23610.htm
    # works as intended - entire html past header is a table
    
    # for https://www.nsf.gov/pubs/2024/nsf24507/nsf24507.htm
    # doesn't work - after section A, stops being a table and is just generic html
    # so file is only processed until section A
    
    # format our document, with the top level element being the first 'td' element that is found
    formatted_document = process_element(soup.find('td'), title, verbose=False)
    # write the results to a text file, delete it if it already exists
    # write the results to a text file
    with open('./src/temp/formatted_nsf.txt', 'w', encoding='utf-8') as f:
        f.write(formatted_document)
        
def change_label_style(text: str, font_size: int=28, font_family: str='Helvetica', font_color: str='#000000'):
    
    font_size += 8
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, a, span class');
        var elem = Array.from(elems).find(x => x.innerText.includes('{text}'));
        elem.style.fontSize = '{font_size}px';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    streamlit.components.v1.html(html, height=0)
        
def main():
    
    subhead = "Please input a policy manual in html format to begin:"
    #subhead = "Please input a policy manual in html format to begin:"
    streamlit.subheader(subhead)
    change_label_style(subhead, 24, 'Helvetica', '#000000')
    #streamlit.subheader("Please input a policy manual in html format to begin:")
    streamlit.components.v1.html(height_hack, height=0)
    
    text_userfile = "Policy Manual"
    user_file = streamlit.text_input(text_userfile, key=1)
    change_label_style(text_userfile, 20, 'Helvetica', '#000000') 
    streamlit.components.v1.html(height_hack, height=0)
    
    if user_file:
        process(user_file)
        
        title = "Proposal Bot :space_invader:"
        streamlit.title(title)
        change_label_style("Proposal Bot", 36, 'Helvetica', '#000000') 
        streamlit.components.v1.html(height_hack, height=0)
        
        file_path = './src/temp/formatted_nsf.txt'
        m.create_retrievalqa(file_path)
        
        # @st.cache_data
        # def send_to_frontend(print_this: str):
        
        #    text_load_state = st.text(print_this)
        
        text_query = "What is your question?"
        my_query = streamlit.text_input(text_query, key=2)
        change_label_style(text_query, 20, 'Helvetica', '#000000') 
        streamlit.components.v1.html(height_hack, height=0)
        
        if my_query:
            sq = "Question: " + my_query
            streamlit.write(":female-detective: " + sq)
            change_label_style(sq, 24, 'Helvetica', '#000000') 
            streamlit.components.v1.html(height_hack, height=0)
            
            answer = m.main_driver(my_query)
            sr = "Response: " + answer
            sr = sr.replace("$", "\$") # '$' alone triggers LaTeX formatting
            streamlit.write(":space_invader: " + sr)
            change_label_style(sr, 24, 'Helvetica', '#000000') 
            streamlit.components.v1.html(height_hack, height=0)
        
if __name__ == '__main__':
	main()