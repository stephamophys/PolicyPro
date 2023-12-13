# PolicyPro
### AI/LLM chatbot webapp that answers questions about NSF research grant proposal requirements
This project was originally developed as part of a team collaboration in Louisiana State Unversity's breakthrough AI/LLM development course. As per the course guidelines, this code is fully under the ownership of the original student developers. This repository is an individually-maintained and updated version of the project. Contact me if you would like the original "version-0" of this project from the end of that course.

## Current Functions
- Accepts guidelines for NSF grant proposals in html format
- Offers a chatbot that will answer questions about those guidelines

## How to Use
NOTE: You will need python >=3.10 and several external libraries to run this. Compiling a list of these libraries is currently a top priority but includes LangChain and StreamLit.
Using the [National Artificial Intelligence (AI) Research Institutes](https://new.nsf.gov/funding/opportunities/national-artificial-intelligence-research) program as an example:
1. Find the NSF webpage for your program of interest
2. Click on the number code underneath "View guidelines"
3. You will be prompted to choose between HTML and PDF formats - pick html
4. The HTML version should open up in your browser - copy the link
5. (Windows) Run 'start_app.bat' - the webapp should open in your browser
6. Paste the link into the text field
7. Now you can chat with proposal bot!
See 'demo.mp4' for an example on what the chatbot can do.

## Planned Functions
- Add in a summarization mode
- Obtain list of all libraries necessary to run this
- Switch from StreamLit to Dash for the frontend
- Offer an offline installation
- Have Mac and Linux versions

## Known Bugs
- This was tested on the guidelines for the [National Artificial Intelligence (AI) Research Institutes](https://www.nsf.gov/pubs/2023/nsf23610/nsf23610.htm) program, which has the entire html body in a '<table>' element. Currently, the code only processes this giant '<table>' element and then continues w/o checking if there is anything afterwards. For instance, inputing the guidelines for the [Incorporating Human Behavior in Epidemiological Models](https://www.nsf.gov/pubs/2024/nsf24507/nsf24507.htm) program results in a cleaned html file that ends in the middle of chapter A under "Proposal Preparation and Submission Instructions," and thus the LLM produces results based off of a now too small html file.
- Chat memory is buggy. Likely, the LLM itself maintains memory, but its corresponing vector store's memory is never updated, so the LLM will have subtle references to past conversations but otherwise act as though it has no memory.
- Summarization mode is currently a WIP, but you can generate a less well-defined summarization by asking the chatbot to summarize the guidelines.
- The logo/icon was generated via DALL-E. I am willing to commission an artist to draw this instead (Yes, this is an AI project, but I don't like using AI _art_).

Currently distributed under the MIT license (subject to change)