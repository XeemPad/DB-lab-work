from flask import Blueprint, render_template, current_app, request
from access import login_required
from auth.auth import check_authorization

from database.sql_provider import SQLProvider
import os
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

report_blueprint = Blueprint(
    'report_bp',
    __name__,
    template_folder='templates'
)


@report_blueprint.route('/', methods=['GET'])
@login_required
def create_report_orders():
    return render_template("create_report.html", 
                           auth_msg=check_authorization()[0])


@report_blueprint.route('/', methods=['GET'])
@login_required
def get_report_orders():
    return render_template("dynamic_report.html", 
                           auth_msg=check_authorization()[0])
