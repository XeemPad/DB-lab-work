from dataclasses import dataclass
from database.select import select_list, insert, delete
from datetime import datetime
from database.DBcm import DBContextManager
from pymysql import Error


@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def model_route_transaction_order(db_config : dict, sql_provider, basket : dict, user_id: int):
    ddate = datetime.now()
    _sql = sql_provider.get('create_order.sql', e_user_id=user_id, e_order_date=ddate)
    print(_sql)
    result = insert(db_config, _sql)
    if not result:
        return ProductInfoRespronse(tuple(), error_message="Заказ не был создан", status=False)
    _sql = sql_provider.get('get_order.sql', e_user_id=user_id, e_order_date=ddate)
    order_id = select_list(db_config,_sql)[0][0]
    print(basket)
    for key, value in basket.items():
        _sql = sql_provider.get('insert_order_line.sql',
                                e_order_id = order_id[0],
                                e_prod_id = int(key),
                                e_amount = int(value))
        print(_sql)
        result = insert(db_config, _sql)
        if not result:
            _sql = sql_provider.get('delete_order.sql', delid = order_id)
            delete(db_config, _sql)
            _sql = sql_provider.get('delete_orders.sql', delid=order_id)
            delete(db_config, _sql)
    result = tuple(order_id)
    return ProductInfoRespronse(result, error_message="", status=True)


def transaction_order(db_config : dict, sql_provider, basket : dict, user_id: int):
    ddate = datetime.today()
    order_id = None
    with DBContextManager(db_config) as cursor:
        cursor.conn(autocommit=False)
        # любая ошибка при ходе выполнения интерпретируется как выход из курсора, см DBContextManager.__exit__
        _sql = sql_provider.get('create_order.sql', e_user_id=user_id, e_order_date=ddate)
        try:
            cursor.execute(_sql)
        except Error as err:
            print("error in transaction_order():", err.args)
            return ProductInfoRespronse(tuple(), error_message="Заказ не был создан", status=False)

        order_id = cursor.lastrowid

        for key, value in basket.items():
            _sql = sql_provider.get('insert_order_line.sql',
                                    e_order_id=order_id[0],
                                    e_prod_id=int(key),
                                    e_amount=int(value))
            result = insert(db_config, _sql)
            # обработка ошибки происходит в database.insert
            if not result:
                return ProductInfoRespronse(tuple(), error_message="Заказ не был создан", status=False)
    result = tuple(order_id)
    return ProductInfoRespronse(result, error_message="", status=True)
















