from elasticsearch import AsyncElasticsearch

class ElasticsearchClient:
    def __init__(self):
        self.client = AsyncElasticsearch()

    async def index_document(self, doc):
        await self.client.index(index="documents", id=doc.id, body={"text": doc.text})

    async def search_documents(self, query):
        response = await self.client.search(index="documents", body={
            "query": {
                "match": {
                    "text": query
                }
            }
        })
        return response['hits']['hits']

    async def delete_document(self, doc_id):
        await self.client.delete(index="documents", id=doc_id)