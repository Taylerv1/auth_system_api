from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from app.database import users_collection


def serialize_user(user: dict | None) -> dict | None:
    if user is None:
        return None

    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "phone_number": user["phone_number"],
        "city": user["city"],
        "age": user["age"],
        "type": user["type"],
        "created_at": user["created_at"],
    }


def to_object_id(user_id: str) -> ObjectId | None:
    try:
        return ObjectId(user_id)
    except (InvalidId, TypeError):
        return None


def get_user_by_email(email: str) -> dict | None:
    return users_collection.find_one({"email": email.lower()})


def get_user_by_id(user_id: str) -> dict | None:
    object_id = to_object_id(user_id)
    if object_id is None:
        return None
    return users_collection.find_one({"_id": object_id})


def create_user(user_data: dict) -> dict:
    user_data["created_at"] = datetime.now(timezone.utc)
    result = users_collection.insert_one(user_data)
    new_user = users_collection.find_one({"_id": result.inserted_id})
    return serialize_user(new_user)


def get_users(skip: int = 0, limit: int = 10) -> list[dict]:
    users = users_collection.find().skip(skip).limit(limit)
    return [serialize_user(user) for user in users]


def update_user(user_id: str, update_data: dict) -> dict | None:
    object_id = to_object_id(user_id)
    if object_id is None:
        return None

    updated_user = users_collection.find_one_and_update(
        {"_id": object_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    return serialize_user(updated_user)


def delete_user(user_id: str) -> bool:
    object_id = to_object_id(user_id)
    if object_id is None:
        return False

    result = users_collection.delete_one({"_id": object_id})
    return result.deleted_count == 1


def count_users() -> int:
    return users_collection.count_documents({})


def average_age() -> float:
    result = list(
        users_collection.aggregate(
            [{"$group": {"_id": None, "average_age": {"$avg": "$age"}}}]
        )
    )
    if not result:
        return 0
    return round(result[0]["average_age"], 2)


def top_cities() -> list[dict]:
    result = users_collection.aggregate(
        [
            {"$group": {"_id": "$city", "count": {"$sum": 1}}},
            {"$sort": {"count": -1, "_id": 1}},
            {"$limit": 3},
        ]
    )
    return [{"city": item["_id"], "count": item["count"]} for item in result]
