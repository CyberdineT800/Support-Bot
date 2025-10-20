import json
import asyncpg
from data import config
from asyncpg.pool import Pool
from asyncpg import Connection
from typing import Optional, Union

class Database:
    def __init__(self):
        self.pool: Optional[Pool] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            port=config.PORT,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        if self.pool is None:
            raise RuntimeError("Connection pool is not initialized. Call Database.create() before using execute().")

        pool = self.pool 
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            telegram_name TEXT,
            username TEXT DEFAULT 'none',
            name TEXT DEFAULT 'none',
            phone TEXT DEFAULT 'none',
            region TEXT DEFAULT 'none',
            city TEXT DEFAULT 'none',
            language TEXT DEFAULT 'uz_latin',
            status TEXT DEFAULT 'unblock'
        );
        """ 
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def update_user_partial_by_id(self, user_id, **kwargs):
        if not kwargs:
            return None  

        sql = "UPDATE Users SET "
        sql += ", ".join([f"{key} = ${i}" for i, key in enumerate(kwargs.keys(), start=2)])
        sql += " WHERE id = $1 RETURNING *"

        return await self.execute(sql, user_id, *kwargs.values(), fetchrow=True)


    async def add_user(self, **kwargs):
        if not kwargs:
            return None 

        columns = ", ".join(kwargs.keys())  
        values_placeholders = ", ".join([f"${i}" for i in range(1, len(kwargs) + 1)])  
        sql = f"INSERT INTO Users ({columns}) VALUES({values_placeholders}) RETURNING *"

        return await self.execute(sql, *kwargs.values(), fetchrow=True)

    async def update_user(self, data):
        sql = ("INSERT INTO Users (telegram_id, username, telegram_name, name, phone, region, city, language, status)"
               " VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9) returning *")
        
        return await self.execute(sql,
                                  data['telegram_id'],
                                  data['username'],
                                  data['telegram_name'],
                                  data['name'],
                                  data['phone'],
                                  data['region'],
                                  data['city'],
                                  data['language'],
                                  data['status'], fetchrow=True)

    async def update_existing_user(self, data):
        sql = """
        UPDATE Users
        SET username = $2, 
            telegram_name = $3,
            name = $4, 
            phone = $5, 
            region = $6, 
            city = $7,  
            language = $8,
            status = $9
        WHERE telegram_id = $1
        RETURNING *
        """

        return await self.execute(sql,
                                  data['telegram_id'],
                                  data['username'],
                                  data['telegram_name'],
                                  data['name'],
                                  data['phone'],
                                  data['region'],
                                  data['city'],
                                  data['language'],
                                  data['status'],
                                  fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        user = await self.execute(sql, *parameters, fetchrow=True)
        
        if user:
            user_dict = dict(user)                     #type: ignore
            return user_dict
        
        return None

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_user_tgid(self, tgid):
        await self.execute("DELETE FROM Users WHERE telegram_id=$1", tgid, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_table_users(self):
        await self.execute("DROP TABLE Users", execute=True)