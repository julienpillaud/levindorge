from datetime import datetime, timezone

date = datetime.now(timezone.utc)

article_to_insert = {
    "type": "Bière",
    "name": {"name1": "", "name2": "TEST"},
    "buy_price": 1.5,
    "excise_duty": 0.2,
    "social_security_levy": 0.0,
    "tax": 20.0,
    "distributor": "Néodif",
    "barcode": "12345",
    "region": "France",
    "color": "Blonde",
    "taste": "",
    "volume": 33.0,
    "alcohol_by_volume": 8.0,
    "packaging": 0,
    "deposit": {"unit": 0.0, "case": 0.0},
    "food_pairing": [],
    "biodynamic": "",
    "validated": False,
    "created_by": "User",
    "created_at": date,
    "updated_at": date,
    "shops": {
        "angouleme": {"sell_price": 3.5, "bar_price": 5.0, "stock_quantity": 0},
        "sainte-eulalie": {"sell_price": 3.5, "bar_price": 5.0, "stock_quantity": 0},
        "pessac": {"sell_price": 3.5, "bar_price": 5.0, "stock_quantity": 0},
    },
}

article_data = {
    "type": "Bière",
    "name1": "",
    "name2": "TEST",
    "region": "France",
    "color": "Blonde",
    "volume": "33",
    "alcohol_by_volume": "8",
    "buy_price": "1.5",
    "tax": "20",
    "excise_duty": "0.2",
    "social_security_levy": "",
    "sell_price_pessac": "3.5",
    "bar_price_pessac": "5",
    "stock_quantity_pessac": "0",
    "distributor": "Néodif",
    "barcode": "000001",
    "unit": "0",
    "case": "0",
    "packaging": "0",
}
