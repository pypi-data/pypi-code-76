# %%
from sklearn.model_selection import ParameterGrid

from sklearn.pipeline import Pipeline, FeatureUnion

import copy

import itertools

# %%
from pyspace.sklearn.core.transformer.common_transformers import *


# %% [markdown]
# ### Compose Models and Pipelines

# %%
def compose_modelkey(modelbasekey, modelparams, key_exclude_grid = {'models':[], 'modelparams':{}}):
    
    if("estimator" in modelparams):
        modelparams = {'estimator': modelparams['estimator']._key,
                       **{x: modelparams[x] for x in modelparams if x != 'estimator'}}
        
    if(modelbasekey in key_exclude_grid['modelparams']):
        modelparams = {x:modelparams[x] for x in modelparams if x not in key_exclude_grid['modelparams'][modelbasekey]}

    key = modelbasekey + str(modelparams).replace(" ","").replace("'","").replace("{}","")
    
    return key

def compose_modelgrid(PIPE_MAPPINGS, model_grid_abstract, key_exclude_grid = {'models':[], 'modelparams':{}}):
    
    pipes = []
    for modelbasekey in model_grid_abstract:
        modelparams = model_grid_abstract[modelbasekey]
        if("estimator" in modelparams):
            modelparams = {'estimator': compose_modelgrid(PIPE_MAPPINGS, modelparams['estimator']),
                           **{x: modelparams[x] for x in modelparamsa if x != 'estimator'}}
        
        paramgrid = list(ParameterGrid(modelparams))
        for params in paramgrid:
            pipes.append((modelbasekey, params))
            
    result = []
    
    for pipe in pipes:
        
        model = PIPE_MAPPINGS[pipe[0]](**pipe[1])
        key = compose_modelkey(pipe[0], pipe[1], key_exclude_grid)
        setattr(model, "_key", key)
        
        result.append(model)
        
    return result


# %%
def product_pipegrid(PIPE_MAPPINGS, base_pipelines={}, model_grid_abstract={}, include_base=True, key_exclude_grid = {'models':[], 'modelparams':{}}):
    
    if base_pipelines == {}:
        empty_pipeline = Pipeline([('identity', IdentityTransformer())]); empty_pipeline.steps.pop(0)
        base_pipelines = {'':empty_pipeline}
        
    result = {}
    if include_base:
        result = {**result, **base_pipelines}
        
    pipemodels = compose_modelgrid(PIPE_MAPPINGS, model_grid_abstract, key_exclude_grid)
    
    for base_pipeline_key in base_pipelines:
        for pipemodel in pipemodels:
            
            pipeline = copy.deepcopy(base_pipelines[base_pipeline_key])
            
            if(pipemodel._key == 'identity'):
                result[base_pipeline_key] = pipeline
                continue
            
            pipemodel = copy.deepcopy(pipemodel)
            pipeline.steps.append((pipemodel._key, pipemodel))
            
            pipeline_key = "_".join([step[0] for step in pipeline.steps if step[0] != '' and step[0] not in key_exclude_grid['models']])
            
            result[pipeline_key] = pipeline
            
    return result

def union_pipegrid(base_pipelines, additional_pipelines, include_base = True):
    
    if base_pipelines == {}:
        empty_pipeline = Pipeline([('identity', IdentityTransformer())]); # empty_pipeline.steps.pop(0)
        base_pipelines = {'':empty_pipeline}
        
    
    result = {}
    if include_base:
        result = {**result, **base_pipelines}
    for pipe1_key in base_pipelines:
        for pipe2_key in additional_pipelines:
            
            pipe1 = base_pipelines[pipe1_key]
            pipe2 = additional_pipelines[pipe2_key]
            
            key1 = "_".join([pipe[0] for pipe in pipe1.steps])
            key2 = "_".join([pipe[0] for pipe in pipe2.steps])
            unionkey = 'union_:_'+key1+'_&_'+key2+'#'
            
            pipeline1 = copy.deepcopy(pipe1)
            pipeline2 = copy.deepcopy(pipe2)
            
            pipeline = Pipeline( [(unionkey, FeatureUnion( [(key1,pipeline1), (key2,pipeline2)]))])
            pipeline_key = "_".join([step[0] for step in pipeline.steps])
            
            result[pipeline_key] = pipeline
            
    return result


# %% [markdown]
# ### Pipeline Generation from Config Dictionary

