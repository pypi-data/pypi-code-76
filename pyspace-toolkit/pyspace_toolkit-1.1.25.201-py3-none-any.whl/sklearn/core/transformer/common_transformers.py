# %%
from sklearn.base import TransformerMixin, BaseEstimator


# %%
class IdentityTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, input_array, y=None):
        return self
    
    def transform(self,input_array,y=None):
        return input_array
    
class DenseTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, input_array, y=None):
        return self
    
    def transform(self,input_array,y=None):
        return input_array.toarray()




# %%
class pdSeriesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, input_array, y=None):
        return self
    
    def transform(self,input_array,y=None):
        return input_array[input_array.columns[0]]
    

class pdValuesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, input_array, y=None):
        return self
    
    def transform(self,input_array,y=None):
        return input_array.values


class npFloat64Transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, input_array, y=None):
        return self
    
    def transform(self,input_array,y=None):
        return input_array.astype('float64')


# %%

class pdColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X, y=None):
        return self
    
    def transform(self,X,y=None):
        return X[self.columns]
