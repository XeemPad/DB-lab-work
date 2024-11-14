from dataclasses import dataclass
from database.select import insert, select_line
from hashlib import sha256


@dataclass
class UserInfoResponse:
    result: tuple
    error_message: str
    status: bool


def model_route_auth_request(db_config, user_input_data, sql_provider):
    error_message = ''
    encrypted_password = hash_password(user_input_data['password'])
    _sql = sql_provider.get('internal_user.sql', login = user_input_data['login'], 
                            password=encrypted_password)
    result = tuple([select_line(db_config, _sql)])
    print(f'result: {result[0]}')
    if result[0]:
        return UserInfoResponse(result, error_message=error_message, status=True)
    return UserInfoResponse(result, error_message=f'No user found using query:\n{_sql}', status=False)


def model_route_reg_exist_check(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('check_user.sql', login=user_input_data['login'])
    result = tuple([select_line(db_config, _sql)])
    if result[0]:
        return UserInfoResponse(result, error_message=error_message, status=True)
    return UserInfoResponse(result, error_message=error_message, status=False)


def model_route_reg_new(db_config, user_input_data, sql_provider):
    error_message = ''
    newuser_group = 'buyer'  # buyer by default. Could add supplier?
    encrypted_password = hash_password(user_input_data['password'])
    _sql = sql_provider.get('create_extuser.sql',
                            login=user_input_data['login'],
                            password=encrypted_password,
                            group=newuser_group)
    result = insert(db_config, _sql)
    if result:
        return UserInfoResponse(tuple(), error_message=error_message, status=True)
    return UserInfoResponse(tuple(), error_message='', status=False)


def hash_password(password: str):
    # Ideally should not be sha256
    return sha256(str(password).encode()).hexdigest()