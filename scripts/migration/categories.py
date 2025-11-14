from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.domain.categories.entities import Category


def update_categories(
    src_database: Database[MongoDocument],
    dst_database: Database[MongoDocument],
) -> None:
    dst_categories: list[MongoDocument] = []
    for src_category in src_database["types"].find():
        dst_category = Category(
            name=src_category["name"],
            pricing_group=src_category["ratio_category"],
            tactill_category=src_category["tactill_category"],
        )
        dst_categories.append(dst_category.model_dump(exclude={"id"}))

    dst_database["categories"].insert_many(dst_categories)
