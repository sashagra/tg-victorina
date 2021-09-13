import os
from typing import Dict, List, Tuple

import sqlite3


conn = sqlite3.connect(os.path.join("db", "victorina.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def _to_objects_list(rows, columns):
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    if len(result) == 1:
        return result[0]
    elif not len(result):
        return None
    else:
        return result


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    return _to_objects_list(rows, columns)


def select_by_keys(table: str, columns: List[str],  *args: Dict,):
    columns_joined = ", ".join(columns)
    search_strings = []
    for arg in args:
        for key in arg.keys():
            search_strings.append(f"{key}='{arg[key]}'")

    query = f"select {columns_joined} from {table} where {' and '.join(search_strings)}"
    cursor.execute(query)
    rows = cursor.fetchall()
    return _to_objects_list(rows, columns)


def delete(table: str, row_id: int) -> None:
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='users'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
