from dataclasses import dataclass


@dataclass
class NavbarCategory:
    code: str
    singular_name: str
    plural_name: str


navbar_categories = {
    "1": [
        NavbarCategory("beer", "Bière", "Bières"),
        NavbarCategory("cider", "Cidre", "Cidres"),
    ],
    "2": [
        NavbarCategory("keg", "Fût", "Fûts"),
        NavbarCategory("mini_keg", "Mini-fût", "Mini-fûts"),
    ],
    "3": [
        NavbarCategory("rhum", "Rhum", "Rhums"),
        NavbarCategory("whisky", "Whisky", "Whiskys"),
        NavbarCategory("arranged", "Arrangé", "Arrangés"),
        NavbarCategory("spirit", "Spiritueux", "Spiritueux"),
    ],
    "4": [
        NavbarCategory("wine", "Vin", "Vins"),
        NavbarCategory("fortified_wine", "Vins muté", "Vins mutés"),
        NavbarCategory("sparkling_wine", "Vins effervescent", "Vins effervescents"),
        NavbarCategory("bib", "BIB", "BIB"),
    ],
    "5": [
        NavbarCategory("box", "Coffret", "Coffrets"),
        NavbarCategory("food", "Alimentation / BSA", "Alimentation / BSA"),
        NavbarCategory("misc", "Accessoire / Emballage", "Accessoire / Emballage"),
    ],
}
