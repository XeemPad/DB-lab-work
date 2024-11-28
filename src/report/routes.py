from os import error
from flask import Blueprint, render_template, current_app, request
from access import group_required
from auth.auth import check_authorization
from report.model_route import check_report_exists, create_new_report, \
    get_report_orders_db, ReportInfoResponse


report_blueprint = Blueprint(
    'report_bp',
    __name__,
    template_folder='templates'
)


@report_blueprint.route('/create', methods=['GET'])
@group_required
def request_report_orders():
    ''' Page with a form for user to input desired period '''
    return render_template("create_report.html", 
                           auth_msg=check_authorization()[0])


@report_blueprint.route('/create', methods=['POST'])
@group_required
def create_report_orders():
    ''' Function that invokes the creation of report in DB '''
    request_data = request.form
    # Check whether report for such data already exists
    exist_info: ReportInfoResponse = check_report_exists(current_app.config['db_config'], 
                                                         request_data)
    if exist_info.status:  # if exists
        return render_template("report_status.html", 
                               status_title='Отчёт на данный период уже существует',
                               status_msg=exist_info.error_message,
                               auth_msg=check_authorization()[0])
    
    # Execute procedure:
    res_info: ReportInfoResponse = create_new_report(current_app.config['db_config'], 
                                                     request_data)
    if res_info.status:
        return render_template("report_status.html", status_title='Отчёт успешно создан',
                                auth_msg=check_authorization()[0])
    return render_template("report_status.html", status_title='Отчёт не был создан',
                            status_msg=res_info.error_message,
                            auth_msg=check_authorization()[0])


@report_blueprint.route('/view', methods=['GET'])
@group_required
def get_report_orders():
    return render_template("get_report.html", 
                           auth_msg=check_authorization()[0])


@report_blueprint.route('/view', methods=['POST'])
@group_required
def extract_report_orders():
    ''' Function that extracts report from DB '''
    request_data = request.form
    # Check whether report for such data already exists
    exist_info: ReportInfoResponse = check_report_exists(current_app.config['db_config'], 
                                                         request_data)
    if not exist_info.status:  # if not exists
        return render_template("report_status.html", 
                               status_title='Отчёт на данный период не существует',
                               status_msg=exist_info.error_message,
                               auth_msg=check_authorization()[0])
    
    res_info: ReportInfoResponse = get_report_orders_db(current_app.config['db_config'], 
                                                        request_data)
    if not res_info.status:
        return render_template("report_status.html", 
                               status_title='Отчёт не найден',
                               status_msg=res_info.error_message,
                               auth_msg=check_authorization()[0])
    
    rows, schema = res_info.result
    if rows[0][1] == 0:  # If no orders were done that month
        return render_template("report_status.html", 
                               status_title='В данный месяц не было совершено ни одного заказа',
                               auth_msg=check_authorization()[0])
    return render_template("dynamic_report.html", 
                           table_title=f'Отчёт за {request_data['year_month']}',
                           header=schema, rows=rows,
                           auth_msg=check_authorization()[0])