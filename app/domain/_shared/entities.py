from enum import StrEnum


class ProducerType(StrEnum):
    BREWERY = "brewery"
    DISTILLERY = "distillery"
    # AOP/AOC, IGP, wine regions, grape varieties, appellations, ...
    WINE_ORIGIN = "wine_origin"
