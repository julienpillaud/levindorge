import http
from typing import Any

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize("shop", ["angouleme", "sainte-eulalie", "pessac"])
def test_create_tags_view(
    client: FlaskClient,
    templates: list[tuple[Any, Any]],
    shop: str,
) -> None:
    response = client.get(f"/tags/create?shop={shop}")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert len(context["articles"]) >= 1


def test_create_tags(
    client: FlaskClient,
    templates: list[tuple[Any, Any]],
) -> None:
    data = {"603d0b2287206cd6ef351759": 9}
    response = client.post("/tags/create?shop=pessac", data=data)
    assert response.status_code == http.HTTPStatus.FOUND


def test_list_tag_files(
    client: FlaskClient,
    templates: list[tuple[Any, Any]],
) -> None:
    response = client.get("/tags/files")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert len(context["files"]) >= 1
