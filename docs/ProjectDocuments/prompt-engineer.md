# 📄 PROMPT_ENGINEERING.md

# LocalPilot - Prompt Engineering Guide

> Prompt versioning, testing, and best practices

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Prompt Engineering Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Prompt Philosophy](#1-prompt-philosophy)
2. [Prompt Structure](#2-prompt-structure)
3. [Prompt Registry](#3-prompt-registry)
4. [Versioning Strategy](#4-versioning-strategy)
5. [Testing Prompts](#5-testing-prompts)
6. [Prompt Templates](#6-prompt-templates)
7. [Best Practices](#7-best-practices)

---

## 1. Prompt Philosophy

### 1.1 Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                   PROMPT PHILOSOPHY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRINCIPLE 1: Prompts Are Code                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Prompts live in version control                              │
│  • Prompts have tests                                            │
│  • Prompts have documentation                                    │
│  • Changes are reviewed                                          │
│                                                                  │
│  PRINCIPLE 2: Determinism Where Possible                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Low temperature for structured output                        │
│  • Clear format instructions                                     │
│  • Consistent context structure                                  │
│                                                                  │
│  PRINCIPLE 3: Fail Gracefully                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Define what to do if output is unparseable                   │
│  • Have fallback prompts                                         │
│  • Log failures for debugging                                    │
│                                                                  │
│  PRINCIPLE 4: Context Efficiency                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Don't waste tokens on unnecessary context                   │
│  • Prioritize most relevant information                         │
│  • Truncate gracefully                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Prompt Types in LocalPilot

| Type | Purpose | Output Format | Temperature |
|------|---------|---------------|-------------|
| **System** | Set assistant behavior | N/A | N/A |
| **Chat** | Conversational response | Markdown | 0.7 |
| **Summary** | Project summary | Markdown | 0.3 |
| **Plan** | Generate TODO plan | Structured MD | 0.2 |
| **Code** | Generate code | Code blocks | 0.2 |

---

## 2. Prompt Structure

### 2.1 Standard Prompt Template

```typescript
interface PromptDefinition {
  // Identity
  id: string;           // Unique identifier
  version: string;      // Semantic version
  name: string;         // Human-readable name
  
  // Classification
  type: 'system' | 'chat' | 'summary' | 'plan' | 'code';
  
  // Configuration
  config: {
    temperature: number;
    maxTokens?: number;
    stopSequences?: string[];
  };
  
  // Content
  template: string;     // Prompt template with {{variables}}
  
  // Validation
  expectedOutput: {
    format: 'markdown' | 'json' | 'code' | 'text';
    schema?: object;    // JSON schema if applicable
  };
  
  // Fallback
  onParseFailure: 'retry' | 'fallback' | 'error';
  fallbackPromptId?: string;
  
  // Metadata
  description: string;
  examples?: PromptExample[];
  changelog: ChangelogEntry[];
}
```

### 2.2 File Structure

```
extension/src/prompts/
├── index.ts              # Prompt registry
├── types.ts              # TypeScript types
├── system/
│   ├── chat.system.ts    # Chat mode system prompt
│   ├── plan.system.ts    # Plan mode system prompt
│   └── act.system.ts     # Act mode system prompt
├── templates/
│   ├── summary.prompt.ts    # Project summary
│   ├── plan-generate.prompt.ts
│   ├── code-create.prompt.ts
│   └── code-modify.prompt.ts
└── __tests__/
    ├── prompts.test.ts
    └── fixtures/
        └── sample-outputs.ts
```

---

## 3. Prompt Registry

### 3.1 Registry Implementation

```typescript
// extension/src/prompts/index.ts

import { PromptDefinition } from './types';
import { CHAT_SYSTEM_PROMPT } from './system/chat.system';
import { PLAN_SYSTEM_PROMPT } from './system/plan.system';
import { SUMMARY_PROMPT } from './templates/summary.prompt';
import { PLAN_GENERATE_PROMPT } from './templates/plan-generate.prompt';
import { CODE_CREATE_PROMPT } from './templates/code-create.prompt';
import { CODE_MODIFY_PROMPT } from './templates/code-modify.prompt';

/**
 * Central registry of all prompts.
 * Enables versioning, testing, and runtime selection.
 */
export const PROMPT_REGISTRY: Record<string, PromptDefinition> = {
  'system.chat.v1': CHAT_SYSTEM_PROMPT,
  'system.plan.v1': PLAN_SYSTEM_PROMPT,
  'template.summary.v1': SUMMARY_PROMPT,
  'template.plan-generate.v1': PLAN_GENERATE_PROMPT,
  'template.code-create.v1': CODE_CREATE_PROMPT,
  'template.code-modify.v1': CODE_MODIFY_PROMPT,
};

/**
 * Get a prompt by ID with variable substitution.
 */
export function getPrompt(
  promptId: string,
  variables: Record<string, string> = {}
): string {
  const definition = PROMPT_REGISTRY[promptId];
  
  if (!definition) {
    throw new Error(`Prompt not found: ${promptId}`);
  }
  
  let prompt = definition.template;
  
  // Substitute variables
  for (const [key, value] of Object.entries(variables)) {
    prompt = prompt.replace(new RegExp(`{{${key}}}`, 'g'), value);
  }
  
  // Warn about unused variables
  const unusedVars = prompt.match(/{{[^}]+}}/g);
  if (unusedVars) {
    console.warn(`Unused variables in prompt ${promptId}:`, unusedVars);
  }
  
  return prompt;
}

/**
 * Get prompt configuration.
 */
export function getPromptConfig(promptId: string) {
  return PROMPT_REGISTRY[promptId]?.config;
}
```

---

## 4. Versioning Strategy

### 4.1 Version Format

```
prompt-id.vMAJOR.MINOR

Examples:
- system.chat.v1      (first version)
- system.chat.v1.1    (minor improvement)
- system.chat.v2      (breaking change)
```

### 4.2 Version Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                   VERSIONING RULES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MAJOR VERSION (v1 → v2):                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Output format changes                                         │
│  • Required variables change                                     │
│  • Fundamental behavior change                                   │
│  • Requires code changes to handle                              │
│                                                                  │
│  MINOR VERSION (v1.0 → v1.1):                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Improved wording                                              │
│  • Better examples                                               │
│  • Clearer instructions                                          │
│  • Same output format                                            │
│  • Backward compatible                                           │
│                                                                  │
│  KEEP BOTH VERSIONS WHEN:                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • A/B testing quality                                           │
│  • Gradual rollout                                               │
│  • Fallback needed                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Changelog Format

```typescript
interface ChangelogEntry {
  version: string;
  date: string;
  changes: string[];
  author: string;
}

// Example
const changelog: ChangelogEntry[] = [
  {
    version: "1.1",
    date: "2024-01-20",
    changes: [
      "Added explicit JSON format instructions",
      "Improved handling of empty code blocks"
    ],
    author: "TarekRefaei"
  },
  {
    version: "1.0",
    date: "2024-01-15",
    changes: ["Initial version"],
    author: "TarekRefaei"
  }
];
```

---

## 5. Testing Prompts

### 5.1 Test Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROMPT TEST TYPES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TYPE 1: Format Tests                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Does output match expected format?                           │
│  • Can it be parsed without errors?                             │
│  • Are all required fields present?                             │
│                                                                  │
│  TYPE 2: Quality Tests                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Is the output relevant?                                       │
│  • Does it follow instructions?                                 │
│  • Is code syntactically valid?                                 │
│                                                                  │
│  TYPE 3: Regression Tests                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Given same input, is output similar?                         │
│  • Did prompt change break anything?                            │
│                                                                  │
│  TYPE 4: Edge Case Tests                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Empty context                                                 │
│  • Very long context                                             │
│  • Unusual queries                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Test Implementation

```typescript
// extension/src/prompts/__tests__/prompts.test.ts

import { describe, it, expect } from 'vitest';
import { getPrompt, PROMPT_REGISTRY } from '../index';
import { parsePlanOutput } from '../parsers/plan-parser';

describe('Plan Generation Prompt', () => {
  const promptId = 'template.plan-generate.v1';
  
  it('should have all required fields', () => {
    const definition = PROMPT_REGISTRY[promptId];
    
    expect(definition).toBeDefined();
    expect(definition.id).toBe(promptId);
    expect(definition.template).toBeDefined();
    expect(definition.config.temperature).toBeLessThan(0.5);
  });
  
  it('should substitute variables correctly', () => {
    const prompt = getPrompt(promptId, {
      goal: 'Add authentication',
      context: 'React app with Express backend'
    });
    
    expect(prompt).toContain('Add authentication');
    expect(prompt).toContain('React app with Express backend');
    expect(prompt).not.toContain('{{goal}}');
  });
  
  it('should generate parseable output', async () => {
    // This test requires actual LLM - mark as integration test
    // In practice, use recorded responses for unit tests
    const sampleOutput = `
## Plan: Add Authentication

### Overview
Add user authentication to the app.

### Implementation Steps
- [ ] 1. **Create auth service**
  📁 src/auth/auth.service.ts
  └─ Handle JWT tokens
    `;
    
    const parsed = parsePlanOutput(sampleOutput);
    
    expect(parsed.title).toBe('Add Authentication');
    expect(parsed.tasks).toHaveLength(1);
    expect(parsed.tasks[0].filePath).toBe('src/auth/auth.service.ts');
  });
});
```

### 5.3 Golden Output Tests

```typescript
// Store known-good outputs for regression testing
const GOLDEN_OUTPUTS = {
  'plan-generate': {
    input: {
      goal: 'Add login page',
      context: 'React app'
    },
    expectedContains: [
      '## Plan:',
      '### Implementation Steps',
      '- [ ]',
      '📁'
    ],
    expectedFormat: 'markdown'
  }
};

describe('Golden Output Tests', () => {
  for (const [name, golden] of Object.entries(GOLDEN_OUTPUTS)) {
    it(`${name} should match expected format`, async () => {
      const output = await generateWithPrompt(name, golden.input);
      
      for (const expected of golden.expectedContains) {
        expect(output).toContain(expected);
      }
    });
  }
});
```

---

## 6. Prompt Templates

### 6.1 Chat System Prompt

```typescript
// extension/src/prompts/system/chat.system.ts

export const CHAT_SYSTEM_PROMPT: PromptDefinition = {
  id: 'system.chat.v1',
  version: '1.0',
  name: 'Chat Mode System Prompt',
  type: 'system',
  
  config: {
    temperature: 0.7,
  },
  
  template: `You are LocalPilot, an AI coding assistant analyzing a local codebase.

## Your Role
- Answer questions about the codebase
- Explain how code works
- Suggest improvements
- Help plan new features

## Your Context
You have access to indexed code from the project through RAG retrieval.
When code is provided in the context, reference it specifically.

## Guidelines
1. Be concise but thorough
2. Reference specific files and line numbers when relevant
3. Use code blocks with language tags
4. If unsure, say so rather than guessing
5. When suggesting implementation, offer to create a plan

## Format
- Use markdown formatting
- Use \`code\` for inline code
- Use code blocks for multi-line code
- Use bullet points for lists

When the user describes a feature they want to implement, suggest:
"Would you like me to create a detailed plan for this? Click 'Transfer to Plan Mode' to proceed."`,
  
  expectedOutput: {
    format: 'markdown',
  },
  
  onParseFailure: 'error',
  
  description: 'System prompt for chat mode conversations',
  changelog: [
    { version: '1.0', date: '2024-01-15', changes: ['Initial version'], author: 'TarekRefaei' }
  ]
};
```

### 6.2 Plan Generation Prompt

```typescript
// extension/src/prompts/templates/plan-generate.prompt.ts

export const PLAN_GENERATE_PROMPT: PromptDefinition = {
  id: 'template.plan-generate.v1',
  version: '1.0',
  name: 'Plan Generation Template',
  type: 'plan',
  
  config: {
    temperature: 0.2,  // Low for consistency
    maxTokens: 2000,
  },
  
  template: `Create a detailed implementation plan for the following goal.

## Goal
{{goal}}

## Project Context
{{context}}

## Relevant Code
{{rag_chunks}}

## Instructions
Create a step-by-step TODO list with the following EXACT format:

## Plan: [Descriptive Title]

### Overview
[2-3 sentences describing what we're building]

### Implementation Steps

- [ ] 1. **[Task Title]**
  📁 \`[exact/file/path.ext]\`
  ├─ [Specific detail 1]
  └─ [Specific detail 2]

- [ ] 2. **[Task Title]**
  📁 \`[exact/file/path.ext]\`
  └─ [Specific detail]

[Continue for all tasks...]

### Testing
- [ ] [How to verify the implementation]

## Rules
1. Each task MUST have a 📁 file path
2. Tasks should be atomic (one file per task)
3. Use existing project patterns from the context
4. Order tasks by dependency (create before use)
5. Include 3-10 tasks typically

Generate the plan now:`,
  
  expectedOutput: {
    format: 'markdown',
    schema: {
      required: ['## Plan:', '### Implementation Steps', '- [ ]', '📁']
    }
  },
  
  onParseFailure: 'retry',
  
  description: 'Generates structured implementation plan from goal',
  changelog: [
    { version: '1.0', date: '2024-01-15', changes: ['Initial version'], author: 'TarekRefaei' }
  ]
};
```

### 6.3 Code Generation Prompt

```typescript
// extension/src/prompts/templates/code-create.prompt.ts

export const CODE_CREATE_PROMPT: PromptDefinition = {
  id: 'template.code-create.v1',
  version: '1.0',
  name: 'Code Creation Template',
  type: 'code',
  
  config: {
    temperature: 0.2,
    maxTokens: 3000,
  },
  
  template: `Generate code for a new file.

## Task
Create file: \`{{file_path}}\`

## Description
{{task_description}}

## Requirements
{{task_details}}

## Project Patterns
The following code shows patterns used in this project:
{{rag_chunks}}

## Instructions
1. Generate ONLY the file content
2. Include all necessary imports
3. Add JSDoc/docstring comments
4. Follow patterns from the project examples
5. Wrap code in \`\`\`{{language}} code block

Generate the complete file:`,
  
  expectedOutput: {
    format: 'code',
  },
  
  onParseFailure: 'retry',
  
  description: 'Generates code for new file creation',
  changelog: [
    { version: '1.0', date: '2024-01-15', changes: ['Initial version'], author: 'TarekRefaei' }
  ]
};
```

---

## 7. Best Practices

### 7.1 Prompt Writing Guidelines

```
┌─────────────────────────────────────────────────────────────────┐
│                  PROMPT WRITING GUIDELINES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DO:                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  ✓ Use clear section headers (##, ###)                         │
│  ✓ Provide explicit format examples                             │
│  ✓ List requirements as numbered points                        │
│  ✓ Include negative examples ("Don't do X")                    │
│  ✓ Use consistent variable naming ({{snake_case}})             │
│  ✓ Keep system prompts under 500 tokens                        │
│  ✓ Test with multiple models if possible                       │
│                                                                  │
│  DON'T:                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  ✗ Use ambiguous instructions                                  │
│  ✗ Assume LLM remembers previous context                       │
│  ✗ Include unnecessary context (wastes tokens)                 │
│  ✗ Use complex nested formats                                   │
│  ✗ Forget to specify output format                             │
│  ✗ Skip testing after changes                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Context Window Management

```typescript
/**
 * Assembles prompt with context, respecting token limits.
 */
function assemblePrompt(
  systemPrompt: string,
  userQuery: string,
  ragChunks: Chunk[],
  history: Message[],
  maxTokens: number = 8000
): string {
  // Reserve tokens for each section
  const systemTokens = 500;
  const responseBuffer = 2000;
  const queryTokens = estimateTokens(userQuery);
  
  const availableForContext = maxTokens - systemTokens - responseBuffer - queryTokens;
  
  // Allocate: 60% RAG, 40% history
  const ragBudget = Math.floor(availableForContext * 0.6);
  const historyBudget = Math.floor(availableForContext * 0.4);
  
  // Truncate RAG chunks
  const ragContext = truncateToTokens(
    formatChunks(ragChunks),
    ragBudget
  );
  
  // Truncate history (keep most recent)
  const historyContext = truncateToTokens(
    formatHistory(history.slice(-10)),
    historyBudget
  );
  
  return `${systemPrompt}

## Retrieved Code Context
${ragContext}

## Conversation History
${historyContext}

## Current Query
${userQuery}`;
}
```

### 7.3 Error Recovery

```typescript
/**
 * Handle prompt failures with retry and fallback.
 */
async function executePromptWithRecovery(
  promptId: string,
  variables: Record<string, string>,
  llm: ILLMProvider
): Promise<string> {
  const definition = PROMPT_REGISTRY[promptId];
  const prompt = getPrompt(promptId, variables);
  
  let attempts = 0;
  const maxAttempts = 3;
  
  while (attempts < maxAttempts) {
    attempts++;
    
    try {
      const response = await llm.chat({
        model: 'qwen2.5-coder:7b',
        messages: [{ role: 'user', content: prompt }],
        options: { temperature: definition.config.temperature }
      });
      
      // Validate output format
      validateOutput(response.content, definition.expectedOutput);
      
      return response.content;
      
    } catch (error) {
      console.warn(`Prompt attempt ${attempts} failed:`, error);
      
      if (attempts >= maxAttempts) {
        if (definition.onParseFailure === 'fallback' && definition.fallbackPromptId) {
          return executePromptWithRecovery(
            definition.fallbackPromptId,
            variables,
            llm
          );
        }
        throw error;
      }
      
      // Add clarification for retry
      variables['_retry_hint'] = 'Please follow the format exactly.';
    }
  }
  
  throw new Error('Prompt execution failed');
}
```

---

*Document Version: 1.0.0*

---