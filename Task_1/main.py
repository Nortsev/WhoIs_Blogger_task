import create_data_base

sql_max = """SELECT strftime('%m %Y', date)as date , SUM(Items.price) as summ 
            FROM Purchases
            INNER JOIN Users ON Purchases.userId = Users.userId
            INNER JOIN Items  on Items.itemId = Purchases.itemId 
            GROUP BY strftime('%YY %m', date) HAVING  Users.age > 35
            ORDER BY summ DESC 
            LIMIT 1"""

sql_top_Items = """ SELECT Purchases.itemId,SUM(Items.price) as summ 
                    FROM Purchases
                    INNER JOIN Items on Items.itemId = Purchases.itemId
                    WHERE date > DATETIME('now','-1 YEAR') 
                    GROUP BY Purchases.itemId 
                    ORDER BY summ DESC 
                    LIMIT 1"""

sql_top_3 = """SELECT Items.itemid, SUM(Items.price),
                SUM(Items.price) * 1.0 / SUM(SUM(Items.price)) OVER () as Fraction
                FROM Purchases 
                INNER JOIN Items
                ON Items.itemid = Purchases.itemId
                WHERE Purchases.date >= '2020-01-01' AND
                      Purchases.date < '2021-01-01'
                GROUP BY Items.itemid
                ORDER BY Fraction DESC
                LIMIT 3;"""


def summ(min, max):
    sql = (f""" SELECT AVG(price)
               FROM Items 
               INNER JOIN Purchases ON Items.itemId = Purchases.itemId
               INNER JOIN Users ON Purchases.userId = Users.userId 
               where Users.age BETWEEN {min} AND {max};""")
    return sql


def main():
    conn = create_data_base.create_connection()
    create_data_base.insert_products(conn)
    cursor = conn.cursor()
    i = 1
    result = cursor.execute(summ(18, 25))
    print(
        f'Средння сумма трат пользователей в возрастном диапазоне от 18 до 25 лет включительно = {int(result.fetchone()[0])}p')
    result = cursor.execute(summ(26, 35))
    print(
        f'Средння сумма трат пользователей в возрастном диапазоне от 26 до 35 лет включительно = {int(result.fetchone()[0])}p')
    result = cursor.execute(sql_max)
    print(f'Самая большая выручка от пользователей в возрастном диапазоне 35+  = {result.fetchone()[0]}')
    result = cursor.execute((sql_top_Items))
    print(f'Саммую большую выручку за последний год дает товар с Id = {result.fetchone()[0]}')
    result = cursor.execute(sql_top_3)
    print("Топ 3 товара: ")
    for results in result:
        print(
            f"Товар №{i} c id {results[0]} c выручкой {results[1]}. Его доля в общем количестве продаж {round(results[2], 2)}")
        i += 1


if __name__ == '__main__':
    main()
