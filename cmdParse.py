"""
This module handles interfacing with the command line and calling dirWalk,
it also handles the output, including calling plotly to graph
"""
import sys, getopt, dirWalk, fileSearch



def main():
    helpstring = """
    Subdirectory Search
    
    options
    -d directory to recursively search, defaults to current directory if none is supplied
    -k keyword to search all files within directory for (regex is supported, include quotes)
    -v verbose
    """
    
    try:
        opts,args = getopt.getopt(sys.argv[1:], 'd:k:hgv', ["verbose","directory", "keyword","help"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
        
    
    graph = False
    verbose = False
    d = None
    k = None
    for opt, arg in opts:
        if opt in ('-v','--verbose'):
            verbose = True
        elif opt in ('-d','--directory'):
            d = arg
        elif opt in ('-k','--keyword'):
            k = arg
        elif opt == '-g':
            try:
                import plotly 
                import plotly.graph_objs as go
                graph = True
            except:
                print("Please install plotly to enable graphing: 'pip install plotly --upgrade'")
                graph = False
        elif opt in ('-h', '--help'):
            print helpstring 
            exit()
        else:
            assert False, "Option {} not supported".format(opt)
    if not d :
        d = "." #default to current directory if none is supplied
    if not k :
        print "Command Requires regex keyword to search for, please include an argument -k"
        exit(2)

    walker = dirWalk.dirWalk(fileSearch.fileSearch(verbose), verbose)
    walker.setDirectory(d)
    walker.setKeyword(k)

            
    validateKeyword(walker)
    validateDir(walker)
    
    print "starting search..."
    results = walker.walkDir()
    print results
    if(graph):
        if(len(results) <= 50): #extract this number out to a config file later
            subdirs = []
            count = []
            for subdir in results:
                subdirs.append(subdir)
                count.append(results[subdir])
            
            data = [go.Bar(
            x=subdirs, 
            y=count,
            text = subdirs
            )]
            layout = go.Layout(title = 'Directory: {} Keyword: {} count found'.format(walker.getDirectory(),walker.getKeyword()))
            fig = go.Figure(data = data, layout = layout)
            try:
                plotly.offline.plot(fig)
            except:
                print "Unable to render graph"
        else:
            print "Too many subdirectories to render in graph"
            
def validateDir(walker):
    if walker.validateDir():
        return
    else:
        print "The following is not a valid directory: {}. Exiting.".format(walker.getDirectory())
        exit()
        
def validateKeyword(walker):
    if walker.validateKey():
        return 
    else:
        print "The following is not a valid keyword: {}. Exiting.".format(walker.getKeyword())
        exit()

if __name__ == "__main__":
    main()