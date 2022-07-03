from rest_framework import status as _status_

def ResponseSuccess(message, status):
    response = {
        'code': 'success',
        'status': status,
        'message': message,
    }
    return response

def ResponseError(message, status=_status_.HTTP_400_BAD_REQUEST):
    response = {
        'code': 'error',
        'status': status,
        'message': message,
    }
    return response


