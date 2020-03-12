import csv
import sqlite3

import pandas
import pandas as pd


def load_from_csv(table: str, db: str, csv_file: str):
    """
    :param table:
    :param db:
    :type csv_file: , separated with header in first line
    """
    csv_reader = csv.DictReader(open(csv_file))
    df = pd.DataFrame(list(csv_reader))

    with sqlite3.connect(db) as con:
        df.to_sql(name=table,
                  con=con,
                  if_exists='append')


if __name__ == '__main__':
    table_name = 'sales_data'
    sqlite_db = 'db.sqlite3'
    file_name = '50000_sales_records.csv'
    # load_from_csv(table_name, sqlite_db, file_name)

    connection = sqlite3.connect(sqlite_db)
    crsr = connection.cursor()

    sql = "select ROW_NUMBER() OVER (order by Region ASC) as 'r' from sales_data"
    df = pandas.read_sql(sql, connection)
    crsr.execute(sql)