# %%
def generate_pipegrid_pandas(PIPE_MAPPINGS, dataconfig, key_exclude_grid):
    
    datatransformers = []
    for columngrid in dataconfig:
        
        columntransformers = {}
        for grid in columngrid[1]:
            columntransformers = product_pipegrid(PIPE_MAPPINGS, columntransformers, grid, include_base=False, key_exclude_grid=key_exclude_grid)
            
        columnsstr = ''.join(columngrid[0])
        columntransformers = [ ( columnsstr + '_' + key if key != '' else columnsstr, 
                                 Pipeline(steps=[
                                     ('colselection', pdColumnSelector(columngrid[0])),
                                     ('colprocess', columntransformers[key]),
                                 ])
                               ) for key in columntransformers]
        datatransformers.append(columntransformers)
        
    datatransformers = list(itertools.product(*datatransformers))
    datatransformers = copy.deepcopy(datatransformers)
    
    pipelines ={}
    for columntransformers in datatransformers:
        pipekey = '<'+'&'.join([transformer[0] for transformer in columntransformers]) + '>'
        pipelines[pipekey] = Pipeline([ (pipekey, FeatureUnion(columntransformers))])
    
    return pipelines
        
def generate_pipegrid_numpy():
    pass
def generate_pipegrid_fork_merge():
    pass

def generate_pipegrid(PIPE_MAPPINGS, pipegrid, key_exclude_grid={'models':['pdvalues','pdseries','npfloat64','toarray'], 'modelparams':{'tfidf':['tokenizer','preprocessor']}}):

    pipelines = {}
    
    for grid in pipegrid:
        
        if('pandas' in grid):
            pipelines = generate_pipegrid_pandas(PIPE_MAPPINGS, grid['pandas'], key_exclude_grid)
            
        else:
            pipelines = product_pipegrid(PIPE_MAPPINGS, pipelines, grid, include_base=False)
            
    return pipelines


# %%
def get_X_y(dataset, mode):
    # get X and y
    
    if(str(type(dataset)) == "<class 'pyspace.sklearn.data_structure.dataset_wrapper.DatasetContainer'>"):
        
        if(mode == 'fit'):
            if(dataset.pre):
                X = dataset.pre.dfX
                y = dataset.pre.y_enc
            else:
                X = dataset.train.dfX
                y = dataset.train.y_enc
                
        elif(mode == 'transform'):
            X = dataset.train.dfX
            y = dataset.train.y_enc
            
        elif(mode == 'fit_transform'):
            X = dataset.train.dfX
            y = dataset.train.y_enc
        
    else:
        if(len(dataset) == 2):
            X = dataset[0]
            y = dataset[1]
        elif(len(dataset) == 1):
            X = dataset[0]
            y = None
        else:
            X = dataset
            y = None
            
    return X, y

def fit_pipegrid(pipelines, dataset):
    
    # get X and y
    X, y = get_X_y(dataset, mode='fit')

    print("pipeline fit")
    print("pipeline count", len(pipelines))
    count = 0
    
    # dataspace = {}
    pkeys = list(pipelines.keys())
    for pkey in pkeys:
        count += 1
        print(cound, end=' ')
        
        try:
            # get pipeline
            pipeline = pipelines[key]
            
            # pipeline fit
            pipeline.fit(X,y)
            
            print(' '*len('FAILED'), end=' ')
        except Exception as e:
            print(e)
            print('FAILED', end=' ')
            del pipelines[pkey]
        finally:
            print(pkey)
            
def transform_pipegrid(pipelines, dataset):
    
    # get X and y
    X, y = get_X_y(dataset, mode='transform')
    
    print("pipeline transform")
    print("pipeline count", len(pipelines))
    count = 0
    
    dataspace = {}
    pkeys = list(pipelines.keys())
    for pkey in pkeys:
        count += 1
        print(count, end=' ')
        
        try:
            # get pipeline
            pipeline = pipelines[pkey]
            
            # pipeline transform train
            datadict = {
                'dfX' : X,
                'X' : pipeline.transform(X),
                'y' : y,
            }
            
            # set result
            dataspace[pkey] = datadict
            
            print(' '*len('FAILED'), end=' ')
        except Exception as e:
            print(e)
            print('FAILED', end=' ')
            # del pipelines[pkey]
        finally:
            print(pkey)
            
    return dataspace

def fit_transform_pipegrid(pipelines, dataset):
    
    # get X and y
    X, y = get_X_y(dataset, mode='fit_transform')
    
    print("pipeline_fit_transform")
    print("pipeline count",len(pipelines))
    count = 0
    
    dataspace = {}
    pkeys = list(pipelines.keys())
    for pkey in pkeys:
        count += 1
        print(count, end=' ')
        
        try:
            # get pipeline
            pipeline = pipelines[pkey]
            
            # pipeline transform train
            datadict = {
                'dfX': X,
                'X': pipeline.fit_transform(X, y),
                'y':y,
            }
            
            # set result
            dataspace[pkey] = datadict
            
            print(' '*len('FAILED'), end=' ')
        except Exception as e:
            print(e)
            print('FAILED', end=' ')
            del pipelines[pkey]
        finally:
            print(pkey)
            
    return dataspace

