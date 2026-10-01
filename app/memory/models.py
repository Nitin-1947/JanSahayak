from dataclasses import dataclass
from typing import Optional


@dataclass
class Memory:

    user_id: str

    key: str

    value: str

    created_at: Optional[str] = None

    updated_at: Optional[str] = None