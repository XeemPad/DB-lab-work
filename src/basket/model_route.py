from dataclasses import dataclass
from database.select import select_line, insert, delete, update
from datetime import datetime
from database.DBcm import DBContextManager
from pymysql import Error


@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def transaction_order(db_config: dict, sql_provider, basket: dict, user_id: int):
    with DBContextManager(db_config) as cursor:
        ddate = datetime.today().replace(microsecond=0)  # microseconds aren't stored in DB
        _sql = sql_provider.get('create_order.sql', e_user_id=user_id, e_order_date=ddate)
        print(_sql)
        result = insert(db_config, _sql, cursor)
        if not result[0]:
            return ProductInfoRespronse(tuple(), error_message="Заказ не был создан", status=False)
        _sql = sql_provider.get('get_order.sql', e_user_id=user_id, e_order_date=ddate)
        status, res_dict = select_line(db_config, _sql, cursor)
        print(_sql)
        if not status:
            return ProductInfoRespronse(tuple(), error_message=f"Не удалось получить созданный заказ. {res_dict}", 
                                        status=False)

        order_id = res_dict['order_id']
        print(basket)
        total_cost = 0
        for key, value in basket.items():
            _sql = sql_provider.get('insert_order_line.sql',
                                    e_order_id=order_id,
                                    e_prod_id=int(key),
                                    e_amount=int(value))
            result = insert(db_config, _sql, cursor)
            print(_sql)
            
            _sql = sql_provider.get('one_good.sql', e_prod_id=int(key))
            status, res_dict = select_line(db_config, _sql, cursor)
            print(_sql)
            if not status:
                return ProductInfoRespronse(value, error_message="Не удалось найти продукт с id = {int(key)}", status=False)
            total_cost += int(value) * res_dict['prod_price']

        _sql = sql_provider.get('update_order.sql', total_cost=total_cost, e_order_id=order_id)
        status, msg = update(db_config, _sql, cursor)
        if not status:
            return ProductInfoRespronse(tuple(), error_message=f"Не удалось обновить общую стоимость заказа. {msg}", status=True)

        return ProductInfoRespronse((order_id, ), error_message="", status=True)
