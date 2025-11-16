# 📄 DOCUMENT #3: USER_JOURNEY.md
# LocalPilot - User Journey & UX Specification

**Version:** 1.0  
**Date:** January 2025  
**Status:** Foundation  
**Author:** LocalPilot UX Team

---

## 📋 Table of Contents

1. [User Personas](#user-personas)
2. [User Stories](#user-stories)
3. [Complete User Flows](#complete-user-flows)
4. [UI Wireframes](#ui-wireframes)
5. [Interaction Patterns](#interaction-patterns)
6. [Visual Design System](#visual-design-system)
7. [Information Architecture](#information-architecture)
8. [Error States & Recovery](#error-states--recovery)
9. [Accessibility](#accessibility)
10. [Success Metrics](#success-metrics)

---

## 👤 User Personas

### Persona 1: **Alex - The Privacy-Conscious Developer**

```yaml
Name: Alex Chen
Age: 32
Role: Senior Full-Stack Developer
Experience: 8 years
Location: Remote worker, travels frequently

Background:
  - Works for a fintech startup
  - Handles sensitive financial code
  - Cannot use cloud-based AI assistants due to company policy
  - Often works offline (planes, cafes with poor internet)

Goals:
  - Code faster without compromising security
  - Understand large codebases quickly
  - Generate boilerplate code safely
  - Maintain full control over code and data

Pain Points:
  - Cloud AI assistants violate company security policy
  - Manual code exploration is time-consuming
  - Repetitive coding tasks slow development
  - No AI assistance when offline

Technical Setup:
  - MacBook Pro (M2, 16GB RAM)
  - VS Code power user
  - Familiar with terminal and Git
  - Has used GitHub Copilot before (can't anymore)

Usage Scenario:
  "I need to add authentication to our payment service. 
  I want AI to help me plan the implementation and generate 
  code, but I can't send our codebase to the cloud."
```

### Persona 2: **Maya - The Junior Developer**

```yaml
Name: Maya Rodriguez
Age: 24
Role: Junior Frontend Developer
Experience: 1.5 years
Location: Office-based, small startup

Background:
  - Recently graduated from bootcamp
  - Learning React and TypeScript
  - Overwhelmed by large codebase
  - Limited budget (no paid AI tools)

Goals:
  - Learn codebase structure quickly
  - Understand how features are implemented
  - Get help with debugging
  - Build features with guidance

Pain Points:
  - Gets lost in large projects
  - Struggles to find relevant code
  - Needs to ask senior devs frequently
  - Can't afford paid AI assistants

Technical Setup:
  - Windows laptop (NVIDIA GTX 1660, 16GB RAM)
  - Basic VS Code setup
  - Git beginner (knows basics)
  - No prior AI assistant experience

Usage Scenario:
  "I need to fix a bug in the checkout flow. Where do I 
  even start? I want to ask questions about the code 
  without bothering my team."
```

### Persona 3: **Sam - The Open Source Contributor**

```yaml
Name: Sam Okafor
Age: 28
Role: DevOps Engineer / OSS Contributor
Experience: 5 years
Location: Nigeria (intermittent internet)

Background:
  - Contributes to open source projects
  - Limited budget and bandwidth
  - Runs local LLMs for AI experiments
  - Active in developer communities

Goals:
  - Contribute to unfamiliar codebases efficiently
  - Understand project architecture quickly
  - Generate comprehensive PRs
  - Work offline during power outages

Pain Points:
  - Cloud AI tools expensive in local currency
  - Unreliable internet connection
  - Need to learn new codebases frequently
  - Limited GPU (GTX 1650, 4GB VRAM)

Technical Setup:
  - Linux (Ubuntu), mid-range PC
  - Advanced terminal user
  - Git expert
  - Already uses Ollama for experiments

Usage Scenario:
  "I want to add a feature to an OSS project I just 
  discovered. I need to understand the codebase fast 
  and generate a solid PR, all offline."
```

---

## 📖 User Stories

### Epic 1: First-Time Setup

```gherkin
Feature: First-Time Setup Experience
  As a new user
  I want a smooth onboarding experience
  So that I can start using LocalPilot quickly

  Scenario: User installs extension
    Given I have VS Code and Ollama installed
    When I install LocalPilot extension
    Then I should see a welcome screen
    And the extension should check my system requirements
    And guide me through initial setup
  
  Scenario: User configures models
    Given I have completed the welcome screen
    When I reach model configuration
    Then I should see my available Ollama models
    And receive smart recommendations based on my hardware
    And be warned if my configuration is dangerous
  
  Scenario: User starts first indexing
    Given I have configured models successfully
    When I start indexing my workspace
    Then I should see clear progress indicators
    And understand what's happening at each phase
    And receive a project summary when complete
```

### Epic 2: Chat Mode Usage

```gherkin
Feature: Conversational Code Exploration
  As a developer
  I want to chat with AI about my codebase
  So that I can understand it better and get assistance

  Scenario: Ask about codebase architecture
    Given I have indexed my workspace
    When I ask "How does authentication work in this app?"
    Then the AI should retrieve relevant code
    And provide a clear explanation with file references
    And show which files it's referencing
  
  Scenario: Request feature implementation plan
    Given I'm chatting about adding a new feature
    When the AI suggests a plan
    Then I should see a "Transfer to Plan" button
    And be able to review the plan before transferring
  
  Scenario: View chat history
    Given I have multiple chat sessions
    When I navigate chat mode
    Then I should see my conversation history
    And be able to continue previous conversations
```

### Epic 3: Plan Mode Usage

```gherkin
Feature: Structured Feature Planning
  As a developer
  I want to create detailed implementation plans
  So that I can execute complex features systematically

  Scenario: Create plan from chat suggestion
    Given AI has suggested a feature plan in chat
    When I transfer to Plan mode
    Then I should see a structured TODO list
    And be able to edit each TODO item
    And see dependencies between items
  
  Scenario: Manually create plan
    Given I'm in Plan mode
    When I create a new plan manually
    Then I should have a plan editor interface
    And be able to add/remove/reorder TODO items
    And define what files each TODO will affect
  
  Scenario: Validate plan before execution
    Given I have completed a plan
    When I click "Start Implementation"
    Then I should see a summary of changes
    And be warned about Git requirements
    And confirm before Act mode begins
```

### Epic 4: Act Mode Usage

```gherkin
Feature: Safe Code Generation
  As a developer
  I want AI to implement code safely
  So that I don't lose work or introduce bugs

  Scenario: Execute plan with Git safety
    Given I have a validated plan
    When Act mode begins execution
    Then a safety branch should be created
    And I should see each file change before it happens
    And be able to approve/reject each change
  
  Scenario: Review generated code
    Given Act mode has generated code for a TODO
    When I review the changes
    Then I should see syntax-highlighted diffs
    And be able to edit before approval
    And have options to Skip/Retry/Rollback
  
  Scenario: Handle execution failure
    Given Act mode encounters an error
    When a TODO fails
    Then execution should pause
    And I should see the error clearly
    And have options to retry, skip, or abort
    And be able to rollback to previous state
```

### Epic 5: Ongoing Usage

```gherkin
Feature: Daily Workflow Integration
  As a regular user
  I want LocalPilot to integrate seamlessly
  So that it enhances my workflow without friction

  Scenario: Incremental re-indexing
    Given I have an indexed workspace
    When I modify files and save
    Then LocalPilot should detect changes
    And incrementally update the index
    And keep the context fresh
  
  Scenario: Quick code questions
    Given I'm viewing a file in VS Code
    When I select code and ask a question
    Then LocalPilot should prioritize that code in context
    And provide relevant answers quickly
  
  Scenario: Model performance adjustment
    Given I notice slow responses
    When I check settings
    Then I should be able to switch to faster models
    And see estimated performance impact
```

---

## 🗺️ Complete User Flows

### Flow 1: First-Time User Experience (FTUE)

```
┌─────────────────────────────────────────────────────────────┐
│                    FIRST-TIME SETUP FLOW                    │
└─────────────────────────────────────────────────────────────┘

Step 1: Extension Activation
├── User installs from VS Code Marketplace
├── Opens a workspace in VS Code
├── Extension activates automatically
└── Shows welcome screen

Step 2: System Requirements Check
├── Check Ollama installation
│   ├── ✓ Found → Continue
│   └── ✗ Not found → Show installation guide
├── Check available models
│   ├── ✓ Models found → List them
│   └── ✗ No models → Show model download guide
├── Check system resources
│   ├── Detect VRAM
│   ├── Detect RAM
│   └── Detect CPU
└── Display system compatibility report

Step 3: Model Configuration
├── Display detected models
├── Show recommended configuration
├── User selects models for each task:
│   ├── Embedding model: [bge-m3] ✓
│   ├── Chat model: [qwen2.5-coder:7b] ✓
│   ├── Planning model: [qwen2.5-coder:14b] ⚠️
│   └── Coding model: [qwen2.5-coder:14b] ⚠️
├── Real-time VRAM calculation
│   └── Show warnings if configuration is unsafe
├── User confirms or adjusts
└── Save configuration

Step 4: Indexing Preferences
├── Show workspace structure preview
├── User sets preferences:
│   ├── Exclude patterns (default: node_modules, .git)
│   ├── Max file size (default: 10MB)
│   └── Languages to index (auto-detect)
├── Show estimated indexing time
└── User confirms

Step 5: Initial Indexing
├── Create .localpilot/ directory
├── Initialize vector database
├── Start indexing with progress UI:
│   ├── Phase 1: Discovery (10%)
│   ├── Phase 2: Documentation (30%)
│   ├── Phase 3: Code Structure (50%)
│   ├── Phase 4: Semantic Chunking (80%)
│   └── Phase 5: Summarization (100%)
├── Stream progress updates to UI
└── Complete with project summary

Step 6: Welcome to LocalPilot
├── Display project summary
├── Show quick tips:
│   ├── "Ask me anything about your codebase"
│   ├── "Use Plan mode to break down features"
│   └── "Act mode safely implements with Git"
├── Enable all three modes
└── Focus on Chat mode to start

Total Time: ~8-12 minutes (depending on project size)
```

### Flow 2: Daily Chat Usage

```
┌─────────────────────────────────────────────────────────────┐
│                    CHAT MODE WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘

Entry Point:
└── Open VS Code Chat view (LocalPilot participant) or select Chat in LocalPilot side panel

Interaction Flow:

1. User asks question
   ├── Types: "How does the payment processing work?"
   ├── Optionally selects code in editor (auto-included)
   └── Clicks Send or presses Ctrl+Enter

2. Backend processes
   ├── Embed query (bge-m3, ~200ms)
   ├── Retrieve context from vector DB (~300ms)
   ├── Build prompt with:
   │   ├── System instructions
   │   ├── Project summary
   │   ├── Retrieved code chunks (top-5)
   │   ├── Current file (if any)
   │   └── User question
   └── Stream response from LLM (qwen2.5-coder:7b)

3. UI updates
   ├── Show "Thinking..." indicator
   ├── Display retrieved context (collapsible):
   │   └── payment-service.ts (lines 45-67, 89% relevant)
   │       payment-gateway.ts (lines 12-34, 82% relevant)
   ├── Stream AI response incrementally
   ├── Highlight code blocks with syntax
   └── Show file references as clickable links

4. User reviews response
   ├── Clicks file reference → Opens in editor
   ├── Asks follow-up question → Back to step 1
   ├── Response is good → Continues conversation
   └── Response suggests plan → Show "Transfer to Plan" button

5. Optional: Transfer to Plan
   ├── User clicks "Transfer to Plan"
   ├── Confirm dialog: "Create plan from this conversation?"
   ├── Switch to Plan mode
   └── Pre-populate plan with AI suggestion

Average time per interaction: 3-5 seconds
```

### Flow 3: Plan Creation & Editing

```
┌─────────────────────────────────────────────────────────────┐
│                    PLAN MODE WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘

Entry Point:
├── From Chat: Click "Transfer to Plan"
└── Direct: Select Plan in LocalPilot side panel, then click "New Plan"

Flow A: From Chat Transfer
───────────────────────────
1. Receive plan suggestion from chat
2. Show plan preview:
   ├── Title: "Add User Authentication"
   ├── Description: AI-generated overview
   └── Estimated complexity: Medium
3. User clicks "Create Plan"
4. AI generates detailed TODO list:
   └── POST /api/plan/generate
       {
         "chat_context": [...],
         "suggestion": {...}
       }
5. Display TODO list (editable)
6. User reviews and edits
7. User approves → Ready for Act mode

Flow B: Manual Plan Creation
─────────────────────────────
1. User clicks "New Plan"
2. Show plan editor:
   ├── Title: [text input]
   ├── Description: [textarea]
   └── TODO items: [list editor]
3. User fills details manually
4. User clicks "Generate TODO Details"
5. AI expands each TODO with:
   ├── Detailed description
   ├── Files to modify
   ├── Dependencies
   └── AI instructions
6. User reviews and adjusts
7. User approves → Ready for Act mode

TODO List Structure:
────────────────────
□ TODO #1: Create User model and schema
  ├── Type: CREATE
  ├── Files: src/models/User.ts (new)
  ├── Dependencies: None
  └── Status: Pending
  
□ TODO #2: Implement authentication middleware
  ├── Type: CREATE
  ├── Files: src/middleware/auth.ts (new)
  ├── Dependencies: TODO #1
  └── Status: Pending
  
□ TODO #3: Update API routes with auth
  ├── Type: MODIFY
  ├── Files: src/routes/api.ts (modify)
  ├── Dependencies: TODO #2
  └── Status: Pending

User Actions:
├── ✏️ Edit TODO
├── ➕ Add TODO
├── ➖ Delete TODO
├── ↕️ Reorder (drag & drop)
├── 🔗 Set dependencies
└── ▶️ Start Implementation

Time to create plan: 2-5 minutes
```

### Flow 4: Safe Code Implementation (Act Mode)

```
┌─────────────────────────────────────────────────────────────┐
│                    ACT MODE WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘

Pre-Execution Safety Checks
────────────────────────────
1. Check Git repository
   ├── ✓ Repo exists
   ├── ✓ No uncommitted changes
   └── ✗ Issues → Show error, block execution

2. Create safety branch
   ├── Branch: localpilot/plan-{id}
   ├── Base: current branch
   └── Checkout safety branch

3. Show execution summary
   ┌─────────────────────────────────────────┐
   │  Ready to Execute Plan                  │
   ├─────────────────────────────────────────┤
   │  Plan: Add User Authentication          │
   │  TODOs: 3                                │
   │  Estimated time: 5-10 minutes            │
   │                                          │
   │  Safety:                                 │
   │  ✓ Git branch created                   │
   │  ✓ All changes reversible               │
   │  ✓ You'll approve each step             │
   │                                          │
   │  [Start Execution]  [Cancel]             │
   └─────────────────────────────────────────┘

4. User confirms → Begin execution

Execution Loop (for each TODO)
───────────────────────────────
TODO #1: Create User model

Step 1: Generate Code
├── AI generates file operations
├── Show "Generating..." indicator
└── Wait for LLM response (~10s)

Step 2: Preview Changes
┌─────────────────────────────────────────┐
│  TODO #1: Create User model             │
├─────────────────────────────────────────┤
│  Operations:                             │
│  📄 CREATE src/models/User.ts           │
│                                          │
│  Preview:                                │
│  ┌───────────────────────────────────┐  │
│  │ interface User {                  │  │
│  │   id: string;                     │  │
│  │   email: string;                  │  │
│  │   passwordHash: string;           │  │
│  │   createdAt: Date;                │  │
│  │ }                                 │  │
│  │                                   │  │
│  │ export class UserModel {          │  │
│  │   // ... implementation           │  │
│  │ }                                 │  │
│  └───────────────────────────────────┘  │
│                                          │
│  [Approve] [Edit] [Skip] [Abort]         │
└─────────────────────────────────────────┘

Step 3: User Decision
├── Approve → Continue to Step 4
├── Edit → Open in editor, wait for save
├── Skip → Mark skipped, next TODO
└── Abort → Stop execution, keep progress

Step 4: Apply Changes
├── Write files to disk
├── Git add & commit
│   └── "[LocalPilot] TODO #1: Create User model"
├── Update progress bar
└── Move to next TODO

Step 5: Repeat for TODO #2, #3...

Post-Execution
──────────────
All TODOs Complete:
┌─────────────────────────────────────────┐
│  ✓ Implementation Complete!             │
├─────────────────────────────────────────┤
│  Completed: 3/3 TODOs                   │
│  Time taken: 8 minutes                  │
│  Files created: 2                       │
│  Files modified: 1                      │
│                                          │
│  Next Steps:                             │
│  1. Review changes in Git               │
│  2. Test the implementation             │
│  3. Merge branch when ready:            │
│     git checkout main                   │
│     git merge localpilot/plan-123       │
│                                          │
│  [View Changes] [Create PR] [Done]       │
└─────────────────────────────────────────┘

Error Handling:
───────────────
If TODO fails:
┌─────────────────────────────────────────┐
│  ⚠️ Error in TODO #2                    │
├─────────────────────────────────────────┤
│  Error: TypeScript compilation error    │
│  File: src/middleware/auth.ts           │
│  Line 23: Cannot find name 'User'       │
│                                          │
│  This might be because TODO #1 was      │
│  skipped or incomplete.                 │
│                                          │
│  Options:                                │
│  [Retry] [Edit Instructions] [Skip]     │
│  [Rollback Last] [Abort All]             │
└─────────────────────────────────────────┘

Total execution time: 5-15 minutes (3 TODOs)
```

### Flow 5: Incremental Re-indexing

```
┌─────────────────────────────────────────────────────────────┐
│               BACKGROUND RE-INDEXING FLOW                   │
└─────────────────────────────────────────────────────────────┘

Trigger: File save event in VS Code

1. File Watcher detects change
   └── Event: workspace.onDidSaveTextDocument

2. Determine if re-indexing needed
   ├── Check file type (is it code?)
   ├── Check exclusion patterns
   └── Check if file is in index

3. Calculate change hash
   ├── Compare with cached hash
   └── If different → re-index

4. Background re-indexing
   ├── Parse file with Tree-sitter
   ├── Extract symbols
   ├── Create chunks
   ├── Generate embeddings
   └── Update vector DB

5. Update UI indicator
   ├── Show subtle notification
   └── "Index updated (src/auth.ts)"

Time: < 2 seconds (background, non-blocking)
User impact: None (transparent)
```

---

## 🎨 UI Wireframes

### Wireframe 0: LocalPilot Side Panel (TreeView)

```
┌───────────────────────────────────────────────────────────────┐
│  Side Bar                                                     │
├───────────────────────────────────────────────────────────────┤
│  LocalPilot (View Container)                                  │
│  ├─ Chat                                                      │
│  ├─ Plans (0)                                                 │
│  ├─ Act                                                       │
│  └─ Status                                                    │
│     ├─ VRAM: 3.8/8GB                                          │
│     ├─ Model: qwen2.5-coder:7b                                │
│     └─ Index: Up to date                                      │
└───────────────────────────────────────────────────────────────┘
```

### Wireframe 1: Welcome Screen

```
┌─────────────────────────────────────────────────────────────────┐
│  LocalPilot                                          [✕]        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         ╔═══════════╗                           │
│                         ║           ║                           │
│                         ║  [LOGO]   ║                           │
│                         ║           ║                           │
│                         ╚═══════════╝                           │
│                                                                 │
│                    LocalPilot v0.1.0                            │
│          Your Local AI Coding Assistant                         │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  System Requirements Check                                │  │
│  │                                                           │  │
│  │  ✓ VS Code 1.75 or higher                                │  │
│  │  ✓ Ollama installed and running                          │  │
│  │  ✓ GPU detected: NVIDIA RTX 4060 (8GB)                   │  │
│  │  ✓ RAM: 16GB available                                   │  │
│  │  ✓ Models found: 3                                       │  │
│  │                                                           │  │
│  │  • qwen2.5-coder:7b-instruct-q4_K_M                      │  │
│  │  • qwen2.5-coder:14b-instruct-q4_K_M                     │  │
│  │  • bge-m3                                                │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│                  ┌─────────────────────┐                        │
│                  │   Get Started   →   │                        │
│                  └─────────────────────┘                        │
│                                                                 │
│                         Learn More                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe 4: Chat Mode Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  VS Code Chat — LocalPilot participant               [✕]        │
├─────────────────────────────────────────────────────────────────┤
│  (LocalPilot side panel is available in the Side Bar)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  💡 Project Summary                              [Collapse ▲]   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ This is a React + TypeScript e-commerce application with │  │
│  │ authentication, product management, and payment          │  │
│  │ processing. Built with Express backend and MongoDB.      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Conversation                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │  👤 You: How does the payment processing work?           │  │
│  │                                                           │  │
│  │  🤖 LocalPilot:                                          │  │
│  │                                                           │  │
│  │  The payment processing is handled through Stripe        │  │
│  │  integration. Here's how it works:                       │  │
│  │                                                           │  │
│  │  1. Payment intent created in PaymentService:            │  │
│  │     📄 src/services/PaymentService.ts (lines 45-67)      │  │
│  │                                                           │  │
│  │  2. Frontend sends payment method to API:                │  │
│  │     📄 src/api/payment.ts (lines 23-41)                  │  │
│  │                                                           │  │
│  │  3. Backend validates and processes:                     │  │
│  │     📄 src/controllers/PaymentController.ts (89-156)     │  │
│  │                                                           │  │
│  │  Would you like me to explain any specific part in       │  │
│  │  more detail?                                            │  │
│  │                                                           │  │
│  │  ─────────────────────────────────────────────────────   │  │
│  │  Context used: 3 files, 245 lines, 92% relevance         │  │
│  │  [Show Context ▼]                                        │  │
│  │                                                           │  │
│  │  👤 You: Can you help me add refund functionality?       │  │
│  │                                                           │  │
│  │  🤖 LocalPilot:                                          │  │
│  │                                                           │  │
│  │  I can help you add refund functionality! Here's a       │  │
│  │  suggested plan:                                         │  │
│  │                                                           │  │
│  │  1. Add refund method to PaymentService                  │  │
│  │  2. Create refund API endpoint                           │  │
│  │  3. Update payment status tracking                       │  │
│  │  4. Add UI for refund requests                           │  │
│  │  5. Implement admin approval workflow                    │  │
│  │                                                           │  │
│  │  This is a medium complexity feature that will modify    │  │
│  │  5-7 files.                                              │  │
│  │                                                           │  │
│  │              ┌──────────────────────────┐                │  │
│  │              │  Transfer to Plan  →     │                │  │
│  │              └──────────────────────────┘                │  │
│  │                                                           │  │
│  └───▼──────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Type your message...                                      │  │
│  │                                                     [Send]│  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe 5: Plan Mode Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  LocalPilot                                          [✕]        │
├─────────────────────────────────────────────────────────────────┤
│  Chat  [Plan]  Act                          🔄 Re-index  ⚙️     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Plan: Add Refund Functionality                  [⋮ Actions]    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Created from chat session • 5 TODOs • Medium complexity │  │
│  │                                                           │  │
│  │  This plan will add refund functionality to the payment  │  │
│  │  system, including backend processing, API endpoints,    │  │
│  │  and admin UI for approval workflow.                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  TODO List                                     [+ Add TODO]      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │  ☐ 1. Add refund method to PaymentService        [⋮]     │  │
│  │     └─ CREATE src/services/PaymentService.ts             │  │
│  │        Dependencies: None                                │  │
│  │        Status: Pending                                   │  │
│  │        [Expand ▼]                                        │  │
│  │                                                           │  │
│  │  ☐ 2. Create refund API endpoints               [⋮]     │  │
│  │     └─ CREATE src/api/refund.ts                          │  │
│  │        MODIFY src/routes/payment.ts                      │  │
│  │        Dependencies: TODO #1                             │  │
│  │        Status: Pending (blocked)                         │  │
│  │                                                           │  │
│  │  ☐ 3. Update payment status tracking            [⋮]     │  │
│  │     └─ MODIFY src/models/Payment.ts                      │  │
│  │        MODIFY src/controllers/PaymentController.ts       │  │
│  │        Dependencies: TODO #1                             │  │
│  │        Status: Pending (blocked)                         │  │
│  │                                                           │  │
│  │  ☐ 4. Add refund request UI component           [⋮]     │  │
│  │     └─ CREATE src/components/RefundRequest.tsx           │  │
│  │        Dependencies: TODO #2                             │  │
│  │        Status: Pending (blocked)                         │  │
│  │                                                           │  │
│  │  ☐ 5. Implement admin approval workflow         [⋮]     │  │
│  │     └─ CREATE src/components/admin/RefundApproval.tsx    │  │
│  │        MODIFY src/api/admin.ts                           │  │
│  │        Dependencies: TODO #3, #4                         │  │
│  │        Status: Pending (blocked)                         │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Summary: 5 TODOs • 3 new files • 4 modifications               │
│                                                                 │
│  ┌──────────────────┐                   ┌───────────────────┐  │
│  │  Save as Draft   │                   │  Start Execution  │  │
│  └──────────────────┘                   └───────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe 6: Act Mode - Execution

```
┌─────────────────────────────────────────────────────────────────┐
│  LocalPilot                                          [✕]        │
├─────────────────────────────────────────────────────────────────┤
│  Chat  Plan  [Act]                          🔄 Re-index  ⚙️     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Executing: Add Refund Functionality                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Progress: ████████░░░░░░░░░░░░░░░░░░░░░░  2/5 TODOs     │  │
│  │  Branch: localpilot/plan-42                              │  │
│  │  Time elapsed: 3m 42s                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Current: TODO #3 - Update payment status tracking              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │  🤖 Generated changes for review:                        │  │
│  │                                                           │  │
│  │  📄 src/models/Payment.ts (MODIFY)          [Open File]  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │   interface Payment {                               │  │  │
│  │  │     id: string;                                     │  │  │
│  │  │     amount: number;                                 │  │  │
│  │  │ -   status: 'pending' | 'completed' | 'failed';     │  │  │
│  │  │ +   status: 'pending' | 'completed' | 'failed' |    │  │  │
│  │  │ +           'refund_requested' | 'refunded';        │  │  │
│  │  │ +   refundAmount?: number;                          │  │  │
│  │  │ +   refundReason?: string;                          │  │  │
│  │  │ +   refundedAt?: Date;                              │  │  │
│  │  │   }                                                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  📄 src/controllers/PaymentController.ts (MODIFY)       │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ + async updatePaymentStatus(                        │  │  │
│  │  │ +   paymentId: string,                              │  │  │
│  │  │ +   status: PaymentStatus                           │  │  │
│  │  │ + ): Promise<Payment> {                             │  │  │
│  │  │ +   // Implementation...                            │  │  │
│  │  │ + }                                                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  Changes: +15 lines, -1 line in 2 files                 │  │
│  │                                                           │  │
│  │  ┌──────────┐  ┌──────┐  ┌──────┐  ┌─────────────────┐  │  │
│  │  │ Approve  │  │ Edit │  │ Skip │  │ Abort Execution │  │  │
│  │  └──────────┘  └──────┘  └──────┘  └─────────────────┘  │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Execution Log                                  [Collapse ▲]    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ✓ TODO #1: Add refund method to PaymentService         │  │
│  │    └─ Created src/services/PaymentService.ts (3m 12s)   │  │
│  │    └─ Committed: a3f892c                                │  │
│  │                                                           │  │
│  │  ✓ TODO #2: Create refund API endpoints                 │  │
│  │    └─ Created src/api/refund.ts (2m 45s)                │  │
│  │    └─ Modified src/routes/payment.ts                    │  │
│  │    └─ Committed: b7e234d                                │  │
│  │                                                           │  │
│  │  ⟳ TODO #3: Update payment status tracking (current)    │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe 7: Settings Panel

```
┌─────────────────────────────────────────────────────────────────┐
│  LocalPilot - Settings                               [✕]        │
├─────────────────────────────────────────────────────────────────┤
│  [General]  Models  Indexing  Advanced                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  General Settings                                               │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  LLM Provider                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  [Ollama ▼]                                               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Ollama Configuration                                           │
│  Host:  [http://localhost:11434                             ]  │
│  [Test Connection]  ✓ Connected                                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  UI Preferences                                                 │
│  ☑ Enable streaming responses                                  │
│  ☑ Show context snippets in chat                               │
│  ☑ Auto-scroll during code generation                          │
│  ☐ Compact mode                                                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Safety                                                         │
│  ☑ Require Git repository for Act mode                         │
│  ☑ Check for uncommitted changes before execution              │
│  ☑ Create safety branch automatically                          │
│  ☐ Auto-approve new files (not recommended)                    │
│  ☐ Auto-approve config file changes                            │
│                                                                 │
│                                                                 │
│                          ┌────────────┐                         │
│                          │    Save    │                         │
│                          └────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Interaction Patterns

### Pattern 1: Keyboard Shortcuts

```yaml
Global Shortcuts:
  "Ctrl+Shift+P" (Cmd+Shift+P on Mac):
    - Open command palette
    - Type "LocalPilot" to see all commands
  
  "Ctrl+Shift+L" (Cmd+Shift+L on Mac):
    - Show LocalPilot views (side panel)
  
  "Ctrl+L" (Cmd+L on Mac):
    - Focus Chat input (LocalPilot participant)

Chat Mode:
  "Ctrl+Enter" (Cmd+Enter):
    - Send message
  
  "↑" (when input is empty):
    - Edit last message
  
  "Esc":
    - Clear input / Cancel streaming response
  
  "Ctrl+K" (Cmd+K):
    - Clear conversation

Plan Mode:
  "Ctrl+N" (Cmd+N):
    - New TODO item
  
  "Ctrl+S" (Cmd+S):
    - Save plan
  
  "↑/↓":
    - Navigate TODO items
  
  "Ctrl+↑/↓" (Cmd+↑/↓):
    - Reorder selected TODO
  
  "Delete":
    - Delete selected TODO

Act Mode:
  "Ctrl+Enter" (Cmd+Enter):
    - Approve current change
  
  "Ctrl+E" (Cmd+E):
    - Edit current change
  
  "Ctrl+S" (Cmd+S):
    - Skip current TODO
  
  "Esc":
    - Pause execution
```

### Pattern 2: File Reference Clicking

```typescript
Behavior:
  When user clicks a file reference in chat:
  1. Check if file exists in workspace
  2. Open file in editor
  3. Navigate to referenced line(s)
  4. Highlight relevant code (temporary highlight)
  5. Focus editor

Example:
  User clicks: "📄 src/api/payment.ts (lines 23-41)"
  
  Result:
  ├── Opens src/api/payment.ts
  ├── Scrolls to line 23
  ├── Selects lines 23-41
  └── Highlights with subtle background (3-second fade)
```

### Pattern 3: Drag and Drop

```yaml
Plan Mode TODO Reordering:
  Gesture: Click and drag TODO item
  Visual Feedback:
    - Dragged item becomes semi-transparent
    - Drop zones show blue line indicator
    - Other items shift to make space
  Constraints:
    - Cannot place child before its dependency
    - Warning shown if dependency would be violated
  
Act Mode File Preview:
  Gesture: Drag file from "Changes" list
  Destinations:
    - VS Code editor: Opens file
    - External diff tool: Opens in tool
    - Trash icon: Skips this file change
```

### Pattern 4: Context Menus

```yaml
Chat Message Context Menu: (Right-click on message)
  - Copy message
  - Copy code blocks
  - Regenerate response
  - Edit and retry
  - Delete message
  - Export conversation

File Reference Context Menu: (Right-click on file link)
  - Open file
  - Open in split editor
  - Copy file path
  - Reveal in explorer
  - Copy referenced code

TODO Item Context Menu: (Right-click on TODO)
  - Edit
  - Duplicate
  - Delete
  - Set dependencies
  - Change type (CREATE/MODIFY/DELETE)
  - Move to top/bottom
```

### Pattern 5: Inline Editing

```yaml
Plan Mode TODO Inline Edit:
  Trigger: Double-click TODO title
  Behavior:
    - Title becomes editable text field
    - Auto-focus with text selected
    - Enter: Save changes
    - Esc: Cancel edit
    - Click outside: Save changes
  
Chat Mode Message Edit:
  Trigger: Click "Edit" on sent message
  Behavior:
    - Message becomes editable
    - Previous response is deleted
    - Edit message
    - Press Ctrl+Enter to resend
    - AI generates new response
```

---

## 🎨 Visual Design System

### Color Palette

```css
/* Following VS Code theme colors with LocalPilot accents */

:root {
  /* Primary (Brand) */
  --lp-primary: #00A8E8;           /* Bright blue */
  --lp-primary-hover: #0094D1;
  --lp-primary-active: #007FB8;
  
  /* Success */
  --lp-success: #4CAF50;
  --lp-success-bg: rgba(76, 175, 80, 0.1);
  
  /* Warning */
  --lp-warning: #FF9800;
  --lp-warning-bg: rgba(255, 152, 0, 0.1);
  
  /* Error */
  --lp-error: #F44336;
  --lp-error-bg: rgba(244, 67, 54, 0.1);
  
  /* Neutral (VS Code integrated) */
  --lp-bg: var(--vscode-sideBar-background);
  --lp-fg: var(--vscode-foreground);
  --lp-border: var(--vscode-panel-border);
  --lp-input-bg: var(--vscode-input-background);
  --lp-input-border: var(--vscode-input-border);
  
  /* Semantic Colors */
  --lp-code-bg: var(--vscode-textCodeBlock-background);
  --lp-link: var(--vscode-textLink-foreground);
  --lp-link-hover: var(--vscode-textLink-activeForeground);
}
```

### Typography

```css
:root {
  /* Font Families (inherit from VS Code) */
  --lp-font-family: var(--vscode-font-family);
  --lp-font-mono: var(--vscode-editor-font-family);
  
  /* Font Sizes */
  --lp-text-xs: 11px;
  --lp-text-sm: 12px;
  --lp-text-base: 13px;
  --lp-text-lg: 14px;
  --lp-text-xl: 16px;
  --lp-text-2xl: 20px;
  
  /* Font Weights */
  --lp-font-normal: 400;
  --lp-font-medium: 500;
  --lp-font-semibold: 600;
  --lp-font-bold: 700;
  
  /* Line Heights */
  --lp-leading-tight: 1.25;
  --lp-leading-normal: 1.5;
  --lp-leading-relaxed: 1.75;
}
```

### Spacing Scale

```css
:root {
  --lp-space-1: 4px;
  --lp-space-2: 8px;
  --lp-space-3: 12px;
  --lp-space-4: 16px;
  --lp-space-5: 20px;
  --lp-space-6: 24px;
  --lp-space-8: 32px;
  --lp-space-10: 40px;
}
```

### Component Styles

```css
/* Button */
.lp-button-primary {
  background: var(--lp-primary);
  color: white;
  padding: var(--lp-space-2) var(--lp-space-4);
  border-radius: 4px;
  font-weight: var(--lp-font-medium);
  transition: all 150ms ease;
}

.lp-button-primary:hover {
  background: var(--lp-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 168, 232, 0.3);
}

/* Progress Bar */
.lp-progress {
  height: 8px;
  background: var(--vscode-progressBar-background);
  border-radius: 4px;
  overflow: hidden;
}

.lp-progress-fill {
  height: 100%;
  background: var(--lp-primary);
  transition: width 300ms ease;
}

/* Message Bubble */
.lp-message-user {
  background: var(--vscode-input-background);
  border-left: 3px solid var(--lp-primary);
  padding: var(--lp-space-3);
  margin: var(--lp-space-2) 0;
  border-radius: 0 8px 8px 0;
}

.lp-message-ai {
  background: rgba(0, 168, 232, 0.05);
  border-left: 3px solid var(--lp-success);
  padding: var(--lp-space-3);
  margin: var(--lp-space-2) 0;
  border-radius: 0 8px 8px 0;
}

/* TODO Item */
.lp-todo-item {
  padding: var(--lp-space-3);
  border: 1px solid var(--lp-border);
  border-radius: 6px;
  margin: var(--lp-space-2) 0;
  transition: all 200ms ease;
}

.lp-todo-item:hover {
  border-color: var(--lp-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.lp-todo-item.completed {
  opacity: 0.6;
  text-decoration: line-through;
}

.lp-todo-item.in-progress {
  border-color: var(--lp-warning);
  background: var(--lp-warning-bg);
}
```

### Animation Tokens

```css
:root {
  --lp-transition-fast: 150ms ease;
  --lp-transition-base: 200ms ease;
  --lp-transition-slow: 300ms ease;
  
  --lp-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --lp-ease-out: cubic-bezier(0, 0, 0.2, 1);
  --lp-ease-in: cubic-bezier(0.4, 0, 1, 1);
}

/* Micro-interactions */
@keyframes lp-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes lp-slide-in {
  from {
    transform: translateY(10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes lp-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

## 🗂️ Information Architecture

### Navigation Hierarchy

```
LocalPilot Extension
│
├── Main Panel (Side Panel)
│   ├── Tab Navigation (Top)
│   │   ├── Chat (Default)
│   │   ├── Plan
│   │   └── Act
│   │
│   ├── Global Actions (Top Right)
│   │   ├── Re-index Button
│   │   └── Settings Icon
│   │
│   └── Mode-Specific Content
│       ├── Chat View
│       │   ├── Project Summary (Collapsible)
│       │   ├── Conversation Area
│       │   │   ├── Message List
│       │   │   └── Context Indicators
│       │   └── Input Area
│       │       └── Send Button
│       │
│       ├── Plan View
│       │   ├── Plan Header
│       │   │   ├── Title & Description
│       │   │   └── Actions Menu
│       │   ├── TODO List
│       │   │   └── TODO Items
│       │   │       ├── Title
│       │   │       ├── Files Affected
│       │   │       ├── Dependencies
│       │   │       └── Status
│       │   └── Action Buttons
│       │       ├── Save
│       │       └── Start Execution
│       │
│       └── Act View
│           ├── Execution Progress
│           │   ├── Progress Bar
│           │   ├── Current TODO
│           │   └── Status
│           ├── Current Change Preview
│           │   ├── File Diffs
│           │   └── Approval Buttons
│           └── Execution Log
│               └── Completed TODOs
│
├── Settings Panel (Modal)
│   ├── General Tab
│   ├── Models Tab
│   ├── Indexing Tab
│   └── Advanced Tab
│
└── Command Palette Commands
    ├── LocalPilot: Open Panel
    ├── LocalPilot: Start Indexing
    ├── LocalPilot: Re-index Workspace
    ├── LocalPilot: Open Settings
    ├── LocalPilot: Clear Chat History
    └── LocalPilot: Export Conversation
```

### Content Priority (Visual Hierarchy)

```
Level 1 (Most Important):
├── Current user input/action
├── AI response (actively streaming)
├── Approval requests (Act mode)
└── Error messages

Level 2 (Secondary):
├── Project summary
├── TODO list
├── Execution progress
└── File references

Level 3 (Tertiary):
├── Context indicators
├── Metadata (timestamps, tokens used)
├── Execution log
└── Settings

Level 4 (Least Prominent):
├── Tips and hints
├── Keyboard shortcuts reminder
└── Version information
```

---

## ⚠️ Error States & Recovery

### Error State 1: Indexing Failure

```
┌─────────────────────────────────────────┐
│  ⚠️ Indexing Failed                     │
├─────────────────────────────────────────┤
│  An error occurred while indexing       │
│  your workspace.                        │
│                                          │
│  Error Details:                          │
│  Failed to parse: src/legacy/old.js     │
│  Reason: Syntax error at line 142       │
│                                          │
│  Indexed: 547/623 files                 │
│  Status: Partial index available        │
│                                          │
│  You can:                                │
│  • Continue with partial index          │
│  • Skip problematic files and retry     │
│  • View error log                       │
│                                          │
│  [Continue Anyway] [Skip & Retry]       │
│  [View Log] [Cancel]                    │
└─────────────────────────────────────────┘

Recovery Actions:
1. Continue Anyway: Use partial index
2. Skip & Retry: Exclude file, re-index rest
3. View Log: Show detailed error log
4. Cancel: Abort indexing
```

### Error State 2: LLM Connection Lost

```
┌─────────────────────────────────────────┐
│  🔌 Connection Lost                     │
├─────────────────────────────────────────┤
│  Cannot connect to Ollama.              │
│                                          │
│  Possible causes:                        │
│  • Ollama service is not running        │
│  • Wrong host configuration             │
│  • Network issue                        │
│                                          │
│  Troubleshooting:                        │
│  1. Check if Ollama is running:         │
│     $ ollama list                       │
│                                          │
│  2. Verify host in settings:            │
│     Currently: http://localhost:11434   │
│                                          │
│  [Retry Connection] [Open Settings]     │
│  [View Documentation]                   │
└─────────────────────────────────────────┘

Auto-Retry:
- Attempts: 3 times
- Delay: 2s, 4s, 8s (exponential backoff)
- User notified after failed attempts
```

### Error State 3: Act Mode Execution Failure

```
┌─────────────────────────────────────────┐
│  ❌ TODO Failed: Create auth middleware │
├─────────────────────────────────────────┤
│  Error Type: TypeScript Compilation     │
│                                          │
│  File: src/middleware/auth.ts           │
│  Line 23: Cannot find name 'UserModel'  │
│                                          │
│  Possible Cause:                         │
│  This TODO depends on TODO #1 which     │
│  was skipped.                           │
│                                          │
│  What happened:                          │
│  ✓ File created successfully            │
│  ✗ TypeScript validation failed         │
│  ✗ Changes NOT committed                │
│                                          │
│  Options:                                │
│  • Retry (ask AI to fix the error)      │
│  • Edit manually (opens file)           │
│  • Go back to TODO #1                   │
│  • Skip this TODO                       │
│  • Abort execution                      │
│                                          │
│  [Retry] [Edit Manually] [Go to TODO #1]│
│  [Skip] [Abort All]                     │
└─────────────────────────────────────────┘

State Preservation:
- Workspace remains in safe state
- No partial commits
- Previous TODOs still committed
- User can resume or rollback
```

### Error State 4: VRAM Overflow

```
┌─────────────────────────────────────────┐
│  ⚠️ Memory Warning                      │
├─────────────────────────────────────────┤
│  GPU memory is critically low.          │
│                                          │
│  VRAM Usage: 7.8GB / 8GB (98%)          │
│                                          │
│  This may cause:                         │
│  • Slow responses                       │
│  • System instability                   │
│  • Potential crashes                    │
│                                          │
│  Recommendations:                        │
│  • Switch to smaller model (7b)         │
│  • Close other GPU applications         │
│  • Restart LocalPilot                   │
│                                          │
│  [Switch to 7b Model] [Continue Anyway] │
│  [Restart Extension]                    │
└─────────────────────────────────────────┘

Prevention:
- Monitor VRAM usage in background
- Warn at 90% utilization
- Block new operations at 95%
- Auto-unload models if possible
```

### Error Recovery Principles

```yaml
Graceful Degradation:
  - Always provide a fallback option
  - Never leave user in broken state
  - Preserve work in progress
  - Clear rollback path

User Communication:
  - Explain what happened (simple language)
  - Explain why it happened (if known)
  - Provide actionable next steps
  - Link to documentation if complex

State Management:
  - Save chat history before errors
  - Preserve plan drafts automatically
  - Git commits ensure code safety
  - Cache indexing progress
```

---

## ♿ Accessibility

### Keyboard Navigation

```yaml
All Interactive Elements:
  - Focusable via Tab
  - Visible focus indicator (outline)
  - Logical tab order (top to bottom, left to right)
  - Escape key closes dialogs/modals

Screen Reader Support:
  - ARIA labels on all buttons
  - ARIA live regions for streaming content
  - ARIA progress bars for indexing
  - Semantic HTML (nav, main, section, article)

Visual:
  - Respect VS Code theme (dark/light)
  - Sufficient color contrast (WCAG AA)
  - No color-only indicators
  - Scalable text (respects zoom)

Reduced Motion:
  - Respect prefers-reduced-motion
  - Disable animations if requested
  - Keep essential animations only
```

### ARIA Annotations (Examples)

```html
<!-- Chat input -->
<textarea
  aria-label="Chat message input"
  aria-describedby="chat-hint"
  role="textbox"
  aria-multiline="true"
/>
<span id="chat-hint" class="sr-only">
  Type your question and press Ctrl+Enter to send
</span>

<!-- Streaming response -->
<div
  role="status"
  aria-live="polite"
  aria-atomic="false"
>
  {streamingResponse}
</div>

<!-- Progress bar -->
<div
  role="progressbar"
  aria-valuenow={current}
  aria-valuemin="0"
  aria-valuemax={total}
  aria-label="Indexing progress"
>
  <div style="width: {percent}%"></div>
</div>

<!-- TODO checkbox -->
<input
  type="checkbox"
  role="checkbox"
  aria-checked={completed}
  aria-label={`TODO ${index}: ${title}`}
/>
```

---

## 📊 Success Metrics

### User Experience Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to First Chat** | < 5 minutes | From install to first message sent |
| **Indexing Completion Rate** | > 95% | Successful full index / total attempts |
| **Chat Response Relevance** | > 80% | User satisfaction survey |
| **Plan Transfer Rate** | > 30% | Plans created / chat sessions |
| **Act Mode Success Rate** | > 70% | TODOs completed / total TODOs |
| **Error Recovery Rate** | > 90% | Errors recovered / total errors |
| **Daily Active Usage** | > 5 interactions | Messages + plans + executions per day |

### UI/UX Specific Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Button Click Success** | > 99% | Successful clicks / total attempts |
| **Form Submission Success** | > 95% | Valid submissions / total submissions |
| **Navigation Efficiency** | < 3 clicks | Average clicks to reach any feature |
| **Modal Dismiss Rate** | < 20% | Modals dismissed / shown |
| **Help Documentation Views** | < 10% | Help views / total sessions (lower is better) |

### Performance Perception

| Metric | Target | User Perception |
|--------|--------|-----------------|
| **Perceived Response Time** | < 1s | "Instant" |
| **Streaming Start Time** | < 500ms | "Responsive" |
| **Progress Indication** | Always visible | "Informed" |
| **Error Recovery Time** | < 30s | "Recoverable" |

---

## 🎬 User Journey Summary

### Journey Map: From Install to Productive Use

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Phase 1    │   Phase 2    │   Phase 3    │   Phase 4    │
│  Discovery   │   Setup      │  Learning    │  Mastery     │
├──────────────┼──────────────┼──────────────┼──────────────┤
│              │              │              │              │
│ • Install    │ • Config     │ • First chat │ • Daily use  │
│ • Welcome    │ • Index      │ • Explore    │ • Advanced   │
│ • Understand │ • Summary    │ • Try plan   │ • Efficient  │
│              │              │ • Learn act  │ • Confident  │
│              │              │              │              │
│ User Feeling:│ User Feeling:│ User Feeling:│ User Feeling:│
│ Curious      │ Excited      │ Impressed    │ Productive   │
│              │              │              │              │
│ Time: 2 min  │ Time: 8 min  │ Time: 20 min │ Ongoing      │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and success criteria
- `TECHNICAL_ARCHITECTURE.md` - System design (PREVIOUS)
- `API_SPECIFICATION.md` - Backend API (NEXT)
- `DATA_MODELS.md` - Data schemas
- `UI_DESIGN_SYSTEM.md` - Detailed component library
- `DEVELOPMENT_GUIDE.md` - Setup and workflow
- `INDEXING_SYSTEM_SPEC.md` - Indexing deep dive

---

**END OF DOCUMENT**