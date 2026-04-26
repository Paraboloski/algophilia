class AppError(Exception):
    pass


class EnvError(AppError):
    pass


class SQliteError(AppError):
    pass
