from enum import StrEnum


class InventoryGroup(StrEnum):
    BEER = "Bière"
    CIDER = "Cidre"
    KEG = "Fût"
    MINI_KEG = "Mini-fût"
    RUM = "Rhum"
    WHISKY = "Whisky"
    ARRANGED = "Arrangé"
    SPIRIT = "Spiritueux"
    WINE = "Vin"
    FORTIFIED_WINE = "Vin muté"
    SPARKLING_WINE = "Vin effervescent"
    BIB = "BIB"
    BOX = "Coffret"
    FOOD = "Alimentation / BSA"
    OTHER = "Accessoire / Emballage"


class PricingGroup(StrEnum):
    BEER = "beer"
    KEG = "keg"
    MINI_KEG = "mini_keg"
    SPIRIT = "spirit"
    ARRANGED = "arranged"
    WINE = "wine"
    BIB = "bib"
    BOX = "box"
    OTHER = "other"
