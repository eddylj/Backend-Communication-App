'''
Echo
'''
from error import InputError

def echo(value):
    '''
    Test echo
    '''
    if value == 'echo':
        raise InputError('Input cannot be echo')
    return value
