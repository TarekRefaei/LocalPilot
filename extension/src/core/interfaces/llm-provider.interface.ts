/**
 * Interface for LLM provider operations
 */
export interface ILLMProvider {
  /** Check if the LLM provider is available */
  isAvailable(): Promise<boolean>;
  /** Get list of available models */
  listModels(): Promise<ModelInfo[]>;
  /** Generate chat completion (non-streaming) */
  chat(request: ChatRequest): Promise<ChatResponse>;
  /** Generate chat completion with streaming */
  chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown>;
  /** Generate embeddings for text */
  embed(text: string, model?: string): Promise<number[]>;
}

export interface ModelInfo {
  name: string;
  size: number;
  modifiedAt: Date;
  family: string;
  parameterSize: string;
  quantizationLevel: string;
}

export interface ChatRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  options?: {
    temperature?: number;
    topP?: number;
    maxTokens?: number;
  };
}

export interface ChatResponse {
  content: string;
  model: string;
  totalDuration: number;
  promptEvalCount: number;
  evalCount: number;
}
