"""Copyright 2022 by Artem Ustsov"""

from dataclasses import dataclass, field


@dataclass()
class SplittingParams:
    val_size: float = field(default=0.2)
    random_state: int = field(default=42)
