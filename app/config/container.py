from app.utils import Dir
from app.data import Executor
from app.config.settings import settings
from app.events import Telegram, Logger, Worker
from dependency_injector import containers, providers


class DependencyInjectorContainer(containers.DeclarativeContainer):
    worker = providers.Singleton(Worker)

    logger = providers.Singleton(
        Logger,
        dir=Dir(settings._log_dir),
        worker=worker,
    )

    telegram = providers.Singleton(
        Telegram,
        token=settings._telegram_token,
        chat_id=settings._telegram_chat_id,
    )

    database = providers.Resource(
        Executor,
        db_url=settings._database_url,
        sql_schema=settings._sql_schema,
        yaml_files=settings._yaml_files,
        logger=logger,
    )

