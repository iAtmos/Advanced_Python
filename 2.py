import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("db/hw_2_database.db") as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM `table_checkout` order by `sold_count` desc').fetchall()
        print("Телефоны какого цвета чаще всего покупают? \n- {}\n".format(result[0][0]))

        count_blue_phone = cursor.execute('SELECT * FROM `table_checkout` WHERE `phone_color` = "Blue"').fetchone()[1]
        count_red_phone = cursor.execute('SELECT * FROM `table_checkout` WHERE `phone_color` = "Red"').fetchone()[1]
        result = 'Синие' if count_blue_phone > count_red_phone else 'Красные'
        print("Какие телефоны чаще покупают: красные или синие? \n- {}\n".format(result))

        result = cursor.execute('SELECT * FROM `table_checkout` order by `sold_count`').fetchall()[0][0]
        print("Какой самый непопулярный цвет телефона? \n-{}".format(result))




