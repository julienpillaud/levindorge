from cleanstack.domain import BaseDomain, CommandHandler

from app.domain.articles.commands import (
    create_article_command,
    delete_article_command,
    get_article_command,
    get_articles_by_display_group_command,
    get_articles_command,
    update_article_command,
)
from app.domain.commons.commands import get_article_type_command, get_view_data_command
from app.domain.context import ContextProtocol
from app.domain.items.commands import (
    delete_deposit_command,
    delete_item_command,
    delete_volume_command,
    get_deposits_command,
    get_items_command,
    get_volumes_command,
)
from app.domain.pos.commands import (
    create_pos_article_command,
    delete_pos_article_command,
    update_pos_article_command,
)
from app.domain.price_labels.commands import (
    create_price_labels_command,
    get_price_labels_files_command,
)
from app.domain.users.commands import get_user_by_email_command


class Domain(BaseDomain[ContextProtocol]):
    # common
    get_view_data = CommandHandler(get_view_data_command)
    get_article_type = CommandHandler(get_article_type_command)
    # items
    get_items = CommandHandler(get_items_command)
    delete_item = CommandHandler(delete_item_command)
    # volumes
    get_volumes = CommandHandler(get_volumes_command)
    delete_volume = CommandHandler(delete_volume_command)
    # deposits
    get_deposits = CommandHandler(get_deposits_command)
    delete_deposit = CommandHandler(delete_deposit_command)

    # users
    get_user_by_email = CommandHandler(get_user_by_email_command)
    # articles
    get_articles = CommandHandler(get_articles_command)
    get_articles_by_display_group = CommandHandler(
        get_articles_by_display_group_command
    )
    get_article = CommandHandler(get_article_command)
    create_article = CommandHandler(create_article_command)
    update_article = CommandHandler(update_article_command)
    delete_article = CommandHandler(delete_article_command)
    # POS article
    create_pos_article = CommandHandler(create_pos_article_command)
    update_pos_article = CommandHandler(update_pos_article_command)
    delete_pos_article = CommandHandler(delete_pos_article_command)
    # price_labels
    create_price_labels = CommandHandler(create_price_labels_command)
    get_price_labels_files = CommandHandler(get_price_labels_files_command)
