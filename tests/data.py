from datetime import datetime, timezone

from application.entities.article import (
    ArticleDeposit,
    ArticleName,
    ArticleShopDetail,
    ArticleShops,
    CreateOrUpdateArticle,
)

date = datetime.now(timezone.utc)

categories_for_list_view = [
    "beer",
    "cider",
    "keg",
    "mini_keg",
    "rhum",
    "whisky",
    "spirit",
    "arranged",
    "wine",
    "fortified_wine",
    "sparkling_wine",
    "bib",
    "box",
    "food",
    "misc",
]

article_to_insert = CreateOrUpdateArticle(
    type="Bière",
    name=ArticleName(name1="", name2="TEST"),
    buy_price=1.5,
    excise_duty=0.2,
    social_security_levy=0.0,
    tax=20.0,
    distributor="Néodif",
    barcode="12345",
    region="France",
    color="Blonde",
    taste="",
    volume=33.0,
    alcohol_by_volume=8.0,
    packaging=0,
    deposit=ArticleDeposit(unit=0.0, case=0.0),
    food_pairing=[],
    biodynamic="",
    validated=False,
    created_by="User",
    created_at=date,
    updated_at=date,
    shops=ArticleShops(
        root={
            "angouleme": ArticleShopDetail(
                sell_price=3.5, bar_price=0.0, stock_quantity=0
            ),
            "sainte-eulalie": ArticleShopDetail(
                sell_price=3.5, bar_price=0.0, stock_quantity=0
            ),
            "pessac": ArticleShopDetail(
                sell_price=3.5, bar_price=5.0, stock_quantity=0
            ),
        }
    ),
)

article_data = {
    "type": article_to_insert.type,
    "name1": article_to_insert.name.name1,
    "name2": article_to_insert.name.name2,
    "region": article_to_insert.region,
    "color": article_to_insert.color,
    "volume": article_to_insert.volume,
    "alcohol_by_volume": article_to_insert.alcohol_by_volume,
    "buy_price": article_to_insert.buy_price,
    "tax": article_to_insert.tax,
    "excise_duty": article_to_insert.excise_duty,
    "social_security_levy": article_to_insert.social_security_levy,
    "sell_price_pessac": article_to_insert.shops["pessac"].sell_price,
    "bar_price_pessac": article_to_insert.shops["pessac"].bar_price,
    "stock_quantity_pessac": article_to_insert.shops["pessac"].stock_quantity,
    "distributor": article_to_insert.distributor,
    "barcode": article_to_insert.barcode,
    "unit": article_to_insert.deposit.unit,
    "case": article_to_insert.deposit.case,
    "packaging": article_to_insert.packaging,
}
