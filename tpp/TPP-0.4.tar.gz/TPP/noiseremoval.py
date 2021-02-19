''' Noise removal class 
    Input = text array []
    Class : noiseremoval(txt,v)
            txt = text array
            v = any exclusions
    Methods: lowercase()
             whitespc() 
             noisewrap() - wrapper for both methods
'''
import re
class noiseremoval:
    def __init__(self,df,exclusion=[]):
        self.df=df
        self.originaldf=df #keep in memory original data for direct method call
        self.exclusion= exclusion

    def lowercase(self,call=0):
        if (call!=0):
            text=self.df #getting text from the class variable
            val=["".join(x.lower()) for x in text]
            self.df=val #reseting pocessed text
        else:
            text=self.originaldf #getting original text from the class variabl
            val=["".join(x.lower()) for x in text]
            
        return val
    def whitespc(self,call=0):
        if (call!=0): # call from wrapper script
            text=self.df#getting text from the class variable
            val=["".join(re.sub('[\s]+','',x)) for x in text]
            self.df=val
        else:# call from main class method
            text=self.originaldf#getting original text from the class variable
            val=["".join(re.sub('[\s]+','',x)) for x in text]
            
        return val
    #wrappe class calling all methods
    def noisewrap(self):
        val=self.lowercase(2) # pass anything other than 0 for wrapper call
        val=self.whitespc(2)  # pass anything other than 0 for wrapper call 
        #val=self.df
        return val