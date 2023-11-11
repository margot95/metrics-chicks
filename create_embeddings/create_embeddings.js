import { QdrantClient } from "@qdrant/js-client-rest";
import { NodeHtmlMarkdown } from "node-html-markdown";
import { HuggingFaceTransformersEmbeddings } from "langchain/embeddings/hf_transformers";
import * as cheerio from "cheerio";
import { promises as fs } from "fs";
import path from "path";


export default async function RUN() {
  const jsonText = await fs.readFile(
    path.join(process.cwd(), "data.json"),
    "utf8"
  );

  //console.log(process.env.QDRANT_URL);

  const articlesData = JSON.parse(jsonText);
  //console.log(articlesData);
  const articles = [];

  Object.entries(articlesData).forEach(([key, value]) => {
    // Assuming each articleData is a string of HTML content
    const structuredData = {
      headings: ["headins"],
      article: value,
      link: "link",
      content: "",
      contentHTML: "",
    };
    //console.log( structuredData);
    articles.push(structuredData);
  });

  //console.log(articles);

  const embeddings = new HuggingFaceTransformersEmbeddings({
    modelName: "Xenova/paraphrase-multilingual-mpnet-base-v2",
    //modelName: "Xenova/gte-small",
  });

  const client = new QdrantClient({ url: process.env.QDRANT_URL });

  const articleChunks = chunkArray(articles, 3);

  let index = 0;

  for (const articles of articleChunks) {
    const articlesText = articles.map(
      (x) =>
        x.headings
          .map((heading, i) => {
            if (i < 5) {
              const headingMarkup = "#".repeat(i);
              return headingMarkup + " " + heading;
            }

            return `**${heading}**`;
          })
          .join("\n") +
        "\n" +
        htmlToMarkdown(x.contentHTML).trim()
    );

    const documentEmbeddings = await embeddings.embedDocuments(articlesText);

    const points = documentEmbeddings.map((vector, i) => {
      index++;
      const title = articles[i].headings.slice(-1)[0];

      const { contentHTML: _, ...payload } = articles[i];

      articles[i].vector = vector;

      return {
        id: index,
        vector,
        payload: {
          title,
          ...payload,
        },
      };
    });

     //Insert into qdrant

     await client.upsert('swiss-or', {
       wait: true,
       points: points,
     });
  }

  return articles
    .map(({ contentHTML: _, ...a }) => a)
    .map((x) =>
      JSON.stringify(
        x
        // null, 2
      )
    )
    .join("\n");
}

function chunkArray(array = [], chunkSize) {
  const chunks = [];
  for (let i = 0; i < array.length; i += chunkSize) {
    chunks.push(array.slice(i, i + chunkSize));
  }
  return chunks;
}

const result = await RUN();

console.log(result);

export function htmlToMarkdown(htmlContent) {
  return (
    NodeHtmlMarkdown.translate(htmlContent, {
      maxConsecutiveNewlines: 3,
      useLinkReferenceDefinitions: true,
    })
      // .replace(/!?\[\]\([^\)]+\)/g, "")
      .replace(/!\[([^\]]*)\]\([^)]+\)\n*/g, (match, altText) => altText)
      .replace(/[ ]+/g, " ")
      .replace(/\[([^\]]+)\]\[\d+\]/g, (_, x) => x.trim()) // Remove useLinkReferenceDefinitions links.
      .replace(/\[[\d]+\]: .*\n*/g, "")
  );
}