import { describe, it, expect } from 'vitest';
import { validatePlan } from '../../plan/plan-validator';

describe('Plan → Act Contract', () => {
  it('blocks Act when plan has semantic warnings', () => {
    const plan = {
      id: 'p1',
      title: 'Test',
      overview: '',
      status: 'draft',
      tasks: [
        {
          id: 'task1',
          orderIndex: 0,
          title: 'Bad Task',
          description: '',
          filePath: '',
          actionType: 'create',
          details: ['x'],
          dependencies: []
        }
      ]
    } as any;

    const warnings = validatePlan(plan);
    expect(warnings.length).toBeGreaterThan(0);
  });

  it('allows Act when plan is fully valid', () => {
    const plan = {
      id: 'p1',
      title: 'Test',
      overview: '',
      status: 'draft',
      tasks: [
        {
          id: 'task1',
          orderIndex: 0,
          title: 'Good Task',
          description: '',
          filePath: 'utils.py',
          actionType: 'modify',
          details: ['x'],
          dependencies: []
        }
      ]
    } as any;

    const warnings = validatePlan(plan);
    expect(warnings.length).toBe(0);
  });
});
