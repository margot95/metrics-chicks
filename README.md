<img src="Simp!LAW Logo.png"
     alt="logo"
     style="float: left; margin-right: 10px;" />

# AI Swiss Legal Assistant 🇨🇭 👩‍⚖️ 🤖

This is a simple conversational-ui RAG (retrieval augmented generation) based on the Swiss Code of Obligations and additional Swiss jurisprudence trilingual dataset (in English, German and French).

> It was created a starting point of the Ginetta Challenge at the women++ Hack'n'Lead hackathon November 2023
> 

Conversational AI model used: [Mistral](https://mistral.ai/)

Source of data used to re-trained the model: https://entscheidsuche.ch/docs (PDF files of Swiss jurisprudence). 



# Steps and associated files

- Text extraction from pdf and write in into a json file → docs/download_pdf.py & docs/extract_texts_from_pdf_and_save_it_to_json.py
- Preprocessing → docs/data-cleaning-fromjsontojson.py
- Embeddings using https://huggingface.co/Xenova/paraphrase-multilingual-mpnet-base-v2 → create_embeddings/create_embeddings.js
- Prompt engineering aimed at better legal assistance → app/api/chat/route.ts



# To launch the chatbot app locally

1. 🦙 Download Ollama and install it locally
2. Run the Mistral model using:
 ```  ollama run mistral ```
(Requires 4.1GB and 8GB of RAM)
3. Open http://localhost:11434 to check if Ollama is running
4. ``` docker pull qdrant/qdrant ```
5. ``` docker run -p 6333:6333 qdrant/qdrant ```
6. Open the Qdrant dashboard console http://localhost:6333/dashboard#/console

7. Create a new collection running this:

PUT collections/swiss-or
{
  "vectors": {
    "size": 384,
    "distance": "Cosine"
  }
}


8. Download our new custom snapshots: [swiss-civil-code-de-paraphrase-multilingual-mpnet-base-v2.zip](https://github.com/margot95/metrics-chicks/files/13328437/swiss-civil-code-de-paraphrase-multilingual-mpnet-base-v2.zip)  , [swiss-code-of-obligations-en-paraphrase-multilingual-mpnet-base-v2.zip](https://github.com/margot95/metrics-chicks/files/13328448/swiss-code-of-obligations-en-paraphrase-multilingual-mpnet-base-v2.zip) 



9. Unzip the file using the terminal

10. Load our snapshot to Qdrant using the following code:
    
```
curl -X POST 'http://localhost:6333/collections/swiss_law/snapshots/upload' -H 'Content-Type:multipart/form-data' -F 'snapshot=@swiss-civil-code-de-paraphrase-multilingual-mpnet-base-v2.snapshot'

curl -X POST 'http://localhost:6333/collections/swiss_law/snapshots/upload' -H 'Content-Type:multipart/form-data' -F 'snapshot=@swiss-code-of-obligations-en-paraphrase-multilingual-mpnet-base-v2.snapshot'
```

11. Copy the file `.env.local.example` and rename it to `.env`. Verify that all environment variables are correct.
12. `yarn install` to install the required dependencies
13. `yarn dev` to launch the development server

Finally -> Go to <http://localhost:3000> and try out the app

