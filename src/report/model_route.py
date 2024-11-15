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
    result: dict = select_line(db_config, _sql)
    if result:
        return ReportInfoResponse(tuple(result.values()), 
                                  error_message='Отчёт для указанных данных уже существует', 
                                  status=False)
    return ReportInfoResponse(tuple(), error_message='', status=True)
    

def create_new_report(db_config, user_input_data):
    year, month = [int(el) for el in user_input_data['year_month'].split('-')]
    status = stored_procedure(db_config, 'create_popularity_report', year, month)
    if not status:
        return ReportInfoResponse(tuple(), 'Status of procedure wasn\'t returned', False)
    if status.lower() == 'success':
        return ReportInfoResponse(tuple(), '', True)
    else:
        return ReportInfoResponse(tuple(), status, False)


def get_report_orders_db(db_config, user_input_data):
    year, month = [int(el) for el in user_input_data['year_month'].split('-')]
    _sql = provider.get('get_report.sql', year=year, month=month)
    print("sql =", _sql)
    result, schema = select_list(db_config, _sql)
    if not result:
        return ReportInfoResponse(tuple(result), 
                                  error_message='Отчёт не найден', 
                                  status=False)
    return ReportInfoResponse((result, schema), error_message='', status=True)
