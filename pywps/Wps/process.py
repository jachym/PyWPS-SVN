# Licence: GNU/GPL
# Author: Jachym Cepicky 2007
#         jachym.cepicky gmail com
#         http://les-ejk.cz


class WPSProcess:
    def __init__(self, Identifier = '', processVersion="1.0", Title="",
            Abstract="", statusSupported="false", storeSupported="false"):
        self.Identifier = Identifier
        self.processVersion = processVersion
        self.Title = Title
        self.Abstract = Abstract
        self.statusSupported=statusSupported
        self.storeSupported=statusSupported
        self.Inputs = []
        self.Outputs = []

    def AddLiteralInput(self, Identifier, Title=None, Abstract=None,
            UOMs="m", MinimumOccurs=1, allowedvalues=("*"), type=type(""), value=None):
        """Add new input item of type LiteralValue to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        if not UOMs: 
            UOMs = "m"

        if not allowedvalues: 
            allowedvalues = ("*")

        if not MinimumOccurs:
            MinimumOccurs = 1

        if not type:
            type = type("")

        while 1:
            if self.GetInput(Identifier):
                Identifier += "-1"
            else:
                break

        self.Inputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "LiteralValue": {"UOMs":UOMs,
                                             "values":allowedvalues},
                            "MinimumOccurs": MinimumOccurs,
                            "dataType":type,
                            "value": value
                            })
        return self.Inputs[-1]

    def AddComplexInput(self, Identifier, Title=None, Abstract=None,
            Formats=["text/xml"], value=None):
        """Add new input item of type ComplexValue to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetInput(Identifier):
                Identifier += "-1"
            else:
                break

        if type(Formats) != type([]):
            Formats = [Formats]

        self.Inputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "ComplexValue": {"Formats":Formats},
                            "value": value
                            })

        return self.Inputs[-1]

    def AddBBoxInput(self, Identifier, Title=None, Abstract=None, value=[]):
        """Add new input item of type BoundingBox to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        if type(value) != type([]):
            value = str(value).split()

        if len(value) < 4:
            for i in range(4-len(value)):
                value.append(0.0)

        while 1:
            if self.GetInput(Identifier):
                Identifier += "-1"
            else:
                break


        self.Inputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "BoundingBoxValue": {},
                            "value": value
                            })

        return self.Inputs[-1]

    def AddLiteralOutput(self, Identifier, Title=None, Abstract=None,
            UOMs="m", value=None):
        """Add new output item of type LiteralValue to this process"""


        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        if not UOMs: 
            UOMs = "m"

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break
        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "LiteralValue": {"UOMs":UOMs,},
                            "value": value
                            })
        return self.Outputs[-1]


    def AddComplexValueOutput(self, Identifier, Title=None, Abstract=None,
            Formats=["text/xml"], value=None):
        """Add new output item of type ComplexValue to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break

        if type(Formats) != type([]):
            Formats = [Formats]

        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "ComplexValue": {"Formats":Formats},
                            "value": value
                            })

        return self.Outputs[-1]

    def AddComplexValueReferenceOutput(self, Identifier, Title=None, Abstract=None,
            Formats=["text/xml"], value=None):
        """Add new output item of type ComplexValueValueReference to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break
        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "ComplexValueReference": {"Formats":Formats},
                            "value": value
                            })


    def AddBBoxOutput(self, Identifier, Title=None, Abstract=None, value=[]):
        """Add new output item of type BoundingBoxOutput to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break

        if len(value) < 4:
            for i in range(4-len(value)):
                value.append(0.0)

        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "BoundingBoxValue": {},
                            "value": value
                            })

        return self.Outputs[-1]

    def GetInput(self,Identifier):
        """Returns input of defined identifier"""
        retinpt = None

        for inpt in self.Inputs:
            if inpt["Identifier"] == Identifier:
                retinpt = inpt
        return retinpt

    def GetOutput(self,Identifier):
        """Returns output of defined identifier"""
        retoupt = None

        for oupt in self.Outputs:
            if oupt["Identifier"] == Identifier:
                retoupt = oupt
        return retoupt

    def GCmd(self,cmd,stdin=None):
        """Runs GRASS command, fetches all GRASS_MESSAGE and
        GRASS_PERCENT messages and sets self.status according to them, so
        the client application can track the progress information, when
        runing with Status=True

        This module is supposed to be used instead of 'os.system()', while
        running GRASS modules
        
        Example Usage:
            self.GCmd("r.los in=elevation.dem out=los coord=1000,1000")

            self.GCmd("v.net.path network afcol=forward abcol=backward \
            out=mypath nlayer=1","1 9 12")
            """

        
        os.environ["GRASS_MESSAGE_FORMAT"] = "gui"

        (module_stdin, module_stdout, module_stderr) = os.popen3(cmd)

        os.environ["GRASS_MESSAGE_FORMAT"] = "text"
       
        if stdin:
            module_stdin.write(stdin)
        module_stdin.close()

        line = module_stderr.readline()
        while 1:
            if not line:
                break
            line = line.strip()
            #-----
            try:
                format,content = line.split(":")
                if format =="GRASS_PERCENT":
                    self.SetStatus(percent=percent)
                else:
                    self.SetStatus(content)
            except:
                self.SetStatus(line)
            #-----
            line = module_stderr.readline()
        return