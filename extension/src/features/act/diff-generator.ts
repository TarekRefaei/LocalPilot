import * as Diff from 'diff';

export type Preview =
  | { kind: 'full'; content: string }
  | { kind: 'diff'; content: string }
  | { kind: 'snapshot'; content: string };

export function generatePreview(
  actionType: 'create' | 'modify' | 'delete',
  existingContent: string | undefined,
  generatedContent: string
): Preview {
  if (actionType === 'create') {
    return { kind: 'full', content: generatedContent };
  }

  if (actionType === 'delete') {
    return { kind: 'snapshot', content: existingContent ?? '' };
  }

  const patch = Diff.createTwoFilesPatch(
    'before',
    'after',
    existingContent ?? '',
    generatedContent
  );

  return { kind: 'diff', content: patch };
}
