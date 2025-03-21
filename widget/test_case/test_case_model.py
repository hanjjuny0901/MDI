# model.py
from dataclasses import dataclass

@dataclass
class TestCase:
    tc_id: int
    scenario: str
    domain_count: int
    publisher: str
    subscriber: str
    data_size_min: int
    data_size_max: int
    qos_policy: str
