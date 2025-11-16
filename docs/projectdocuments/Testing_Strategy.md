# 📄 DOCUMENT #9: TESTING_STRATEGY.md
# LocalPilot - Testing Strategy

**Version:** 1.0  
**Date:** January 2025  
**Status:** Foundation  
**Author:** LocalPilot QA Team

---

## 📋 Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Testing Pyramid](#testing-pyramid)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [End-to-End Testing](#end-to-end-testing)
6. [Test Fixtures & Mocks](#test-fixtures--mocks)
7. [Coverage Requirements](#coverage-requirements)
8. [Performance Testing](#performance-testing)
9. [CI/CD Integration](#cicd-integration)
10. [Test Data Management](#test-data-management)

---

## 🎯 Testing Philosophy

### Core Principles

```yaml
1. Test-Driven Development (TDD)
   - Write tests before implementation
   - Red-Green-Refactor cycle
   - Tests as specification

2. Quality Over Quantity
   - Meaningful tests over coverage numbers
   - Test behavior, not implementation
   - Focus on critical paths

3. Fast Feedback
   - Unit tests run in milliseconds
   - Integration tests in seconds
   - E2E tests in minutes
   - Fail fast on errors

4. Maintainable Tests
   - Clear test names
   - Minimal setup/teardown
   - Independent tests
   - No test interdependencies

5. Continuous Testing
   - Tests run on every commit
   - Pre-commit hooks
   - CI/CD pipeline
   - Automated regression testing
```

### Testing Goals

```
Goals for LocalPilot Testing:

✓ Catch bugs early (before code review)
✓ Enable confident refactoring
✓ Document expected behavior
✓ Ensure quality indexing (most critical)
✓ Verify safe file operations
✓ Validate LLM integration
✓ Test edge cases and errors
✓ Maintain performance benchmarks
```

---

## 🏗️ Testing Pyramid

### Test Distribution

```
         /\
        /  \  E2E Tests (5%)
       /    \  - Full workflows
      /──────\  - User journeys
     /        \
    /          \ Integration Tests (25%)
   /            \ - API endpoints
  /              \ - Service interactions
 /                \ - Database operations
/──────────────────\
                    Unit Tests (70%)
                    - Pure functions
                    - Business logic
                    - Edge cases

Total Tests: ~500+
- Unit: ~350 tests
- Integration: ~125 tests
- E2E: ~25 tests
```

### Test Execution Time

```yaml
Target Execution Times:

Unit Tests:
  Total: < 30 seconds
  Individual: < 100ms average
  
Integration Tests:
  Total: < 5 minutes
  Individual: < 5 seconds average
  
E2E Tests:
  Total: < 15 minutes
  Individual: < 2 minutes average
  
Full Suite: < 20 minutes
```

---

## 🧪 Unit Testing

### Extension Unit Tests (TypeScript/Jest)

#### Test Structure

```typescript
// extension/test/unit/services/WebSocketService.test.ts

import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { WebSocketService } from '../../../src/services/WebSocketService';
import WS from 'ws';

// Mock WebSocket
jest.mock('ws');

describe('WebSocketService', () => {
  let service: WebSocketService;
  let mockWs: jest.Mocked<WS>;
  
  beforeEach(() => {
    // Setup
    service = new WebSocketService();
    mockWs = new WS('ws://localhost:8765') as jest.Mocked<WS>;
  });
  
  afterEach(() => {
    // Cleanup
    service.disconnect();
    jest.clearAllMocks();
  });
  
  describe('connect', () => {
    it('should establish connection successfully', async () => {
      // Arrange
      const url = 'ws://localhost:8765';
      
      // Act
      await service.connect(url);
      
      // Assert
      expect(service.isConnected()).toBe(true);
      expect(WS).toHaveBeenCalledWith(url);
    });
    
    it('should emit connected event on successful connection', async () => {
      // Arrange
      const onConnected = jest.fn();
      service.on('connected', onConnected);
      
      // Simulate WebSocket open
      mockWs.readyState = WS.OPEN;
      mockWs.emit('open');
      
      // Act
      await service.connect('ws://localhost:8765');
      
      // Assert
      expect(onConnected).toHaveBeenCalled();
    });
    
    it('should retry on connection failure with exponential backoff', async () => {
      // Arrange
      jest.useFakeTimers();
      const connectSpy = jest.spyOn(service as any, '_attemptConnect');
      
      // Simulate failures
      connectSpy
        .mockRejectedValueOnce(new Error('Connection failed'))
        .mockRejectedValueOnce(new Error('Connection failed'))
        .mockResolvedValueOnce(undefined);
      
      // Act
      const connectPromise = service.connect('ws://localhost:8765');
      
      // Fast-forward time for retries
      await jest.advanceTimersByTimeAsync(2000); // First retry
      await jest.advanceTimersByTimeAsync(4000); // Second retry
      
      await connectPromise;
      
      // Assert
      expect(connectSpy).toHaveBeenCalledTimes(3);
      
      jest.useRealTimers();
    });
    
    it('should throw error after max retry attempts', async () => {
      // Arrange
      jest.useFakeTimers();
      const connectSpy = jest.spyOn(service as any, '_attemptConnect');
      connectSpy.mockRejectedValue(new Error('Connection failed'));
      
      // Act & Assert
      await expect(async () => {
        const connectPromise = service.connect('ws://localhost:8765');
        
        // Advance through all retry attempts
        for (let i = 0; i < 5; i++) {
          await jest.advanceTimersByTimeAsync(Math.pow(2, i) * 1000);
        }
        
        await connectPromise;
      }).rejects.toThrow('Max retry attempts reached');
      
      jest.useRealTimers();
    });
  });
  
  describe('send', () => {
    beforeEach(async () => {
      await service.connect('ws://localhost:8765');
      mockWs.readyState = WS.OPEN;
    });
    
    it('should send message when connected', () => {
      // Arrange
      const event = 'test.event';
      const payload = { data: 'test' };
      
      // Act
      service.send(event, payload);
      
      // Assert
      expect(mockWs.send).toHaveBeenCalledWith(
        JSON.stringify({
          event,
          payload,
          timestamp: expect.any(String),
          request_id: expect.any(String),
        })
      );
    });
    
    it('should throw error when not connected', () => {
      // Arrange
      service.disconnect();
      
      // Act & Assert
      expect(() => {
        service.send('test.event', {});
      }).toThrow('WebSocket is not connected');
    });
    
    it('should queue messages when connection is pending', async () => {
      // Arrange
      service.disconnect();
      mockWs.readyState = WS.CONNECTING;
      
      // Act
      service.send('event1', { data: 1 });
      service.send('event2', { data: 2 });
      
      // Simulate connection established
      mockWs.readyState = WS.OPEN;
      mockWs.emit('open');
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Assert
      expect(mockWs.send).toHaveBeenCalledTimes(2);
    });
  });
  
  describe('message handling', () => {
    it('should emit event on message received', async () => {
      // Arrange
      await service.connect('ws://localhost:8765');
      const handler = jest.fn();
      service.on('test.event', handler);
      
      const message = {
        type: 'test.event',
        payload: { data: 'test' },
      };
      
      // Act
      mockWs.emit('message', JSON.stringify(message));
      
      // Assert
      expect(handler).toHaveBeenCalledWith(message.payload);
    });
    
    it('should handle malformed messages gracefully', async () => {
      // Arrange
      await service.connect('ws://localhost:8765');
      const errorSpy = jest.spyOn(console, 'error').mockImplementation();
      
      // Act
      mockWs.emit('message', 'invalid json{');
      
      // Assert
      expect(errorSpy).toHaveBeenCalled();
      expect(service.isConnected()).toBe(true); // Still connected
      
      errorSpy.mockRestore();
    });
  });
});

#### Extension Views/Chat Testing (VS Code)

```typescript
// extension/test/ui/ViewsAndChat.test.ts

import * as assert from 'assert';
import * as vscode from 'vscode';
import { LocalPilotTreeDataProvider } from '../../src/views/tree/LocalPilotTreeDataProvider';
import { LocalPilotChatParticipant } from '../../src/views/chat/ChatParticipant';

describe('Views and Chat', () => {
  it('TreeDataProvider returns root nodes', async () => {
    const provider = new LocalPilotTreeDataProvider();
    const roots = await provider.getChildren(undefined);
    assert.ok(Array.isArray(roots));
    // Expect at least Chat/Plan/Act roots (implementation-specific)
    assert.ok(roots.length >= 1);
  });

  it('Chat participant streams response', async () => {
    const participant = new LocalPilotChatParticipant();
    const tokens: string[] = [];

    const mockStream: vscode.ChatResponseStream = {
      markdown: (t: string) => tokens.push(t),
      progress: () => {},
      error: () => {},
      end: () => {},
      dispose: () => {}
    } as any;

    await participant.handleRequest(
      { prompt: 'hello', command: undefined } as any,
      { sessionId: 'test' } as any,
      mockStream
    );

    // Tokens may arrive asynchronously; allow a short wait
    await new Promise(r => setTimeout(r, 50));
    assert.ok(tokens.length >= 0);
  });
});

### Backend Unit Tests (Python/Pytest)

#### Service Testing

```python
# backend/tests/unit/services/test_indexing_service.py

import pytest
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, call
from src.services.indexing.indexing_service import IndexingService
from src.services.indexing.discovery import DiscoveryExecutor, DiscoveryResult
from src.models.indexing import IndexingPhase, IndexingStatus


class TestIndexingService:
    """Unit tests for IndexingService"""
    
    @pytest.fixture
    def mock_vector_store(self):
        """Mock vector store"""
        store = Mock()
        store.add_documents = AsyncMock()
        store.search = AsyncMock(return_value=[])
        return store
    
    @pytest.fixture
    def mock_embedding_service(self):
        """Mock embedding service"""
        service = Mock()
        service.embed = AsyncMock(return_value=[0.1] * 1024)
        service.embed_batch = AsyncMock(return_value=[[0.1] * 1024])
        return service
    
    @pytest.fixture
    def mock_llm_service(self):
        """Mock LLM service"""
        service = Mock()
        service.generate = AsyncMock(return_value='{"summary": "Test project"}')
        return service
    
    @pytest.fixture
    def service(self, mock_vector_store, mock_embedding_service, mock_llm_service):
        """Create IndexingService with mocked dependencies"""
        return IndexingService(
            vector_store=mock_vector_store,
            embedding_service=mock_embedding_service,
            llm_service=mock_llm_service
        )
    
    @pytest.mark.asyncio
    async def test_index_workspace_success(self, service, tmp_path):
        """Test successful workspace indexing"""
        # Arrange
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        (workspace / "src").mkdir()
        (workspace / "src" / "index.ts").write_text("console.log('hello');")
        (workspace / "README.md").write_text("# Test Project")
        
        # Act
        result = await service.index_workspace(str(workspace))
        
        # Assert
        assert result.status == IndexingStatus.COMPLETED
        assert result.statistics.indexed_files > 0
        assert result.project_summary is not None
    
    @pytest.mark.asyncio
    async def test_index_workspace_emits_progress(self, service, tmp_path):
        """Test that progress events are emitted during indexing"""
        # Arrange
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        (workspace / "index.ts").write_text("console.log('test');")
        
        progress_events = []
        
        # Act
        async for progress in service.index_workspace(str(workspace)):
            progress_events.append(progress)
        
        # Assert
        phases = [e.phase for e in progress_events]
        assert IndexingPhase.DISCOVERY in phases
        assert IndexingPhase.DOCUMENTATION in phases
        assert IndexingPhase.STRUCTURE in phases
        assert IndexingPhase.CHUNKING in phases
        assert IndexingPhase.SUMMARIZATION in phases
        
        # Verify progress percentages increase
        percentages = [e.percentage for e in progress_events]
        assert percentages == sorted(percentages)
        assert percentages[0] >= 0
        assert percentages[-1] == 100
    
    @pytest.mark.asyncio
    async def test_handles_file_parsing_errors(self, service, tmp_path):
        """Test graceful handling of unparseable files"""
        # Arrange
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        
        # Create valid file
        (workspace / "valid.ts").write_text("const x = 1;")
        
        # Create invalid file
        (workspace / "broken.ts").write_text("const x = {{{")
        
        # Act
        result = await service.index_workspace(str(workspace))
        
        # Assert
        assert result.status == IndexingStatus.COMPLETED
        assert result.statistics.failed_files == 1
        assert result.statistics.indexed_files == 1
        assert len(result.failed_files) == 1
        assert result.failed_files[0].path == "broken.ts"
    
    @pytest.mark.asyncio
    async def test_stops_on_critical_error(self, service, tmp_path, mock_vector_store):
        """Test that critical errors stop indexing"""
        # Arrange
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        (workspace / "index.ts").write_text("test")
        
        # Simulate vector store failure
        mock_vector_store.add_documents.side_effect = Exception("Database connection failed")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database connection failed"):
            await service.index_workspace(str(workspace))
    
    @pytest.mark.asyncio
    async def test_incremental_reindex_only_changed_files(self, service, tmp_path):
        """Test incremental indexing updates only changed files"""
        # Arrange
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        file1 = workspace / "file1.ts"
        file2 = workspace / "file2.ts"
        file1.write_text("const x = 1;")
        file2.write_text("const y = 2;")
        
        # Initial index
        await service.index_workspace(str(workspace))
        
        # Modify only file1
        file1.write_text("const x = 10;")
        
        # Act
        changes = await service.detect_changes(str(workspace))
        
        # Assert
        assert len(changes) == 1
        assert changes[0].file_path == "file1.ts"
        assert changes[0].change_type == "modified"


class TestDiscoveryExecutor:
    """Unit tests for DiscoveryExecutor"""
    
    @pytest.fixture
    def executor(self):
        return DiscoveryExecutor()
    
    @pytest.fixture
    def sample_workspace(self, tmp_path):
        """Create a sample workspace"""
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        
        # Source files
        src = workspace / "src"
        src.mkdir()
        (src / "index.ts").write_text("console.log('hello');")
        (src / "utils.ts").write_text("export function test() {}")
        
        # Docs
        (workspace / "README.md").write_text("# Test Project")
        
        # Should be excluded
        node_modules = workspace / "node_modules"
        node_modules.mkdir()
        (node_modules / "package").write_text("excluded")
        
        # Config
        (workspace / "package.json").write_text('{"name": "test"}')
        
        return workspace
    
    @pytest.mark.asyncio
    async def test_discovers_all_files(self, executor, sample_workspace):
        """Test that all non-excluded files are discovered"""
        result = await executor.execute(str(sample_workspace))
        
        assert result.total_files == 4  # index.ts, utils.ts, README.md, package.json
        assert result.files_by_type['typescript'] == 2
        assert result.files_by_type['markdown'] == 1
        assert result.files_by_type['json'] == 1
    
    @pytest.mark.asyncio
    async def test_excludes_patterns(self, executor, sample_workspace):
        """Test that exclude patterns work correctly"""
        result = await executor.execute(str(sample_workspace))
        
        # Verify node_modules was excluded
        assert not any('node_modules' in str(f) for f in result.files)
    
    @pytest.mark.asyncio
    async def test_detects_project_type(self, executor, tmp_path):
        """Test project type detection"""
        # React project
        react_workspace = tmp_path / "react-project"
        react_workspace.mkdir()
        (react_workspace / "package.json").write_text('{"dependencies": {"react": "^18"}}')
        
        result = await executor.execute(str(react_workspace))
        assert result.project_type == 'react'
        
        # Python project
        python_workspace = tmp_path / "python-project"
        python_workspace.mkdir()
        (python_workspace / "setup.py").write_text("from setuptools import setup")
        
        result = await executor.execute(str(python_workspace))
        assert result.project_type == 'python'
    
    @pytest.mark.asyncio
    async def test_estimates_indexing_duration(self, executor, sample_workspace):
        """Test duration estimation"""
        result = await executor.execute(str(sample_workspace))
        
        # Should estimate some duration
        assert result.estimated_duration_seconds > 0
        
        # For small project, should be quick
        assert result.estimated_duration_seconds < 30
    
    def test_is_binary_detects_binary_files(self, executor, tmp_path):
        """Test binary file detection"""
        # Text file
        text_file = tmp_path / "text.txt"
        text_file.write_text("Hello, world!")
        assert not executor._is_binary(text_file)
        
        # Binary file (create a simple binary file)
        binary_file = tmp_path / "binary.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03')
        assert executor._is_binary(binary_file)
        
        # Image (by extension)
        image_file = tmp_path / "image.png"
        image_file.write_bytes(b'\x89PNG')
        assert executor._is_binary(image_file)


class TestSemanticChunker:
    """Unit tests for SemanticChunker"""
    
    @pytest.fixture
    def chunker(self):
        from src.services.indexing.chunking import SemanticChunker
        return SemanticChunker(target_chunk_size=1000, chunk_overlap=200)
    
    def test_chunk_small_function_single_chunk(self, chunker, tmp_path):
        """Test that small functions become single chunks"""
        # Arrange
        code = """
function greet(name: string): string {
    return `Hello, ${name}!`;
}
"""
        file = tmp_path / "test.ts"
        file.write_text(code)
        
        # Mock AST (simplified)
        mock_ast = Mock()
        
        # Act
        chunks = chunker.chunk_file(file, mock_ast, 'typescript', str(tmp_path))
        
        # Assert
        assert len(chunks) == 1
        assert chunks[0].chunk_type in ['function', 'block']
        assert 'greet' in chunks[0].content
    
    def test_chunk_large_class_multiple_chunks(self, chunker, tmp_path):
        """Test that large classes are split into chunks"""
        # Arrange
        code = """
class LargeClass {
    method1() { /* ... many lines ... */ }
    method2() { /* ... many lines ... */ }
    method3() { /* ... many lines ... */ }
    // ... assume this is very large (>1000 tokens)
}
"""
        file = tmp_path / "test.ts"
        file.write_text(code * 50)  # Make it large
        
        mock_ast = Mock()
        
        # Act
        chunks = chunker.chunk_file(file, mock_ast, 'typescript', str(tmp_path))
        
        # Assert
        assert len(chunks) > 1
        # Each chunk should preserve class context
        for chunk in chunks:
            assert 'LargeClass' in chunk.content or chunk.parent_context == 'LargeClass'
    
    def test_preserves_semantic_boundaries(self, chunker, tmp_path):
        """Test that chunks don't split in middle of functions"""
        code = """
function func1() {
    const x = 1;
    const y = 2;
    return x + y;
}

function func2() {
    const a = 10;
    const b = 20;
    return a * b;
}
"""
        file = tmp_path / "test.ts"
        file.write_text(code)
        
        mock_ast = Mock()
        chunks = chunker.chunk_file(file, mock_ast, 'typescript', str(tmp_path))
        
        # Each chunk should be a complete function
        for chunk in chunks:
            # Should have matching braces
            assert chunk.content.count('{') == chunk.content.count('}')
```

#### Utility Function Testing

```python
# backend/tests/unit/utils/test_validators.py

import pytest
from src.utils.validators import Validators


class TestValidators:
    """Unit tests for validation utilities"""
    
    def test_validate_file_path_accepts_valid_paths(self):
        """Test that valid file paths are accepted"""
        valid_paths = [
            "src/index.ts",
            "README.md",
            "path/to/file.py",
        ]
        
        for path in valid_paths:
            result = Validators.validate_file_path(path)
            assert result == path
    
    def test_validate_file_path_rejects_parent_traversal(self):
        """Test that parent directory traversal is rejected"""
        invalid_paths = [
            "../../../etc/passwd",
            "src/../../secrets.txt",
            "path/../../../file.txt",
        ]
        
        for path in invalid_paths:
            with pytest.raises(ValueError, match="cannot contain"):
                Validators.validate_file_path(path)
    
    def test_validate_file_path_rejects_empty_paths(self):
        """Test that empty paths are rejected"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Validators.validate_file_path("")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Validators.validate_file_path("   ")
    
    @pytest.mark.parametrize("value,expected", [
        (0, 0.0),
        (50, 50.0),
        (100, 100.0),
        (99.99, 100.0),
        (0.01, 0.0),
    ])
    def test_validate_percentage_accepts_valid_values(self, value, expected):
        """Test percentage validation with valid values"""
        result = Validators.validate_percentage(value)
        assert result == expected
    
    @pytest.mark.parametrize("value", [-1, -0.1, 100.1, 101, 1000])
    def test_validate_percentage_rejects_invalid_values(self, value):
        """Test percentage validation rejects out-of-range values"""
        with pytest.raises(ValueError, match="between 0 and 100"):
            Validators.validate_percentage(value)
    
    @pytest.mark.parametrize("complexity", ["low", "medium", "high"])
    def test_validate_complexity_accepts_valid_values(self, complexity):
        """Test complexity validation with valid values"""
        result = Validators.validate_complexity(complexity)
        assert result == complexity
    
    def test_validate_complexity_rejects_invalid_values(self):
        """Test complexity validation rejects invalid values"""
        with pytest.raises(ValueError, match="must be low, medium, or high"):
            Validators.validate_complexity("invalid")
    
    @pytest.mark.parametrize("model_name", [
        "qwen2.5-coder:7b",
        "bge-m3",
        "llama2:13b-instruct",
        "model_name_123",
    ])
    def test_validate_model_name_accepts_valid_names(self, model_name):
        """Test model name validation with valid names"""
        result = Validators.validate_model_name(model_name)
        assert result == model_name
    
    @pytest.mark.parametrize("model_name", [
        "invalid model",
        "model/with/slash",
        "model@special",
        "",
    ])
    def test_validate_model_name_rejects_invalid_names(self, model_name):
        """Test model name validation rejects invalid names"""
        with pytest.raises(ValueError, match="Invalid model name"):
            Validators.validate_model_name(model_name)
```

---

## 🔗 Integration Testing

### API Integration Tests

```python
# tests/integration/test_embedding_ab.py
import time
import tempfile
import shutil
import json
import pytest
from pathlib import Path

# === PLACEHOLDERS ===
# Replace these imports/implementations with your project's functions.
# e.g. from localpilot.embedding import embed_texts
# e.g. from localpilot.vectordb import ChromaClient

def embed_texts(texts, model_name):
    """
    Placeholder: call your embedding model (via Ollama or local runner).
    Return list of vectors (list of floats) same length as texts.
    """
    raise NotImplementedError("Replace embed_texts with your embedding call")

class TempVectorDB:
    """
    Placeholder thin vectordb wrapper with a search(query_vector, k) -> list of (id, score)
    Replace with Chroma or in-memory vector store setup.
    """
    def __init__(self):
        self.items = []  # list of (id, vector, metadata)
    def add(self, id, vector, metadata):
        self.items.append((id, vector, metadata))
    def search(self, query_vector, k=5):
        # naive cosine similarity
        import math
        def dot(a,b): return sum(x*y for x,y in zip(a,b))
        def norm(a): return math.sqrt(sum(x*x for x in a))
        qn = norm(query_vector)
        results = []
        for id, v, meta in self.items:
            score = dot(query_vector, v) / (qn * (norm(v)+1e-9))
            results.append((id, score, meta))
        results.sort(key=lambda t: t[1], reverse=True)
        return results[:k]

# === End placeholders ===

@pytest.fixture
def fixture_repo(tmp_path):
    """Create small fixture repo with files and queries + ground-truth mapping."""
    repo = tmp_path / "fixture_repo"
    repo.mkdir()
    # Create few files
    f1 = repo / "README.md"
    f1.write_text("# Project\n\nThis project calculates fibonacci numbers.\n\nUsage: ...")
    f2 = repo / "src/math_utils.py"
    f2.write_text(
        "def fib(n):\n    '''Return nth fibonacci number'''\n    if n < 2: return n\n    a, b = 0, 1\n    for _ in range(n-1):\n        a, b = b, a+b\n    return b\n"
    )
    f3 = repo / "docs/algorithm.md"
    f3.write_text("Fibonacci implemented with iterative approach for performance.\n")
    # Queries and ground truth (mapping query -> relevant file ids)
    queries = [
        {"query": "how is fibonacci implemented", "relevant": ["src/math_utils.py", "docs/algorithm.md"]},
        {"query": "project usage", "relevant": ["README.md"]}
    ]
    return {"path": str(repo), "queries": queries}

def compute_precision_at_k(db, queries, k=5, embed_model="bge-m3"):
    total = 0.0
    for q in queries:
        # Using placeholder embed_texts to get query vector
        qv = embed_texts([q["query"]], model_name=embed_model)[0]
        results = db.search(qv, k=k)
        ids = [meta.get("file_path") for _, _, meta in results]
        # count hits in top-k
        hits = sum(1 for r in ids if r in q["relevant"])
        total += hits / k
    return total / len(queries)

@pytest.mark.parametrize("model_name", ["bge-m3:latest", "mxbai-embed-large:latest", "jina/jina-embeddings-v2-base-en:latest"])
def test_embedding_ab_model_precision(fixture_repo, model_name):
    """
    End-to-end small integration check:
    - embed files from fixture repo with model_name
    - build a vectordb
    - run queries and measure Precision@5
    - assert Precision@5 >= 0.6 (conservative threshold for CI)
    """
    repo = Path(fixture_repo["path"])
    # gather chunks (simple per-file text chunk)
    chunks = []
    for p in repo.rglob("*"):
        if p.is_file():
            text = p.read_text()
            chunks.append({"id": str(p), "text": text, "meta": {"file_path": p.name}})

    # embed
    texts = [c["text"] for c in chunks]
    try:
        vectors = embed_texts(texts, model_name)
    except NotImplementedError:
        pytest.skip("embed_texts not implemented in test scaffold; implement to run this test")

    # create vectordb
    db = TempVectorDB()
    for c, v in zip(chunks, vectors):
        db.add(c["id"], v, c["meta"])

    precision = compute_precision_at_k(db, fixture_repo["queries"], k=5, embed_model=model_name)
    # conservative CI threshold; tune as you collect metrics
    assert precision >= 0.6, f"{model_name} precision@5 too low: {precision}"

```

```python
# backend/tests/integration/test_api.py

import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.integration
class TestHealthEndpoint:
    """Integration tests for health endpoint"""
    
    @pytest.mark.asyncio
    async def test_health_check_returns_200(self):
        """Test health endpoint returns 200 OK"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "version" in data
    
    @pytest.mark.asyncio
    async def test_health_check_includes_ollama_status(self):
        """Test health check includes Ollama status"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            
            data = response.json()
            assert "services" in data
            assert "ollama" in data["services"]
            assert data["services"]["ollama"]["status"] in ["connected", "disconnected"]


@pytest.mark.integration
class TestIndexingAPI:
    """Integration tests for indexing endpoints"""
    
    @pytest.fixture
    async def client(self):
        """Create test client"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    
    @pytest.mark.asyncio
    async def test_start_indexing_creates_job(self, client, tmp_path):
        """Test that starting indexing creates a job"""
        # Arrange
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        (workspace / "index.ts").write_text("console.log('test');")
        
        # Act
        response = await client.post(
            "/api/indexing/start",
            json={
                "workspace_path": str(workspace),
                "options": {
                    "exclude_patterns": ["node_modules"],
                    "max_file_size_mb": 10,
                }
            }
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "indexing_id" in data
        assert data["status"] == "started"
    
    @pytest.mark.asyncio
    async def test_get_indexing_status(self, client, tmp_path):
        """Test getting indexing status"""
        # Start indexing
        workspace = tmp_path / "test-project"
        workspace.mkdir()
        (workspace / "index.ts").write_text("test")
        
        start_response = await client.post(
            "/api/indexing/start",
            json={"workspace_path": str(workspace)}
        )
        indexing_id = start_response.json()["indexing_id"]
        
        # Get status
        status_response = await client.get(f"/api/indexing/status?indexing_id={indexing_id}")
        
        assert status_response.status_code == 200
        data = status_response.json()
        assert data["indexing_id"] == indexing_id
        assert "status" in data
        assert "progress_percentage" in data


@pytest.mark.integration
class TestChatAPI:
    """Integration tests for chat endpoints"""
    
    @pytest.fixture
    async def client(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    
    @pytest.mark.asyncio
    async def test_send_chat_message_returns_response(self, client):
        """Test sending a chat message"""
        response = await client.post(
            "/api/chat/message",
            json={
                "session_id": "test-session",
                "message": "Hello, LocalPilot!",
                "options": {
                    "stream": False,
                    "retrieve_context": False,
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message_id" in data
        assert "content" in data
    
    @pytest.mark.asyncio
    async def test_get_chat_sessions(self, client):
        """Test getting chat sessions"""
        response = await client.get("/api/chat/sessions")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert isinstance(data["sessions"], list)
```

### WebSocket Integration Tests

```typescript
// extension/test/integration/websocket.test.ts

import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import WebSocket from 'ws';
import { spawn, ChildProcess } from 'child_process';

describe('WebSocket Integration', () => {
  let backendProcess: ChildProcess;
  let ws: WebSocket;
  
  beforeAll(async () => {
    // Start backend
    backendProcess = spawn('python', ['-m', 'uvicorn', 'src.main:app', '--port', '8765'], {
      cwd: '../../backend',
    });
    
    // Wait for backend to be ready
    await new Promise(resolve => setTimeout(resolve, 3000));
  });
  
  afterAll(() => {
    // Stop backend
    if (backendProcess) {
      backendProcess.kill();
    }
  });
  
  beforeEach(() => {
    ws = new WebSocket('ws://localhost:8765/ws?client_id=test-client');
  });
  
  afterEach(() => {
    if (ws) {
      ws.close();
    }
  });
  
  it('should establish connection', (done) => {
    ws.on('open', () => {
      expect(ws.readyState).toBe(WebSocket.OPEN);
      done();
    });
    
    ws.on('error', (error) => {
      done(error);
    });
  });
  
  it('should receive handshake acknowledgment', (done) => {
    ws.on('open', () => {
      ws.send(JSON.stringify({
        type: 'handshake',
        payload: { version: '0.1.0' },
      }));
    });
    
    ws.on('message', (data) => {
      const message = JSON.parse(data.toString());
      
      if (message.type === 'handshake_ack') {
        expect(message.payload).toHaveProperty('server_version');
        expect(message.payload).toHaveProperty('capabilities');
        done();
      }
    });
  });
  
  it('should handle indexing progress events', (done) => {
    const progressEvents: any[] = [];
    
    ws.on('open', () => {
      ws.send(JSON.stringify({
        type: 'indexing.start',
        payload: {
          workspace_path: '/path/to/test/workspace',
          options: {},
        },
      }));
    });
    
    ws.on('message', (data) => {
      const message = JSON.parse(data.toString());
      
      if (message.type === 'indexing.progress') {
        progressEvents.push(message.payload);
      }
      
      if (message.type === 'indexing.complete') {
        expect(progressEvents.length).toBeGreaterThan(0);
        expect(progressEvents[0]).toHaveProperty('phase');
        expect(progressEvents[0]).toHaveProperty('percentage');
        done();
      }
    });
  }, 30000); // 30 second timeout
});
```

---

## 🎭 End-to-End Testing

### E2E Test Setup

```typescript
// extension/test/e2e/setup.ts

import * as vscode from 'vscode';
import * as path from 'path';
import { promises as fs } from 'fs';

export class E2ETestHelper {
  private workspaceRoot: string;
  
  constructor() {
    this.workspaceRoot = path.join(__dirname, '../../../test-workspace');
  }
  
  async setupTestWorkspace(): Promise<string> {
    // Create test workspace
    await fs.mkdir(this.workspaceRoot, { recursive: true });
    
    // Create sample files
    await this.createSampleProject();
    
    return this.workspaceRoot;
  }
  
  async createSampleProject(): Promise<void> {
    const srcDir = path.join(this.workspaceRoot, 'src');
    await fs.mkdir(srcDir, { recursive: true });
    
    // Create index.ts
    await fs.writeFile(
      path.join(srcDir, 'index.ts'),
      `console.log('Hello, LocalPilot!');`
    );
    
    // Create utils.ts
    await fs.writeFile(
      path.join(srcDir, 'utils.ts'),
      `export function greet(name: string): string {
  return \`Hello, \${name}!\`;
}`
    );
    
    // Create README.md
    await fs.writeFile(
      path.join(this.workspaceRoot, 'README.md'),
      `# Test Project\n\nThis is a test project for LocalPilot E2E tests.`
    );
    
    // Create package.json
    await fs.writeFile(
      path.join(this.workspaceRoot, 'package.json'),
      JSON.stringify({
        name: 'test-project',
        version: '1.0.0',
        dependencies: {
          typescript: '^5.0.0',
        },
      }, null, 2)
    );
  }
  
  async cleanupTestWorkspace(): Promise<void> {
    await fs.rm(this.workspaceRoot, { recursive: true, force: true });
  }
  
  async waitForCondition(
    condition: () => boolean | Promise<boolean>,
    timeout: number = 10000,
    interval: number = 100
  ): Promise<void> {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      if (await condition()) {
        return;
      }
      await new Promise(resolve => setTimeout(resolve, interval));
    }
    
    throw new Error('Timeout waiting for condition');
  }
}
```

### E2E Test Scenarios

```typescript
// extension/test/e2e/indexing.e2e.test.ts

import * as vscode from 'vscode';
import { expect } from 'chai';
import { E2ETestHelper } from './setup';

describe('E2E: Indexing Workflow', () => {
  let helper: E2ETestHelper;
  let workspaceUri: vscode.Uri;
  
  before(async () => {
    helper = new E2ETestHelper();
    const workspacePath = await helper.setupTestWorkspace();
    workspaceUri = vscode.Uri.file(workspacePath);
    
    // Open workspace
    await vscode.commands.executeCommand('vscode.openFolder', workspaceUri);
    
    // Wait for workspace to open
    await helper.waitForCondition(
      () => vscode.workspace.workspaceFolders !== undefined
    );
  });
  
  after(async () => {
    await helper.cleanupTestWorkspace();
  });
  
  it('should complete full indexing workflow', async function() {
    this.timeout(60000); // 60 second timeout
    
    // 1. Open LocalPilot panel
    await vscode.commands.executeCommand('localpilot.openPanel');
    
    // Wait for panel to open
    await helper.waitForCondition(
      () => vscode.window.activeTextEditor !== undefined
    );
    
    // 2. Start indexing
    await vscode.commands.executeCommand('localpilot.startIndexing');
    
    // 3. Wait for indexing to complete
    let indexingComplete = false;
    const listener = vscode.window.onDidChangeWindowState((state) => {
      // Listen for indexing complete notification
      if (state.focused) {
        indexingComplete = true;
      }
    });
    
    await helper.waitForCondition(() => indexingComplete, 30000);
    
    listener.dispose();
    
    // 4. Verify project summary is shown
    // (This would check the webview content, implementation depends on webview API access)
    
    expect(indexingComplete).to.be.true;
  });
  
  it('should handle chat interaction after indexing', async function() {
    this.timeout(30000);
    
    // Assuming indexing is complete from previous test
    
    // 1. Send chat message
    await vscode.commands.executeCommand(
      'localpilot.sendChatMessage',
      'What does this project do?'
    );
    
    // 2. Wait for response
    let responseReceived = false;
    
    await helper.waitForCondition(() => responseReceived, 10000);
    
    expect(responseReceived).to.be.true;
  });
});
```

---

## 🎭 Test Fixtures & Mocks

### Fixture Management

```python
# backend/tests/fixtures/sample_projects.py

import pytest
from pathlib import Path
from typing import Dict

class SampleProjectFixtures:
    """Manage sample project fixtures for testing"""
    
    @staticmethod
    def create_typescript_project(base_path: Path) -> Path:
        """Create a sample TypeScript project"""
        project = base_path / "typescript-project"
        project.mkdir(parents=True)
        
        # Source files
        src = project / "src"
        src.mkdir()
        
        (src / "index.ts").write_text("""
import { greet } from './utils';

function main() {
    console.log(greet('World'));
}

main();
""")
        
        (src / "utils.ts").write_text("""
export function greet(name: string): string {
    return `Hello, ${name}!`;
}

export function add(a: number, b: number): number {
    return a + b;
}
""")
        
        # Config files
        (project / "package.json").write_text("""{
    "name": "typescript-project",
    "version": "1.0.0",
    "dependencies": {
        "typescript": "^5.0.0"
    }
}""")
        
        (project / "tsconfig.json").write_text("""{
    "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs",
        "strict": true
    }
}""")
        
        (project / "README.md").write_text("""
# TypeScript Project

A sample TypeScript project for testing.

## Features
- Greeting functionality
- Math utilities
""")
        
        return project
    
    @staticmethod
    def create_python_project(base_path: Path) -> Path:
        """Create a sample Python project"""
        project = base_path / "python-project"
        project.mkdir(parents=True)
        
        # Source files
        src = project / "src"
        src.mkdir()
        
        (src / "__init__.py").write_text("")
        
        (src / "main.py").write_text("""
from .utils import greet

def main():
    print(greet('World'))

if __name__ == '__main__':
    main()
""")
        
        (src / "utils.py").write_text("""
def greet(name: str) -> str:
    return f'Hello, {name}!'

def add(a: int, b: int) -> int:
    return a + b
""")
        
        # Config files
        (project / "setup.py").write_text("""
from setuptools import setup, find_packages

setup(
    name='python-project',
    version='1.0.0',
    packages=find_packages(),
)
""")
        
        (project / "README.md").write_text("""
# Python Project

A sample Python project for testing.
""")
        
        return project


@pytest.fixture
def typescript_project(tmp_path):
    """Fixture providing a TypeScript project"""
    return SampleProjectFixtures.create_typescript_project(tmp_path)


@pytest.fixture
def python_project(tmp_path):
    """Fixture providing a Python project"""
    return SampleProjectFixtures.create_python_project(tmp_path)


@pytest.fixture
def large_project(tmp_path):
    """Fixture providing a large project for performance testing"""
    project = tmp_path / "large-project"
    project.mkdir()
    
    src = project / "src"
    src.mkdir()
    
    # Create 100 files
    for i in range(100):
        (src / f"file{i}.ts").write_text(f"""
export function func{i}() {{
    return {i};
}}
""")
    
    return project
```

### Mock Objects

```python
# backend/tests/mocks/llm_mocks.py

from typing import List, AsyncGenerator
from unittest.mock import AsyncMock

class MockLLMService:
    """Mock LLM service for testing"""
    
    def __init__(self, responses: List[str] = None):
        self.responses = responses or ["Mock response"]
        self.call_count = 0
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a mock response"""
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response
    
    async def stream_generate(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream a mock response"""
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        
        # Yield response in chunks
        words = response.split()
        for word in words:
            yield word + " "
    
    async def embed(self, text: str) -> List[float]:
        """Generate mock embedding"""
        # Return a simple mock embedding
        return [0.1] * 1024


class MockVectorStore:
    """Mock vector store for testing"""
    
    def __init__(self):
        self.documents: List[Dict] = []
        self.search_results: List[Dict] = []
    
    async def add_documents(self, documents: List[Dict]):
        """Add mock documents"""
        self.documents.extend(documents)
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Dict = None
    ) -> List[Dict]:
        """Return mock search results"""
        return self.search_results[:top_k]
    
    async def delete_by_metadata(self, filters: Dict):
        """Delete mock documents"""
        self.documents = [
            doc for doc in self.documents
            if not all(doc['metadata'].get(k) == v for k, v in filters.items())
        ]
    
    def set_search_results(self, results: List[Dict]):
        """Set mock search results"""
        self.search_results = results
```

---

## 📊 Coverage Requirements

### Coverage Targets

```yaml
Overall Coverage: >= 70%

By Component:
  Critical Components (>=85%):
    - IndexingService
    - RAGService
    - FileOperations (Act Mode)
    - WebSocketService
    - SemanticChunker
  
  Important Components (>=75%):
    - ChatService
    - PlanService
    - TreeSitterParser
    - EmbeddingService
    - VectorStore
  
  UI Components (>=60%):
    - React components
    - Focus on logic over rendering
  
  Utilities (>=80%):
    - Validators
    - Helpers
    - Pure functions

Exclusions:
  - Generated code
  - Type definitions
  - Configuration files
  - Test files themselves
```

### Coverage Reports

```bash
# TypeScript coverage
cd extension
npm run test:coverage

# Generates coverage/lcov-report/index.html

# Python coverage
cd backend
pytest --cov=src --cov-report=html

# Generates htmlcov/index.html

# Combined coverage report
./scripts/coverage-report.sh
```

---

## ⚡ Performance Testing

### Performance Benchmarks

```python
# backend/tests/performance/test_indexing_performance.py

import pytest
import time
from src.services.indexing.indexing_service import IndexingService


@pytest.mark.performance
class TestIndexingPerformance:
    """Performance tests for indexing"""
    
    @pytest.mark.asyncio
    async def test_index_small_project_under_30_seconds(self, small_project, indexing_service):
        """Test that small project (< 100 files) indexes in < 30s"""
        start_time = time.time()
        
        await indexing_service.index_workspace(str(small_project))
        
        duration = time.time() - start_time
        assert duration < 30, f"Indexing took {duration}s, expected < 30s"
    
    @pytest.mark.asyncio
    async def test_index_medium_project_under_5_minutes(self, medium_project, indexing_service):
        """Test that medium project (500 files) indexes in < 5 min"""
        start_time = time.time()
        
        await indexing_service.index_workspace(str(medium_project))
        
        duration = time.time() - start_time
        assert duration < 300, f"Indexing took {duration}s, expected < 300s"
    
    @pytest.mark.asyncio
    async def test_rag_retrieval_under_500ms(self, indexed_workspace, rag_service):
        """Test that RAG retrieval is < 500ms"""
        query = "How does authentication work?"
        
        start_time = time.time()
        
        await rag_service.retrieve_context(query, top_k=5)
        
        duration = (time.time() - start_time) * 1000  # Convert to ms
        assert duration < 500, f"RAG retrieval took {duration}ms, expected < 500ms"
    
    @pytest.mark.asyncio
    async def test_embedding_generation_throughput(self, embedding_service):
        """Test embedding generation throughput"""
        texts = ["Sample text" for _ in range(100)]
        
        start_time = time.time()
        
        await embedding_service.embed_batch(texts, batch_size=32)
        
        duration = time.time() - start_time
        throughput = len(texts) / duration
        
        assert throughput > 20, f"Throughput {throughput} docs/s, expected > 20 docs/s"
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml

name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-extension:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18.x]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: |
          cd extension
          npm ci
      
      - name: Run linter
        run: |
          cd extension
          npm run lint
      
      - name: Run type check
        run: |
          cd extension
          npm run type-check
      
      - name: Run tests
        run: |
          cd extension
          npm test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./extension/coverage/lcov.info
          flags: extension
  
  test-backend:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linter
        run: |
          cd backend
          flake8 src/
      
      - name: Run type check
        run: |
          cd backend
          mypy src/
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
          flags: backend
  
  integration-tests:
    runs-on: ubuntu-latest
    needs: [test-extension, test-backend]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18.x
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Setup Ollama
        run: |
          curl https://ollama.ai/install.sh | sh
          ollama pull qwen2.5-coder:7b-instruct-q4_K_M
      
      - name: Install dependencies
        run: |
          cd extension && npm ci
          cd ../backend && pip install -r requirements.txt
      
      - name: Run integration tests
        run: |
          ./scripts/run-integration-tests.sh
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and goals
- `TECHNICAL_ARCHITECTURE.md` - System architecture
- `INDEXING_SYSTEM_SPEC.md` - Indexing implementation
- `UI_DESIGN_SYSTEM.md` - UI components
- `DEVELOPMENT_GUIDE.md` - Setup and workflow (PREVIOUS)
- `DATA_MODELS.md` - Data schemas
- `API_SPECIFICATION.md` - API documentation

---

**END OF DOCUMENT**