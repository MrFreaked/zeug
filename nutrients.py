from dataclasses import dataclass

@dataclass
class Nutrients:
    kcal: float
    protein: float
    fat: float
    carbs: float
    fiber: float = 0.0
    vitamin_c: float = 0.0
    iron: float = 0.0
