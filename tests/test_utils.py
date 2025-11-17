from app.utils.utils import iter_dicts


def test_iter_dicts_simple() -> None:
    data = {"a": 1, "b": 2}
    result = list(iter_dicts(data))
    assert len(result) == 1
    assert result[0] == data


def test_iter_dicts_nested() -> None:
    data = {"a": {"c": 1}, "b": {"d": 2}}
    result = list(iter_dicts(data))
    assert data in result
    assert {"c": 1} in result
    assert {"d": 2} in result


def test_iter_dicts_list() -> None:
    data = {"items": [{"id": 1}, {"id": 2}]}
    result = list(iter_dicts(data))
    assert data in result
    assert {"id": 1} in result
    assert {"id": 2} in result
