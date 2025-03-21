# model.py
from dataclasses import dataclass
from typing import List

@dataclass
class Parameter:
    name: str
    options: List[str]
    default_value: str = ""

@dataclass
class Category:
    name: str
    parameters: List[Parameter]
