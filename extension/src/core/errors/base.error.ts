export type ErrorCategory =
  | 'connection'
  | 'indexing'
  | 'llm'
  | 'file'
  | 'validation';

/**
 * Base error class for all LocalPilot errors.
 * Enforces structured, serializable errors.
 */
export abstract class LocalPilotError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  abstract readonly recoverable: boolean;

  constructor(
    message: string,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;

    // Preserve stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      category: this.category,
      recoverable: this.recoverable,
      details: this.details,
    };
  }
}
