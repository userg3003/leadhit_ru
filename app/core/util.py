import re
from datetime import date, datetime, time, timedelta

from loguru import logger
from pydantic import BaseModel, EmailStr
from pydantic.dataclasses import dataclass


@dataclass
class Email:
    email: EmailStr


class Date(BaseModel):
    d: date


def get_type(param: tuple) -> tuple:
    if param[1] == "":
        return param[0], None
    try:
        Date(d=param[1])
        return param[0], "date"
    except Exception:
        pass
    if len(param[1]) == 10:
        try:
            datetime.strptime(param[1], "%d.%m.%Y")
            return param[0], "date"
        except Exception:
            pass
    if len(param[1]) == 16 and re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", param[1]):
        return param[0], "phone"
    try:
        Email(param[1])
        return param[0], "email"
    except Exception:
        pass

    return param[0], "text"
