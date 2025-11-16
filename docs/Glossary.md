# Glossary

- Side Panel Views: Native VS Code views rendered in the Activity Bar container `localpilot.views`.
- Chat Participant: An entity registered with the VS Code Chat API that responds to user messages (id: `localpilot`).
- Partial-ready: Indexing milestone where enough data exists for limited retrieval (docs-first mode) before full completion.
- Docs-first mode: UX state where documentation-derived chunks are available while code parsing continues.
- Plan: A structured set of steps with acceptance criteria used to guide implementation.
- Transfer to Plan: Action in Chat inserting a suggested plan into the Plans view for editing.
- Act mode: Safe execution mode applying code changes via a dry-run and approval workflow.
- Dry-run: Show diffs without applying changes.
- Approval: Explicit user confirmation required before applying changes in Act mode.
- VRAM cap: Upper limit on GPU memory usage to avoid OOM; target ≤ 90%.
- Model swapper: Component that loads/unloads models based on LRU strategy and VRAM thresholds.
- Multi-level retrieval: Combines project summary, symbol/metadata, semantic vector search, and lexical search.
- Fusion & diversity re-rank: Merge results from multiple retrieval strategies and promote diverse context.
- Indexing phases: Discovery → Documentation → Structure → Chunking → Summarization.
- Contract version: Version number embedded in events to track compatibility (e.g., 0.1.0).
