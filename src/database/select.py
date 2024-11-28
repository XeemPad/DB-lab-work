# функции связанные с выполнением запроса в базу данных

from turtle import st

from database.DBcm import DBContextManager


class CursorError(Exception):
    pass


def select_list(db_config: dict, _sql: str):

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise CursorError("Cursor could not be created")
        else:
            print('Trying to execute an SQL query')
            cursor.execute(_sql)
            result = cursor.fetchall()
            # print(cursor.description)
            # в cursor.description[0] лежат имена полей из таблицы

            schema = [item[0] for item in cursor.description]
            return result, schema
    print('With clause was exited early in select.py/select_list')
    return [], []

def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def select_line(db_config: dict, _sql: str):
    print(select_line, _sql)

    with DBContextManager(db_config) as cursor:

        if cursor is None:
            raise CursorError("Cursor could not be created")
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            if not result:
                return dict()
            result = result[0]

            res_dict = dict([(item[0], result[i]) for i, item in enumerate(cursor.description)])
            return res_dict

    print('With clause was exited early in select.py/select_line')
    return dict()


def insert(db_config: dict, _sql: str):
    print(insert, _sql)
    with DBContextManager(db_config) as cursor:

        if cursor is None:
            raise CursorError("Cursor could not be created")
        else:
            result = cursor.execute(_sql)

            return result
    return False


def stored_procedure(db_config: dict, procedure_name: str, *args) -> bool:
    print(stored_procedure, procedure_name, *args)

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise CursorError("Cursor could not be created")
        else:
            
            cursor.callproc(procedure_name, (*args, ))

            
    return True