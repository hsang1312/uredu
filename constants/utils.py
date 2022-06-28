def ResponseSuccess(message, status):
    response = {
        'code': 'success',
        'status': status,
        'message': message,
    }
    return response
