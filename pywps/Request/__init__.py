__all__ = ["GetCapabilities"]

class Request:
    """WPS Request class"""

    language = None
    service = None
    request = None

    def __init__(self,request,method):

        if method == "POST":
            self._parseRequestPOST(request)

        else:

            try:
                from urlparse import parse_qs
            except ImportError:
                from urllib.parse import parse_qs

            qs = parse_qs(request)
            self._parseRequestGET(qs)

    def _parseRequestPOST(self,request):
        """Parse request via POST method"""
        pass

    def _parseRequestGET(self,request):
        """Parse request via GET method"""
        pass

def getRequestTypePOST(request):
    """Returns proper request instance based on request comming via 
    HTTP POST method

    :param request: XML request
    :type request: String
    """
    pass

def getRequestTypeGET(request):
    """Returns proper request instance based on request comming via 
    HTTP GET method

    :param request: URL string
    :type request: String
    """
    pass
