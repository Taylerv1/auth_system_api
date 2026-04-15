from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.auth import create_access_token, hash_password, verify_password
from app.crud import create_user, get_user_by_email
from app.schemas import TokenResponse, UserLogin, UserRegister, UserResponse


router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    user_data = user.model_dump(mode="json")
    password = user_data.pop("password")
    user_data["hashed_password"] = hash_password(password)

    try:
        return create_user(user_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if db_user is None or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(db_user["_id"]), "type": db_user["type"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}
