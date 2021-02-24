from tensorflow.keras.preprocessing.sequence import pad_sequences


class xPadder:
    
    def __init__(self, maxlen, value):
        self.maxlen = maxlen
        self.value = value
        
    def pad(self, tokenizedlist):
        return pad_sequences(tokens, maxlen = self.maxlen, padding='post', value=self.value)
