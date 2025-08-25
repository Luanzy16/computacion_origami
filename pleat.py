
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

Signal = Optional[bool]  # True/False/None (indefinida)


@dataclass
class Pleat:
    """
    Representa una 'tira' (pleat) con un nombre único y una señal booleana o None.
    """
    name: str
    value: Signal = None

    def __repr__(self) -> str:
        return f"Pleat(name={self.name!r}, value={self.value})"
