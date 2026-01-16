import random
from decimal import Decimal


def generate_decimal(
    gt: float = 0.1,
    ge: float = 0,
    lt: float = 99,
    le: float = 100,
    decimal_places: int = 4,
) -> Decimal:
    low = max(gt, ge)
    high = min(lt, le)

    val = random.uniform(low, high)
    return Decimal(str(round(val, decimal_places)))
