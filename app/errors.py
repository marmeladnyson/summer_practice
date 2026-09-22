from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, code: str, message: str, http_status: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(message)


class NoteNotFoundError(AppError):
    def __init__(self, note_id: str):
        super().__init__(
            code="NOTE_NOT_FOUND",
            message=f"Заметка с id={note_id} не найдена",
            http_status=status.HTTP_404_NOT_FOUND,
        )


class UserNotFoundError(AppError):
    def __init__(self, user_id: str):
        super().__init__(
            code="USER_NOT_FOUND",
            message=f"Пользователь с id={user_id} не найден",
            http_status=status.HTTP_404_NOT_FOUND,
        )


class DatabaseConflictError(AppError):
    def __init__(self, detail: str = "Конфликт данных"):
        super().__init__(
            code="DATABASE_CONFLICT",
            message=detail,
            http_status=status.HTTP_409_CONFLICT,
        )


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status,
        content={"code": exc.code, "message": exc.message, "status": exc.http_status},
    )