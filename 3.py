import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("db/hw_3_database.db") as conn:
        cursor = conn.cursor()
        for i in range(1, 4):
            count_lines = cursor.execute(f"SELECT count(*) FROM `table_{i}`").fetchone()
            print("Кол-во записей в таблице {}: {}".format(i, count_lines[0]))

        unique_entries = cursor.execute('SELECT DISTINCT `value` FROM `table_1`').fetchall()
        print("\nСколько в таблице table_1 уникальных записей? \n-{}\n".format(len(unique_entries)))

        shared_entries = cursor.execute('SELECT count(*) FROM (SELECT * FROM table_1 INTERSECT SELECT * FROM table_2)').fetchall()[0]
        print(F'Как много записей из таблицы table_1 встречается в table_2? \n- {shared_entries[0]}\n')

        shared_entries = cursor.execute('SELECT count(*) FROM (SELECT * FROM table_1 INTERSECT SELECT * FROM table_2 INTERSECT SELECT * FROM table_3)').fetchall()[0]
        print(F'Как много записей из таблицы table_1 встречается и в table_2, и в table_3? \n- {shared_entries[0]}')
