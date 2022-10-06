from pydantic import ValidationError

class AppError(Exception):
    code = 500
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason

class NotFoundError(AppError):
    code = 404
    def __init__(self, name: str, uid: int) -> None:
        super().__init__(f'{name} [{uid}] not found')
        self.name = name
        self.uid = uid

def handle_app_error(e: AppError):
    return {'error': str(e)}, e.code

def handle_validation_error(e: ValidationError):
    return {'error': str(e)}, 400
