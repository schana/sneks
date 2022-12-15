from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class Game:
    rows: int
    columns: int
    dynamic_food: bool
    food: int


@dataclass
class Colors:
    background: Tuple[int, int, int]
    border: Tuple[int, int, int]
    invalid: Tuple[int, int, int]
    food: Tuple[int, int, int]
    snake: List[Tuple[int, int, int]]


@dataclass
class Graphics:
    display: bool
    headless: bool
    cell_size: int
    padding: int
    colors: Colors
    delay: int
    record: bool
    record_prefix: str


@dataclass
class Config:
    game: Game
    graphics: Optional[Graphics]
    runs: int
    turn_limit: int
    registrar_prefix: str
    registrar_submission_sneks: int
