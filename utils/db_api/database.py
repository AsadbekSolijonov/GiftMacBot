import logging
import pysqlite3
from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self):
        self.conn = pysqlite3.connect('/Users/asadbeksolijonov/Bots/GiftMacShopBot/database.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    @abstractmethod
    def create_table(self):
        pass


class Gifts(Database):
    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        name TEXT NOT NULL)"""
        self.cursor.execute(sql)

    def insert_gift(self, name):
        with self.conn:
            sql = f"""INSERT INTO gifts (name) VALUES (?)"""
            self.cursor.execute(sql, (name,))

    def has_gift(self, name):
        sql = f"""SELECT * FROM gifts WHERE name LIKE '{name}'"""
        data = self.cursor.execute(sql).fetchone()
        return data if data else None

    def delete_gift(self, gift_id):
        with self.conn:
            sql = f"""DELETE FROM gifts WHERE id=?"""
            self.cursor.execute(sql, (gift_id,))

    def has_gift_by_id(self, gift_id):
        sql = """SELECT * FROM gifts WHERE id=?"""
        data = self.cursor.execute(sql, (gift_id,)).fetchone()
        return data if data else None

    def all_gifts(self):
        sql = """SELECT * FROM gifts"""
        data = self.cursor.execute(sql).fetchall()
        return data if data else None


class Clients(Database):
    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS Clients
        (chat_id INTEGER NOT NULL,
        name TEXT,
        contact NUMERIC,
        gift TEXT,
        status TEXT DEFAULT 'open',
        attempt DEFAULT 0,
        day datetime DEFAULT CURRENT_TIMESTAMP)"""
        self.cursor.execute(sql)

    def has_client_id(self, chat_id):
        sql = """SELECT * FROM Clients WHERE chat_id=?"""
        data = self.cursor.execute(sql, (chat_id,)).fetchone()
        return data if data else None

    def insert_clients(self, **kwargs):
        keys = tuple(kwargs.keys())
        values = tuple(kwargs.values())
        with self.conn:
            sql = f"""INSERT INTO Clients {keys} VALUES {values}"""
            self.cursor.execute(sql)

    def update_clients(self, chat_id, **kwargs):
        dict_format = ', '.join([f"{key}='{value}'" for key, value in kwargs.items()])
        logging.info(dict_format)
        with self.conn:
            sql = f"""UPDATE Clients SET {dict_format} WHERE chat_id = ?"""
            self.cursor.execute(sql, (chat_id,))

    def plus_attempt(self, chat_id):
        with self.conn:
            sql = """UPDATE Clients SET attempt=attempt + 1 WHERE chat_id = ?"""
            self.cursor.execute(sql, (chat_id,))

    def how_attempt_status(self, chat_id):
        sql = """SELECT attempt, status FROM Clients WHERE chat_id = ?"""
        data = self.cursor.execute(sql, (chat_id,)).fetchone()
        return data if data else None

    def find_gift(self, chat_id):
        sql = """SELECT gift, status, day FROM Clients WHERE chat_id = ?"""
        data = self.cursor.execute(sql, (chat_id,)).fetchone()
        return data if data else None


if __name__ == "__main__":
    Clients()
    Gifts()
