<img src="Simp!LAW Logo.png"
     alt="logo"
     style="float: left; margin-right: 10px;" />

# AI Swiss Legal Assistant 🇨🇭 👩‍⚖️ 🤖

This is a simple conversational-ui RAG (retrieval augmented generation) based on the Swiss Code of Obligations and additional Swiss jurisprudence trilingual dataset (in English, German and French).

> It was created a starting point of the Ginetta Challenge at the women++ Hack'n'Lead hackathon November 2023
> 

Conversational AI model used: [Mistral](https://mistral.ai/)

Source of data used to re-trained the model: https://entscheidsuche.ch/docs (PDF files of Swiss jurisprudence). 

Steps and associated files:

- Text extraction from pdf and write in into a json file → docs/download_pdf.py & docs/extract_texts_from_pdf_and_save_it_to_json.py
- Preprocessing → docs/data-cleaning-fromjsontojson.py
- Embeddings using https://huggingface.co/Xenova/paraphrase-multilingual-mpnet-base-v2 → create_embeddings/create_embeddings.js
- Prompt engineering aimed at better legal assistance → app/api/chat/route.ts

To launch the code locally: 

```
curl -X POST 'http://localhost:6333/collections/swiss_law/snapshots/upload' -H 'Content-Type:multipart/form-data' -F 'snapshot=@[name_of_the_snapshot].snapshot'
```
