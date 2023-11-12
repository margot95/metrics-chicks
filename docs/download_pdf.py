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

def download_pdf_and_save_text(base_url):
    # Get the links from the base URL
    links = get_links(base_url)
    row_counter = 0
    for link in links:
        pdf_links = get_pdf_links(link)
        for i, link in enumerate(pdf_links):
            print(link)
            response = requests.get(link)
            filename = "pdfs/pdf"+str(i)+".pdf"
            pdf = open(filename, 'wb')
            pdf.write(response.content)
            pdf.close()
            texts = extract_text_from_pdf(filename)
            for text in texts:
                text = text.replace('\n', ' ')
                if text == "":
                    continue
                result[row_counter] = {"article": text,
                                       "link": link,
                                       "headings": [],
                                       "content": "",
                                       "contentHTML": ""}
                row_counter += 1
            print("File ", i, " downloaded")
            with open('data.json', 'w') as f:
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


download_pdf_and_save_text(base_url)




