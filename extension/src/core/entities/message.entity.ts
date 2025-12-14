/**
 * Represents a single chat message.
 */
export interface Message {
  /** Unique message ID */
  id: string;
  /** Who sent the message */
  role: 'user' | 'assistant' | 'system';
  /** Message content (may include markdown) */
  content: string;
  /** When the message was created */
  timestamp: Date;
  /** If this message used RAG context */
  ragContext?: RAGContext;
  /** Status for assistant messages (streaming) */
  status?: 'streaming' | 'complete' | 'error';
  /** Error details if status is 'error' */
  error?: string;
}

export interface RAGContext {
  /** Chunks used to generate response */
  chunks: RetrievedChunk[];
  /** Query that was sent to RAG */
  query: string;
}

export interface RetrievedChunk {
  /** Chunk ID in vector store */
  id: string;
  /** Code content */
  content: string;
  /** File path relative to workspace */
  filePath: string;
  /** Starting line number */
  lineStart: number;
  /** Ending line number */
  lineEnd: number;
  /** Type of code unit */
  chunkType: ChunkType;
  /** Symbol name (function/class name) */
  symbolName?: string;
  /** Programming language */
  language: string;
  /** Similarity score (0-1) */
  score: number;
}

export type ChunkType =
  | 'function'
  | 'class'
  | 'method'
  | 'interface'
  | 'type'
  | 'variable'
  | 'import'
  | 'module'
  | 'file';
