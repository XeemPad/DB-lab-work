from flask import Blueprint, render_template, current_app, request
from access import login_required
from query.model_route import get_prods_from_db
from auth.auth import check_authorization

from database.sql_provider import SQLProvider
import os
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

query_blueprint = Blueprint(
    'query_blueprint',
    __name__,
    template_folder='templates'
)


@query_blueprint.route('/', methods=['GET'])
@login_required
def request_products():
    return render_template("input_category.html", auth_msg=check_authorization()[0])

@query_blueprint.route('/', methods=['POST'])
@login_required
def output_products():
    request_data = request.form
    res_info = get_prods_from_db(current_app.config['db_config'], request_data, provider)
    print("Products from db:", res_info.result)
    if res_info.status:
        prod_title = f'Продукты из категории "{request_data['prod_category']}"'
        return render_template("dynamic_out.html", prod_title=prod_title,
                               products=res_info.result, auth_msg=check_authorization()[0])
    else:
        return render_template("error.html", error_title='Нет результатов', 
                               error_msg=res_info.error_message, auth_msg=check_authorization()[0])
