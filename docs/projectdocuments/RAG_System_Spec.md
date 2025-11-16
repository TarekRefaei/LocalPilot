# 📄 DOCUMENT #11: RAG_SYSTEM_SPEC.md
# LocalPilot - RAG System Specification

**Version:** 1.0  
**Date:** January 2025  
**Status:** Advanced Specification  
**Author:** LocalPilot RAG Team

---

## 📋 Table of Contents

- [📄 DOCUMENT #11: RAG\_SYSTEM\_SPEC.md](#-document-11-rag_system_specmd)
- [LocalPilot - RAG System Specification](#localpilot---rag-system-specification)
  - [📋 Table of Contents](#-table-of-contents)
  - [🎯 Overview](#-overview)
    - [Purpose](#purpose)
    - [Critical Success Factors](#critical-success-factors)
  - [🏗️ RAG Architecture](#️-rag-architecture)
    - [System Architecture](#system-architecture)
  - [🧬 Embedding Strategy](#-embedding-strategy)
    - [bge-m3 Optimization](#bge-m3-optimization)
    - [Embedding Quality Optimization](#embedding-quality-optimization)
  - [🔍 Vector Search \& Retrieval](#-vector-search--retrieval)
    - [Vector Search Implementation](#vector-search-implementation)
  - [📊 Multi-Level Retrieval](#-multi-level-retrieval)
    - [Multi-Level Retrieval Strategy](#multi-level-retrieval-strategy)
  - [🪟 Context Window Management](#-context-window-management)
    - [Context Budget Optimizer](#context-budget-optimizer)
  - [🎯 Relevance Scoring](#-relevance-scoring)
    - [Advanced Relevance Scoring System](#advanced-relevance-scoring-system)
  - [🔧 Query Optimization](#-query-optimization)
    - [Query Enhancement \& Expansion](#query-enhancement--expansion)
  - [🔀 Hybrid Search](#-hybrid-search)
    - [Hybrid Search Implementation](#hybrid-search-implementation)
  - [⚡ Performance Optimization](#-performance-optimization)
    - [RAG Performance Optimizer](#rag-performance-optimizer)
  - [💾 Caching Strategies](#-caching-strategies)
    - [Multi-Level Caching System](#multi-level-caching-system)
  - [📊 Quality Metrics](#-quality-metrics)
    - [RAG Quality Evaluation System](#rag-quality-evaluation-system)
  - [📚 Related Documents](#-related-documents)

---

## 🎯 Overview

### Purpose

The RAG (Retrieval-Augmented Generation) system is the **intelligence layer** that connects user queries to relevant code context. Quality RAG is essential for:

1. **Accurate Responses**: Retrieve the most relevant code for user questions
2. **Context Awareness**: Provide LLM with sufficient context to generate helpful responses
3. **Performance**: Sub-500ms retrieval time for real-time chat
4. **Quality**: >80% relevance score on retrieved chunks

### Critical Success Factors

```yaml
Quality Metrics (Must Achieve):
  Precision@5: >= 0.80
    - At least 4 out of top 5 results are relevant
  
  Recall@10: >= 0.70
    - Captures 70% of relevant chunks in top 10
  
  Response Time: < 500ms
    - From query to context ready
  
  Context Quality: >= 0.85
    - Retrieved context helps LLM answer correctly

Design Principles:
  1. Quality over Quantity
     - Better to retrieve 3 perfect chunks than 10 mediocre ones
  
  2. Context Preservation
     - Include surrounding context (imports, class definitions)
  
  3. Multi-Level Retrieval
     - Project → Directory → File → Chunk hierarchy
  
  4. Semantic + Lexical
     - Combine embedding similarity with keyword matching
  
  5. User Context Awareness
     - Prioritize files user is currently viewing/editing
```

---

## 🏗️ RAG Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                               │
│              "How does authentication work?"                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Query Processor                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │  1. Query Analysis                                 │     │
│  │     - Intent detection                             │     │
│  │     - Entity extraction (file names, functions)    │     │
│  │     - Query expansion                              │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Multi-Level Retrieval Pipeline                 │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Level 1: Project Summary Retrieval                │     │
│  │  └─> Check if question is project-wide             │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Level 2: Symbol/Metadata Search                   │     │
│  │  └─> Search for classes, functions, files          │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Level 3: Semantic Vector Search                   │     │
│  │  └─> Embed query, search similar chunks (bge-m3)   │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Level 4: Keyword/Lexical Search                   │     │
│  │  └─> BM25 search for exact matches                 │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Result Fusion & Ranking                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │  1. Combine results from all levels                │     │
│  │  2. Re-rank by relevance score                     │     │
│  │  3. Apply user context boost                       │     │
│  │  4. Deduplicate chunks                             │     │
│  │  5. Select top-K results                           │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Context Window Optimization                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │  1. Calculate token budget (4000 tokens)           │     │
│  │  2. Prioritize chunks by relevance                 │     │
│  │  3. Add surrounding context                        │     │
│  │  4. Include project summary                        │     │
│  │  5. Format for LLM consumption                     │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Retrieved Context                        │
│              Ready for LLM Processing                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧬 Embedding Strategy

### bge-m3 Optimization

```python
# backend/src/services/rag/embedding_service.py

from typing import List, Optional, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Optimized embedding service using bge-m3
    
    bge-m3 Specifications:
    - Dimensions: 1024
    - Max sequence length: 8192 tokens
    - Multilingual support
    - Optimized for code and technical text
    """
    
    def __init__(
        self,
        model_name: str = 'bge-m3',
        device: str = 'cuda',
        batch_size: int = 32,
    ):
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        
        # Load model
        logger.info(f"Loading embedding model: {model_name}")
        self.model = self._load_model()
        
        # Statistics
        self._embed_count = 0
        self._cache_hits = 0
        
        # Query cache (for repeated queries)
        self._query_cache: Dict[str, np.ndarray] = {}
        self._max_cache_size = 1000
    
    def _load_model(self) -> SentenceTransformer:
        """Load bge-m3 model via Ollama"""
        # Note: In practice, we use Ollama's embedding API
        # This is a conceptual implementation
        
        if self.device == 'cuda' and torch.cuda.is_available():
            device = 'cuda'
            logger.info("Using GPU acceleration for embeddings")
        else:
            device = 'cpu'
            logger.warning("GPU not available, using CPU for embeddings")
        
        # Load via sentence-transformers (alternative to Ollama)
        # In production, we'll use Ollama's API
        model = SentenceTransformer('BAAI/bge-m3', device=device)
        
        return model
    
    async def embed_query(
        self,
        query: str,
        use_cache: bool = True
    ) -> np.ndarray:
        """
        Embed a single query
        
        Args:
            query: Query text
            use_cache: Use cached embedding if available
            
        Returns:
            1024-dimensional embedding vector
        """
        # Check cache
        if use_cache and query in self._query_cache:
            self._cache_hits += 1
            logger.debug(f"Cache hit for query: {query[:50]}...")
            return self._query_cache[query]
        
        # Prepare query for bge-m3
        # Add query prefix for better retrieval
        prepared_query = f"Represent this query for searching code: {query}"
        
        # Generate embedding
        embedding = self.model.encode(
            prepared_query,
            normalize_embeddings=True,  # L2 normalization for cosine similarity
            convert_to_numpy=True,
        )
        
        self._embed_count += 1
        
        # Cache query embedding
        if use_cache:
            if len(self._query_cache) >= self._max_cache_size:
                # Remove oldest entry (simple FIFO)
                self._query_cache.pop(next(iter(self._query_cache)))
            
            self._query_cache[query] = embedding
        
        return embedding
    
    async def embed_documents(
        self,
        documents: List[str],
        batch_size: Optional[int] = None,
        show_progress: bool = False
    ) -> List[np.ndarray]:
        """
        Embed multiple documents in batches
        
        Args:
            documents: List of document texts
            batch_size: Batch size (default: self.batch_size)
            show_progress: Show progress bar
            
        Returns:
            List of 1024-dimensional embedding vectors
        """
        if batch_size is None:
            batch_size = self.batch_size
        
        all_embeddings = []
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Prepare documents for bge-m3
            # Add document prefix for better retrieval
            prepared_batch = [
                f"Represent this code for retrieval: {doc}"
                for doc in batch
            ]
            
            # Generate embeddings
            batch_embeddings = self.model.encode(
                prepared_batch,
                normalize_embeddings=True,
                convert_to_numpy=True,
                batch_size=len(batch),
                show_progress_bar=show_progress,
            )
            
            all_embeddings.extend(batch_embeddings)
            self._embed_count += len(batch)
        
        logger.info(f"Generated {len(all_embeddings)} embeddings")
        
        return all_embeddings
    
    async def embed_chunks(
        self,
        chunks: List[Dict],
        batch_size: Optional[int] = None
    ) -> List[Dict]:
        """
        Embed code chunks with metadata
        
        Args:
            chunks: List of chunk dicts with 'content' and 'metadata'
            batch_size: Batch size
            
        Returns:
            Chunks with added 'embedding' field
        """
        contents = [chunk['content'] for chunk in chunks]
        embeddings = await self.embed_documents(contents, batch_size)
        
        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding.tolist()
        
        return chunks
    
    def compute_similarity(
        self,
        query_embedding: np.ndarray,
        document_embeddings: List[np.ndarray]
    ) -> List[float]:
        """
        Compute cosine similarity between query and documents
        
        Args:
            query_embedding: Query embedding vector
            document_embeddings: List of document embedding vectors
            
        Returns:
            List of similarity scores (0-1)
        """
        # Convert to numpy arrays
        query_vec = np.array(query_embedding)
        doc_matrix = np.array(document_embeddings)
        
        # Cosine similarity (embeddings are already normalized)
        similarities = np.dot(doc_matrix, query_vec)
        
        return similarities.tolist()
    
    def get_statistics(self) -> Dict:
        """Get embedding service statistics"""
        return {
            'total_embeddings_generated': self._embed_count,
            'cache_size': len(self._query_cache),
            'cache_hits': self._cache_hits,
            'cache_hit_rate': (
                self._cache_hits / (self._embed_count + self._cache_hits)
                if (self._embed_count + self._cache_hits) > 0
                else 0.0
            ),
            'model': self.model_name,
            'device': self.device,
            'batch_size': self.batch_size,
        }
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 8192) -> str:
        """
        Truncate text to fit within bge-m3's max sequence length
        
        Args:
            text: Input text
            max_length: Maximum length in tokens (approximate by chars/4)
            
        Returns:
            Truncated text
        """
        # Rough approximation: 1 token ≈ 4 characters
        max_chars = max_length * 4
        
        if len(text) <= max_chars:
            return text
        
        # Truncate at word boundary
        truncated = text[:max_chars]
        last_space = truncated.rfind(' ')
        
        if last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + '...'
```

### Embedding Quality Optimization

```python
# backend/src/services/rag/embedding_optimizer.py

from typing import List, Dict
import numpy as np

class EmbeddingOptimizer:
    """Optimize embeddings for better retrieval quality"""
    
    @staticmethod
    def prepare_code_for_embedding(
        code: str,
        metadata: Dict
    ) -> str:
        """
        Prepare code chunk for optimal embedding
        
        Strategy:
        1. Include context hints (file, function name)
        2. Preserve important tokens (class names, function names)
        3. Add natural language description if available
        """
        
        parts = []
        
        # Add context from metadata
        if 'file_path' in metadata:
            parts.append(f"File: {metadata['file_path']}")
        
        if 'symbols' in metadata and metadata['symbols']:
            symbols = ', '.join(metadata['symbols'][:3])
            parts.append(f"Symbols: {symbols}")
        
        if 'chunk_type' in metadata:
            parts.append(f"Type: {metadata['chunk_type']}")
        
        # Add docstring/comment if available
        if 'docstring' in metadata and metadata['docstring']:
            parts.append(f"Description: {metadata['docstring']}")
        
        # Add the actual code
        parts.append(code)
        
        return '\n'.join(parts)
    
    @staticmethod
    def prepare_query_for_embedding(
        query: str,
        context: Dict
    ) -> str:
        """
        Prepare user query for optimal embedding
        
        Strategy:
        1. Add context from user's current state
        2. Expand abbreviations
        3. Add domain hints
        """
        
        parts = [query]
        
        # Add current file context
        if 'current_file' in context and context['current_file']:
            parts.append(f"Current file: {context['current_file']}")
        
        # Add mode context
        if 'mode' in context:
            parts.append(f"Mode: {context['mode']}")
        
        return ' '.join(parts)
    
    @staticmethod
    def rerank_by_diversity(
        results: List[Dict],
        top_k: int = 5,
        diversity_weight: float = 0.3
    ) -> List[Dict]:
        """
        Re-rank results to promote diversity
        
        Prevents returning too many chunks from the same file
        """
        
        if len(results) <= top_k:
            return results
        
        selected = []
        remaining = results.copy()
        file_counts = {}
        
        while len(selected) < top_k and remaining:
            # Score remaining results
            scored = []
            for result in remaining:
                file_path = result['metadata'].get('file_path', '')
                file_count = file_counts.get(file_path, 0)
                
                # Penalty for files already selected
                diversity_penalty = file_count * diversity_weight
                adjusted_score = result['score'] - diversity_penalty
                
                scored.append((adjusted_score, result))
            
            # Select best
            scored.sort(key=lambda x: x[0], reverse=True)
            best_score, best_result = scored[0]
            
            selected.append(best_result)
            remaining.remove(best_result)
            
            # Update file count
            file_path = best_result['metadata'].get('file_path', '')
            file_counts[file_path] = file_counts.get(file_path, 0) + 1
        
        return selected
```

---

## 🔍 Vector Search & Retrieval

### Vector Search Implementation

```python
# backend/src/services/rag/vector_search.py

from typing import List, Dict, Optional
import numpy as np
import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)

class VectorSearchService:
    """Vector-based semantic search using ChromaDB"""
    
    def __init__(
        self,
        persist_directory: str = '.localpilot/vectordb',
        collection_name: str = 'localpilot_codebase'
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 200,  # Higher = better quality
                "hnsw:M": 16,  # Connections per layer
            }
        )
        
        logger.info(f"Vector search initialized: {self.collection.count()} documents")
    
    async def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 10,
        filters: Optional[Dict] = None,
        min_score: float = 0.0
    ) -> List[Dict]:
        """
        Search for similar code chunks
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Metadata filters (e.g., {'language': 'typescript'})
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of results with content, metadata, and scores
        """
        
        # Convert numpy array to list
        query_vector = query_embedding.tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=filters,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        
        for i in range(len(results['ids'][0])):
            # Convert distance to similarity score
            # ChromaDB returns cosine distance: distance = 1 - similarity
            distance = results['distances'][0][i]
            similarity = 1.0 - distance
            
            # Filter by minimum score
            if similarity < min_score:
                continue
            
            formatted_results.append({
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': round(similarity, 4),
            })
        
        logger.debug(f"Found {len(formatted_results)} results (score >= {min_score})")
        
        return formatted_results
    
    async def search_with_context(
        self,
        query_embedding: np.ndarray,
        user_context: Dict,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Search with user context boosting
        
        Boosts results from:
        - Currently open file
        - Recently edited files
        - Files in same directory
        """
        
        # Initial search (get more results for re-ranking)
        initial_results = await self.search(
            query_embedding,
            top_k=top_k * 2,
            min_score=0.5  # Minimum threshold
        )
        
        # Apply context boosting
        for result in initial_results:
            boost = self._calculate_context_boost(result, user_context)
            result['original_score'] = result['score']
            result['score'] = result['score'] * boost
            result['boost_factor'] = boost
        
        # Re-sort by boosted score
        initial_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top-k
        return initial_results[:top_k]
    
    def _calculate_context_boost(
        self,
        result: Dict,
        user_context: Dict
    ) -> float:
        """
        Calculate context boost factor (1.0 = no boost, >1.0 = boost)
        """
        boost = 1.0
        
        file_path = result['metadata'].get('file_path', '')
        
        # Boost if current file
        if 'current_file' in user_context:
            if file_path == user_context['current_file']:
                boost *= 1.5
                logger.debug(f"Current file boost: {file_path}")
        
        # Boost if recently edited
        if 'recent_files' in user_context:
            if file_path in user_context['recent_files']:
                boost *= 1.3
                logger.debug(f"Recent file boost: {file_path}")
        
        # Boost if same directory
        if 'current_directory' in user_context:
            current_dir = user_context['current_directory']
            if file_path.startswith(current_dir):
                boost *= 1.2
                logger.debug(f"Same directory boost: {file_path}")
        
        return boost
    
    async def search_by_metadata(
        self,
        filters: Dict,
        limit: int = 100
    ) -> List[Dict]:
        """
        Search by metadata only (no semantic search)
        
        Useful for finding specific files, symbols, etc.
        """
        
        results = self.collection.get(
            where=filters,
            limit=limit,
            include=['documents', 'metadatas']
        )
        
        formatted = []
        for i in range(len(results['ids'])):
            formatted.append({
                'id': results['ids'][i],
                'content': results['documents'][i],
                'metadata': results['metadatas'][i],
                'score': 1.0,  # Exact match
            })
        
        return formatted
    
    def get_statistics(self) -> Dict:
        """Get vector store statistics"""
        count = self.collection.count()
        
        # Sample some documents to analyze
        sample = self.collection.peek(limit=100)
        
        languages = {}
        chunk_types = {}
        
        for metadata in sample['metadatas']:
            lang = metadata.get('language', 'unknown')
            languages[lang] = languages.get(lang, 0) + 1
            
            chunk_type = metadata.get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        
        return {
            'total_chunks': count,
            'collection_name': self.collection_name,
            'languages': languages,
            'chunk_types': chunk_types,
        }
```

---

## 📊 Multi-Level Retrieval

### Multi-Level Retrieval Strategy

```python
# backend/src/services/rag/multi_level_retrieval.py

from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RetrievalResult:
    """Result from retrieval"""
    chunks: List[Dict]
    metadata: Dict
    total_tokens: int

class MultiLevelRetriever:
    """
    Multi-level retrieval strategy
    
    Levels:
    1. Project Summary (high-level context)
    2. Symbol/Metadata Search (exact matches)
    3. Semantic Vector Search (relevance)
    4. Keyword/Lexical Search (exact terms)
    """
    
    def __init__(
        self,
        vector_search,
        metadata_store,
        embedding_service
    ):
        self.vector_search = vector_search
        self.metadata_store = metadata_store
        self.embedding_service = embedding_service
    
    async def retrieve(
        self,
        query: str,
        user_context: Dict,
        top_k: int = 5
    ) -> RetrievalResult:
        """
        Execute multi-level retrieval
        
        Args:
            query: User query
            user_context: User context (current file, etc.)
            top_k: Number of chunks to return
            
        Returns:
            RetrievalResult with chunks and metadata
        """
        
        all_results = []
        retrieval_metadata = {
            'levels_used': [],
            'query': query,
        }
        
        # Level 1: Project Summary
        project_summary = await self._level1_project_summary(query)
        if project_summary:
            all_results.extend(project_summary)
            retrieval_metadata['levels_used'].append('project_summary')
        
        # Level 2: Symbol/Metadata Search
        symbol_results = await self._level2_symbol_search(query)
        if symbol_results:
            all_results.extend(symbol_results)
            retrieval_metadata['levels_used'].append('symbol_search')
        
        # Level 3: Semantic Vector Search (PRIMARY)
        semantic_results = await self._level3_semantic_search(
            query,
            user_context,
            top_k=top_k * 2  # Get more for fusion
        )
        all_results.extend(semantic_results)
        retrieval_metadata['levels_used'].append('semantic_search')
        
        # Level 4: Keyword/Lexical Search
        keyword_results = await self._level4_keyword_search(query, top_k=10)
        if keyword_results:
            all_results.extend(keyword_results)
            retrieval_metadata['levels_used'].append('keyword_search')
        
        # Fusion & Re-ranking
        fused_results = self._fuse_results(all_results, top_k)
        
        # Calculate total tokens
        total_tokens = sum(
            result['metadata'].get('tokens', 0)
            for result in fused_results
        )
        
        retrieval_metadata['results_by_level'] = {
            'project_summary': len(project_summary) if project_summary else 0,
            'symbol_search': len(symbol_results) if symbol_results else 0,
            'semantic_search': len(semantic_results),
            'keyword_search': len(keyword_results) if keyword_results else 0,
        }
        retrieval_metadata['final_count'] = len(fused_results)
        
        logger.info(
            f"Multi-level retrieval: {len(fused_results)} chunks, "
            f"{total_tokens} tokens, "
            f"levels: {retrieval_metadata['levels_used']}"
        )
        
        return RetrievalResult(
            chunks=fused_results,
            metadata=retrieval_metadata,
            total_tokens=total_tokens
        )
    
    async def _level1_project_summary(self, query: str) -> Optional[List[Dict]]:
        """
        Level 1: Retrieve project summary if query is project-wide
        
        Examples:
        - "What does this project do?"
        - "What technologies are used?"
        - "Give me an overview"
        """
        
        # Detect if query is project-wide
        project_keywords = [
            'project', 'overview', 'summary', 'what is', 'what does',
            'technologies', 'architecture', 'purpose'
        ]
        
        is_project_query = any(
            keyword in query.lower()
            for keyword in project_keywords
        )
        
        if not is_project_query:
            return None
        
        # Retrieve project summary from metadata
        summary = await self.metadata_store.get_project_summary()
        
        if summary:
            return [{
                'id': 'project-summary',
                'content': summary,
                'metadata': {
                    'type': 'project_summary',
                    'source': 'indexing',
                },
                'score': 1.0,
                'level': 'project_summary'
            }]
        
        return None
    
    async def _level2_symbol_search(self, query: str) -> Optional[List[Dict]]:
        """
        Level 2: Search for exact symbol matches
        
        If query mentions specific function/class names, retrieve them directly
        """
        
        # Extract potential symbol names from query
        # Simple heuristic: CamelCase or snake_case words
        import re
        
        # Find CamelCase words
        camel_case = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', query)
        
        # Find snake_case words
        snake_case = re.findall(r'\b[a-z]+_[a-z_]+\b', query)
        
        potential_symbols = camel_case + snake_case
        
        if not potential_symbols:
            return None
        
        results = []
        
        for symbol in potential_symbols:
            # Search for symbol in metadata
            symbol_chunks = await self.vector_search.search_by_metadata(
                filters={'symbols': {'$contains': symbol}},
                limit=3
            )
            
            for chunk in symbol_chunks:
                chunk['level'] = 'symbol_search'
                chunk['matched_symbol'] = symbol
                results.append(chunk)
        
        return results if results else None
    
    async def _level3_semantic_search(
        self,
        query: str,
        user_context: Dict,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Level 3: Semantic vector search (PRIMARY retrieval method)
        """
        
        # Embed query
        query_embedding = await self.embedding_service.embed_query(query)
        
        # Search with context
        results = await self.vector_search.search_with_context(
            query_embedding,
            user_context,
            top_k=top_k
        )
        
        # Tag with level
        for result in results:
            result['level'] = 'semantic_search'
        
        return results
    
    async def _level4_keyword_search(
        self,
        query: str,
        top_k: int = 10
    ) -> Optional[List[Dict]]:
        """
        Level 4: Keyword/lexical search using BM25
        
        Useful for exact term matches (e.g., "useState", "async/await")
        """
        
        # Extract important keywords
        keywords = self._extract_keywords(query)
        
        if not keywords:
            return None
        
        # Search for chunks containing keywords
        # (Simplified - in production, use proper BM25)
        results = []
        
        for keyword in keywords[:3]:  # Top 3 keywords
            keyword_chunks = await self.vector_search.search_by_metadata(
                filters={'content': {'$contains': keyword}},
                limit=5
            )
            
            for chunk in keyword_chunks:
                chunk['level'] = 'keyword_search'
                chunk['matched_keyword'] = keyword
                # Score by keyword frequency
                chunk['score'] = chunk['content'].lower().count(keyword.lower()) / 10
                results.append(chunk)
        
        return results if results else None
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        # Remove common words
        stop_words = {
            'how', 'does', 'what', 'is', 'the', 'a', 'an', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'this', 'that', 'these',
            'those', 'work', 'works', 'working', 'use', 'used', 'using'
        }
        
        words = query.lower().split()
        keywords = [
            word for word in words
            if word not in stop_words and len(word) > 2
        ]
        
        return keywords
    
    def _fuse_results(
        self,
        all_results: List[Dict],
        top_k: int
    ) -> List[Dict]:
        """
        Fuse results from all levels using weighted scoring
        
        Strategy:
        - Remove duplicates
        - Re-rank by weighted scores
        - Apply diversity
        """
        
        # Deduplicate by chunk ID
        seen_ids = set()
        unique_results = []
        
        for result in all_results:
            chunk_id = result.get('id')
            if chunk_id not in seen_ids:
                seen_ids.add(chunk_id)
                unique_results.append(result)
        
        # Apply level-specific weights
        level_weights = {
            'project_summary': 1.2,
            'symbol_search': 1.3,
            'semantic_search': 1.0,
            'keyword_search': 0.8,
        }
        
        for result in unique_results:
            level = result.get('level', 'semantic_search')
            weight = level_weights.get(level, 1.0)
            result['weighted_score'] = result['score'] * weight
        
        # Sort by weighted score
        unique_results.sort(key=lambda x: x['weighted_score'], reverse=True)
        
        # Apply diversity (from EmbeddingOptimizer)
        from .embedding_optimizer import EmbeddingOptimizer
        diverse_results = EmbeddingOptimizer.rerank_by_diversity(
            unique_results,
            top_k=top_k,
            diversity_weight=0.2
        )
        
        return diverse_results
```

---

## 🪟 Context Window Management

### Context Budget Optimizer

```python
# backend/src/services/rag/context_optimizer.py

from typing import List, Dict, Tuple
import tiktoken
import logging

logger = logging.getLogger(__name__)

class ContextWindowOptimizer:
    """
    Optimize context to fit within LLM's context window
    
    Target Context Budget: 4000 tokens (for 8k context models)
    
    Allocation:
    - System Prompt: 500 tokens
    - Project Summary: 300 tokens
    - Retrieved Chunks: 2000 tokens
    - Conversation History: 1000 tokens
    - User Query: 200 tokens
    """
    
    def __init__(
        self,
        max_context_tokens: int = 4000,
        tokenizer_name: str = 'cl100k_base'  # GPT-4 tokenizer
    ):
        self.max_context_tokens = max_context_tokens
        self.tokenizer = tiktoken.get_encoding(tokenizer_name)
        
        # Token budget allocation
        self.budget = {
            'system_prompt': 500,
            'project_summary': 300,
            'retrieved_chunks': 2000,
            'conversation_history': 1000,
            'user_query': 200,
        }
    
    def optimize_context(
        self,
        system_prompt: str,
        project_summary: str,
        retrieved_chunks: List[Dict],
        conversation_history: List[Dict],
        user_query: str
    ) -> Dict:
        """
        Optimize all context components to fit in budget
        
        Returns:
            Optimized context with token counts
        """
        
        # Tokenize all components
        system_tokens = self._count_tokens(system_prompt)
        summary_tokens = self._count_tokens(project_summary)
        query_tokens = self._count_tokens(user_query)
        
        # Start with fixed components
        used_tokens = system_tokens + query_tokens
        
        # Optimize project summary
        if summary_tokens > self.budget['project_summary']:
            project_summary = self._truncate_to_budget(
                project_summary,
                self.budget['project_summary']
            )
            summary_tokens = self._count_tokens(project_summary)
        
        used_tokens += summary_tokens
        
        # Optimize conversation history
        optimized_history, history_tokens = self._optimize_conversation_history(
            conversation_history,
            self.budget['conversation_history']
        )
        
        used_tokens += history_tokens
        
        # Optimize retrieved chunks (most important!)
        available_for_chunks = self.max_context_tokens - used_tokens
        optimized_chunks, chunk_tokens = self._optimize_chunks(
            retrieved_chunks,
            available_for_chunks
        )
        
        used_tokens += chunk_tokens
        
        logger.info(
            f"Context optimized: {used_tokens}/{self.max_context_tokens} tokens "
            f"(chunks: {chunk_tokens}, history: {history_tokens})"
        )
        
        return {
            'system_prompt': system_prompt,
            'project_summary': project_summary,
            'retrieved_chunks': optimized_chunks,
            'conversation_history': optimized_history,
            'user_query': user_query,
            'token_usage': {
                'system_prompt': system_tokens,
                'project_summary': summary_tokens,
                'retrieved_chunks': chunk_tokens,
                'conversation_history': history_tokens,
                'user_query': query_tokens,
                'total': used_tokens,
                'max': self.max_context_tokens,
                'utilization': round(used_tokens / self.max_context_tokens, 2),
            }
        }
    
    def _optimize_chunks(
        self,
        chunks: List[Dict],
        token_budget: int
    ) -> Tuple[List[Dict], int]:
        """
        Optimize retrieved chunks to fit in budget
        
        Strategy:
        1. Prioritize by relevance score
        2. Add chunks until budget exceeded
        3. Include surrounding context when possible
        """
        
        if not chunks:
            return [], 0
        
        optimized = []
        used_tokens = 0
        
        for chunk in chunks:
            content = chunk['content']
            chunk_tokens = self._count_tokens(content)
            
            # Add surrounding context (imports, class definition)
            enhanced_content = self._add_surrounding_context(chunk)
            enhanced_tokens = self._count_tokens(enhanced_content)
            
            # Check if we can fit enhanced version
            if used_tokens + enhanced_tokens <= token_budget:
                optimized.append({
                    **chunk,
                    'content': enhanced_content,
                    'tokens': enhanced_tokens,
                    'enhanced': True,
                })
                used_tokens += enhanced_tokens
            
            # Otherwise try basic version
            elif used_tokens + chunk_tokens <= token_budget:
                optimized.append({
                    **chunk,
                    'tokens': chunk_tokens,
                    'enhanced': False,
                })
                used_tokens += chunk_tokens
            
            # No more space
            else:
                break
        
        logger.debug(
            f"Optimized chunks: {len(optimized)}/{len(chunks)} chunks, "
            f"{used_tokens} tokens"
        )
        
        return optimized, used_tokens
    
    def _add_surrounding_context(self, chunk: Dict) -> str:
        """
        Add surrounding context to chunk
        
        Examples:
        - Add import statements
        - Add class definition if method
        - Add function signature if inside function
        """
        
        content = chunk['content']
        metadata = chunk.get('metadata', {})
        
        context_parts = []
        
        # Add file path as comment
        if 'file_path' in metadata:
            context_parts.append(f"// File: {metadata['file_path']}")
        
        # Add imports if available
        if 'imports' in metadata and metadata['imports']:
            imports = metadata['imports'][:5]  # Top 5 imports
            for imp in imports:
                context_parts.append(f"import {imp};")
        
        # Add parent context (class name, etc.)
        if 'parent_context' in metadata and metadata['parent_context']:
            context_parts.append(f"// In class: {metadata['parent_context']}")
        
        # Add the actual content
        context_parts.append(content)
        
        return '\n'.join(context_parts)
    
    def _optimize_conversation_history(
        self,
        history: List[Dict],
        token_budget: int
    ) -> Tuple[List[Dict], int]:
        """
        Optimize conversation history
        
        Strategy:
        - Keep most recent messages
        - Summarize older messages if needed
        """
        
        if not history:
            return [], 0
        
        optimized = []
        used_tokens = 0
        
        # Add messages in reverse (most recent first)
        for message in reversed(history):
            content = message['content']
            tokens = self._count_tokens(content)
            
            if used_tokens + tokens <= token_budget:
                optimized.insert(0, message)
                used_tokens += tokens
            else:
                # Budget exceeded
                break
        
        logger.debug(
            f"Conversation history: {len(optimized)}/{len(history)} messages, "
            f"{used_tokens} tokens"
        )
        
        return optimized, used_tokens
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            return len(self.tokenizer.encode(text))
        except:
            # Fallback: rough approximation
            return len(text.split()) * 1.3
    
    def _truncate_to_budget(self, text: str, budget: int) -> str:
        """Truncate text to fit token budget"""
        tokens = self.tokenizer.encode(text)
        
        if len(tokens) <= budget:
            return text
        
        # Truncate tokens
        truncated_tokens = tokens[:budget - 10]  # Leave room for "..."
        
        # Decode back to text
        truncated_text = self.tokenizer.decode(truncated_tokens)
        
        return truncated_text + '...'
```

---

## 🎯 Relevance Scoring

### Advanced Relevance Scoring System

```python
# backend/src/services/rag/relevance_scorer.py

from typing import List, Dict, Optional
import numpy as np
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ScoringWeights:
    """Weights for different scoring factors"""
    semantic_similarity: float = 0.4
    keyword_match: float = 0.2
    recency: float = 0.1
    file_importance: float = 0.15
    symbol_match: float = 0.15

class RelevanceScorer:
    """
    Advanced relevance scoring combining multiple signals
    
    Scoring Factors:
    1. Semantic similarity (vector search)
    2. Keyword match (lexical overlap)
    3. Recency (recently edited files)
    4. File importance (based on dependencies, size)
    5. Symbol match (exact function/class name match)
    """
    
    def __init__(self, weights: Optional[ScoringWeights] = None):
        self.weights = weights or ScoringWeights()
        
        # Normalize weights to sum to 1.0
        total = sum([
            self.weights.semantic_similarity,
            self.weights.keyword_match,
            self.weights.recency,
            self.weights.file_importance,
            self.weights.symbol_match,
        ])
        
        self.weights.semantic_similarity /= total
        self.weights.keyword_match /= total
        self.weights.recency /= total
        self.weights.file_importance /= total
        self.weights.symbol_match /= total
    
    def score_results(
        self,
        results: List[Dict],
        query: str,
        user_context: Dict,
        file_importance_map: Optional[Dict[str, float]] = None
    ) -> List[Dict]:
        """
        Score and re-rank results
        
        Args:
            results: Initial results from retrieval
            query: User query
            user_context: User context (current file, recent files, etc.)
            file_importance_map: Pre-computed file importance scores
            
        Returns:
            Re-ranked results with detailed scores
        """
        
        if file_importance_map is None:
            file_importance_map = {}
        
        # Extract query keywords
        query_keywords = self._extract_keywords(query)
        
        # Score each result
        for result in results:
            scores = {}
            
            # 1. Semantic similarity (already computed)
            semantic_score = result.get('score', 0.0)
            scores['semantic'] = semantic_score
            
            # 2. Keyword match score
            keyword_score = self._calculate_keyword_score(
                result['content'],
                query_keywords
            )
            scores['keyword'] = keyword_score
            
            # 3. Recency score
            recency_score = self._calculate_recency_score(
                result,
                user_context
            )
            scores['recency'] = recency_score
            
            # 4. File importance score
            file_path = result['metadata'].get('file_path', '')
            importance_score = file_importance_map.get(file_path, 0.5)
            scores['file_importance'] = importance_score
            
            # 5. Symbol match score
            symbol_score = self._calculate_symbol_score(
                result,
                query
            )
            scores['symbol'] = symbol_score
            
            # Calculate weighted final score
            final_score = (
                scores['semantic'] * self.weights.semantic_similarity +
                scores['keyword'] * self.weights.keyword_match +
                scores['recency'] * self.weights.recency +
                scores['file_importance'] * self.weights.file_importance +
                scores['symbol'] * self.weights.symbol_match
            )
            
            result['relevance_score'] = round(final_score, 4)
            result['score_breakdown'] = scores
            
            logger.debug(
                f"Scored {file_path}: {final_score:.3f} "
                f"(sem:{semantic_score:.2f}, kw:{keyword_score:.2f}, "
                f"rec:{recency_score:.2f}, imp:{importance_score:.2f}, "
                f"sym:{symbol_score:.2f})"
            )
        
        # Re-sort by final score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        # Remove stop words
        stop_words = {
            'how', 'does', 'what', 'is', 'the', 'a', 'an', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'this', 'that', 'these',
            'those', 'work', 'works', 'working', 'use', 'used', 'using', 'can',
            'could', 'should', 'would', 'do', 'are', 'was', 'were', 'been'
        }
        
        # Tokenize and filter
        words = query.lower().split()
        keywords = [
            word.strip('.,!?;:')
            for word in words
            if word.lower() not in stop_words and len(word) > 2
        ]
        
        return keywords
    
    def _calculate_keyword_score(
        self,
        content: str,
        keywords: List[str]
    ) -> float:
        """
        Calculate keyword match score using BM25-like formula
        
        Returns score between 0 and 1
        """
        if not keywords:
            return 0.0
        
        content_lower = content.lower()
        
        # Count keyword occurrences
        matches = 0
        total_occurrences = 0
        
        for keyword in keywords:
            count = content_lower.count(keyword.lower())
            if count > 0:
                matches += 1
                total_occurrences += count
        
        # Calculate score
        # Match ratio: how many keywords found
        match_ratio = matches / len(keywords)
        
        # Frequency score: how often keywords appear (with diminishing returns)
        freq_score = min(total_occurrences / (len(keywords) * 3), 1.0)
        
        # Combine
        score = (match_ratio * 0.7) + (freq_score * 0.3)
        
        return min(score, 1.0)
    
    def _calculate_recency_score(
        self,
        result: Dict,
        user_context: Dict
    ) -> float:
        """
        Calculate recency score based on user's recent activity
        
        Returns score between 0 and 1
        """
        file_path = result['metadata'].get('file_path', '')
        
        score = 0.5  # Base score
        
        # Check if current file
        if 'current_file' in user_context:
            if file_path == user_context['current_file']:
                score = 1.0
                return score
        
        # Check if in recent files
        if 'recent_files' in user_context:
            recent_files = user_context['recent_files']
            if file_path in recent_files:
                # More recent = higher score
                position = recent_files.index(file_path)
                score = 0.9 - (position * 0.1)
                score = max(score, 0.6)
                return score
        
        # Check if in current directory
        if 'current_directory' in user_context:
            current_dir = user_context['current_directory']
            if file_path.startswith(current_dir):
                score = 0.7
        
        return score
    
    def _calculate_symbol_score(
        self,
        result: Dict,
        query: str
    ) -> float:
        """
        Calculate symbol match score
        
        Higher score if query mentions exact symbols (functions, classes)
        """
        symbols = result['metadata'].get('symbols', [])
        
        if not symbols:
            return 0.0
        
        query_lower = query.lower()
        
        # Check for exact symbol name matches
        matches = 0
        for symbol in symbols:
            if symbol.lower() in query_lower:
                matches += 1
        
        if matches == 0:
            return 0.0
        
        # Score based on match ratio
        score = min(matches / len(symbols), 1.0)
        
        # Boost if multiple matches
        if matches > 1:
            score = min(score * 1.2, 1.0)
        
        return score
    
    def calculate_file_importance(
        self,
        file_path: str,
        dependency_graph: Dict,
        metadata: Dict
    ) -> float:
        """
        Calculate file importance score
        
        Factors:
        - Number of imports/dependencies
        - File size (moderate size preferred)
        - File type (entry points, configs)
        """
        
        score = 0.5  # Base score
        
        # 1. Dependency importance
        incoming = dependency_graph.get(file_path, {}).get('incoming', [])
        outgoing = dependency_graph.get(file_path, {}).get('outgoing', [])
        
        # Files with many imports are important
        dependency_score = min(len(incoming) / 10, 0.3)
        score += dependency_score
        
        # 2. Entry point detection
        entry_points = ['index.ts', 'main.py', 'App.tsx', 'main.dart', '__init__.py']
        if any(ep in file_path for ep in entry_points):
            score += 0.2
        
        # 3. File size (prefer moderate size)
        file_size = metadata.get('file_size', 0)
        if 100 < file_size < 10000:  # Between 100 and 10k lines
            score += 0.1
        
        return min(score, 1.0)


class RelevanceEvaluator:
    """Evaluate relevance of retrieved results"""
    
    @staticmethod
    def calculate_precision_at_k(
        results: List[Dict],
        ground_truth: List[str],
        k: int = 5
    ) -> float:
        """
        Calculate Precision@K
        
        Args:
            results: Retrieved results
            ground_truth: List of relevant document IDs
            k: Number of top results to consider
            
        Returns:
            Precision score (0-1)
        """
        top_k = results[:k]
        relevant_count = sum(
            1 for result in top_k
            if result['id'] in ground_truth
        )
        
        return relevant_count / k if k > 0 else 0.0
    
    @staticmethod
    def calculate_recall_at_k(
        results: List[Dict],
        ground_truth: List[str],
        k: int = 10
    ) -> float:
        """
        Calculate Recall@K
        
        Args:
            results: Retrieved results
            ground_truth: List of relevant document IDs
            k: Number of top results to consider
            
        Returns:
            Recall score (0-1)
        """
        if not ground_truth:
            return 0.0
        
        top_k = results[:k]
        retrieved_relevant = [
            result['id'] for result in top_k
            if result['id'] in ground_truth
        ]
        
        return len(retrieved_relevant) / len(ground_truth)
    
    @staticmethod
    def calculate_mrr(
        results: List[Dict],
        ground_truth: List[str]
    ) -> float:
        """
        Calculate Mean Reciprocal Rank
        
        Returns:
            MRR score (0-1)
        """
        for rank, result in enumerate(results, 1):
            if result['id'] in ground_truth:
                return 1.0 / rank
        
        return 0.0
```

---

## 🔧 Query Optimization

### Query Enhancement & Expansion

```python
# backend/src/services/rag/query_optimizer.py

from typing import List, Dict, Optional
import re
import logging

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """
    Optimize and enhance user queries for better retrieval
    
    Techniques:
    1. Query expansion (add synonyms, related terms)
    2. Entity extraction (file names, function names)
    3. Intent detection (what is user trying to do?)
    4. Query reformulation (improve clarity)
    """
    
    def __init__(self):
        # Code-specific synonyms
        self.synonyms = {
            'auth': ['authentication', 'login', 'authorization', 'access'],
            'db': ['database', 'storage', 'persistence'],
            'api': ['endpoint', 'route', 'service', 'interface'],
            'ui': ['interface', 'view', 'component', 'screen'],
            'config': ['configuration', 'settings', 'options'],
            'test': ['testing', 'spec', 'unit test'],
        }
        
        # Common abbreviations
        self.abbreviations = {
            'fn': 'function',
            'func': 'function',
            'cls': 'class',
            'var': 'variable',
            'const': 'constant',
            'param': 'parameter',
            'arg': 'argument',
            'ret': 'return',
            'err': 'error',
            'resp': 'response',
            'req': 'request',
        }
    
    def optimize_query(
        self,
        query: str,
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Optimize query for better retrieval
        
        Returns:
            {
                'original': original query,
                'optimized': optimized query,
                'expanded_terms': list of added terms,
                'entities': extracted entities,
                'intent': detected intent
            }
        """
        
        # 1. Detect intent
        intent = self._detect_intent(query)
        
        # 2. Extract entities (file names, function names)
        entities = self._extract_entities(query)
        
        # 3. Expand abbreviations
        expanded_query = self._expand_abbreviations(query)
        
        # 4. Add synonyms/related terms
        expanded_terms = self._expand_with_synonyms(expanded_query)
        
        # 5. Add context if available
        if user_context:
            expanded_query = self._add_context(expanded_query, user_context)
        
        # 6. Reformulate for clarity
        optimized_query = self._reformulate(expanded_query, intent)
        
        logger.info(
            f"Query optimization: '{query}' -> '{optimized_query}' "
            f"(intent: {intent}, entities: {len(entities)})"
        )
        
        return {
            'original': query,
            'optimized': optimized_query,
            'expanded_terms': expanded_terms,
            'entities': entities,
            'intent': intent,
        }
    
    def _detect_intent(self, query: str) -> str:
        """
        Detect user intent
        
        Intents:
        - explain: User wants explanation
        - implement: User wants to implement something
        - debug: User has a problem
        - find: User is looking for specific code
        - learn: User wants to understand how something works
        """
        
        query_lower = query.lower()
        
        # Explain intent
        if any(word in query_lower for word in ['what', 'explain', 'how does', 'describe']):
            return 'explain'
        
        # Implement intent
        if any(word in query_lower for word in ['create', 'add', 'implement', 'build', 'make']):
            return 'implement'
        
        # Debug intent
        if any(word in query_lower for word in ['error', 'bug', 'issue', 'problem', 'fix', 'broken']):
            return 'debug'
        
        # Find intent
        if any(word in query_lower for word in ['where', 'find', 'locate', 'show me']):
            return 'find'
        
        # Learn intent
        if any(word in query_lower for word in ['learn', 'understand', 'tutorial', 'example']):
            return 'learn'
        
        return 'general'
    
    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        """
        Extract entities from query
        
        Entities:
        - File names (*.ts, *.py, etc.)
        - Function names (camelCase, snake_case)
        - Class names (PascalCase)
        - Paths (src/components/...)
        """
        
        entities = {
            'files': [],
            'functions': [],
            'classes': [],
            'paths': [],
        }
        
        # Extract file names
        file_pattern = r'\b[\w-]+\.(ts|tsx|js|jsx|py|kt|dart|swift|java)\b'
        files = re.findall(file_pattern, query, re.IGNORECASE)
        entities['files'] = [f[0] for f in files] if files else []
        
        # Extract PascalCase (likely class names)
        pascal_pattern = r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b'
        classes = re.findall(pascal_pattern, query)
        entities['classes'] = classes
        
        # Extract camelCase and snake_case (likely function names)
        camel_pattern = r'\b[a-z]+[A-Z][a-zA-Z]*\b'
        snake_pattern = r'\b[a-z]+_[a-z_]+\b'
        
        camel_case = re.findall(camel_pattern, query)
        snake_case = re.findall(snake_pattern, query)
        entities['functions'] = camel_case + snake_case
        
        # Extract paths
        path_pattern = r'[\w-]+/[\w-/]+'
        paths = re.findall(path_pattern, query)
        entities['paths'] = paths
        
        return entities
    
    def _expand_abbreviations(self, query: str) -> str:
        """Expand common abbreviations"""
        expanded = query
        
        for abbr, full in self.abbreviations.items():
            # Replace whole words only
            pattern = r'\b' + abbr + r'\b'
            expanded = re.sub(pattern, full, expanded, flags=re.IGNORECASE)
        
        return expanded
    
    def _expand_with_synonyms(self, query: str) -> List[str]:
        """
        Add synonyms for better recall
        
        Returns list of additional search terms
        """
        expanded_terms = []
        query_lower = query.lower()
        
        for term, synonyms in self.synonyms.items():
            if term in query_lower:
                expanded_terms.extend(synonyms)
        
        return expanded_terms
    
    def _add_context(self, query: str, user_context: Dict) -> str:
        """Add user context to query"""
        context_parts = [query]
        
        # Add current file context
        if 'current_file' in user_context and user_context['current_file']:
            file_name = user_context['current_file'].split('/')[-1]
            context_parts.append(f"in context of {file_name}")
        
        # Add language context
        if 'language' in user_context:
            context_parts.append(f"for {user_context['language']}")
        
        return ' '.join(context_parts)
    
    def _reformulate(self, query: str, intent: str) -> str:
        """
        Reformulate query based on intent for better retrieval
        """
        
        # Add intent-specific prefixes for better embedding
        if intent == 'explain':
            return f"Explain how this works: {query}"
        elif intent == 'implement':
            return f"Code implementation for: {query}"
        elif intent == 'debug':
            return f"Debug and fix: {query}"
        elif intent == 'find':
            return f"Find code related to: {query}"
        
        return query
    
    def generate_multi_queries(self, query: str, count: int = 3) -> List[str]:
        """
        Generate multiple query variants for better coverage
        
        Technique: Multi-Query Retrieval
        """
        
        variants = [query]  # Original
        
        # Variant 1: More specific
        specific = f"specific implementation of {query}"
        variants.append(specific)
        
        # Variant 2: More general
        words = query.split()
        if len(words) > 3:
            general = ' '.join(words[:3])
            variants.append(general)
        
        # Variant 3: Question form
        if not query.lower().startswith(('what', 'how', 'where', 'why')):
            question = f"how does {query} work"
            variants.append(question)
        
        return variants[:count]
```

---

## 🔀 Hybrid Search

### Hybrid Search Implementation

```python
# backend/src/services/rag/hybrid_search.py

from typing import List, Dict, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)

class HybridSearchService:
    """
    Hybrid search combining semantic and lexical search
    
    Methods:
    1. Dense retrieval (semantic vectors)
    2. Sparse retrieval (BM25, TF-IDF)
    3. Fusion (RRF - Reciprocal Rank Fusion)
    """
    
    def __init__(
        self,
        vector_search,
        lexical_search,
        fusion_weight: float = 0.5
    ):
        self.vector_search = vector_search
        self.lexical_search = lexical_search
        self.fusion_weight = fusion_weight  # Weight for semantic vs lexical
    
    async def hybrid_search(
        self,
        query: str,
        query_embedding: np.ndarray,
        top_k: int = 10,
        semantic_weight: float = 0.7,
        lexical_weight: float = 0.3
    ) -> List[Dict]:
        """
        Perform hybrid search
        
        Args:
            query: Text query
            query_embedding: Query embedding vector
            top_k: Number of results
            semantic_weight: Weight for semantic search
            lexical_weight: Weight for lexical search
            
        Returns:
            Fused and ranked results
        """
        
        # 1. Semantic search
        semantic_results = await self.vector_search.search(
            query_embedding,
            top_k=top_k * 2  # Get more for fusion
        )
        
        # 2. Lexical search (BM25)
        lexical_results = await self.lexical_search.search(
            query,
            top_k=top_k * 2
        )
        
        # 3. Fuse results using RRF
        fused_results = self._reciprocal_rank_fusion(
            semantic_results,
            lexical_results,
            semantic_weight,
            lexical_weight
        )
        
        # 4. Return top-k
        return fused_results[:top_k]
    
    def _reciprocal_rank_fusion(
        self,
        semantic_results: List[Dict],
        lexical_results: List[Dict],
        semantic_weight: float = 0.7,
        lexical_weight: float = 0.3,
        k: int = 60
    ) -> List[Dict]:
        """
        Reciprocal Rank Fusion (RRF)
        
        Formula: score(d) = Σ (1 / (k + rank(d)))
        
        Args:
            semantic_results: Results from semantic search
            lexical_results: Results from lexical search
            semantic_weight: Weight for semantic scores
            lexical_weight: Weight for lexical scores
            k: Constant (typically 60)
            
        Returns:
            Fused results sorted by combined score
        """
        
        # Build score maps
        scores = {}
        
        # Add semantic scores
        for rank, result in enumerate(semantic_results, 1):
            doc_id = result['id']
            rrf_score = semantic_weight / (k + rank)
            
            if doc_id not in scores:
                scores[doc_id] = {
                    'result': result,
                    'rrf_score': 0,
                    'semantic_rank': None,
                    'lexical_rank': None,
                }
            
            scores[doc_id]['rrf_score'] += rrf_score
            scores[doc_id]['semantic_rank'] = rank
        
        # Add lexical scores
        for rank, result in enumerate(lexical_results, 1):
            doc_id = result['id']
            rrf_score = lexical_weight / (k + rank)
            
            if doc_id not in scores:
                scores[doc_id] = {
                    'result': result,
                    'rrf_score': 0,
                    'semantic_rank': None,
                    'lexical_rank': None,
                }
            
            scores[doc_id]['rrf_score'] += rrf_score
            scores[doc_id]['lexical_rank'] = rank
        
        # Sort by RRF score
        sorted_results = sorted(
            scores.values(),
            key=lambda x: x['rrf_score'],
            reverse=True
        )
        
        # Format results
        fused = []
        for item in sorted_results:
            result = item['result'].copy()
            result['hybrid_score'] = round(item['rrf_score'], 4)
            result['semantic_rank'] = item['semantic_rank']
            result['lexical_rank'] = item['lexical_rank']
            fused.append(result)
        
        logger.debug(
            f"Hybrid fusion: {len(fused)} unique results "
            f"(semantic: {len(semantic_results)}, lexical: {len(lexical_results)})"
        )
        
        return fused


class LexicalSearchService:
    """
    BM25-based lexical search for exact term matching
    """
    
    def __init__(self, metadata_store):
        self.metadata_store = metadata_store
        # In production, use proper BM25 implementation (e.g., rank_bm25)
    
    async def search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Dict]:
        """
        BM25 search
        
        Note: Simplified implementation
        In production, use rank_bm25 or Elasticsearch
        """
        
        # Extract query terms
        query_terms = query.lower().split()
        
        # Retrieve all documents (in production, use inverted index)
        all_docs = await self.metadata_store.get_all_chunks()
        
        # Score documents
        scored = []
        for doc in all_docs:
            score = self._bm25_score(doc['content'], query_terms)
            if score > 0:
                scored.append({
                    'id': doc['id'],
                    'content': doc['content'],
                    'metadata': doc['metadata'],
                    'score': score,
                })
        
        # Sort and return top-k
        scored.sort(key=lambda x: x['score'], reverse=True)
        
        return scored[:top_k]
    
    def _bm25_score(
        self,
        document: str,
        query_terms: List[str],
        k1: float = 1.5,
        b: float = 0.75
    ) -> float:
        """
        Simplified BM25 scoring
        
        In production, use proper BM25 with:
        - Document frequency (DF)
        - Inverse document frequency (IDF)
        - Average document length
        """
        
        doc_lower = document.lower()
        doc_terms = doc_lower.split()
        doc_len = len(doc_terms)
        
        # Simplified score: term frequency
        score = 0.0
        
        for term in query_terms:
            tf = doc_terms.count(term)
            if tf > 0:
                # Simplified BM25 (without IDF)
                score += (tf * (k1 + 1)) / (tf + k1)
        
        return score
```

---

## ⚡ Performance Optimization

### RAG Performance Optimizer

```python
# backend/src/services/rag/performance_optimizer.py

import time
import asyncio
from typing import List, Dict, Callable
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RAGPerformanceOptimizer:
    """Optimize RAG system performance"""
    
    def __init__(self):
        self.metrics = {
            'query_times': [],
            'embedding_times': [],
            'search_times': [],
            'total_queries': 0,
        }
    
    @staticmethod
    def timed(operation_name: str):
        """Decorator to time operations"""
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                start = time.time()
                result = await func(self, *args, **kwargs)
                duration = time.time() - start
                
                logger.debug(f"{operation_name}: {duration*1000:.2f}ms")
                
                # Store metric
                if hasattr(self, 'metrics'):
                    metric_key = f"{operation_name}_times"
                    if metric_key not in self.metrics:
                        self.metrics[metric_key] = []
                    self.metrics[metric_key].append(duration)
                
                return result
            return wrapper
        return decorator
    
    async def parallel_search(
        self,
        query_variants: List[str],
        search_func: Callable
    ) -> List[Dict]:
        """
        Execute multiple search queries in parallel
        
        Useful for multi-query retrieval
        """
        
        # Execute searches in parallel
        tasks = [search_func(query) for query in query_variants]
        results_list = await asyncio.gather(*tasks)
        
        # Deduplicate and merge
        seen_ids = set()
        merged = []
        
        for results in results_list:
            for result in results:
                if result['id'] not in seen_ids:
                    seen_ids.add(result['id'])
                    merged.append(result)
        
        # Re-sort by score
        merged.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return merged
    
    async def batch_embed_with_cache(
        self,
        texts: List[str],
        embed_func: Callable,
        cache: Dict
    ) -> List:
        """
        Batch embedding with caching
        """
        
        embeddings = []
        to_embed = []
        to_embed_indices = []
        
        # Check cache
        for i, text in enumerate(texts):
            cache_key = hash(text)
            if cache_key in cache:
                embeddings.append(cache[cache_key])
            else:
                embeddings.append(None)
                to_embed.append(text)
                to_embed_indices.append(i)
        
        # Embed uncached texts
        if to_embed:
            new_embeddings = await embed_func(to_embed)
            
            # Store in cache and results
            for idx, embedding in zip(to_embed_indices, new_embeddings):
                cache_key = hash(texts[idx])
                cache[cache_key] = embedding
                embeddings[idx] = embedding
        
        return embeddings
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        stats = {}
        
        for metric_name, times in self.metrics.items():
            if times:
                stats[metric_name] = {
                    'avg_ms': round(sum(times) / len(times) * 1000, 2),
                    'min_ms': round(min(times) * 1000, 2),
                    'max_ms': round(max(times) * 1000, 2),
                    'count': len(times),
                }
        
        return stats
    
    def suggest_optimizations(self, stats: Dict) -> List[str]:
        """Suggest optimizations based on stats"""
        suggestions = []
        
        # Check embedding time
        if 'embedding_times' in stats:
            avg_embed = stats['embedding_times']['avg_ms']
            if avg_embed > 500:
                suggestions.append(
                    f"Embedding is slow ({avg_embed:.0f}ms avg). "
                    "Consider: 1) Using GPU, 2) Smaller model, 3) Caching queries"
                )
        
        # Check search time
        if 'search_times' in stats:
            avg_search = stats['search_times']['avg_ms']
            if avg_search > 200:
                suggestions.append(
                    f"Vector search is slow ({avg_search:.0f}ms avg). "
                    "Consider: 1) Reducing index size, 2) HNSW optimization, "
                    "3) Using approximate search"
                )
        
        # Check total query time
        if 'query_times' in stats:
            avg_query = stats['query_times']['avg_ms']
            if avg_query > 1000:
                suggestions.append(
                    f"Total query time exceeds 1s ({avg_query:.0f}ms avg). "
                    "Consider: 1) Parallel operations, 2) Caching, 3) Reducing top_k"
                )
        
        return suggestions
```

---

## 💾 Caching Strategies

### Multi-Level Caching System

```python
# backend/src/services/rag/cache_manager.py

from typing import Dict, Any, Optional
import hashlib
import json
import time
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    timestamp: float
    ttl: float  # Time to live in seconds
    hits: int = 0
    
    @property
    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl
    
    @property
    def age_seconds(self) -> float:
        return time.time() - self.timestamp

class RAGCacheManager:
    """
    Multi-level caching for RAG system
    
    Cache Levels:
    1. Query cache (frequently asked questions)
    2. Embedding cache (query embeddings)
    3. Results cache (retrieval results)
    4. Context cache (assembled contexts)
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: float = 3600  # 1 hour
    ):
        self.max_size = max_size
        self.default_ttl = default_ttl
        
        # Separate caches for different types
        self.query_cache: Dict[str, CacheEntry] = {}
        self.embedding_cache: Dict[str, CacheEntry] = {}
        self.results_cache: Dict[str, CacheEntry] = {}
        self.context_cache: Dict[str, CacheEntry] = {}
        
        # Statistics
        self.stats = {
            'query_hits': 0,
            'query_misses': 0,
            'embedding_hits': 0,
            'embedding_misses': 0,
            'results_hits': 0,
            'results_misses': 0,
            'context_hits': 0,
            'context_misses': 0,
        }
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs,
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_query_embedding(self, query: str) -> Optional[Any]:
        """Get cached query embedding"""
        key = self._generate_key(query)
        
        if key in self.embedding_cache:
            entry = self.embedding_cache[key]
            
            if not entry.is_expired:
                entry.hits += 1
                self.stats['embedding_hits'] += 1
                logger.debug(f"Embedding cache HIT: {query[:50]}...")
                return entry.value
            else:
                # Remove expired entry
                del self.embedding_cache[key]
        
        self.stats['embedding_misses'] += 1
        return None
    
    def set_query_embedding(
        self,
        query: str,
        embedding: Any,
        ttl: Optional[float] = None
    ):
        """Cache query embedding"""
        key = self._generate_key(query)
        
        entry = CacheEntry(
            key=key,
            value=embedding,
            timestamp=time.time(),
            ttl=ttl or self.default_ttl
        )
        
        self.embedding_cache[key] = entry
        self._evict_if_needed(self.embedding_cache)
    
    def get_results(
        self,
        query: str,
        user_context: Dict,
        top_k: int
    ) -> Optional[List[Dict]]:
        """Get cached retrieval results"""
        key = self._generate_key(query, user_context, top_k)
        
        if key in self.results_cache:
            entry = self.results_cache[key]
            
            if not entry.is_expired:
                entry.hits += 1
                self.stats['results_hits'] += 1
                logger.debug(f"Results cache HIT: {query[:50]}...")
                return entry.value
            else:
                del self.results_cache[key]
        
        self.stats['results_misses'] += 1
        return None
    
    def set_results(
        self,
        query: str,
        user_context: Dict,
        top_k: int,
        results: List[Dict],
        ttl: Optional[float] = None
    ):
        """Cache retrieval results"""
        key = self._generate_key(query, user_context, top_k)
        
        entry = CacheEntry(
            key=key,
            value=results,
            timestamp=time.time(),
            ttl=ttl or self.default_ttl
        )
        
        self.results_cache[key] = entry
        self._evict_if_needed(self.results_cache)
    
    def invalidate_on_index_update(self):
        """Invalidate all caches when index is updated"""
        logger.info("Invalidating all RAG caches due to index update")
        
        self.results_cache.clear()
        self.context_cache.clear()
        # Keep embedding cache (still valid)
    
    def _evict_if_needed(self, cache: Dict[str, CacheEntry]):
        """Evict entries if cache is full (LRU)"""
        if len(cache) >= self.max_size:
            # Sort by hits (keep frequently used) and age
            sorted_entries = sorted(
                cache.items(),
                key=lambda x: (x[1].hits, -x[1].age_seconds)
            )
            
            # Remove least used, oldest entries
            to_remove = len(cache) - int(self.max_size * 0.9)
            for key, _ in sorted_entries[:to_remove]:
                del cache[key]
            
            logger.debug(f"Cache eviction: removed {to_remove} entries")
    
    def get_statistics(self) -> Dict:
        """Get cache statistics"""
        total_hits = sum(v for k, v in self.stats.items() if 'hits' in k)
        total_misses = sum(v for k, v in self.stats.items() if 'misses' in k)
        total_requests = total_hits + total_misses
        
        hit_rate = total_hits / total_requests if total_requests > 0 else 0
        
        return {
            'hit_rate': round(hit_rate, 3),
            'total_hits': total_hits,
            'total_misses': total_misses,
            'cache_sizes': {
                'query': len(self.query_cache),
                'embedding': len(self.embedding_cache),
                'results': len(self.results_cache),
                'context': len(self.context_cache),
            },
            'details': self.stats,
        }
    
    def clear_all(self):
        """Clear all caches"""
        self.query_cache.clear()
        self.embedding_cache.clear()
        self.results_cache.clear()
        self.context_cache.clear()
        logger.info("All RAG caches cleared")
```

---

## 📊 Quality Metrics

### RAG Quality Evaluation System

```python
# backend/src/services/rag/quality_metrics.py

from typing import List, Dict, Optional
from dataclasses import dataclass
import numpy as np
import logging

logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """RAG quality metrics"""
    precision_at_5: float
    recall_at_10: float
    mrr: float  # Mean Reciprocal Rank
    ndcg: float  # Normalized Discounted Cumulative Gain
    context_relevance: float
    response_time_ms: float
    
    @property
    def overall_quality_score(self) -> float:
        """Weighted overall quality score"""
        return (
            self.precision_at_5 * 0.3 +
            self.recall_at_10 * 0.2 +
            self.mrr * 0.2 +
            self.ndcg * 0.15 +
            self.context_relevance * 0.15
        )

class RAGQualityEvaluator:
    """Evaluate RAG system quality"""
    
    def __init__(self):
        self.evaluation_history: List[QualityMetrics] = []
    
    def evaluate_retrieval(
        self,
        retrieved_results: List[Dict],
        ground_truth: List[str],
        response_time_ms: float
    ) -> QualityMetrics:
        """
        Comprehensive evaluation of retrieval quality
        
        Args:
            retrieved_results: Results from RAG system
            ground_truth: List of relevant document IDs
            response_time_ms: Query response time
            
        Returns:
            QualityMetrics object
        """
        
        # Calculate metrics
        precision_at_5 = self._precision_at_k(retrieved_results, ground_truth, k=5)
        recall_at_10 = self._recall_at_k(retrieved_results, ground_truth, k=10)
        mrr = self._mean_reciprocal_rank(retrieved_results, ground_truth)
        ndcg = self._ndcg(retrieved_results, ground_truth, k=10)
        context_relevance = self._context_relevance(retrieved_results)
        
        metrics = QualityMetrics(
            precision_at_5=precision_at_5,
            recall_at_10=recall_at_10,
            mrr=mrr,
            ndcg=ndcg,
            context_relevance=context_relevance,
            response_time_ms=response_time_ms
        )
        
        self.evaluation_history.append(metrics)
        
        logger.info(
            f"RAG Quality: P@5={precision_at_5:.2f}, R@10={recall_at_10:.2f}, "
            f"MRR={mrr:.2f}, Overall={metrics.overall_quality_score:.2f}"
        )
        
        return metrics
    
    def _precision_at_k(
        self,
        results: List[Dict],
        ground_truth: List[str],
        k: int
    ) -> float:
        """Calculate Precision@K"""
        top_k = results[:k]
        relevant = sum(1 for r in top_k if r['id'] in ground_truth)
        return relevant / k if k > 0 else 0.0
    
    def _recall_at_k(
        self,
        results: List[Dict],
        ground_truth: List[str],
        k: int
    ) -> float:
        """Calculate Recall@K"""
        if not ground_truth:
            return 0.0
        
        top_k = results[:k]
        retrieved_relevant = sum(1 for r in top_k if r['id'] in ground_truth)
        return retrieved_relevant / len(ground_truth)
    
    def _mean_reciprocal_rank(
        self,
        results: List[Dict],
        ground_truth: List[str]
    ) -> float:
        """Calculate MRR"""
        for rank, result in enumerate(results, 1):
            if result['id'] in ground_truth:
                return 1.0 / rank
        return 0.0
    
    def _ndcg(
        self,
        results: List[Dict],
        ground_truth: List[str],
        k: int
    ) -> float:
        """Calculate Normalized Discounted Cumulative Gain"""
        def dcg(relevances):
            return sum(
                (2 ** rel - 1) / np.log2(idx + 2)
                for idx, rel in enumerate(relevances)
            )
        
        # Actual relevance scores (1 if relevant, 0 otherwise)
        actual_relevances = [
            1 if result['id'] in ground_truth else 0
            for result in results[:k]
        ]
        
        # Ideal relevance scores (all relevant items first)
        ideal_relevances = sorted(actual_relevances, reverse=True)
        
        actual_dcg = dcg(actual_relevances)
        ideal_dcg = dcg(ideal_relevances)
        
        return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0
    
    def _context_relevance(self, results: List[Dict]) -> float:
        """
        Evaluate overall context relevance
        
        Based on diversity and score distribution
        """
        if not results:
            return 0.0
        
        scores = [r.get('score', 0) for r in results]
        
        # High scores are good
        avg_score = np.mean(scores)
        
        # Diversity: files should come from different locations
        file_paths = [r['metadata'].get('file_path', '') for r in results]
        unique_files = len(set(file_paths))
        diversity_score = unique_files / len(results) if results else 0
        
        # Combined relevance
        relevance = (avg_score * 0.7) + (diversity_score * 0.3)
        
        return min(relevance, 1.0)
    
    def get_average_metrics(self, last_n: Optional[int] = None) -> Dict:
        """Get average metrics over evaluation history"""
        if not self.evaluation_history:
            return {}
        
        history = self.evaluation_history[-last_n:] if last_n else self.evaluation_history
        
        return {
            'avg_precision_at_5': np.mean([m.precision_at_5 for m in history]),
            'avg_recall_at_10': np.mean([m.recall_at_10 for m in history]),
            'avg_mrr': np.mean([m.mrr for m in history]),
            'avg_ndcg': np.mean([m.ndcg for m in history]),
            'avg_context_relevance': np.mean([m.context_relevance for m in history]),
            'avg_response_time_ms': np.mean([m.response_time_ms for m in history]),
            'avg_overall_quality': np.mean([m.overall_quality_score for m in history]),
            'sample_size': len(history),
        }
    
    def check_quality_thresholds(self, metrics: QualityMetrics) -> Dict[str, bool]:
        """Check if metrics meet quality thresholds"""
        return {
            'precision_ok': metrics.precision_at_5 >= 0.80,
            'recall_ok': metrics.recall_at_10 >= 0.70,
            'mrr_ok': metrics.mrr >= 0.60,
            'context_relevance_ok': metrics.context_relevance >= 0.85,
            'response_time_ok': metrics.response_time_ms <= 500,
            'overall_ok': metrics.overall_quality_score >= 0.75,
        }
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and timeline
- `TECHNICAL_ARCHITECTURE.md` - System architecture
- `INDEXING_SYSTEM_SPEC.md` - Indexing pipeline (PREVIOUS)
- `MODEL_MANAGEMENT_SPEC.md` - Model swapping and VRAM
- `DEVELOPMENT_GUIDE.md` - Setup and workflow
- `TESTING_STRATEGY.md` - Test specifications
- `PHASE_1_IMPLEMENTATION.md` - Implementation roadmap (NEXT)

---

**END OF DOCUMENT**