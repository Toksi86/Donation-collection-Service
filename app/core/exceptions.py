from fastapi import HTTPException
from http import HTTPStatus


class BadRequest(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)
