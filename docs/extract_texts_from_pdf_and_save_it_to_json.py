#!/usr/bin/env python
# coding: utf-8

import fitz  # PyMuPDF
import json


result = {}


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


def save_data(number_of_pdfs):
    for i in range(number_of_pdfs):
        print(i)
        result[i] = extract_text_from_pdf(f'pdf{i}.pdf')

    with open('data.json', 'w') as f:
        f.write(json.dumps(result, indent=4))



save_data(3919)


