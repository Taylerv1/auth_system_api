from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.errors import DuplicateKeyError

from app.crud import delete_user, get_user_by_email, get_user_by_id, get_users, update_user
from app.dependencies import require_admin
from app.schemas import UserResponse, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_admin: dict = Depends(require_admin),
):
    return get_users(skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def edit_user(
    user_id: str,
    user: UserUpdate,
    current_admin: dict = Depends(require_admin),
):
    existing_user = get_user_by_id(user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user.model_dump(exclude_unset=True, exclude_none=True, mode="json")
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided",
        )

    if "email" in update_data and update_data["email"] != existing_user["email"]:
        if get_user_by_email(update_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

    try:
        updated_user = update_user(user_id, update_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return updated_user


@router.delete("/{user_id}")
def remove_user(
    user_id: str,
    current_admin: dict = Depends(require_admin),
):
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": "User deleted successfully"}
