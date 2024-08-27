from fastapi import FastAPI, HTTPException
from elastic_client import ElasticsearchClient
from database import DatabaseClient
from pydantic import BaseModel
from typing import List

app = FastAPI()

db_client = DatabaseClient()
es_client = ElasticsearchClient()

class Document(BaseModel):
    id: int
    rubrics: List[str]
    text: str
    created_date: str

@app.post("/documents/")
async def create_document(doc: Document):
    await db_client.create_document(doc)
    await es_client.index_document(doc)
    return {"message": "Document created"}

@app.get("/search/")
async def search_documents(query: str):
    results = await es_client.search_documents(query)
    return results

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: int):
    await db_client.delete_document(doc_id)
    await es_client.delete_document(doc_id)
    return {"message": "Document deleted"}