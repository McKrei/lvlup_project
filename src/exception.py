from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse




class RedirectException(HTTPException):
    def __init__(self, url: str):
        super().__init__(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail="Отказано в доступе"
        )
        self.headers = {"Location": url}
