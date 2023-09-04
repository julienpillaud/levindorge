"""
Module to acces Tactill API

https://documentation.tactill.com/docs
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

requests.packages.urllib3.disable_warnings()

API_URL = "https://api4.tactill.com/v1"
EXCLUED_CATEGORIES = ["AUTRE", "BAR", "CONSIGNE", "STREETFOOD", "VDO"]
TIMEOUT = 5


class Tactill:
    """Acces to a Tactill shop"""

    def __init__(self, api_key, verify=True):
        self._session = requests.Session()
        self._session.verify = verify
        _retry = Retry(total=3, allowed_methods=False, status_forcelist=[502, 504])
        self._session.mount(API_URL, HTTPAdapter(max_retries=_retry))
        self._session.headers = {"x-api-key": api_key}

        res = self._session.get(f"{API_URL}/account/account", timeout=TIMEOUT)
        self.account_infos = res.json()
        if not self.account_infos:
            raise ConnectionError("Can not acces to API")

        self.node_id = self.account_infos["nodes"][0]
        self.company_id = self.account_infos["companies"][0]
        self.shop_id = self.account_infos["shops"][0]

    def get_articles(
        self, deprecated="false", is_default="false", query="in", **kwargs
    ):
        """Get a list of Article based on the given filters in query"""
        url = f"{API_URL}/catalog/articles"
        filter_ = f"deprecated={deprecated}&is_default={is_default}"

        for key, value in kwargs.items():
            if key == "category":
                categories = self.get_categories(name=value)
                if not categories:
                    return []
                category_ids = [x["_id"] for x in categories]
                key = "category_id"
                value = category_ids[0] if len(category_ids) == 1 else category_ids

            if isinstance(value, list):
                filter_ += f"&{key}[{query}]=" + f"&{key}[{query}]=".join(value)
            elif isinstance(value, (int, str)):
                filter_ += f"&{key}={value}"

        params = {"filter": filter_, "node_id": self.node_id}
        response = self._session.get(url, params=params, timeout=TIMEOUT)
        response = response.json()
        return response or []

    def create_article(self, category, tax_rate, name, full_price, **kwargs):
        """Create an article"""
        categories = self.get_categories(name=category)
        category = categories[0] if categories else {}
        category_id = category.get("_id")

        taxes = self.get_taxes(rate=tax_rate)
        tax = taxes[0] if taxes else {}
        taxes = [tax.get("_id")]

        data = {
            "node_id": self.node_id,
            "category_id": category_id,
            "taxes": taxes,
            "name": name,
            "full_price": full_price,
        }
        data.update(kwargs)

        url = f"{API_URL}/catalog/articles"
        return self._session.post(url, json=data)

    def delete_article(self, reference):
        """Delete an article"""
        article = self.get_articles(reference=reference)
        article = next(iter(article), {})
        article_id = article.get("_id")

        url = f"{API_URL}/catalog/articles/{article_id}"
        return self._session.delete(url, timeout=TIMEOUT)

    def update_article(self, reference, tax_rate=None, **kwargs):
        """update an article"""
        article = self.get_articles(reference=reference)
        article = next(iter(article), {})
        article_id = article.get("_id")

        taxes = article.get("taxes")
        if tax_rate:
            tax = self.get_taxes(rate=tax_rate)
            tax = next(iter(tax), {}).get("_id")
            taxes = [tax]

        # in_stock is true to prevent the removal of stock_quantity
        data = {"taxes": taxes, "in_stock": "true"}
        data.update(kwargs)

        url = f"{API_URL}/catalog/articles/{article_id}"
        return self._session.put(url, json=data)

    def get_categories(
        self, deprecated="false", is_default="false", query="in", **kwargs
    ):
        """Get a list of Category based on the given filters in query"""
        url = f"{API_URL}/catalog/categories"
        filter_ = f"deprecated={deprecated}&is_default={is_default}"

        for key, value in kwargs.items():
            if isinstance(value, list):
                filter_ += f"&{key}[{query}]=" + f"&{key}[{query}]=".join(value)
            elif isinstance(value, (int, str)):
                filter_ += f"&{key}={value}"

        params = {"filter": filter_, "company_id": self.company_id}
        response = self._session.get(url, params=params, timeout=TIMEOUT)
        response = response.json()
        return response or []

    def get_taxes(self, deprecated="false", rate=None):
        """Get a list of Tax based on the given filters in query"""
        url = f"{API_URL}/catalog/taxes"
        filter_ = f"deprecated={deprecated}"
        params = {"filter": filter_, "company_id": self.company_id}

        response = self._session.get(url, params=params, timeout=TIMEOUT)
        response = response.json()
        if not response:
            return []
        if rate:
            return [x for x in response if x["rate"] == rate]
        return response
