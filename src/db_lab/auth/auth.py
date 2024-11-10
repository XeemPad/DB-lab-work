from flask import session


def check_authorization():
    if 'user_group' in session:
        user_group = session.get('user_group')
        user_login = session.get('login')
        message = f'Вы авторизованы как {user_login} ({user_group})'
        return message, True
    return 'Вы не авторизованы', False