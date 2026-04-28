from app.utils import Dir
from app.config.settings import settings
from app.data import Repository, Database  
from app.events import Telegram, Logger, Worker
from dependency_injector import containers, providers

class DependencyInjectorContainer(containers.DeclarativeContainer):
    worker = providers.Singleton(Worker)

    logger = providers.Singleton(
        Logger,
        directory=Dir(settings._log_dir),
        worker=worker,
    )

    telegram = providers.Singleton(
        Telegram,
        token=settings._telegram_token,
        chat_id=settings._telegram_chat_id,
    )

    database = providers.Singleton(
        Database,
        url=settings._database_url,
        sql=settings._sql_schema,
        yaml=settings._yaml_files,
        logger=logger,
    )

    repository = providers.Singleton(
        Repository,
        db=database, 
        logger=logger,
    )