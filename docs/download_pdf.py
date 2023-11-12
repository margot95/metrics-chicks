#!/usr/bin/env python
# coding: utf-8

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz  # PyMuPDF
import json

# Base URL of the site to scrape
base_url = 'https://entscheidsuche.ch/docs/'
result = {}

link_mapping = {'ZH_OG': 'https://entscheidsuche.ch/docs/ZH_Obergericht/',
                'ZH_KS': 'https://entscheidsuche.ch/docs/ZH_Obergericht/',
                'ZH_BK': 'https://entscheidsuche.ch/docs/ZH_Obergericht/',
                'ZH_HG': 'https://entscheidsuche.ch/docs/ZH_Obergericht/',
                'ZH_SR': 'https://entscheidsuche.ch/docs/ZH_Steuerrekurs/',
                'JU_TC': 'https://entscheidsuche.ch/docs/JU_Gerichte/',
                'JU_TP': 'https://entscheidsuche.ch/docs/JU_Gerichte/',}

#change folder name according to language l59-60
language='de'
#language='fr'


def get_links(url):
    # Send request to the given URL
    response = requests.get(url)
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all 'a' tags, as they contain links
    links = soup.find_all('a')
    final = []
    for link in links:
        if 'docs' in link['href']:
            canton = link['href'].split('/')[-2]
            if canton != '' and canton != 'docs' and '_' in canton:
                final.append(url+canton)
    return final


def get_pdf_links(url):
    # Send request to the given URL
    response = requests.get(url)
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all 'a' tags, as they contain links
    links = soup.find_all('a')
    #print(links)
    pdf_links = []
    for link in links:
        href = link['href']
        if '.pdf' in href:
            #print(href)
            pdf_links.append(url+'/'+href.split('/')[-1])
    return pdf_links

def download_pdf_and_save_text(base_url, foldername='pdfs'):
    # Get the links from the base URL
    links = get_links(base_url)
    links.sort(reverse=True)
    row_counter = 0
    pdf_counter = 0
    #print(links)
    for link in links:
        if pdf_counter > 5000:
            break
        pdf_links = get_pdf_links(link)
        for i, link in enumerate(pdf_links):
            print(link)
            response = requests.get(link)
            filename = f"{foldername}/{link.split('/')[-1]}"
            pdf = open(filename, 'wb')
            pdf.write(response.content)
            pdf.close()
            texts = extract_text_from_pdf(filename)
            for text in texts:
                text = text.replace('\n', ' ')
                if text == "":
                    continue
                result[row_counter] = {"article": link.split('/')[-1].replace('.pdf', ''),
                                       "link": link,
                                       "headings": [],
                                       "content": text,
                                       "contentHTML": ""}
                row_counter += 1
            print("File ", i, " downloaded")
        pdf_counter += 1
    with open('../create_embeddings/{foldername}_new.json', 'w') as f:
        f.write(json.dumps(result, indent=4))


def create_json(foldername='pdfs'):
    row_counter = 0
    files = os.listdir(foldername)
    links = get_links(base_url)
    #for link in links:
    #    print(link)
    for i, filename in enumerate(files):
        print(i)
        texts = extract_text_from_pdf(f'{foldername}/{filename}')
        link = link_mapping[filename[:5]]
        for page, text in enumerate(texts):
                text = text.replace('\n', ' ')
                if text == "":
                    continue
                result[row_counter] = {"article": f'#{page+1}',
                                       "link": link+filename,
                                       "headings": ["headings"],
                                       "content": text,
                                       "contentHTML": "contentHTML"}
                row_counter += 1

    with open(f'../create_embeddings/{foldername}.json', 'w') as f:
        f.write(json.dumps(result, indent=4))


def extract_text_from_pdf(pdf_path):
    # Open the provided PDF file
    pdf_document = fitz.open(pdf_path)
    extracted_texts = []

    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]

        # Extract text from the page
        text = page.get_text()

        # Append the text to our list
        extracted_texts.append(text)

    # Close the PDF after extraction
    pdf_document.close()
    return extracted_texts


#download_pdf_and_save_text(base_url, 'pdfs_new')


create_json('pdfs_new')


