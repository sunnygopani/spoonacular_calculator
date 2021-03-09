class Exceptions:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def get_error_object(self):
        return {'status': False, 'error_code': self.code, 'error_message': self.message.lower(), "data": ""}
