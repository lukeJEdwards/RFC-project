class InvalidCredentials(Exception):
    """Exception related to Invalid Credentials"""
    pass        

class RequestFailed(Exception):
    """Exception related to an Invalid Request"""
    pass
        
class MissingHost(Exception):
    """Exception related when a host is missing"""
    pass