
"""
This file will handle walking the directory and sending files over to the fileSearch module

It also will handle the collection of results from the filesearch 
"""


import os, threading

class dirWalk:
    def __init__(self, fileSearch, verbose):
        self.directory = None
        self.keyword = None
        self.matchCount = {}
        self.threads = []
        self.fs = fileSearch
        self.verbose = verbose
        self.validKey = False
        self.validDir = False
    
    def walkDir(self):
        if(self.validKey and self.validDir):
            for subdir, dirs, files, in os.walk(self.directory):
                self.matchCount[subdir] = 0
                t = threading.Thread(target=self.directoryThread, args =(files, subdir, self.matchCount))
                self.threads.append(t)
                t.start()
                if self.verbose:
                    print "thread started"
            for thread in self.threads:
                thread.join()
            return self.matchCount
        else:
            raise Exception("Validation Error, key and directory not validated before walking")
            
        
    def directoryThread(self, files, subdir, matchCount):
        for file_ in files:
            if self.fs.search(os.path.join(subdir,file_), file_):
                self.matchCount[subdir] = self.matchCount[subdir] + 1
        
    def validateDir(self):
        if(self.directory[0] == '/'):
            self.directory = self.directory[1:]
        try:
            self.validDir = os.path.isdir(self.directory)
            return self.validDir
        except:
            return False
    
    """Validates the keyword argument, 
    modifying it to be valid with regex if necessary
    returns true in current cases, 
    but left to modify if certain forms of regex or terms should be excluded"""
    def validateKey(self):
        #currently escape characters work as intended without additional filtering
        #space left here to allow for filtering and future fixes

        self.fs.setRegex(self.keyword)
        self.validKey = True
        return self.validKey
        
        
        
    def setDirectory(self, directory):
        self.directory = directory
        
    def setKeyword(self, keyword):
        self.keyword = keyword
        

    
    def getDirectory(self):
        return self.directory
        
    def getKeyword(self):
        return self.keyword

            
    