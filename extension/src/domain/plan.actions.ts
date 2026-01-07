export const ACTION_TYPES = ['create', 'modify', 'delete'] as const;
export type ActionType = typeof ACTION_TYPES[number];
