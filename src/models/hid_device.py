from dataclasses import dataclass
from typing import List

@dataclass
class HIDDevice:
    vendor_id: int
    product_id: int
    manufacturer_name: str
    product_name: str
    report: List[int]
