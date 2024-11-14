from http.client import ImproperConnectionState
import os

from flask import Flask, render_template, session, json
from query.routes import query_blueprint
from auth.routes import auth_blueprint
from report.routes import report_blueprint
from auth.auth import check_authorization


cur_dir = os.path.dirname(__file__)

app = Flask(__name__)
with open(os.path.join(cur_dir, "data/dbconfig.json")) as f:
    app.config['db_config'] = json.load(f)

with open(os.path.join(cur_dir, "data/db_access.json")) as f:
    app.config['db_access'] = json.load(f)
app.secret_key = 'dasecretkey'

app.register_blueprint(query_blueprint, url_prefix='/query')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(report_blueprint, url_prefix='/report')


@app.route('/')
def main_menu():
    auth_msg, auth_status = check_authorization()
    return render_template('main_menu.html', auth_status=auth_status, auth_msg=auth_msg)


@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('error.html', error_title='Вы вышли из аккаунта', 
                           auth_msg=check_authorization()[0])


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
