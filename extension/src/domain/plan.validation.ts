import { ACTION_TYPES, type ActionType } from './plan.actions';

export enum ValidationCode {
  EMPTY_PLAN = 'empty_plan',
  NO_TASKS = 'no_tasks',
  MISSING_FILE_PATH = 'missing_file_path',
  MISSING_ACTION_TYPE = 'missing_action_type',
  INVALID_ACTION_TYPE = 'invalid_action_type',
  INVALID_ORDER = 'invalid_order',
  DUPLICATE_TASK_ID = 'duplicate_task_id',
  FILE_ALREADY_EXISTS = 'file_already_exists',
  FILE_NOT_FOUND = 'file_not_found',
  FILE_NOT_INDEXED = 'file_not_indexed',
  PATH_OUTSIDE_WORKSPACE = 'path_outside_workspace',
}

export function isBlockingValidationCode(code: ValidationCode): boolean {
  return [
    ValidationCode.FILE_ALREADY_EXISTS,
    ValidationCode.FILE_NOT_FOUND,
    ValidationCode.PATH_OUTSIDE_WORKSPACE,
  ].includes(code);
}

export function isValidActionType(value: string): value is ActionType {
  return (ACTION_TYPES as readonly string[]).includes(value);
}
