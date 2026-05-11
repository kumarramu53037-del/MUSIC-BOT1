# =========================================
# utils/database.py
# =========================================

import pymongo
import redis

from datetime import datetime, timedelta

from config import (
    MONGO_DB_URL,
    MONGO_DB_NAME,
    REDIS_URL
)

# =========================================
# DATABASE CLASS
# =========================================

class Database:

    def __init__(self):

        # MongoDB Client
        self.mongo = None

        # Database
        self.db = None

        # Redis Client
        self.redis_client = None

        # =====================================
        # CONNECT MONGODB
        # =====================================

        if MONGO_DB_URL:

            self.mongo = pymongo.MongoClient(
                MONGO_DB_URL
            )

            self.db = self.mongo[
                MONGO_DB_NAME
            ]

            print("✅ MongoDB Connected")

        # =====================================
        # CONNECT REDIS
        # =====================================

        if REDIS_URL:

            self.redis_client = redis.from_url(
                REDIS_URL
            )

            print("✅ Redis Connected")

        # =====================================
        # MEMORY STORAGE
        # =====================================

        self.memory = {
            "users": {},
            "groups": {},
            "playlists": {},
            "queues": {}
        }

    # =========================================
    # USER SYSTEM
    # =========================================

    async def get_user(self, user_id: int):

        """
        Get user data
        """

        # MongoDB
        if self.db:

            user = self.db.users.find_one(
                {"_id": user_id}
            )

            # Create New User
            if not user:

                user = {
                    "_id": user_id,
                    "coins": 0,
                    "premium": False,
                    "songs_played": 0,
                    "downloads": 0,
                    "registered_at": datetime.utcnow()
                }

                self.db.users.insert_one(user)

            return user

        # Memory Fallback
        return self.memory["users"].get(
            user_id,
            {
                "coins": 0,
                "premium": False
            }
        )

    # =========================================
    # UPDATE USER
    # =========================================

    async def update_user(
        self,
        user_id: int,
        data: dict
    ):

        """
        Update user data
        """

        if self.db:

            self.db.users.update_one(
                {"_id": user_id},
                {"$set": data},
                upsert=True
            )

        else:

            self.memory["users"][user_id] = {

                **self.memory["users"].get(
                    user_id,
                    {}
                ),

                **data
            }

    # =========================================
    # ADD COINS
    # =========================================

    async def add_coins(
        self,
        user_id: int,
        amount: int
    ):

        user = await self.get_user(user_id)

        current = user.get("coins", 0)

        new_balance = current + amount

        await self.update_user(
            user_id,
            {
                "coins": new_balance
            }
        )

        return new_balance

    # =========================================
    # REMOVE COINS
    # =========================================

    async def remove_coins(
        self,
        user_id: int,
        amount: int
    ):

        user = await self.get_user(user_id)

        current = user.get("coins", 0)

        new_balance = max(
            0,
            current - amount
        )

        await self.update_user(
            user_id,
            {
                "coins": new_balance
            }
        )

        return new_balance

    # =========================================
    # PREMIUM SYSTEM
    # =========================================

    async def set_premium(
        self,
        user_id: int,
        days: int = 30
    ):

        expiry = (
            datetime.utcnow()
            + timedelta(days=days)
        )

        await self.update_user(
            user_id,
            {
                "premium": True,
                "premium_expiry": expiry
            }
        )

    # =========================================
    # GROUP SETTINGS
    # =========================================

    async def get_group(
        self,
        group_id: int
    ):

        if self.db:

            group = self.db.groups.find_one(
                {"_id": group_id}
            )

            if not group:

                group = {
                    "_id": group_id,
                    "volume": 100,
                    "autoplay": False,
                    "loop": False,
                    "language": "en"
                }

                self.db.groups.insert_one(group)

            return group

        return self.memory["groups"].get(
            group_id,
            {
                "volume": 100,
                "autoplay": False
            }
        )

    # =========================================
    # UPDATE GROUP
    # =========================================

    async def update_group(
        self,
        group_id: int,
        data: dict
    ):

        if self.db:

            self.db.groups.update_one(
                {"_id": group_id},
                {"$set": data},
                upsert=True
            )

        else:

            self.memory["groups"][group_id] = {

                **self.memory["groups"].get(
                    group_id,
                    {}
                ),

                **data
            }

    # =========================================
    # PLAYLIST SYSTEM
    # =========================================

    async def save_playlist(
        self,
        user_id: int,
        name: str,
        songs: list
    ):

        if self.db:

            self.db.playlists.update_one(
                {
                    "user_id": user_id,
                    "name": name
                },
                {
                    "$set": {
                        "songs": songs
                    }
                },
                upsert=True
            )

    async def get_playlist(
        self,
        user_id: int,
        name: str
    ):

        if self.db:

            return self.db.playlists.find_one(
                {
                    "user_id": user_id,
                    "name": name
                }
            )

        return None

    async def get_all_playlists(
        self,
        user_id: int
    ):

        if self.db:

            return list(
                self.db.playlists.find(
                    {
                        "user_id": user_id
                    }
                )
            )

        return []

    # =========================================
    # GLOBAL STATS
    # =========================================

    async def get_stats(self):

        if self.db:

            users = self.db.users.count_documents(
                {}
            )

            groups = self.db.groups.count_documents(
                {}
            )

            playlists = self.db.playlists.count_documents(
                {}
            )

            return {
                "users": users,
                "groups": groups,
                "playlists": playlists
            }

        return {
            "users": 0,
            "groups": 0,
            "playlists": 0
        }


# =========================================
# DATABASE INSTANCE
# =========================================

db = Database()
