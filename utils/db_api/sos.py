from typing import Union, Optional

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class SOS_Database:
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

    # ===================== TABLE MAN SOS ===================== #
    async def create_table_man_sos(self):
        sql = """CREATE TABLE IF NOT EXISTS man_sos (
        id SERIAL UNIQUE,
        fullname TEXT NOT NULL,
        user_id BIGINT NOT NULL,
        audio_id TEXT NULL,
        document_id TEXT NULL,
        photo_id TEXT NULL,
        text TEXT NULL,
        video_id TEXT NULL,
        voice_id TEXT NULL,
        unique_id TEXT NULL,
        caption TEXT NULL,
        turi TEXT NULL);"""
        await self.execute(sql, execute=True)

    async def add_man_audio(self, fullname, user_id, audio_id, unique_id, caption, turi):
        sql = "INSERT INTO man_sos (fullname, user_id, audio_id, unique_id, caption, turi) VALUES ($1, $2, $3, $4, " \
              "$5, $6) returning*"
        return await self.execute(sql, fullname, user_id, audio_id, unique_id, caption, turi, fetchrow=True)

    async def select_man_audio(self, user_id, turi):
        sql = "SELECT audio_id, unique_id, caption FROM man_sos WHERE user_id=$1 AND turi=$2"
        return await self.execute(sql, user_id, turi, fetch=True)

    async def add_man_document(self, fullname, user_id, document_id, unique_id, caption, turi):
        sql = "INSERT INTO man_sos (fullname, user_id, document_id, unique_id, caption, turi) VALUES ($1, $2, $3, $4, " \
              "$5, $6) returning*"
        return await self.execute(sql, fullname, user_id, document_id, unique_id, caption, turi, fetchrow=True)

    async def select_man_document(self, user_id, turi):
        sql = "SELECT document_id, unique_id, caption FROM man_sos WHERE user_id=$1 AND turi=$2"
        return await self.execute(sql, user_id, turi, fetch=True)

    async def add_man_photo(self, fullname, user_id, photo_id, unique_id, caption, turi):
        sql = "INSERT INTO man_sos (fullname, user_id, photo_id, unique_id, caption, turi) VALUES ($1, $2, $3, $4, " \
              "$5, $6) returning*"
        return await self.execute(sql, fullname, user_id, photo_id, unique_id, caption, turi, fetchrow=True)

    async def select_man_photo(self, user_id, turi):
        sql = "SELECT photo_id, unique_id, caption FROM man_sos WHERE user_id=$1 AND turi=$2"
        return await self.execute(sql, user_id, turi, fetch=True)

    async def add_man_text(self, fullname, user_id, text, turi):
        sql = "INSERT INTO man_sos (fullname, user_id, text, turi) VALUES ($1, $2, $3, $4) returning*"
        return await self.execute(sql, fullname, user_id, text, turi, fetchrow=True)

    async def select_man_text(self, user_id, turi):
        sql = "SELECT id, text FROM man_sos WHERE user_id=$1 AND turi=$2"
        return await self.execute(sql, user_id, turi, fetch=True)

    async def add_man_video(self, fullname, user_id, video_id, unique_id, caption, turi):
        sql = "INSERT INTO man_sos (fullname, user_id, video_id, unique_id, caption, turi) VALUES ($1, $2, $3, $4, " \
              "$5, $6) returning*"
        return await self.execute(sql, fullname, user_id, video_id, unique_id, caption, turi, fetchrow=True)

    async def select_man_video(self, user_id, turi):
        sql = "SELECT video_id, unique_id, caption FROM man_sos WHERE user_id=$1 AND turi=$2"
        return await self.execute(sql, user_id, turi, fetch=True)

    async def add_man_voice(self, fullname, user_id, voice_id, unique_id, caption, turi):
        sql = "INSERT INTO man_sos (fullname, user_id, voice_id, unique_id, caption, turi) VALUES ($1, $2, $3, $4, " \
              "$5, $6) returning*"
        return await self.execute(sql, fullname, user_id, voice_id, unique_id, caption, turi, fetchrow=True)

    async def select_man_voice(self, user_id, turi):
        sql = "SELECT voice_id, unique_id, caption FROM man_sos WHERE user_id=$1 AND turi=$2"
        return await self.execute(sql, user_id, turi, fetch=True)

    async def select_all_manuser(self, user_id):
        sql = "SELECT * FROM man_sos WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def select_all_man(self):
        sql = "SELECT * FROM man_sos"
        return await self.execute(sql, fetch=True)

    async def select_question_man(self):
        sql = "SELECT DISTINCT fullname, user_id FROM man_sos"
        return await self.execute(sql, fetch=True)

    async def delete_man_unique(self, unique_id):
        await self.execute("DELETE FROM man_sos WHERE unique_id=$1", unique_id, execute=True)

    async def delete_man_text(self, text):
        await self.execute("DELETE FROM man_sos WHERE text=$1", text, execute=True)

    async def delete_man_id(self, m_id):
        await self.execute("DELETE FROM man_sos WHERE id=$1", m_id, execute=True)

    async def drop_table_man_sos(self):
        await self.execute("DROP TABLE man_sos", execute=True)


    # ===================== TABLE BOT ANSWER ===================== #
    async def create_table_bot_answer(self):
        sql = """CREATE TABLE IF NOT EXISTS bot_answer (
        id SERIAL UNIQUE NOT NULL,
        man TEXT NULL,
        woman TEXT NULL,
        gender TEXT NOT NULL
        );"""
        await self.execute(sql, execute=True)

    async def add_bot_answer(self, text, gender):
        sql = "INSERT INTO bot_answer (man, gender) VALUES ($1, $2) returning*"
        return await self.execute(sql, text, gender, fetchrow=True)

    async def select_bot_answer(self, gender):
        sql = "SELECT * FROM bot_answer WHERE gender=$1"
        return await self.execute(sql, gender, fetch=True)

    async def update_bot_answerman(self, text, gender):
        sql = "UPDATE bot_answer SET man=$1 WHERE gender=$2"
        return await self.execute(sql, text, gender, execute=True)

    async def update_bot_answerwoman(self, text, gender):
        sql = "UPDATE bot_answer SET woman=$1 WHERE gender=$2"
        return await self.execute(sql, text, gender, execute=True)

    async def delete_bot_answer(self, gender):
        await self.execute("DELETE FROM bot_answer WHERE gender=$1", gender, execute=True)

    async def drop_table_bot_answer(self):
        await self.execute("DROP TABLE bot_answer", execute=True)

    # ===================== TABLE ADMINS ===================== #
    async def create_table_admins(self):
        sql = """CREATE TABLE IF NOT EXISTS admins (
        id SERIAL UNIQUE NOT NULL,
        user_id BIGINT UNIQUE NOT NULL,
        fullname TEXT NULL
        );"""
        await self.execute(sql, execute=True)

    async def add_admins(self, user_id, fullname):
        sql = "INSERT INTO admins (user_id, fullname) VALUES ($1, $2) returning*"
        return await self.execute(sql, user_id, fullname, fetchrow=True)

    async def all_admins(self):
        sql = "SELECT * FROM admins"
        return await self.execute(sql, fetch=True)

    async def select_admins(self, user_id):
        sql = "SELECT user_id FROM admins WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def delete_admin(self, user_id):
        await self.execute("DELETE FROM admins WHERE user_id=$1", user_id, execute=True)

    async def drop_table_admins(self):
        await self.execute("DROP TABLE admins", execute=True)
