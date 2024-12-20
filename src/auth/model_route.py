from dataclasses import dataclass
from database.select import insert, select_line
from hashlib import sha256


@dataclass
class UserInfoResponse:
    result: dict | str
    error_message: str
    status: bool


def model_route_auth_request(db_config, user_input_data, sql_provider):
    if 'is_internal' in user_input_data:  # if user trying to login as internal
        sql_file = 'internal_user.sql'
    else:
        sql_file = 'external_user.sql'
    encrypted_password = hash_password(user_input_data['password'])

    _sql = sql_provider.get(sql_file, login=user_input_data['login'], 
                            password=encrypted_password)
    
    status, dict_ = select_line(db_config, _sql)
    print(f'result: {dict_}')
    if status:
        return UserInfoResponse(dict_, error_message='', status=True)
    return UserInfoResponse(dict_, error_message=f'No user found using query:\n{_sql}. {dict_}', 
                            status=False)


def model_route_reg_exist_check(db_config, user_input_data, sql_provider):
    _sql = sql_provider.get('check_user.sql', login=user_input_data['login'])

    status, dict_ = select_line(db_config, _sql)
    if status:
        return UserInfoResponse(dict_, error_message='', status=True)
    return UserInfoResponse(dict_, error_message=f'No user found using query:\n{_sql}. {status}', 
                            status=False)


def model_route_reg_new(db_config, user_input_data, sql_provider):
    newuser_group = 'buyer'  # buyer by default. Could add supplier?
    encrypted_password = hash_password(user_input_data['password'])

    _sql = sql_provider.get('create_extuser.sql',
                            login=user_input_data['login'],
                            password=encrypted_password,
                            group=newuser_group)
    status, result = insert(db_config, _sql)
    if status:
        return UserInfoResponse(dict(), error_message='', status=True)
    return UserInfoResponse(dict(), error_message=f'No user found using query:\n{_sql}. {result}',
                            status=False)


def hash_password(password: str):
    # Ideally should not be sha256
    return sha256(str(password).encode()).hexdigest()