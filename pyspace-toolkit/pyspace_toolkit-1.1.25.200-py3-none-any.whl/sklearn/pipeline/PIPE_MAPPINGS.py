# %%
import pyspace


from pyspace.sklearn.core.transformer.common_transformers import pdSeriesTransformer
from pyspace.sklearn.core.transformer.common_transformers import pdValuesTransformer
from pyspace.sklearn.core.transformer.common_transformers import npFloat64Transformer
from pyspace.sklearn.core.transformer.common_transformers import DenseTransformer
from pyspace.sklearn.core.transformer.common_transformers import IdentityTransformer
    
from pyspace.sklearn.core.transformer.text_transformers import TokenizerTransformer
from pyspace.sklearn.core.transformer.text_transformers import TokenTransformer
from pyspace.sklearn.core.transformer.text_transformers import SentenceTransformer
    
from pyspace.sklearn.core.transformer.text_transformers import WordvectorTransformer
from pyspace.sklearn.core.transformer.text_transformers import WordvectorDiscreteTransformer

from pyspace.sklearn.core.transformer.text_transformers import SupervisedMergedTfidfTransformer
from pyspace.sklearn.core.transformer.text_transformers import SupervisedCdfidfTransformer
    
from pyspace.sklearn.core.model.custom_classifier import LinearSVCExtended
    
from pyspace.sklearn.core.model.custom_cluster import AgglomerativeClusteringThreshold
    
from pyspace.sklearn.core.model.custom_classifier import HierarchicalClassifierExtended

# %%
import sklearn

# %%
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# %%
from sklearn.decomposition import PCA, TruncatedSVD

# %%
from sklearn.svm import LinearSVC

# %%
from sklearn.cluster import AgglomerativeClustering

# %%
PIPE_MAPPINGS = {
    'pdseries':  pdSeriesTransformer,
    'pdvalues':  pdValuesTransformer,
    'npfloat64':  npFloat64Transformer,
    'toarray':  DenseTransformer,
    'identity':  IdentityTransformer,
    
    'tokenize':  TokenizerTransformer,
    'ontoken':  TokenTransformer,
    'onsent':  SentenceTransformer,
    
    'wordvector':  WordvectorTransformer,
    'discrete':  WordvectorDiscreteTransformer,

    'onehot': OneHotEncoder,
    'tfidf': TfidfVectorizer,
    'tf': CountVectorizer,
    'mtfidf':  SupervisedMergedTfidfTransformer,
    'cdfidf':  SupervisedCdfidfTransformer,
    
    'pca': PCA,
    'tsvd': TruncatedSVD,
    
    'lsvm': LinearSVC,
    'lsvm+':  LinearSVCExtended,
    
    'agg+':  AgglomerativeClusteringThreshold,
    'agg': AgglomerativeClustering,
    
    'hierarchic':  HierarchicalClassifierExtended,
}

# %%
try:
    import lightgbm
    PIPE_MAPPINGS['lgbm'] = lightgbm.LGBMClassifier
except:
    pass

# %%
try:
    import xgboost
    PIPE_MAPPINGS['xgb'] = xgboost.XGBClassifier
except:
    pass
