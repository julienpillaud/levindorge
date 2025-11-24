from rich import print

from app.core.core import Context
from app.domain.origins.entities import Country, Origin, Region


def create_origins(dst_context: Context) -> list[Origin]:
    result = dst_context.origin_repository.create_many(ORIGINS)
    count = len(result)
    print(f"Created {count} origins")
    return dst_context.origin_repository.get_all(limit=count).items


ORIGINS = [
    Country(name="Afrique du Sud", code="ZA"),
    Country(name="Allemagne", code="DE"),
    Country(name="Angleterre", code="GB-ENG"),
    Country(name="Argentine", code="AR"),
    Country(name="Australie", code="AU"),
    Country(name="Barbade", code="BB"),
    Region(name="Beaujolais"),
    Country(name="Belgique", code="BE"),
    Region(name="Bordeaux"),
    Region(name="Bourgogne"),
    Region(name="Californie"),
    Region(name="Caraïbes"),
    Region(name="Champagne"),
    Country(name="Chili", code="CL"),
    Country(name="Colombie", code="CO"),
    Country(name="Corée du Sud", code="KR"),
    Country(name="Costa Rica", code="CR"),
    Country(name="Cuba", code="CU"),
    Country(name="Écosse", code="GB-SCT"),
    Country(name="Espagne", code="ES"),
    Country(name="Estonie", code="EE"),
    Country(name="États-Unis", code="US"),
    Country(name="France", code="FR"),
    Country(name="Guatemala", code="GT"),
    Country(name="Guyana", code="GY"),
    Country(name="Haïti", code="HT"),
    Country(name="Hongrie", code="HU"),
    Country(name="Inde", code="IN"),
    Country(name="Irlande", code="IE"),
    Country(name="Italie", code="IT"),
    Country(name="Jamaïque", code="JM"),
    Country(name="Japon", code="JP"),
    Region(name="Languedoc"),
    Country(name="Luxembourg", code="LU"),
    Country(name="Maurice", code="MU"),
    Country(name="Mexique", code="MX"),
    Country(name="Nicaragua", code="NI"),
    Country(name="Nouvelle-Zélande", code="NZ"),
    Country(name="Panama", code="PA"),
    Country(name="Pays de Galles", code="GB-WLS"),
    Country(name="Pays-Bas", code="NL"),
    Country(name="Philippines", code="PH"),
    Country(name="Pologne", code="PL"),
    Country(name="Porto Rico", code="PR"),
    Country(name="Portugal", code="PT"),
    Region(name="Provence"),
    Country(name="Pérou", code="PE"),
    Region(name="Roussillon"),
    Country(name="Russie", code="RU"),
    Country(name="République dominicaine", code="DO"),
    Country(name="Tchéquie", code="CZ"),
    Country(name="Salvador", code="SV"),
    Region(name="Sud Ouest"),
    Country(name="Suisse", code="CH"),
    Country(name="Suède", code="SE"),
    Country(name="Taïwan", code="TW"),
    Country(name="Trinité-et-Tobago", code="TT"),
    Region(name="Vallée de la Loire"),
    Region(name="Vallée du Rhône"),
    Country(name="Venezuela", code="VE"),
]
