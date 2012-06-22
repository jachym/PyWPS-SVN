__all__ = ["GetCapabilities","DescribeProcess"]
NSMAP = {
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xlink': 'http://www.w3.org/1999/xlink',
        'ows': 'http://www.opengis.net/ows/1.1',
        'wps': 'http://www.opengis.net/wps/1.0.0'
}

class Request:
    """WPS Request class

    .. attribute:: language
    .. attribute:: service
    .. attribute:: request
    .. attribute:: validate
    """

    language = None
    service = None
    request = None
    validate = False

    def __init__(self,request,method):

        if method == "POST":
            try:
                from lxml import etree
            except ImportError:
                import xml.etree.ElementTree as etree

            parser = etree.XMLParser(ns_clean = True,
                                    # TODO huge_tree,
                                    # ...
                                    )
            self._parseRequestPOST(etree.fromstring(request,parser))

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
