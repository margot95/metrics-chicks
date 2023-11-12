#!/usr/bin/env python
# coding: utf-8

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the site to scrape
base_url = 'https://entscheidsuche.ch/docs/'

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

def download_pdf(base_url):
    # Get the links from the base URL
    links = get_links(base_url)
    for link in links:
        pdf_links = get_pdf_links(link)
        for i, link in enumerate(pdf_links):
            print(link)
            response = requests.get(link)
            #l59 for saving German pdf to German folder, l60 for French
            filename = os.path.join("pdf_files_de", "pdf"+str(i)+"-"+language+".pdf")
            #filename = os.path.join("pdf_files_fr", "pdf"+str(i)+"-"+language+".pdf")
            pdf = open(filename, 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")


download_pdf(base_url)
