# 📄 DOCUMENT #7: UI_DESIGN_SYSTEM.md
# LocalPilot - UI Design System

**Version:** 1.0  
**Date:** January 2025  
**Status:** Foundation  
**Author:** LocalPilot UI Team

---

## 🔔 UI Strategy Update (January 2025)

LocalPilot's MVP UI will be implemented using the native VS Code side panel Views API and Chat API (not a React webview). The design tokens, principles, and interaction patterns in this document still apply. Any React-based examples below are considered illustrative only and are deprecated for MVP. Use the following native constructs:

- TreeView and TreeItem for navigation and status nodes
- Commands and QuickPick for actions
- Chat participant for conversational UI in the built-in Chat view
- Status bar items and Notifications for lightweight feedback

Styling should rely on VS Code theme tokens. Avoid custom CSS frameworks in MVP.

## 📋 Table of Contents

1. [Design Principles](#design-principles)
2. [Design Tokens](#design-tokens)
3. [Component Library](#component-library)
4. [Layout System](#layout-system)
5. [Typography](#typography)
6. [Icons & Illustrations](#icons--illustrations)
7. [Animations & Transitions](#animations--transitions)
8. [Accessibility](#accessibility)
9. [Dark Mode Support](#dark-mode-support)
10. [Implementation Guide](#implementation-guide)

---

## 🎨 Design Principles

### Core Principles

```yaml
1. Native VS Code Integration
   - Feel like a natural part of VS Code
   - Respect user's theme preferences
   - Use VS Code design language
   - Seamless visual integration

2. Clarity & Simplicity
   - Clear information hierarchy
   - Minimal cognitive load
   - Progressive disclosure
   - Focused user attention

3. Performance-First
   - Fast rendering
   - Smooth animations
   - Lazy loading
   - Optimized re-renders

4. Accessibility
   - WCAG AA compliant
   - Keyboard navigation
   - Screen reader support
   - High contrast support

5. Consistency
   - Predictable interactions
   - Consistent patterns
   - Reusable components
   - Design system adherence
```

### Design Philosophy

> **"LocalPilot should feel invisible until you need it, then indispensable."**

```
Visual Hierarchy Priorities:
1. User Input Area (most prominent)
2. AI Responses (secondary prominence)
3. Context/Metadata (tertiary)
4. Navigation/Controls (subtle but accessible)

Interaction Patterns:
- Optimistic UI updates
- Real-time feedback
- Clear loading states
- Graceful error handling
```

---

## 🎨 Design Tokens

### Color System

```typescript
// webview/src/design/tokens.ts

/**
 * Design tokens for LocalPilot
 * Integrates with VS Code theme system
 */

export const colors = {
  // Primary brand color
  primary: {
    DEFAULT: 'var(--vscode-button-background)',
    hover: 'var(--vscode-button-hoverBackground)',
    active: 'var(--vscode-button-activeBackground)',
    foreground: 'var(--vscode-button-foreground)',
  },
  
  // Semantic colors
  success: {
    DEFAULT: '#4CAF50',
    light: 'rgba(76, 175, 80, 0.1)',
    dark: '#2E7D32',
  },
  
  warning: {
    DEFAULT: '#FF9800',
    light: 'rgba(255, 152, 0, 0.1)',
    dark: '#E65100',
  },
  
  error: {
    DEFAULT: '#F44336',
    light: 'rgba(244, 67, 54, 0.1)',
    dark: '#C62828',
  },
  
  info: {
    DEFAULT: '#2196F3',
    light: 'rgba(33, 150, 243, 0.1)',
    dark: '#1565C0',
  },
  
  // VS Code integrated colors
  background: {
    DEFAULT: 'var(--vscode-editor-background)',
    secondary: 'var(--vscode-sideBar-background)',
    elevated: 'var(--vscode-editorWidget-background)',
    overlay: 'var(--vscode-editorOverlayWidget-background)',
  },
  
  foreground: {
    DEFAULT: 'var(--vscode-foreground)',
    secondary: 'var(--vscode-descriptionForeground)',
    muted: 'var(--vscode-disabledForeground)',
  },
  
  border: {
    DEFAULT: 'var(--vscode-panel-border)',
    focus: 'var(--vscode-focusBorder)',
    contrast: 'var(--vscode-contrastBorder)',
  },
  
  input: {
    background: 'var(--vscode-input-background)',
    foreground: 'var(--vscode-input-foreground)',
    border: 'var(--vscode-input-border)',
    placeholder: 'var(--vscode-input-placeholderForeground)',
  },
  
  list: {
    hover: 'var(--vscode-list-hoverBackground)',
    active: 'var(--vscode-list-activeSelectionBackground)',
    focus: 'var(--vscode-list-focusBackground)',
  },
  
  // Custom LocalPilot colors
  accent: {
    blue: '#00A8E8',
    purple: '#9C27B0',
    green: '#00C853',
    orange: '#FF6D00',
  },
  
  // Code-specific colors
  code: {
    background: 'var(--vscode-textCodeBlock-background)',
    border: 'var(--vscode-textBlockQuote-border)',
    inline: 'var(--vscode-textPreformat-foreground)',
  },
  
  // Link colors
  link: {
    DEFAULT: 'var(--vscode-textLink-foreground)',
    active: 'var(--vscode-textLink-activeForeground)',
  },
} as const;

export type ColorToken = keyof typeof colors;
```

### Spacing System

```typescript
// webview/src/design/tokens.ts

/**
 * Spacing scale (4px base unit)
 */
export const spacing = {
  0: '0',
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',
  8: '32px',
  10: '40px',
  12: '48px',
  16: '64px',
  20: '80px',
  24: '96px',
} as const;

/**
 * Component-specific spacing
 */
export const componentSpacing = {
  // Padding
  paddingXs: spacing[2],   // 8px
  paddingSm: spacing[3],   // 12px
  paddingMd: spacing[4],   // 16px
  paddingLg: spacing[6],   // 24px
  paddingXl: spacing[8],   // 32px
  
  // Gaps
  gapXs: spacing[2],       // 8px
  gapSm: spacing[3],       // 12px
  gapMd: spacing[4],       // 16px
  gapLg: spacing[6],       // 24px
  
  // Margins
  marginXs: spacing[2],
  marginSm: spacing[3],
  marginMd: spacing[4],
  marginLg: spacing[6],
} as const;
```

### Typography

```typescript
// webview/src/design/tokens.ts

/**
 * Typography system
 */
export const typography = {
  fontFamily: {
    base: 'var(--vscode-font-family)',
    mono: 'var(--vscode-editor-font-family)',
  },
  
  fontSize: {
    xs: '11px',
    sm: '12px',
    base: '13px',
    lg: '14px',
    xl: '16px',
    '2xl': '20px',
    '3xl': '24px',
  },
  
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
    loose: 2,
  },
  
  letterSpacing: {
    tight: '-0.02em',
    normal: '0',
    wide: '0.02em',
  },
} as const;

/**
 * Pre-defined text styles
 */
export const textStyles = {
  h1: {
    fontSize: typography.fontSize['3xl'],
    fontWeight: typography.fontWeight.bold,
    lineHeight: typography.lineHeight.tight,
  },
  h2: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.semibold,
    lineHeight: typography.lineHeight.tight,
  },
  h3: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.semibold,
    lineHeight: typography.lineHeight.normal,
  },
  h4: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.medium,
    lineHeight: typography.lineHeight.normal,
  },
  body: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.normal,
    lineHeight: typography.lineHeight.normal,
  },
  bodySmall: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.normal,
    lineHeight: typography.lineHeight.normal,
  },
  code: {
    fontFamily: typography.fontFamily.mono,
    fontSize: typography.fontSize.sm,
    lineHeight: typography.lineHeight.relaxed,
  },
  caption: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.normal,
    lineHeight: typography.lineHeight.normal,
    color: colors.foreground.secondary,
  },
} as const;
```

### Shadows & Elevation

```typescript
// webview/src/design/tokens.ts

/**
 * Shadow system for elevation
 */
export const shadows = {
  none: 'none',
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
} as const;

/**
 * Border radius
 */
export const borderRadius = {
  none: '0',
  sm: '2px',
  DEFAULT: '4px',
  md: '6px',
  lg: '8px',
  xl: '12px',
  full: '9999px',
} as const;
```

### Z-Index Scale

```typescript
// webview/src/design/tokens.ts

/**
 * Z-index scale for layering
 */
export const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,

---

## 🧩 Component Library

### Button Component

```typescript
// webview/src/components/common/Button.tsx

import React from 'react';
import { VSCodeButton } from '@vscode/webview-ui-toolkit/react';
import { spacing } from '../../design/tokens';
import './Button.css';

export interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit';
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  onClick,
  type = 'button',
  className = '',
}) => {
  const classes = [
    'lp-button',
    `lp-button--${variant}`,
    `lp-button--${size}`,
    fullWidth && 'lp-button--full-width',
    disabled && 'lp-button--disabled',
    loading && 'lp-button--loading',
    className,
  ].filter(Boolean).join(' ');
  
  return (
    <VSCodeButton
      appearance={variant === 'primary' ? 'primary' : 'secondary'}
      disabled={disabled || loading}
      onClick={onClick}
      className={classes}
    >
      {loading && (
        <span className="lp-button__spinner">
          <LoadingSpinner size="sm" />
        </span>
      )}
      {!loading && icon && iconPosition === 'left' && (
        <span className="lp-button__icon lp-button__icon--left">
          {icon}
        </span>
      )}
      <span className="lp-button__text">{children}</span>
      {!loading && icon && iconPosition === 'right' && (
        <span className="lp-button__icon lp-button__icon--right">
          {icon}
        </span>
      )}
    </VSCodeButton>
  );
};
```

```css
/* webview/src/components/common/Button.css */

.lp-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 150ms ease;
  font-family: var(--vscode-font-family);
  cursor: pointer;
}

/* Sizes */
.lp-button--sm {
  padding: 4px 12px;
  font-size: 12px;
  height: 24px;
}

.lp-button--md {
  padding: 6px 16px;
  font-size: 13px;
  height: 32px;
}

.lp-button--lg {
  padding: 8px 20px;
  font-size: 14px;
  height: 40px;
}

/* Variants */
.lp-button--primary {
  background: var(--vscode-button-background);
  color: var(--vscode-button-foreground);
}

.lp-button--primary:hover:not(:disabled) {
  background: var(--vscode-button-hoverBackground);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.lp-button--secondary {
  background: var(--vscode-button-secondaryBackground);
  color: var(--vscode-button-secondaryForeground);
  border: 1px solid var(--vscode-button-border);
}

.lp-button--ghost {
  background: transparent;
  color: var(--vscode-foreground);
  border: none;
}

.lp-button--ghost:hover:not(:disabled) {
  background: var(--vscode-list-hoverBackground);
}

.lp-button--danger {
  background: #F44336;
  color: white;
}

/* States */
.lp-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lp-button--loading {
  pointer-events: none;
}

.lp-button--full-width {
  width: 100%;
}

/* Icon */
.lp-button__icon {
  display: flex;
  align-items: center;
  font-size: 16px;
}

/* Spinner */
.lp-button__spinner {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

/* Focus state */
.lp-button:focus-visible {
  outline: 2px solid var(--vscode-focusBorder);
  outline-offset: 2px;
}
```

### Input Component

```typescript
// webview/src/components/common/Input.tsx

import React, { forwardRef } from 'react';
import { VSCodeTextField } from '@vscode/webview-ui-toolkit/react';
import './Input.css';

export interface InputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  label?: string;
  helperText?: string;
  type?: 'text' | 'password' | 'email' | 'number';
  autoFocus?: boolean;
  maxLength?: number;
  className?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({
  value,
  onChange,
  placeholder,
  disabled = false,
  error,
  label,
  helperText,
  type = 'text',
  autoFocus = false,
  maxLength,
  className = '',
}, ref) => {
  return (
    <div className={`lp-input-wrapper ${className}`}>
      {label && (
        <label className="lp-input-label">
          {label}
        </label>
      )}
      <VSCodeTextField
        ref={ref}
        value={value}
        onInput={(e: any) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        type={type}
        autofocus={autoFocus}
        maxlength={maxLength}
        className={`lp-input ${error ? 'lp-input--error' : ''}`}
      />
      {error && (
        <span className="lp-input-error">
          {error}
        </span>
      )}
      {helperText && !error && (
        <span className="lp-input-helper">
          {helperText}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';
```

### TextArea Component

```typescript
// webview/src/components/common/TextArea.tsx

import React, { forwardRef, useRef, useEffect } from 'react';
import { VSCodeTextArea } from '@vscode/webview-ui-toolkit/react';
import './TextArea.css';

export interface TextAreaProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  rows?: number;
  maxRows?: number;
  autoResize?: boolean;
  error?: string;
  label?: string;
  maxLength?: number;
  showCount?: boolean;
  onKeyDown?: (e: React.KeyboardEvent) => void;
  className?: string;
}

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(({
  value,
  onChange,
  placeholder,
  disabled = false,
  rows = 3,
  maxRows = 10,
  autoResize = true,
  error,
  label,
  maxLength,
  showCount = false,
  onKeyDown,
  className = '',
}, ref) => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  
  // Auto-resize functionality
  useEffect(() => {
    if (autoResize && textAreaRef.current) {
      const element = textAreaRef.current;
      element.style.height = 'auto';
      
      const scrollHeight = element.scrollHeight;
      const lineHeight = parseInt(getComputedStyle(element).lineHeight);
      const maxHeight = lineHeight * maxRows;
      
      element.style.height = `${Math.min(scrollHeight, maxHeight)}px`;
    }
  }, [value, autoResize, maxRows]);
  
  return (
    <div className={`lp-textarea-wrapper ${className}`}>
      {label && (
        <label className="lp-textarea-label">
          {label}
        </label>
      )}
      <VSCodeTextArea
        ref={textAreaRef}
        value={value}
        onInput={(e: any) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        rows={rows}
        maxlength={maxLength}
        onKeyDown={onKeyDown}
        className={`lp-textarea ${error ? 'lp-textarea--error' : ''}`}
      />
      <div className="lp-textarea-footer">
        {error && (
          <span className="lp-textarea-error">
            {error}
          </span>
        )}
        {showCount && maxLength && (
          <span className="lp-textarea-count">
            {value.length} / {maxLength}
          </span>
        )}
      </div>
    </div>
  );
});

TextArea.displayName = 'TextArea';
```

### ProgressBar Component

```typescript
// webview/src/components/common/ProgressBar.tsx

import React from 'react';
import { VSCodeProgressRing } from '@vscode/webview-ui-toolkit/react';
import './ProgressBar.css';

export interface ProgressBarProps {
  value: number; // 0-100
  label?: string;
  showPercentage?: boolean;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'success' | 'warning' | 'error';
  indeterminate?: boolean;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  label,
  showPercentage = true,
  size = 'md',
  variant = 'default',
  indeterminate = false,
  className = '',
}) => {
  const percentage = Math.min(Math.max(value, 0), 100);
  
  return (
    <div className={`lp-progress ${className}`}>
      {label && (
        <div className="lp-progress-header">
          <span className="lp-progress-label">{label}</span>
          {showPercentage && !indeterminate && (
            <span className="lp-progress-percentage">
              {percentage.toFixed(1)}%
            </span>
          )}
        </div>
      )}
      <div className={`lp-progress-track lp-progress--${size}`}>
        <div
          className={`lp-progress-fill lp-progress-fill--${variant}`}
          style={{
            width: indeterminate ? '100%' : `${percentage}%`,
            animation: indeterminate ? 'progress-indeterminate 1.5s ease-in-out infinite' : 'none',
          }}
        />
      </div>
    </div>
  );
};
```

```css
/* webview/src/components/common/ProgressBar.css */

.lp-progress {
  width: 100%;
}

.lp-progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.lp-progress-label {
  font-size: 12px;
  color: var(--vscode-foreground);
}

.lp-progress-percentage {
  font-size: 12px;
  color: var(--vscode-descriptionForeground);
  font-variant-numeric: tabular-nums;
}

.lp-progress-track {
  background: var(--vscode-progressBar-background);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.lp-progress--sm {
  height: 4px;
}

.lp-progress--md {
  height: 8px;
}

.lp-progress--lg {
  height: 12px;
}

.lp-progress-fill {
  height: 100%;
  transition: width 300ms ease;
  border-radius: 4px;
}

.lp-progress-fill--default {
  background: var(--vscode-progressBar-background);
}

.lp-progress-fill--success {
  background: #4CAF50;
}

.lp-progress-fill--warning {
  background: #FF9800;
}

.lp-progress-fill--error {
  background: #F44336;
}

@keyframes progress-indeterminate {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
```

### Message Component (Chat)

```typescript
// webview/src/components/chat/Message.tsx

import React from 'react';
import { MessageRole } from '../../../shared/types/chat';
import { CodeBlock } from '../common/CodeBlock';
import { FileReference } from './FileReference';
import './Message.css';

export interface MessageProps {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  streaming?: boolean;
  contextFiles?: Array<{
    path: string;
    lines: string;
    relevance: number;
  }>;
}

export const Message: React.FC<MessageProps> = ({
  role,
  content,
  timestamp,
  streaming = false,
  contextFiles,
}) => {
  const isUser = role === 'user';
  
  // Parse content for code blocks and file references
  const parsedContent = parseMessageContent(content);
  
  return (
    <div className={`lp-message lp-message--${role}`}>
      <div className="lp-message-header">
        <span className="lp-message-role">
          {isUser ? '👤 You' : '🤖 LocalPilot'}
        </span>
        <span className="lp-message-timestamp">
          {formatTimestamp(timestamp)}
        </span>
      </div>
      
      <div className="lp-message-content">
        {parsedContent.map((block, index) => {
          if (block.type === 'text') {
            return (
              <p key={index} className="lp-message-text">
                {block.content}
              </p>
            );
          } else if (block.type === 'code') {
            return (
              <CodeBlock
                key={index}
                code={block.content}
                language={block.language}
              />
            );
          }
          return null;
        })}
        
        {streaming && (
          <span className="lp-message-cursor">▊</span>
        )}
      </div>
      
      {contextFiles && contextFiles.length > 0 && (
        <div className="lp-message-context">
          <details>
            <summary>
              📎 Context ({contextFiles.length} files)
            </summary>
            <div className="lp-message-context-list">
              {contextFiles.map((file, index) => (
                <FileReference
                  key={index}
                  path={file.path}
                  lines={file.lines}
                  relevance={file.relevance}
                />
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
};

// Helper functions
function parseMessageContent(content: string) {
  // Parse markdown-style code blocks and text
  const blocks: Array<{
    type: 'text' | 'code';
    content: string;
    language?: string;
  }> = [];
  
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  let lastIndex = 0;
  let match;
  
  while ((match = codeBlockRegex.exec(content)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      blocks.push({
        type: 'text',
        content: content.slice(lastIndex, match.index).trim(),
      });
    }
    
    // Add code block
    blocks.push({
      type: 'code',
      content: match[2].trim(),
      language: match[1] || 'text',
    });
    
    lastIndex = match.index + match[0].length;
  }
  
  // Add remaining text
  if (lastIndex < content.length) {
    blocks.push({
      type: 'text',
      content: content.slice(lastIndex).trim(),
    });
  }
  
  return blocks;
}

function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
```

### CodeBlock Component

```typescript
// webview/src/components/common/CodeBlock.tsx

import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from './Button';
import './CodeBlock.css';

export interface CodeBlockProps {
  code: string;
  language: string;
  showLineNumbers?: boolean;
  fileName?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language,
  showLineNumbers = true,
  fileName,
}) => {
  const [copied, setCopied] = useState(false);
  
  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  return (
    <div className="lp-codeblock">
      <div className="lp-codeblock-header">
        {fileName && (
          <span className="lp-codeblock-filename">{fileName}</span>
        )}
        <span className="lp-codeblock-language">{language}</span>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleCopy}
          icon={copied ? '✓' : '📋'}
        >
          {copied ? 'Copied!' : 'Copy'}
        </Button>
      </div>
      <SyntaxHighlighter
        language={language}
        style={vscDarkPlus}
        showLineNumbers={showLineNumbers}
        customStyle={{
          margin: 0,
          borderRadius: '0 0 4px 4px',
          fontSize: '12px',
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
};
```

### FileReference Component

```typescript
// webview/src/components/chat/FileReference.tsx

import React from 'react';
import './FileReference.css';

export interface FileReferenceProps {
  path: string;
  lines: string;
  relevance: number;
  onClick?: () => void;
}

export const FileReference: React.FC<FileReferenceProps> = ({
  path,
  lines,
  relevance,
  onClick,
}) => {
  return (
    <div
      className="lp-file-reference"
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      <div className="lp-file-reference-icon">📄</div>
      <div className="lp-file-reference-content">
        <div className="lp-file-reference-path">{path}</div>
        <div className="lp-file-reference-meta">
          <span className="lp-file-reference-lines">Lines {lines}</span>
          <span className="lp-file-reference-relevance">
            {(relevance * 100).toFixed(0)}% relevant
          </span>
        </div>
      </div>
      <div className="lp-file-reference-arrow">→</div>
    </div>
  );
};
```

```css
/* webview/src/components/chat/FileReference.css */

.lp-file-reference {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: var(--vscode-input-background);
  border: 1px solid var(--vscode-input-border);
  border-radius: 4px;
  cursor: pointer;
  transition: all 150ms ease;
}

.lp-file-reference:hover {
  background: var(--vscode-list-hoverBackground);
  border-color: var(--vscode-focusBorder);
}

.lp-file-reference-icon {
  font-size: 20px;
}

.lp-file-reference-content {
  flex: 1;
  min-width: 0;
}

.lp-file-reference-path {
  font-size: 13px;
  color: var(--vscode-textLink-foreground);
  font-family: var(--vscode-editor-font-family);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.lp-file-reference-meta {
  display: flex;
  gap: 12px;
  margin-top: 2px;
  font-size: 11px;
  color: var(--vscode-descriptionForeground);
}

.lp-file-reference-arrow {
  color: var(--vscode-descriptionForeground);
  font-size: 14px;
}
```

### TodoItem Component

```typescript
// webview/src/components/plan/TodoItem.tsx

import React, { useState } from 'react';
import { TodoItem as TodoItemType, TodoStatus, FileOperationType } from '../../../shared/types/plan';
import { Button } from '../common/Button';
import './TodoItem.css';

export interface TodoItemProps {
  todo: TodoItemType;
  onEdit?: () => void;
  onDelete?: () => void;
  onToggle?: () => void;
}

export const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  onEdit,
  onDelete,
  onToggle,
}) => {
  const [expanded, setExpanded] = useState(false);
  
  const getStatusIcon = (status: TodoStatus) => {
    switch (status) {
      case 'completed': return '✓';
      case 'in_progress': return '⟳';
      case 'failed': return '✗';
      case 'skipped': return '⊘';
      default: return '○';
    }
  };
  
  const getTypeIcon = (type: FileOperationType) => {
    switch (type) {
      case 'create': return '➕';
      case 'modify': return '✏️';
      case 'delete': return '🗑️';
      case 'research': return '🔍';
    }
  };
  
  return (
    <div className={`lp-todo-item lp-todo-item--${todo.status}`}>
      <div className="lp-todo-item-header" onClick={() => setExpanded(!expanded)}>
        <div className="lp-todo-item-status">
          <span className="lp-todo-item-status-icon">
            {getStatusIcon(todo.status)}
          </span>
        </div>
        
        <div className="lp-todo-item-content">
          <div className="lp-todo-item-title">
            <span className="lp-todo-item-type-icon">
              {getTypeIcon(todo.type)}
            </span>
            {todo.title}
          </div>
          <div className="lp-todo-item-meta">
            <span>{todo.files.length} file{todo.files.length !== 1 ? 's' : ''}</span>
            {todo.dependencies.length > 0 && (
              <span>• Depends on {todo.dependencies.length} TODO{todo.dependencies.length !== 1 ? 's' : ''}</span>
            )}
          </div>
        </div>
        
        <div className="lp-todo-item-actions">
          <button
            className="lp-todo-item-expand"
            onClick={(e) => {
              e.stopPropagation();
              setExpanded(!expanded);
            }}
          >
            {expanded ? '▼' : '▶'}
          </button>
        </div>
      </div>
      
      {expanded && (
        <div className="lp-todo-item-details">
          <div className="lp-todo-item-description">
            {todo.description}
          </div>
          
          <div className="lp-todo-item-files">
            <h4>Files to modify:</h4>
            <ul>
              {todo.files.map((file, index) => (
                <li key={index}>
                  <span className="lp-todo-file-operation">
                    {file.operation.toUpperCase()}
                  </span>
                  <span className="lp-todo-file-path">{file.path}</span>
                  {file.estimatedChanges && (
                    <span className="lp-todo-file-changes">
                      {file.estimatedChanges}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </div>
          
          {todo.error && (
            <div className="lp-todo-item-error">
              <strong>Error:</strong> {todo.error}
            </div>
          )}
          
          <div className="lp-todo-item-footer">
            <Button variant="ghost" size="sm" onClick={onEdit}>
              Edit
            </Button>
            <Button variant="ghost" size="sm" onClick={onDelete}>
              Delete
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};
```

### LoadingSpinner Component

```typescript
// webview/src/components/common/LoadingSpinner.tsx

import React from 'react';
import './LoadingSpinner.css';

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  text,
  className = '',
}) => {
  return (
    <div className={`lp-spinner-wrapper ${className}`}>
      <div className={`lp-spinner lp-spinner--${size}`}>
        <div className="lp-spinner-circle" />
      </div>
      {text && (
        <span className="lp-spinner-text">{text}</span>
      )}
    </div>
  );
};
```

```css
/* webview/src/components/common/LoadingSpinner.css */

.lp-spinner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.lp-spinner {
  display: inline-block;
  position: relative;
}

.lp-spinner--sm {
  width: 16px;
  height: 16px;
}

.lp-spinner--md {
  width: 24px;
  height: 24px;
}

.lp-spinner--lg {
  width: 40px;
  height: 40px;
}

.lp-spinner-circle {
  width: 100%;
  height: 100%;
  border: 2px solid var(--vscode-progressBar-background);
  border-top-color: var(--vscode-button-background);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.lp-spinner-text {
  font-size: 12px;
  color: var(--vscode-descriptionForeground);
}
```

---

## 📐 Layout System

### Main Layout

```typescript
// webview/src/layouts/MainLayout.tsx

import React from 'react';
import { TabNav } from '../components/navigation/TabNav';
import './MainLayout.css';

export interface MainLayoutProps {
  children: React.ReactNode;
  currentTab: 'chat' | 'plan' | 'act';
  onTabChange: (tab: string) => void;
  onReindex?: () => void;
  onSettings?: () => void;
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  currentTab,
  onTabChange,
  onReindex,
  onSettings,
}) => {
  return (
    <div className="lp-layout">
      <header className="lp-layout-header">
        <TabNav
          currentTab={currentTab}
          onTabChange={onTabChange}
        />
        <div className="lp-layout-actions">
          <button
            className="lp-layout-action-btn"
            onClick={onReindex}
            title="Re-index workspace"
          >
            🔄
          </button>
          <button
            className="lp-layout-action-btn"
            onClick={onSettings}
            title="Settings"
          >
            ⚙️
          </button>
        </div>
      </header>
      
      <main className="lp-layout-content">
        {children}
      </main>
    </div>
  );
};
```

```css
/* webview/src/layouts/MainLayout.css */

.lp-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--vscode-editor-background);
  color: var(--vscode-foreground);
  font-family: var(--vscode-font-family);
}

.lp-layout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  border-bottom: 1px solid var(--vscode-panel-border);
  background: var(--vscode-sideBar-background);
}

.lp-layout-actions {
  display: flex;
  gap: 8px;
}

.lp-layout-action-btn {
  background: transparent;
  border: none;
  color: var(--vscode-foreground);
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 150ms ease;
}

.lp-layout-action-btn:hover {
  background: var(--vscode-list-hoverBackground);
}

.lp-layout-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
```

### Chat View Layout

```typescript
// webview/src/views/ChatView.tsx

import React, { useRef, useEffect } from 'react';
import { Message } from '../components/chat/Message';
import { TextArea } from '../components/common/TextArea';
import { Button } from '../components/common/Button';
import './ChatView.css';

export const ChatView: React.FC = () => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [message, setMessage] = React.useState('');
  const [messages, setMessages] = React.useState([]);
  const [streaming, setStreaming] = React.useState(false);
  
  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSend = () => {
    if (!message.trim()) return;
    
    // Send message logic
    setMessage('');
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <div className="lp-chat-view">
      <div className="lp-chat-messages">
        {messages.map((msg) => (
          <Message key={msg.id} {...msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="lp-chat-input-area">
        <TextArea
          value={message}
          onChange={setMessage}
          placeholder="Ask about your codebase... (Ctrl+Enter to send)"
          rows={3}
          maxRows={10}
          autoResize
          onKeyDown={handleKeyDown}
          disabled={streaming}
        />
        <div className="lp-chat-input-footer">
          <span className="lp-chat-input-hint">
            Ctrl+Enter to send
          </span>
          <Button
            onClick={handleSend}
            disabled={!message.trim() || streaming}
            loading={streaming}
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};
```

```css
/* webview/src/views/ChatView.css */

.lp-chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.lp-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.lp-chat-input-area {
  border-top: 1px solid var(--vscode-panel-border);
  padding: 16px;
  background: var(--vscode-sideBar-background);
}

.lp-chat-input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.lp-chat-input-hint {
  font-size: 11px;
  color: var(--vscode-descriptionForeground);
}
```

---

## 🎬 Animations & Transitions

### Animation Tokens

```typescript
// webview/src/design/animations.ts

export const animations = {
  // Durations
  duration: {
    fast: '150ms',
    base: '200ms',
    slow: '300ms',
    slower: '500ms',
  },
  
  // Easing functions
  easing: {
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    spring: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;
```

### Common Animations

```css
/* webview/src/design/animations.css */

/* Fade in */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fadeIn 200ms ease-out;
}

/* Slide in from bottom */
@keyframes slideInUp {
  from {
    transform: translateY(10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-in-up {
  animation: slideInUp 200ms ease-out;
}

/* Pulse (for loading states) */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Skeleton loader */
@keyframes skeleton {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
}

.animate-skeleton {
  background: linear-gradient(
    90deg,
    var(--vscode-input-background) 0px,
    var(--vscode-list-hoverBackground) 40px,
    var(--vscode-input-background) 80px
  );
  background-size: 200px 100%;
  animation: skeleton 1.5s ease-in-out infinite;
}

/* Typing indicator */
@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background: var(--vscode-foreground);
  border-radius: 50%;
  animation: typing 1.4s ease-in-out infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}
```

---

## ♿ Accessibility

### Accessibility Guidelines

```yaml
Keyboard Navigation:
  - All interactive elements focusable
  - Logical tab order
  - Escape key closes modals/dropdowns
  - Enter/Space activates buttons
  - Arrow keys for navigation in lists

Screen Reader Support:
  - Semantic HTML elements
  - ARIA labels on all controls
  - ARIA live regions for dynamic content
  - Alt text for images
  - Skip navigation links

Focus Management:
  - Visible focus indicators
  - Focus trap in modals
  - Return focus after modal close
  - Focus on first input in forms

Color & Contrast:
  - WCAG AA compliant (4.5:1 for text)
  - Don't rely on color alone
  - Respect user's theme preferences
  - Support high contrast mode
```

### Accessibility Utilities

```typescript
// webview/src/utils/accessibility.ts

/**
 * Screen reader only text
 */
export const srOnly: React.CSSProperties = {
  position: 'absolute',
  width: '1px',
  height: '1px',
  padding: 0,
  margin: '-1px',
  overflow: 'hidden',
  clip: 'rect(0, 0, 0, 0)',
  whiteSpace: 'nowrap',
  borderWidth: 0,
};

/**
 * Focus trap for modals
 */
export function useFocusTrap(ref: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };
    
    element.addEventListener('keydown', handleTab);
    firstElement?.focus();
    
    return () => {
      element.removeEventListener('keydown', handleTab);
    };
  }, [ref]);
}

/**
 * Announce to screen readers
 */
export function announce(message: string, priority: 'polite' | 'assertive' = 'polite') {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.style.cssText = Object.entries(srOnly)
    .map(([key, value]) => `${key}: ${value}`)
    .join('; ');
  announcement.textContent = message;
  
  document.body.appendChild(announcement);
  
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
}
```

---

## 🌓 Dark Mode Support

### Theme Integration

```typescript
// webview/src/hooks/useTheme.ts

import { useState, useEffect } from 'react';

export type Theme = 'dark' | 'light' | 'high-contrast';

export function useTheme() {
  const [theme, setTheme] = useState<Theme>('dark');
  
  useEffect(() => {
    // Detect VS Code theme
    const computedStyle = getComputedStyle(document.body);
    const backgroundColor = computedStyle.getPropertyValue('--vscode-editor-background');
    
    // Simple heuristic: if background is dark, it's a dark theme
    const isDark = isColorDark(backgroundColor);
    setTheme(isDark ? 'dark' : 'light');
    
    // Listen for theme changes
    const observer = new MutationObserver(() => {
      const newBg = getComputedStyle(document.body).getPropertyValue('--vscode-editor-background');
      const newIsDark = isColorDark(newBg);
      setTheme(newIsDark ? 'dark' : 'light');
    });
    
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'style'],
    });
    
    return () => observer.disconnect();
  }, []);
  
  return theme;
}

function isColorDark(color: string): boolean {
  // Parse RGB color and calculate luminance
  const rgb = color.match(/\d+/g);
  if (!rgb || rgb.length < 3) return true;
  
  const [r, g, b] = rgb.map(Number);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  return luminance < 0.5;
}
```

---

## 🛠️ Implementation Guide

### Setup Tailwind CSS

```javascript
// webview/tailwind.config.js

module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'vscode-bg': 'var(--vscode-editor-background)',
        'vscode-fg': 'var(--vscode-foreground)',
        'vscode-border': 'var(--vscode-panel-border)',
      },
      fontFamily: {
        sans: 'var(--vscode-font-family)',
        mono: 'var(--vscode-editor-font-family)',
      },
    },
  },
  plugins: [],
  // Prevent Tailwind from overriding VS Code variables
  corePlugins: {
    preflight: false,
  },
};
```

### Global Styles

```css
/* webview/src/index.css */

/* VS Code theme integration */
:root {
  /* Use VS Code CSS variables */
  color-scheme: var(--vscode-color-scheme, dark);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--vscode-font-family);
  font-size: 13px;
  color: var(--vscode-foreground);
  background: var(--vscode-editor-background);
  overflow: hidden;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: var(--vscode-scrollbarSlider-background);
}

::-webkit-scrollbar-thumb {
  background: var(--vscode-scrollbarSlider-background);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--vscode-scrollbarSlider-hoverBackground);
}

::-webkit-scrollbar-thumb:active {
  background: var(--vscode-scrollbarSlider-activeBackground);
}

/* Focus visible (keyboard only) */
:focus-visible {
  outline: 2px solid var(--vscode-focusBorder);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}

/* Selection */
::selection {
  background: var(--vscode-editor-selectionBackground);
}
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and mission
- `TECHNICAL_ARCHITECTURE.md` - System architecture
- `USER_JOURNEY.md` - User flows and wireframes (PREVIOUS)
- `API_SPECIFICATION.md` - API documentation
- `DATA_MODELS.md` - Data schemas
- `INDEXING_SYSTEM_SPEC.md` - Indexing deep dive
- `DEVELOPMENT_GUIDE.md` - Setup and workflow (NEXT)
- `TESTING_STRATEGY.md` - Test specifications

---

**END OF DOCUMENT**