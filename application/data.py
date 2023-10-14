from dataclasses import dataclass


@dataclass
class NavbarCategory:
    name: str
    title: str


navbar_categories = {
    "1": [NavbarCategory("beer", "Bières"), NavbarCategory("cider", "Cidres")],
    "2": [NavbarCategory("keg", "Fûts"), NavbarCategory("mini_keg", "Mini-fûts")],
    "3": [
        NavbarCategory("rhum", "Rhums"),
        NavbarCategory("whisky", "Whiskys"),
        NavbarCategory("arranged", "Arrangés"),
        NavbarCategory("spirit", "Autres"),
    ],
    "4": [
        NavbarCategory("wine", "Vins"),
        NavbarCategory("fortified_wine", "Vins mutés"),
        NavbarCategory("sparkling_wine", "Vins effervescents"),
        NavbarCategory("bib", "BIB"),
    ],
    "5": [
        NavbarCategory("box", "Coffrets"),
        NavbarCategory("food", "Alimentation / BSA"),
        NavbarCategory("misc", "Accessoire / Emballage"),
    ],
}
