import shutil, os
if not os.path.exists(os.path.join(os.getcwd(),"assets")):
    shutil.copytree(os.path.join(os.path.dirname(os.path.realpath(__file__)),"templates/assets"),os.path.join(os.getcwd(),"assets"))
def main():
    import sys
    from cvdastwrapper import fuzzallspecs
    from cvdastwrapper import runall
    
    #print(sys.argv[1:], "argv")
    if sys.argv[1:]:
        if "--generate-tests" in sys.argv[1:]:
            #print(sys.argv)
            fuzzallspecs.fuzzspecs()
            return
    runall.main()
    
        
if __name__ == "__main__":
    # execute only if run as a script
    main()
        