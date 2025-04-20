import json
from collections import defaultdict
from typing import Any


def extract_name(data: dict[str, Any]) -> None:
    data["name"] = {
        "name1": data.pop("name1", ""),
        "name2": data.pop("name2", ""),
    }


def extract_volume(data: dict[str, Any]) -> None:
    volume_data = data.pop("volume", None)

    try:
        volume = json.loads(volume_data)
        data["volume"] = volume
    except json.decoder.JSONDecodeError:
        data["volume"] = None


def extract_deposit(data: dict[str, Any]) -> None:
    data["deposit"] = {
        "unit": data.pop("unit", 0),
        "case": data.pop("case", 0),
    }


def extract_shops(data: dict[str, Any]) -> None:
    shops = defaultdict(defaultdict)
    for key, value in data.items():
        if "sell_price_" in key or "bar_price_" in key:
            field, _, shop = key.partition("_price_")

            shops[shop][f"{field}_price"] = float(value)
            shops[shop]["stock_quantity"] = 0

    data["shops"] = shops
