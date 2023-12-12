import os


OPEN_API_KEY = "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"
os.environ["OPEN_API_KEY"] = OPEN_API_KEY

COHERE_API_KEY = "9T7g3ZJ4d49BMk5MceXcYFnwD5KdarAFlieCn8Vc"
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

table_prompt_initial = """

<TABLE START>:
{table}
<TABLE END>:
The above text between "<TABLE START>" and "<TABLE END>" is a table formatted in plain language. It contains rows and columns and some rows may have more columns than others. Each row starts with "RX:" where "X" is the row number, starting at 0. Each column in each row starts with "CY:" where "Y" is the column number, starting at 0, followed by the text contained in the column, which is surrounded by quotation marks.\n\n
"""

text_containing_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'strong']

prompt_template = """
<CONTEXT START>
{context}
<CONTEXT END>

Chat History:
{chat_history}

You are an expert in NSF grant proposals and are tasked with answering questions about opportunities to receive an NSF grant. The context above contains portions of the NSF proposal guidelines. Using the context and chat history provided above, try to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. You are allowed to change the language of the response if doing so will make the response more clear and as long as the underlying meaning or facts do not change.
Question: {question}
"""