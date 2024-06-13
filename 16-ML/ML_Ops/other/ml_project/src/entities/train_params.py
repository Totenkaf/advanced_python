from dataclasses import dataclass, field


@dataclass()
class TrainingParams:
    model_type: str = field(default='KNeighborsClassifier')
    random_state: int = field(default=42)
    grid_search: bool = field(default=True)
