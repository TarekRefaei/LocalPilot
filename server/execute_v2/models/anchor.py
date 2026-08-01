from typing import Optional, Literal
from pydantic import BaseModel


class Anchor(BaseModel):
    type: Literal["function", "imports", "file_end"]
    symbol: Optional[str] = None
    verified: bool = False
