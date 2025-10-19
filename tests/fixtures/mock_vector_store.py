from typing import List, Dict, Any
import numpy as np


class MockVectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = []
        self.add_document_called = False
        self.search_called = False
        
    def add_document(self, text: str, metadata: Dict[str, Any] | None = None):
        self.add_document_called = True
        embedding = np.random.rand(384).tolist()
        self.documents.append({
            "text": text,
            "metadata": metadata if metadata is not None else {},
            "embedding": embedding
        })
        self.embeddings.append(embedding)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        self.search_called = True
        return [
            {
                "text": f"Document {i}",
                "metadata": {"source": f"source_{i}"},
                "similarity": 0.9 - (i * 0.1)
            }
            for i in range(min(top_k, len(self.documents)))
        ]
    
    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        return self.search("", top_k)
    
    def get_document_count(self) -> int:
        return len(self.documents)
    
    def clear(self):
        self.documents = []
        self.embeddings = []


def create_mock_vector_store():
    store = MockVectorStore()
    store.add_document("Sample CRM document 1", {"type": "crm", "customer_id": "1"})
    store.add_document("Sample CRM document 2", {"type": "crm", "customer_id": "2"})
    store.add_document("Sample market insight 1", {"type": "market", "topic": "AI"})
    return store
