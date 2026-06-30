from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from google import genai
from groq import Groq


def query_answer(pdf_path, llm, model, api_key, page_range, page_start, page_end, query):

    if llm == "gemini":
        #Loading google gemini client before hand for safety
        client = genai.Client(
            api_key=api_key
        )

    if llm == "groq":
        #Loading groq client before hand for safety
        groq_client = Groq(api_key)


    reader = PdfReader(pdf_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150 #custom choice by me
    )

    chunks = []

    for page_num, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text: #checking if the page isn't empty

            page_chunks = text_splitter.split_text(page_text)

            for chunk in page_chunks:

                chunks.append({
                    "page": page_num,
                    "text": chunk
                })


    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    chunk_embeddings = embedding_model.encode(
        [chunk["text"] for chunk in chunks],
        convert_to_numpy=True
    )


    dimension = chunk_embeddings.shape[1]
    vdbase = faiss.IndexFlatL2(dimension)
    vdbase.add(chunk_embeddings)


    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    top_k = 7
    distances, indices = vdbase.search(
        query_embedding,
        top_k
    )

    retrieved_chunks = [
        chunks[i]
        for i in indices[0]
    ]


    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    rel_pages = list(dict.fromkeys(
        chunk["page"]
        for chunk in retrieved_chunks
    ))


    prompt = f"""
    You are a document assistant. Use ONLY the information present in the context.
    If the answer is not present in the context, reply exactly:
    Incomplete info in document to answer.

    Context:
    {context}

    Question:
    {query}
    """

    try:

        if llm == "gemini":
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

        elif llm == "groq":
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

        error = ""

    except Exception as e:
        error = e
        response = None


    print("\n\n\nBy the way, following information for your reference on the document:")
    print(f"Loaded {len(reader.pages)} pages")
    print(f"Created {len(chunks)} chunks")


    return {

        "rel_pages": rel_pages,
        "answer": response.text,
        "error": error

    }