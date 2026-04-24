class AppError(Exception):
    pass

class EnvError(AppError):
    pass

class DataError(AppError):
    pass