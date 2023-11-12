import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

sub_url = 'https://entscheidsuche.ch/docs/JU_Gerichte/'

def download_pdfs(sub_url):
    response = requests.get(sub_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links with 'pdf' in the href attribute
    pdf_links = [a['href'] for a in soup.find_all('a', href=lambda x: x and 'pdf' in x)]

    # Create a folder to save the PDF files
    os.makedirs("pdf_files_fr", exist_ok=True)

    for i, pdf_link in enumerate(pdf_links):
        full_url = urljoin(sub_url, pdf_link)
        response = requests.get(full_url)

        #filename = os.path.join("pdf_files_de", f"pdf{i+1}-{full_url.split('/')[-1]}")
        filename = os.path.join("pdf_files_fr", f"pdf{i+1}-{full_url.split('/')[-1]}")

        with open(filename, 'wb') as pdf_file:
            pdf_file.write(response.content)
            print(f"Downloaded: {filename}")


download_pdfs(sub_url)
