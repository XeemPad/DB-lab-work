SELECT login 
FROM internal_user 
WHERE login = '$login'

UNION ALL

SELECT login
FROM external_user
WHERE login = '$login';