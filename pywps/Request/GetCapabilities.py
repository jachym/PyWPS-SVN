from pywps.Request import Request

class GetCapabilities(Request):
    """GetCapabilites request class

    .. attribute:: language
    .. attribute:: acceptedVersions
    .. attribute:: service
    .. attribute:: request
    """

    acceptVersions = None
    request = None

    def __init__(self,request,method):
        Request.__init__(self,request,method)

        self.request = "getcapabilities"

    def _parseRequestPOST(self,request):
        """Parse request via POST method"""
        pass

    def _parseRequestGET(self,qs):
        """Parse request via GET method
        
        :param qs: dictionary
        """

        for i in qs.iterkeys():
            lowI = i.lower()
            if lowI == "language":
                self.language = qs[i][0].lower()
            elif lowI == "acceptversions":
                self.acceptVersions = qs[i]
            elif lowI == "service":
                self.service = qs[i][0].lower()
            elif lowI == "request":
                self.request = qs[i][0].lower()
        pass
