from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Query(BaseModel):
    question: str
    context: str

@app.post("/rag")
def rag_query(query: Query):
    prompt = f"""
    Use the following context to answer the question.

    Context:
    {query.context}

    Question:
    {query.question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content
    }