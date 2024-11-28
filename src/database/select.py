# функции связанные с выполнением запроса в базу данных

from typing import Tuple
from database.DBcm import DBContextManager


class CursorError(Exception):
    pass


def select_list(db_config: dict, _sql: str) -> Tuple[tuple, list | str]:
    try:
        with DBContextManager(db_config) as cursor:
            if not cursor:
                raise CursorError("Cursor could not be created")
            else:
                print('Trying to execute an SQL query')
                cursor.execute(_sql)
                result = cursor.fetchall()
                # print(cursor.description)
                # в cursor.description[0] лежат имена полей из таблицы

                schema = [item[0] for item in cursor.description]
                return result, schema
    except CursorError as ce:
        return tuple(), str(ce)
    return tuple(), 'Something went wrong'


def select_dict(db_config: dict, _sql: str) -> list[dict]:
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def select_line(db_config: dict, _sql: str) -> Tuple[bool, dict | str]:
    print(select_line, _sql)
    try:
        with DBContextManager(db_config) as cursor:

            if cursor is None:
                raise CursorError("Cursor could not be created")
            else:
                cursor.execute(_sql)
                result = cursor.fetchall()
                if not result:
                    return True, dict()
                result = result[0]

                res_dict = dict([(item[0], result[i]) for i, item in enumerate(cursor.description)])
                return True, res_dict
    except CursorError as ce:
        return False, str(ce)

    return False, 'Something went wrong'


def insert(db_config: dict, _sql: str) -> Tuple[bool, int | str]:
    print(insert, _sql)
    try:
        with DBContextManager(db_config) as cursor:

            if cursor is None:
                raise CursorError("Cursor could not be created")
            else:
                result = cursor.execute(_sql)

                return True, result
    except CursorError as ce:
        return False, str(ce)

    return False, 'Something went wrong'


def stored_procedure(db_config: dict, procedure_name: str, *args) -> bool:
    print(stored_procedure, procedure_name, *args)

    try:
        with DBContextManager(db_config) as cursor:
            if not cursor:
                raise CursorError("Cursor could not be created")
            else:
                cursor.callproc(procedure_name, (*args, ))
    except CursorError:
        return False
    
    return True