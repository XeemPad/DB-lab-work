import re
from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from auth.model_route import model_route_auth_request, model_route_reg_exist_check, model_route_reg_new
from auth.auth import check_authorization


blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_auth.route('/', methods=['GET'])
def auth_index():
    info = session.pop('info', default='')
    return render_template('login.html', info=info,
                           auth_msg=check_authorization()[0])


@blueprint_auth.route('/', methods=['POST'])
def auth_main():
    user_data = request.form
    res_info = model_route_auth_request(current_app.config['db_config'], user_data, provider)
    print(res_info)
    if not res_info.status:
        print('Ошибка авторизации:', res_info.error_message)
        return render_template('auth_error.html', error_title='Не удалось войти', 
                               error_msg='Неверный логин или пароль', auth_msg=check_authorization()[0])

    session['login'] = res_info.result[0]['login']
    session['user_group'] = res_info.result[0]['user_group']
    user_id = res_info.result[0]['user_id'] if 'user_id' in res_info.result[0] \
        else res_info.result[0]['extuser_id']
    session['user_id'] = str(user_id)
    print(f'User with user_id {session['user_id']} ({session['user_group']}) authorized')


    if 'next' in session:
        prev_url = session['next']
        if prev_url:
            session.pop('next')
            return redirect(prev_url)
    return redirect(url_for('main_menu'))

@blueprint_auth.route('/registration', methods=['GET'])
def registration_index():
    return render_template('registration.html', auth_msg=check_authorization()[0])

@blueprint_auth.route('/registration', methods=['POST'])
def registration_main():
    user_data = request.form
    res_info = model_route_reg_exist_check(current_app.config['db_config'], user_data, provider)
    print(res_info)
    if res_info.status:
        return render_template('auth_error.html', error_title='Не удалось зарегистрироваться', 
                               error_msg="Такой пользователь уже существует", auth_msg=check_authorization()[0])

    if user_data['password'] != user_data['password_verify']:
        return render_template('auth_error.html', error_title='Не удалось зарегистрироваться', 
                               error_msg="Пароли не совпадают", auth_msg=check_authorization()[0])
    res_info = model_route_reg_new(current_app.config['db_config'], user_data, provider)
    if not res_info.status:
        return render_template('auth_error.html', error_title='Не удалось зарегистрироваться', 
                               error_msg=res_info.error_message, auth_msg=check_authorization()[0])

    print("Регистрация успешна")

    return render_template('reg_success.html', auth_msg=check_authorization()[0])
