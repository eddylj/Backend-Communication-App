'''
error
'''
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    '''
    AccessError
    '''
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    '''
    InputError
    '''
    code = 400
    message = 'No message specified'
