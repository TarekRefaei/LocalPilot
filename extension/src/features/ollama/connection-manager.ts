import { OllamaConnectionError } from '../../core/errors';

const DEFAULT_OLLAMA_URL = 'http://localhost:11434';

/**
 * Checks whether Ollama is reachable.
 * Phase 0: connectivity only (no model logic).
 */
export async function checkOllamaAvailability(
  baseUrl: string = DEFAULT_OLLAMA_URL
): Promise<boolean> {
  try {
    const res = await fetch(`${baseUrl}/api/version`);
    return res.ok;
  } catch (error) {
    throw new OllamaConnectionError(baseUrl, error as Error);
  }
}
