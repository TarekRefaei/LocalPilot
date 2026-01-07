/**
 * PLAN MODE Prompt Rules
 *
 * Purpose:
 * - Guide the LLM to produce a high-level implementation plan only.
 * - Ensure output adheres strictly to the required schema and format.
 *
 * Forbidden Behaviors:
 * - Emitting code or shell commands.
 * - Assuming files/frameworks beyond the indexed project.
 * - Producing any content other than the required plan and embedded JSON.
 */
