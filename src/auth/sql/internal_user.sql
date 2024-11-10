SELECT
    user_id,
    login,
    user_group
FROM internal_user
WHERE 1=1
    AND login='$login'
    AND password='$password'