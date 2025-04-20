from typing import Any

import pytest


@pytest.fixture(scope="session")
def article() -> dict[str, Any]:
    return {
        "type": "",
        "name1": "",
        "name2": "",
        "buy_price": 1,
        "excise_duty": 0.3,
        "social_security_levy": 0.1,
        "tax": 20,
        "distributor": "Néodif",
        "barcode": "12345",
        "region": "France",
        "color": "Blonde",
        "taste": "",
        "volume": '{"value": 33.0,"unit": "cL"}',
        "alcohol_by_volume": 8.4,
        "packaging": 24,
        "case": 0,
        "unit": 0,
        "food_pairing": [],
        "biodynamic": "",
        "bar_price_shop-test": 0,
        "sell_price_shop-test": 0,
    }
