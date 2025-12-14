import { LocalPilotError } from './base.error';

/**
 * Thrown when Ollama cannot be reached.
 */
export class OllamaConnectionError extends LocalPilotError {
  readonly code = 'OLLAMA_CONNECTION_FAILED';
  readonly category = 'connection' as const;
  readonly recoverable = true;

  constructor(url: string, cause?: Error) {
    super(
      `Cannot connect to Ollama at ${url}. Make sure Ollama is running.`,
      { url, cause: cause?.message }
    );
  }
}

/**
 * Thrown when a requested model is missing.
 */
export class OllamaModelNotFoundError extends LocalPilotError {
  readonly code = 'OLLAMA_MODEL_NOT_FOUND';
  readonly category = 'llm' as const;
  readonly recoverable = true;

  constructor(model: string) {
    super(
      `Model "${model}" not found. Run "ollama pull ${model}" to install it.`,
      { model }
    );
  }
}

/**
 * Thrown when generation fails unexpectedly.
 */
export class OllamaGenerationError extends LocalPilotError {
  readonly code = 'OLLAMA_GENERATION_FAILED';
  readonly category = 'llm' as const;
  readonly recoverable = true;

  constructor(message: string, model: string) {
    super(message, { model });
  }
}
