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


def select_line(db_config: dict, _sql: str, cursor=None) -> Tuple[bool, dict | str]:
    print(select_line, _sql)
    if cursor:
        cursor.execute(_sql)
        result = cursor.fetchall()
        if not result:
            return False, dict()
        result = result[0]

        res_dict = dict([(item[0], result[i]) for i, item in enumerate(cursor.description)])
        return True, res_dict
    try:
        with DBContextManager(db_config) as cursor:

            if cursor is None:
                raise CursorError("Cursor could not be created")
            else:
                cursor.execute(_sql)
                result = cursor.fetchall()
                if not result:
                    return False, dict()
                result = result[0]

                res_dict = dict([(item[0], result[i]) for i, item in enumerate(cursor.description)])
                return True, res_dict
    except CursorError as ce:
        return False, str(ce)

    return False, 'Something went wrong'


def insert(db_config: dict, _sql: str, cursor=None) -> Tuple[bool, int | str]:
    print(insert, _sql)
    if cursor:
        result = cursor.execute(_sql)
        return True, result
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

def update(db_config: dict, _sql: str, cursor=None):
    try:
        if cursor:
            cursor.execute(_sql)
        else:
            with DBContextManager(db_config) as cursor:
                if cursor is None:
                    raise ValueError("Cursor not created")
                else:
                    cursor.execute(_sql)
    except Exception as e:
        return False, str(e)
    return True, 'success'

def delete(db_config: dict, _sql: str):
    try:
        with DBContextManager(db_config) as cursor:
            if cursor is None:
                raise ValueError("Cursor not created")
            else:
                cursor.execute(_sql)
    except Exception as e:
        return False, str(e)
    return True, 'success'


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