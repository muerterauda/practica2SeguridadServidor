from bson import ObjectId

from mongo.entity.usuario import User
from mongo.mongo_manager import usuarios


def save_user(user: User):
    usuarios.insert_one(user.user_to_dict())


def find_user_by_id(user_id) -> User:
    res = usuarios.find_one({"id": user_id})
    if res is not None:
        return User(res)


def replace_user_by_id(user_id, new_user: User):
    return usuarios.replace_one({"_id": ObjectId(user_id)}, new_user.user_to_dict())


def update_user_by_id(user_id, actualizacion_user: dict):
    return usuarios.update_one({"_id": ObjectId(user_id)}, {"$set": actualizacion_user}, upsert=False)