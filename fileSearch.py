import re, os
class fileSearch:
    
    def __init__(self, verbose):
        #add option to turn ignorecase on or off
        self.regex = None
        self.verbose = verbose
        
    def search(self, fileName, shortName):
        #splitting new thread off here is possible
        try:
            if(os.stat(fileName).st_size > 0): #catch empty files and prevent opening them
                f = open(fileName, "r")
                content = f.read()
                match = self.regex.search(content)
                f.close()
                if match and match.group(0):
                    return True
                else:
                    return False
            else:
                return False
        except AttributeError as err:
            if self.verbose:
                print(str(err))
                print("File {} unable to be read".format(shortName))
    
    def setRegex(self, keyword):
        self.regex = re.compile(keyword, re.IGNORECASE)
        
        