import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("db/hw_4_database.db") as conn:
        cursor = conn.cursor()

    poverty_statistics = cursor.execute('SELECT * FROM `salaries` WHERE `salary` < 5000').fetchall()
    print(f'Выяснить, сколько человек с острова N находятся за чертой бедности, то есть получает '
          f'меньше 5000 гульденов в год. \n- {len(poverty_statistics)}')

    average_salary = cursor.execute('SELECT AVG(`salary`) FROM `salaries`').fetchall()[0]
    print(f'Посчитать среднюю зарплату по острову N. \n- {average_salary[0]}\n')

    median_salary = cursor.execute('SELECT AVG(`salary`) FROM (SELECT `salary` FROM `salaries` '
                                   'ORDER BY `salary` LIMIT 2 OFFSET (SELECT (COUNT(*) - 1) / 2 '
                                   'FROM `salaries`))').fetchall()[0]
    print(f'Посчитать медианную зарплату по острову. \n- {median_salary[0]}\n')

    count_lines = cursor.execute(f"SELECT count(*) FROM `salaries`").fetchone()[0]
    count_highest_salaries = round(count_lines / 100 * 10)
    count_lowest_salaries = count_lines - count_highest_salaries
    highest_salaries = cursor.execute(f"SELECT SUM(CAST(`salary` AS INT)) FROM `salaries` ORDER BY salary DESC LIMIT {count_highest_salaries}").fetchone()[0]
    lowest_salaries = cursor.execute(f"SELECT SUM(CAST(`salary` AS INT)) FROM `salaries` ORDER BY salary LIMIT {count_lowest_salaries}").fetchone()[0]
    print(f"Число социального неравенства: \n- {highest_salaries / lowest_salaries}")