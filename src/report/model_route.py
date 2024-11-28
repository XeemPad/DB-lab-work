from dataclasses import dataclass
from database.select import select_line, select_list, stored_procedure

from database.sql_provider import SQLProvider
import os
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@dataclass
class ReportInfoResponse:
    result: tuple  # ?
    error_message: str
    status: bool


def check_report_exists(db_config, user_input_data):
    year, month = [int(el) for el in user_input_data['year_month'].split('-')]
    print('Requested month and year:', month, year)
    _sql = provider.get('get_report.sql', year=year, month=month)
    print("sql =", _sql)
    status, dict_ = select_line(db_config, _sql)
    if status:
        print(status, dict_)
        return ReportInfoResponse((dict_,), 
                                  error_message='Отчёт для указанных данных уже существует', 
                                  status=True)
    return ReportInfoResponse((dict_,), error_message='', status=False)
    

def create_new_report(db_config, user_input_data):
    year, month = [int(el) for el in user_input_data['year_month'].split('-')]
    status = stored_procedure(db_config, 'create_popularity_report', year, month)
    if not status:
        return ReportInfoResponse(tuple(), 'Something went wrong', False)
    return ReportInfoResponse(tuple(), '', True)


def get_report_orders_db(db_config, user_input_data):
    year, month = [int(el) for el in user_input_data['year_month'].split('-')]
    _sql = provider.get('get_report.sql', year=year, month=month)
    print("sql =", _sql)
    result, schema_or_error = select_list(db_config, _sql)
    print(result)
    if not result:
        return ReportInfoResponse(tuple(result), 
                                  error_message=f'Отчёт не найден. {schema_or_error}', 
                                  status=False)
    return ReportInfoResponse((result, schema_or_error), error_message=f'', status=True)
