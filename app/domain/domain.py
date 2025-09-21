from cleanstack.domain import BaseDomain, CommandHandler

from app.domain.articles.commands import (
    create_article_command,
    delete_article_command,
    get_article_command,
    get_articles_by_category_command,
    get_articles_command,
)
from app.domain.commons.commands import get_view_data_command
from app.domain.context import ContextProtocol
from app.domain.price_labels.commands import (
    create_price_labels_command,
    get_price_labels_files_command,
)
from app.domain.users.commands import get_user_by_email_command


class Domain(BaseDomain[ContextProtocol]):
    # common
    get_view_data = CommandHandler(get_view_data_command)
    # users
    get_user_by_email = CommandHandler(get_user_by_email_command)
    # articles
    get_articles = CommandHandler(get_articles_command)
    get_articles_by_category = CommandHandler(get_articles_by_category_command)
    get_article = CommandHandler(get_article_command)
    create_article = CommandHandler(create_article_command)
    delete_article = CommandHandler(delete_article_command)
    # price_labels
    create_price_labels = CommandHandler(create_price_labels_command)
    get_price_labels_files = CommandHandler(get_price_labels_files_command)
