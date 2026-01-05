from cleanstack.domain import BaseDomain, CommandHandler

from app.domain.articles.commands import (
    create_article_command,
    delete_article_command,
    get_article_command,
    get_articles_by_ids_command,
    get_articles_command,
    update_article_command,
)
from app.domain.categories.commands import (
    get_categories_command,
    get_category_by_name_command,
)
from app.domain.commons.commands import (
    get_view_data_command,
)
from app.domain.context import ContextProtocol
from app.domain.deposits.commands import (
    create_deposit_command,
    delete_deposit_command,
    get_deposits_command,
)
from app.domain.distributors.commands import (
    create_distributor_command,
    delete_distributor_command,
    get_distributors_command,
)
from app.domain.inventories.commands import (
    create_inventory_command,
    delete_inventory_command,
    get_inventories_command,
    get_inventory_command,
)
from app.domain.origins.commands import get_origins_command
from app.domain.pos.commands import (
    create_pos_article_command,
    delete_pos_article_command,
    reset_pos_stocks_command,
    update_pos_article_command,
)
from app.domain.price_labels.commands import (
    create_price_labels_command,
    delete_price_labels_command,
    get_price_labels_command,
    get_price_labels_sheet_command,
)
from app.domain.producers.commands import (
    create_producer_command,
    delete_producer_command,
    get_producers_command,
)
from app.domain.stores.commands import get_stores_command
from app.domain.users.commands import (
    refresh_token_command,
    sign_in_with_password_command,
    update_user_password_command,
)
from app.domain.volumes.commands import get_volumes_command


class Domain(BaseDomain[ContextProtocol]):
    update_user_password = CommandHandler(update_user_password_command)
    sign_in_with_password = CommandHandler(sign_in_with_password_command)
    refresh_token = CommandHandler(refresh_token_command)

    # common
    get_view_data = CommandHandler(get_view_data_command)
    # stores
    get_stores = CommandHandler(get_stores_command)
    # categories
    get_categories = CommandHandler(get_categories_command)
    get_category_by_name = CommandHandler(get_category_by_name_command)
    # producers
    get_producers = CommandHandler(get_producers_command)
    create_producer = CommandHandler(create_producer_command)
    delete_producer = CommandHandler(delete_producer_command)
    # distributors
    get_distributors = CommandHandler(get_distributors_command)
    create_distributor = CommandHandler(create_distributor_command)
    delete_distributor = CommandHandler(delete_distributor_command)
    # origins
    get_origins = CommandHandler(get_origins_command)
    # volumes
    get_volumes = CommandHandler(get_volumes_command)
    # deposits
    get_deposits = CommandHandler(get_deposits_command)
    create_deposit = CommandHandler(create_deposit_command)
    delete_deposit = CommandHandler(delete_deposit_command)
    # articles
    get_articles = CommandHandler(get_articles_command)
    get_articles_by_ids = CommandHandler(get_articles_by_ids_command)
    get_article = CommandHandler(get_article_command)
    create_article = CommandHandler(create_article_command)
    update_article = CommandHandler(update_article_command)
    delete_article = CommandHandler(delete_article_command)
    # POS article
    create_pos_article = CommandHandler(create_pos_article_command)
    update_pos_article = CommandHandler(update_pos_article_command)
    delete_pos_article = CommandHandler(delete_pos_article_command)
    reset_pos_stocks = CommandHandler(reset_pos_stocks_command)
    # price_labels
    create_price_labels = CommandHandler(create_price_labels_command)
    get_price_labels = CommandHandler(get_price_labels_command)
    get_price_labels_sheet = CommandHandler(get_price_labels_sheet_command)
    delete_price_labels = CommandHandler(delete_price_labels_command)
    # inventories
    get_inventories = CommandHandler(get_inventories_command)
    get_inventory = CommandHandler(get_inventory_command)
    create_inventory = CommandHandler(create_inventory_command)
    delete_inventory = CommandHandler(delete_inventory_command)
