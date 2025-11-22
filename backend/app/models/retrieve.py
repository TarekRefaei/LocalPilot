"""
Retrieval request/response models for the /retrieve endpoint.
"""

from typing import Any

from pydantic import BaseModel, Field


class UserContext(BaseModel):
    """User context for retrieval (current file, recent files, etc.)."""

    current_file: str | None = Field(None, description="Currently open file path")
    recent_files: list[str] = Field(default_factory=list, description="Recently accessed files")
    selected_text: str | None = Field(None, description="Currently selected text in editor")


class ScoreBreakdown(BaseModel):
    """Score breakdown for a result (only included when debug=true)."""

    semantic_score: float = Field(..., description="Semantic search score (0-1)")
    symbol_score: float = Field(..., description="Symbol/metadata search score (0-1)")
    keyword_score: float = Field(..., description="Keyword/BM25 search score (0-1)")
    summary_score: float = Field(..., description="Project summary score (0-1)")
    fused_score: float = Field(..., description="Fused score before diversity re-ranking")


class RetrieveResult(BaseModel):
    """A single retrieval result."""

    id: str = Field(..., description="Unique result identifier")
    file_path: str = Field(..., description="Source file path")
    chunk_index: int = Field(..., description="Chunk index within file")
    content: str = Field(..., description="Chunk content")
    start_line: int = Field(..., description="Start line number in source file")
    end_line: int = Field(..., description="End line number in source file")
    symbols: list[str] = Field(default_factory=list, description="Symbols (functions, classes) in chunk")
    score: float | None = Field(None, description="Final diversity-adjusted score (omitted when debug=false)")
    diversity_adjusted_score: float | None = Field(
        None, description="Diversity penalty applied (omitted when debug=false)"
    )
    scores: ScoreBreakdown | None = Field(None, description="Score breakdown (omitted when debug=false)")


class RetrieveRequest(BaseModel):
    """Request body for /retrieve endpoint."""

    query: str = Field(..., description="Search query", min_length=1)
    top_k: int = Field(5, description="Number of results to return", ge=1, le=50)
    debug: bool = Field(False, description="Include debug info (scores, breakdown)")
    user_context: UserContext | None = Field(None, description="Optional user context for boosting")


class RetrieveResponse(BaseModel):
    """Response body for /retrieve endpoint."""

    results: list[RetrieveResult] = Field(..., description="Retrieved results")
    total_count: int = Field(..., description="Total number of results found")
    query: str = Field(..., description="Echoed query")
    top_k: int = Field(..., description="Echoed top_k parameter")
    debug: bool = Field(..., description="Echoed debug flag")
