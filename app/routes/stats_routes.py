from fastapi import APIRouter

from app.crud import average_age, count_users, top_cities
from app.schemas import AverageAgeResponse, TopCitiesResponse, UserCountResponse


router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/count", response_model=UserCountResponse)
def get_user_count():
    return {"total_users": count_users()}


@router.get("/average-age", response_model=AverageAgeResponse)
def get_average_age():
    return {"average_age": average_age()}


@router.get("/top-cities", response_model=TopCitiesResponse)
def get_top_cities():
    return {"cities": top_cities()}
