export type ExecutionErrorCode =
  | 'FILE_SCOPE_VIOLATION'
  | 'ACTION_TYPE_VIOLATION'
  | 'EMPTY_DIFF_NOT_ALLOWED'
  | 'CONTEXT_MISMATCH';

export interface ExecutionError {
  code: ExecutionErrorCode;
  message: string;
  retryable: boolean;
}
