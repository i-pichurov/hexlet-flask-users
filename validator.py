def validate(data):
    errors = {}

    if not data['name']:
        errors['name'] = 'Имя пользователя не заполнено'
    if not data['email']:
        errors['email'] = 'Email пользователя не заполнен'
    return errors
