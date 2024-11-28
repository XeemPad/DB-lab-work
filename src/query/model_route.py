from dataclasses import dataclass
from database.select import select_list

@dataclass
class ProductInfoResponse:
    result: tuple
    error_message: str
    status: bool


def get_prods_from_db(db_config, user_input_data, sql_provider):
    if 'prod_category' not in user_input_data:
        print("user_input_data=", user_input_data)
        result = ()
        return ProductInfoResponse(result, error_message='', status=False)
    _sql = sql_provider.get('product.sql', prod_category=user_input_data['prod_category'])
    print("sql =", _sql)
    result, schema_or_error = select_list(db_config, _sql)
    if result:
        return ProductInfoResponse(result, error_message='', status=True)
    return ProductInfoResponse(result, error_message=f'No rows found for query "{_sql}". {schema_or_error}', status=False)