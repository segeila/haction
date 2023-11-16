import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import requests
from helpers.custom_function import extract_keywords

@st.cache_data(persist=True)
def fetch_latest_arxiv_papers(keyword, num_papers=2):
    """
    Fetch the latest papers from arXiv API for a given category.
    
    Parameters:
    - category (str): The arXiv category (e.g., 'cs' for Computer Science)
    - num_papers (int): Number of latest papers to fetch
    
    Returns:
    - response (requests.Response): The API response object
    """
    # Define the query parameters
    params = {
        'search_query': f'ti:"{keyword}"',
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
        'start': 0,
        'max_results': num_papers
    }
    
    # Perform the API request
    response = requests.get('http://export.arxiv.org/api/query', params=params)
    return response

def parse_arxiv_response(response):
    ns = '{http://www.w3.org/2005/Atom}'
    root = ET.fromstring(response.content)
    entries = root.findall(f'{ns}entry')
    summaries = []
    titles = []
    pdf_links = []

    print(f"Len entries: {len(entries)}")

    for entry in entries:
        print(entry)
        title = entry.find(f'{ns}title').text
        summary = entry.find(f'{ns}summary').text
        link = entry.find(f'{ns}link[@title="pdf"]')
        pdf_link = link.attrib['href'] if link is not None else None

        titles.append(title)
        summaries.append(summary)
        pdf_links.append(pdf_link)

    return pd.DataFrame({'title': titles, 'summary': summaries, 'pdf_links': pdf_links})

@st.cache_data(persist=True)
def generate_full_text(user_name, month, condition):
    response = parse_arxiv_response(fetch_latest_arxiv_papers(condition, 2))

    if response is None:
        st.warning("No papers found for the given keyword.")

    summaries = response['summary']
    titles = response['title']
    links = response['pdf_links']
    keywords = []

    closure = " This is all for today. Until next month, keep your curiosity alive and your research glasses on!"
    intro = f"Hello {user_name}! It is {month} first. The month is new, and so are the insights we've got just for you!"

    full_text = intro + f" This month we have {len(summaries)} papers about {condition}. Let's get started!\n\n"

    for i, s in enumerate(summaries):
        n = "first"
        if i == 1:
            n = "second"
        full_text += f" The {n} paper is about {titles[i]}. \n\n"
        full_text += s.replace("\n", " ").replace("\n\n", " ")
        full_text += "\n\n"
        keyword = extract_keywords(summaries[i])
        keywords.append(keyword)  # Append the keyword to the list

    full_text += "\n\n" + closure

    return full_text, links, titles, keywords