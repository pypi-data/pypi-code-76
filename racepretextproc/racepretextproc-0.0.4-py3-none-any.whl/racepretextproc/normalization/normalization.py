from textblob import TextBlob

class normalization:
    '''Normalization class'''

    def __init__(self,df,exclusion=[]):
        self.df=df
        self.originaldf=df #keep in memory original data for direct method call
        self.exclusion= exclusion    
   
    def spellcorr(self,call):
        '''Function uses TextBlob to auto correct spelling errors'''

        if (call!=0): # call from wrapper script
            text=self.df#getting text from the class variable
            val=" ".join([str(TextBlob(x).correct()) for x in text.split(' ')])
            self.df=val
        else:# call from main class method
            text=self.originaldf#getting text from the class variable
            val=" ".join([str(TextBlob(x).correct()) for x in text.split(' ')])
        return val
    def normalizmain(self,spellcorr=True):
        '''Main normalization function to call sub funtions'''

        if spellcorr:
            val=self.spellcorr(2)  # pass anything other than 0 for wrapper call 
        #val=self.df
            return val
