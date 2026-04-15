import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import UserType


PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


def strip_required_text(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    return value


class UserRegister(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone_number: str
    city: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)
    type: UserType
    password: str = Field(..., min_length=1)

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value: str) -> str:
        return strip_required_text(value, "first_name")

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: str) -> str:
        return strip_required_text(value, "last_name")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        value = value.strip()
        if not PHONE_REGEX.fullmatch(value):
            raise ValueError("phone_number must contain 7 to 15 digits and may start with +")
        return value

    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str) -> str:
        return strip_required_text(value, "city")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("password must not be empty")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("password must not be empty")
        return value


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    city: str | None = None
    age: int | None = Field(default=None, gt=0)
    type: UserType | None = None

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return strip_required_text(value, "first_name")

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return strip_required_text(value, "last_name")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr | None) -> str | None:
        if value is None:
            return value
        return str(value).lower()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not PHONE_REGEX.fullmatch(value):
            raise ValueError("phone_number must contain 7 to 15 digits and may start with +")
        return value

    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return strip_required_text(value, "city")


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    city: str
    age: int
    type: UserType
    created_at: datetime

    model_config = ConfigDict(use_enum_values=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCountResponse(BaseModel):
    total_users: int


class AverageAgeResponse(BaseModel):
    average_age: float


class CityCount(BaseModel):
    city: str
    count: int


class TopCitiesResponse(BaseModel):
    cities: list[CityCount]
