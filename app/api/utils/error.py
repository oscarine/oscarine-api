from contextlib import contextmanager
from typing import Dict, Generator, NoReturn, Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from starlette.status import HTTP_409_CONFLICT

DEFAULT_ERROR_MESSAGE = "An error occurred"


@contextmanager
def expected_integrity_error(
    session: Session,
    *,
    detail: Optional[str] = None,
    status_code: int = HTTP_409_CONFLICT,
    debug: bool,
) -> Generator[None, None, None]:
    try:
        yield
    except IntegrityError as exc:
        session.rollback()
        _raise_api_response_error(detail, status_code, exc=exc, debug=debug)


def _raise_api_response_error(
    detail: Optional[str],
    status_code: int,
    headers: Optional[Dict[str, str]] = None,
    exc: Optional[Exception] = None,
    debug: bool = False,
) -> NoReturn:
    if debug and exc is not None:
        detail = str(exc)
    if detail is None:
        detail = DEFAULT_ERROR_MESSAGE
    raise HTTPException(detail=detail, status_code=status_code, headers=headers)
