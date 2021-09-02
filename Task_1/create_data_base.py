import sqlite3
import json

database_file = "database.db"
sql_create = """ CREATE TABLE IF NOT EXISTS Users(
                        userId INTEGER PRIMARY KEY,
                        age INTEGER NOT NULL );

                CREATE TABLE IF NOT EXISTS Purchases (
                purchaseId INTEGER PRIMARY KEY,
                userId INTEGER,
                itemId INTEGER,
                date  retrieved_time DATE DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (userId) REFERENCES Users(userId),
                FOREIGN KEY (itemId) REFERENCES Items(itemId));

                CREATE TABLE IF NOT EXISTS Items(
                itemId INTEGER PRIMARY KEY,
                price INTEGER
                )"""

def create_connection(database=database_file):
    """Create and connection to database"""
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.executescript(sql_create)
    except Exception as e:
        print(f'ERROR create data base: {e}')
    return conn


def insert_products(conn):
    """Insert data in data base"""
    try:
        cursor = conn.cursor()
        with open('data/table_purchases.json', 'r') as write:
            datas = json.load(write)
            sql = """INSERT INTO Purchases(purchaseId,userId,itemId,date ) VALUES(?,?,?,?)"""
            for data in datas['objects']:
                table = (data['purchaseId'], data['userId'], data['itemId'], data['date'])
                cursor.execute(sql, table)

        with open('data/table_users.json', 'r') as write:
            datas = json.load(write)
            sql = """INSERT INTO Users (userId,age) VALUES(?,?)"""
            for data in datas['objects']:
                table = (data['userId'], data['age'])
                cursor.execute(sql, table)

        with open('data/table_item.json', 'r') as write:
            datas = json.load(write)
            sql = """INSERT INTO Items (itemId,price) VALUES(?,?)"""
            for data in datas['objects']:
                table = (data['itemId'], data['price'])
                cursor.execute(sql, table)
        print("Данные в таблицу успешно занесенны")
    except sqlite3.IntegrityError:
        print("Данные данные уже имеются в таблице")


    conn.commit()