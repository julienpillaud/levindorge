from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response

from app.domain.exceptions import DepositInUseError, ItemInUseError, VolumeInUseError


def add_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(ItemInUseError)
    async def item_in_use_exception_handler(
        request: Request, exc: ItemInUseError
    ) -> Response:
        message = f"'{exc.item_name}' ne peut pas être supprimé"
        request.session["_messages"] = [("danger", message)]
        return RedirectResponse(
            url=request.url_for("get_items_view", item_type=exc.item_type),
            status_code=status.HTTP_302_FOUND,
        )

    @app.exception_handler(VolumeInUseError)
    async def volume_in_use_exception_handler(
        request: Request, exc: VolumeInUseError
    ) -> Response:
        message = f"'{exc.item_name}' ne peut pas être supprimé"
        request.session["_messages"] = [("danger", message)]
        return RedirectResponse(
            url=request.url_for("get_volumes_view"),
            status_code=status.HTTP_302_FOUND,
        )

    @app.exception_handler(DepositInUseError)
    async def deposit_in_use_exception_handler(
        request: Request, exc: DepositInUseError
    ) -> Response:
        message = f"'{exc.item_name}' ne peut pas être supprimé"
        request.session["_messages"] = [("danger", message)]
        return RedirectResponse(
            url=request.url_for("get_deposits_view"),
            status_code=status.HTTP_302_FOUND,
        )
