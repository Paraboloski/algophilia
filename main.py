import sys
import flet as ft
from app.view.app import App
from typing import Any, Never
from app.utils import AppError
from app.config import Container

def panic(err: Any) -> Never:
    print(f"panic: {err}", file=sys.stderr)
    sys.exit(1)

async def bootstrap(container: Container) -> None:
    logger = container.logger()
    logger.subscribe(container.telegram().send)

    result = await container.database().start()
    if result.is_err():
        err = result.unwrap_err()
        logger.error(f"Bootstrap: Errore inizializzazione DB | {err}")
        panic(err)

async def shutdown(container: Container) -> None:
    result = await container.database().disconnect()
    if result.is_err():
        container.logger().error(f"Shutdown: {result.unwrap_err()}")

    container.worker().shutdown()
    container.logger()._directory._rmdir()

async def main(page: ft.Page) -> None:
    container = Container()
    _done = False

    def cleanup() -> None:
        nonlocal _done
        if not _done:
            _done = True
            page.run_task(shutdown, container)

    page.on_close = cleanup
    page.on_disconnect = cleanup

    await bootstrap(container)

    try:
        await App(page, container).build()
    except AppError as e:
        panic(e)

if __name__ == "__main__":
    ft.run(main, assets_dir="app/assets")