import jwt
import time
import logging
#import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
import pymongo

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


# def search_global(title='', content='', tag=''):
#     return 200, "ok"


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        # Check if user with the same user_id already exists
        existing_user = self.conn['user'].find_one({"user_id": user_id})
        if existing_user:
            # If user with the same user_id exists, return an error
            return error.error_exist_user_id(user_id)

        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            user_doc = {
                "user_id": user_id,
                "password": password,
                "balance": 0,
                "token": token,
                "terminal": terminal
            }
            self.conn['user'].insert_one(user_doc)
        except pymongo.errors.PyMongoError as e:
            return 528, str(e)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        user = self.conn['user'].find_one({'user_id': user_id})
        if user is None:
            return error.error_authorization_fail()
        db_token = user.get('token', '')
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        user = self.conn['user'].find_one({'user_id': user_id})
        if user is None:
            return error.error_authorization_fail()

        if password != user.get('password'):
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            result = self.conn['user'].update_one({'user_id': user_id}, {'$set': {'token': token, 'terminal': terminal}})
            if result.matched_count == 0:
                return error.error_authorization_fail() + ("",)
        except pymongo.errors.PyMongoError as e:
            return 528, str(e), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            result = self.conn['user'].update_one({'user_id': user_id}, {'$set': {'token': dummy_token, 'terminal': terminal}})
            if result.matched_count == 0:
                return error.error_authorization_fail()
        except pymongo.errors.PyMongoError as e:
            return 528, str(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            result = self.conn['user'].delete_one({'user_id': user_id})
            if result.deleted_count != 1:
                return error.error_authorization_fail()
        except pymongo.errors.PyMongoError as e:
            return 528, str(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.conn['user'].update_one(
                {'user_id': user_id},
                {'$set': {
                    'password': new_password,
                    'token': token,
                    'terminal': terminal,
                }},
            )
        except pymongo.errors.PyMongoError as e:
            return 528, str(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def search_book(self, title='', content='', tag='', store_id=''):
        try:
            query = {}

            if title:
                query['title'] = {"$regex": title}
            if content:
                query['content'] = {"$regex": content}
            if tag:
                query['tags'] = {"$regex": tag}

            # 检查 store_id 是否为空
            if store_id:
                # 查询 store 集合，获取指定 store_id 下的所有 book_id
                store_query = {"store_id": store_id}
                store_result = list(self.conn["store"].find(store_query))
                if len(store_result) == 0:
                    return error.error_non_exist_store_id(store_id)
                book_ids = [item["book_id"] for item in store_result]
                # 添加 book_id 到查询条件
                query['id'] = {"$in": book_ids}

            # 执行查询
            results = list(self.conn["books"].find(query))
        except pymongo.errors.PyMongoError as e:
            return 528, str(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        if not results:
            return 529, "No matching books found."
        else:
            return 200, "ok"
