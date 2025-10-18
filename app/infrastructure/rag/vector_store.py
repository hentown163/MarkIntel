"""Vector store for RAG (Retrieval-Augmented Generation)"""
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from openai import OpenAI
from app.core.settings import settings
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Document:
    """Represents a document in the vector store"""
    id: str
    content: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class VectorStore:
    """
    Vector store for storing and retrieving documents using embeddings
    
    This implements RAG (Retrieval-Augmented Generation) by:
    1. Embedding documents using OpenAI embeddings
    2. Storing embeddings in memory
    3. Retrieving similar documents using cosine similarity
    """
    
    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.embedding_model = embedding_model
        self.documents: Dict[str, Document] = {}
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text using OpenAI
        
        Falls back to random embedding if OpenAI is not available (for testing)
        """
        if not self.client:
            # Fallback: generate random embedding for testing
            np.random.seed(hash(text) % (2**32))
            return np.random.rand(1536)
        
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Fallback to random
            np.random.seed(hash(text) % (2**32))
            return np.random.rand(1536)
    
    def add_document(self, doc_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a document to the vector store"""
        embedding = self._get_embedding(content)
        doc = Document(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {}
        )
        self.documents[doc_id] = doc
    
    def add_documents(self, documents: List[Tuple[str, str, Optional[Dict]]]):
        """Batch add documents to the vector store"""
        for doc_id, content, metadata in documents:
            self.add_document(doc_id, content, metadata)
    
    def retrieve(self, query: str, top_k: int = 5, filter_metadata: Optional[Dict] = None) -> List[Document]:
        """
        Retrieve most similar documents to the query
        
        Args:
            query: Query text to search for
            top_k: Number of top results to return
            filter_metadata: Optional metadata filters (e.g., {"customer_segment": "enterprise"})
        
        Returns:
            List of most similar documents
        """
        if not self.documents:
            return []
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Filter documents by metadata if provided
        filtered_docs = self.documents.values()
        if filter_metadata:
            filtered_docs = [
                doc for doc in filtered_docs
                if all(doc.metadata.get(k) == v for k, v in filter_metadata.items())
            ]
        
        if not filtered_docs:
            return []
        
        # Calculate cosine similarity
        doc_embeddings = np.array([doc.embedding for doc in filtered_docs])
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return top documents
        filtered_docs_list = list(filtered_docs)
        return [filtered_docs_list[i] for i in top_indices]
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get a specific document by ID"""
        return self.documents.get(doc_id)
    
    def delete_document(self, doc_id: str):
        """Delete a document from the vector store"""
        if doc_id in self.documents:
            del self.documents[doc_id]
    
    def clear(self):
        """Clear all documents from the vector store"""
        self.documents = {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        return {
            "total_documents": len(self.documents),
            "embedding_model": self.embedding_model,
            "metadata_keys": list(set(
                key for doc in self.documents.values()
                for key in doc.metadata.keys()
            ))
        }


# Global singleton instance
_vector_store = VectorStore()


def get_vector_store() -> VectorStore:
    """Get the global vector store instance"""
    return _vector_store
