import tensorflow as tf
import json
import numpy as np
from tqdm import tqdm
import os
import random
from string import digits 
  
    
# using translate and digits 
# to remove numeric digits from string 
_remove_digits = str.maketrans('', '', digits)

# Helperfunctions to make your feature definition more readable

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy()
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
    
_byte_types = ['bytes', 'str']
_float_types = ['float', 'cfloat', 'double']
_int64_types = ['int', 'bool', 'uint', 'enum']
        
    

def save_numpy(data:dict, file:str):  
    '''
    Save input data to a compressed npz file.

    Parameters
    ----------
    data : dict
        Input data, the keys will be the name for each field, and the value is the data.
    file : str
        destination file path.

    Returns
    -------
    None.

    '''
    kwargs = {}
    for name, value in data.items():
        kwargs[name] = np.stack(value)
    np.savez_compressed(file, **kwargs)
                            

def load_numpys(folder:str, names:list = None, sample:list = None):
    '''
    Load data from npz shards.

    Parameters
    ----------
    folder : str
        Data folder path.
    names : list, optional
        List of names of returned fields. If 'None', all fields will be returned. The default is None.
    sample : list, optional
        List of shards to be loaded. If 'None', all shards will be loaded. The default is None.

    Returns
    -------
    tuple
        A tuple including all selected data fields.

    '''
    output = {}
    if(sample is None):
        sample = [file[:-4] for file in os.listdir(folder) if file.endswith('.npz')]
    for n in sample:
        data = np.load(os.path.join(folder, str(n) + '.npz'))
        
        if(names is None):
            names = data.files
            
        for i, name in enumerate(names):
            try:
                output[i].append(data[name])
            except:
                output[i] = [data[name]]
    return (np.vstack(o) for o in output.values())
            
           
        
    
        
def to_numpys(generator, folder:str, names:list = ['X','Y'], size:int=10000, total:int = None):
    '''
    Save generator output to npz shards.

    Parameters
    ----------
    generator : Generator
        Data generator.
    folder : str
        Data folder.
    names : list, optional
        The names of fields. If the names are not specified, 'valuen' will be used. The default is ['X','Y'].
    size : int, optional
        The size of each shard. If size is 0 or less, all data will be saved in one shard. The default is 10000.
    total : int, optional
        The total number for progress bar. The default is None.

    Returns
    -------
    None.

    '''
    
    if(not os.path.exists(folder)):
        os.makedirs(folder)   
    data = {}
    batch = 0
    count = 0
    for output in tqdm(generator, total=total):
        output = list(output)        
        for i,o in enumerate(output): 
            try:
                name = names[i]
            except:
                names.append['value'+str(i)]
            try:
                data[name].append(o)
            except:
                data[name]=[o]
                   
        count+=1
        if(count==size):
            save_numpy(data, os.path.join(folder, str(batch)+'.npz'))
            count=0
            batch+=1
            for name in names:
                data[name] = []
                
            
    save_numpy(data, os.path.join(folder, str(batch)+'.npz'))
    values = {}
    for i,o in enumerate(output): 
        values[names[i]] = {
            'shape':str(o.shape),
            'dtype':str(o.dtype)
        }
    data = {
        'batch':batch,
        'size':size,
        'count':(count+batch*size),
        'values':values
    }
            
            
    with open(os.path.join(folder, 'profile.json'), 'w') as outfile:
        json.dump(data, outfile)

        

        
def to_tfrecords(generator, folder:str, size:int=10000, fixed_length:list = None, names:list = None, total:int=None):
    '''    
    Save generator output to TFRecord shards.

    Parameters
    ----------
    generator : Generator
        Data generator.
    folder : str
        Data folder.
    size : int, optional
        The size of each shard. If size is 0 or less, all data will be saved in one shard. The default is 10000.
    fixed_length : list, optional
        Whether the length of the fields is fixed. If not specified, a field will be treated as of fixed length. The default is None.
    names : list, optional
        The names of fields. If not specified, index will be used as the name. The default is None.
    total : int, optional
        The total number for progress bar. The default is None.

    Returns
    -------
    None.

    '''
    if(size==0):
        size = -1
    if(not os.path.exists(folder)):
        os.makedirs(folder)   
    count = 0
    batch = 0
    writer = tf.io.TFRecordWriter(os.path.join(folder, str(batch)+'.tfr'))
    for output in tqdm(generator, total=total):   
        #print(count,size)
        if(count==size):
            writer.close()
            count = 0
            batch+=1
            writer = tf.io.TFRecordWriter(os.path.join(folder, str(batch)+'.tfr'))
            
        try:
            example = _serialize_example(output, dtypes)
        except:
            dtypes = []
            for i, o in enumerate(output):
                try:
                    if(not fixed_length[i]):
                        dtypes.append(None)
                    else:
                        dtypes.append(o.dtype)
                except:
                    dtypes.append(o.dtype)
            example = _serialize_example(output, dtypes)
            
        writer.write(example)
        count+=1
    writer.close()
    
    
    
    
    
    
    
    
    out = list(output)
    values = {}
    for i, o in enumerate(out):
        try:
            name = names[i] 
        except:
            name = i
        data = {
            'shape': np.asarray(o).shape,
            'dtype': str(np.asarray(o).dtype)
        }

        try:
            if(not fixed_length[i]):                    
                data['shape'] = None
                data['dtype'] = None
        except:
            pass
        values[name] = data
    output = {
        'batch':batch,
        'size':size,
        'count':(count+batch*size),
        'values':values
    }
        
    with open(os.path.join(folder, 'profile.json'), 'w') as outfile:
        json.dump(output, outfile)
                
        
def to_tfrecord(generator, tfrecords_filename:str, fixed_length:list = None, names:list = None, total:int=None):
    '''
    Save generator output to a TFRecord file.

    Parameters
    ----------
    generator : Generator
        Data generator.
    tfrecords_filename : str
        TFRecord file path.
    fixed_length : list, optional
        Whether the length of the fields is fixed. If not specified, a field will be treated as of fixed length. The default is None.
    names : list, optional
        The names of fields. If not specified, index will be used as the name. The default is None.
    total : int, optional
        The total number for progress bar. The default is None.

    Returns
    -------
    None.

    '''
    with tf.io.TFRecordWriter(tfrecords_filename) as writer:
        count = 0
        for output in tqdm(generator, total=total):    
            count+=1
            try:
                example = _serialize_example(output, dtypes)
            except:
                dtypes = []
                for i, o in enumerate(output):
                    try:
                        if(not fixed_length[i]):
                            dtypes.append(None)
                        else:
                            dtypes.append(o.dtype)
                    except:
                        dtypes.append(o.dtype)
                example = _serialize_example(output, dtypes)
            writer.write(example)
    out = list(output)
    values = {}
    for i, o in enumerate(out):
        data = {
            'shape': np.asarray(o).shape,
            'dtype': str(dtypes[i])
        }
        #if(names!=None):
        #    data['name'+str(i)] = names[i] 
        try:
            name = names[i]
        except:
            name = i
            
        try:
            if(not fixed_length[i]):                    
                data['shape'] = None                
                data['dtype'] = None
        except:
            pass
        values[name] = data
    output = {'values':values,
              'count': count
             }

    with open(tfrecords_filename + '.profile', 'w') as outfile:
        json.dump(output, outfile)
    
    
    
def _parse_numpy(data, shape, dtype):
    data = data.numpy()
    dtype = dtype.numpy().decode()
    return np.frombuffer(data, dtype=dtype).reshape(shape)
    


def _parse_inline_numpy(data, shape, dtype):
    data = data.numpy()
    shape = tuple(np.frombuffer(shape.numpy(), dtype='int'))
    dtype = dtype.numpy().decode('utf-8')
    return np.frombuffer(data, dtype=dtype).reshape(shape)


def _get_feature_description(varn, shapes, dtypes):
    feature_description = {} 
    for i in range(varn):       
        feature_description['value'+str(i)] = tf.io.FixedLenFeature([], tf.string, default_value='')
        if(shapes[i] == None):
            feature_description['shape'+str(i)] = tf.io.FixedLenFeature([], tf.string, default_value='')
            feature_description['dtype'+str(i)] = tf.io.FixedLenFeature([], tf.string, default_value='')
        elif(dtypes[i].startswith('<U')):
            feature_description['dtype'+str(i)] = tf.io.FixedLenFeature([], tf.string, default_value='')
            
        
    return feature_description


def load_tfrecords_profile(folder:str):
    try:
        with open(os.path.join(folder, 'profile.json')) as f:
            return json.load(f)
    except:
        pass


def load_tfrecords(folder:str, sample:list = None, shapes:list = None, dtypes:list = None, names = None, ignore_order = True):
    '''
    Load data from TFRecord shards.

    

    Parameters
    ----------
    folder : str
        TFRecord shard folder path.
    sample : list, optional
        List of shards to be loaded. If 'None', all shards will be loaded. The default is None.
    shapes : list, optional
        Specify field shapes. If 'None', shapes will be loaded from profile. The default is None.
    dtypes : list, optional
        Specify field types. If 'None', types will be loaded from profile. The default is None.
    names : TYPE, optional
        List of names of returned fields. If 'None', all fields will be returned. The default is None.
    ignore_order : TYPE, optional
        Whether uses data as soon as it streams in, rather than in its original order. The default is True.

    Returns
    -------
    tuple
        A tuple including all selected data fields.

    '''



    def _load_function(proto):      
        parsed_features = tf.io.parse_single_example(proto, feature_description) 
        output = []
                
        for i in variable:
            if(shapes[i] == None):
                try:
                    value = tf.py_function(func=_parse_inline_numpy, inp=[parsed_features['value'+str(i)], parsed_features['shape'+str(i)],parsed_features['dtype'+str(i)]], Tout=tf.float32)
                except:
                    value = tf.py_function(func=_parse_inline_numpy, inp=[parsed_features['value'+str(i)], parsed_features['shape'+str(i)],parsed_features['dtype'+str(i)]], Tout=tf.string)
            else:
                if(dtypes[i].startswith('<U')):
                    value = tf.py_function(func=_parse_numpy, inp=[parsed_features['value'+str(i)], shapes[i], parsed_features['dtype'+str(i)]], Tout=tf.string)
                else:
                    value = tf.py_function(func=_parse_numpy, inp=[parsed_features['value'+str(i)], shapes[i], dtypes[i]], Tout=tf.float32)
                value.set_shape(shapes[i])
            output.append(value)
        return tuple(output)
    
     
    try:
        with open(os.path.join(folder, 'profile.json')) as f:
            profiles = json.load(f)
    except:
        pass
    profiles = profiles['values']
    varn = len(profiles)
    
    if(sample is None):        
        sample = [file[:-4] for file in os.listdir(folder) if file.endswith('.tfr')]
        
        
    
    if(names==None):
        variable = range(varn)
    else:
        keys = list(profiles.keys())
        variable = []
        for var in names:
            try:
                variable.append(keys.index(str(var)))      
            except:
                pass
                  
                
    if(shapes == None):  
        shapes = []
        for i,profile in profiles.items():
            try:
                shapes.append(profile['shape'])
            except:
                shapes.append(None)
                
                
    if(dtypes == None):     
        dtypes = []
        for i,profile in profiles.items():   
            try:
                dtypes.append(profile['dtype'])
            except:
                dtypes.append(None)
                
    
    feature_description = _get_feature_description(varn, shapes, dtypes)
    raw_dataset = tf.data.TFRecordDataset([os.path.join(folder, str(s)+'.tfr') for s in sample])
    if(ignore_order):
        options = tf.data.Options()
        options.experimental_deterministic = False
        raw_dataset = raw_dataset.with_options(options)
    return raw_dataset.map(_load_function)

def load_tfrecord_profile(tfrecords_filename:str):     
    try:
        with open(tfrecords_filename + '.profile') as f:
            return json.load(f)
    except:
        pass

    
    

def load_tfrecord(tfrecords_filename:str, shapes:list = None, dtypes:list = None, names = None):
    '''
    Load data from a TFRecord file.
    

    Parameters
    ----------
    tfrecords_filename : str
        TFRecord file path..
    shapes : list, optional
        Specify field shapes. If 'None', shapes will be loaded from profile. The default is None.
    dtypes : list, optional
        Specify field types. If 'None', types will be loaded from profile. The default is None.
    names : TYPE, optional
        List of names of returned fields. If 'None', all fields will be returned. The default is None.

    Returns
    -------
    tuple
        A tuple including all selected data fields.

    '''


    def _load_function(proto):      
        parsed_features = tf.io.parse_single_example(proto, feature_description) 
        output = []
                
        for i in variable:
            if(shapes[i] == None):
                try:
                    value = tf.py_function(func=_parse_inline_numpy, inp=[parsed_features['value'+str(i)], parsed_features['shape'+str(i)],parsed_features['dtype'+str(i)]], Tout=tf.float32)
                except:
                    value = tf.py_function(func=_parse_inline_numpy, inp=[parsed_features['value'+str(i)], parsed_features['shape'+str(i)],parsed_features['dtype'+str(i)]], Tout=tf.string)
            else:
                if(dtypes[i].startswith('<U')):
                    value = tf.py_function(func=_parse_numpy, inp=[parsed_features['value'+str(i)], shapes[i], parsed_features['dtype'+str(i)]], Tout=tf.string)
                else:
                    value = tf.py_function(func=_parse_numpy, inp=[parsed_features['value'+str(i)], shapes[i], dtypes[i]], Tout=tf.float32)
                value.set_shape(shapes[i])
            output.append(value)
        return tuple(output)
    
     
    try:
        with open(tfrecords_filename + '.profile') as f:
            profiles = json.load(f)
    except:
        pass
    profiles = profiles['values']
    varn = len(profiles)
        
        
        
    
    if(names==None):
        variable = range(varn)
    else:
        keys = list(profiles.keys())
        variable = []
        for var in names:
            try:
                variable.append(keys.index(str(var)))      
            except:
                pass
                  
                
    if(shapes == None):  
        shapes = []
        for i,profile in profiles.items():
            try:
                shapes.append(profile['shape'])
            except:
                shapes.append(None)
                
                
    if(dtypes == None):     
        dtypes = []
        for i,profile in profiles.items():   
            try:
                dtypes.append(profile['dtype'])
            except:
                dtypes.append(None)
                
    
    feature_description = _get_feature_description(varn, shapes, dtypes)
    raw_dataset = tf.data.TFRecordDataset(tfrecords_filename)
    return raw_dataset.map(_load_function)





def _serialize_example(inputs:tuple, dtypes:list = None):
    inputs = list(inputs)
    feature={}
    for i, iput in enumerate(inputs):
        dtype = dtypes[i]
        if(dtype is None):
            feature['value'+str(i)] = _bytes_feature(np.asarray(iput).tostring())
            feature['shape'+str(i)] = _bytes_feature(np.asarray(iput.shape).tostring())
            feature['dtype'+str(i)] = _bytes_feature(iput.dtype.name.encode('utf-8'))
        else:
            feature['value'+str(i)] = _bytes_feature(np.asarray(iput).astype(dtype).tostring())
            if(str(dtype).startswith('<U')):
                feature['dtype'+str(i)] = _bytes_feature(str(iput.dtype).encode('utf-8'))
               
            
    return tf.train.Example(features=tf.train.Features(feature=feature)).SerializeToString()   




def test_gen():
    yield np.asarray([1]), np.asarray([[1,2,3],[4,5,6]]),np.asarray([2])
    yield np.asarray([2.4]), np.asarray([[2,2,3],[4,5,6]]),np.asarray([3])
    
def test():
    import shutil
    l = 20
    x = np.around(np.asarray([[i] for i in range(l)]),3)
    y = np.asarray([['string' + str(i)] for i in range(l)])
    z = np.around(np.random.rand(l, 2, 2),3)
    def gen():
        for i in range(10):
            yield x[i], y[i], z[i]
            
    to_tfrecord(gen(),'test.tfr')
    raw_dataset =  load_tfrecord('test.tfr')
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
        
        
        
        
             
        
            
    to_tfrecord(gen(),'test.tfr', fixed_length = [True])
    raw_dataset =  load_tfrecord('test.tfr')
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
            
            
            
    to_tfrecord(gen(),'test.tfr', fixed_length = [False])
    raw_dataset =  load_tfrecord('test.tfr')
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
        
    to_tfrecord(gen(),'test.tfr', names = ['x','y'])
    raw_dataset =  load_tfrecord('test.tfr')
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
        
        
        
    to_tfrecord(gen(),'test.tfr', names = ['x'])
    raw_dataset =  load_tfrecord('test.tfr', names=['1','x','1'])
    row = 0
    for vy, vx, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        assert (vz.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
    shutil.rmtree('test')    
    to_tfrecords(gen(),'test')
    raw_dataset =  load_tfrecords('test')
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
        
        
    to_tfrecords(gen(),'test', size=3)
    raw_dataset =  load_tfrecords('test')
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
    to_tfrecords(gen(),'test', size=3)
    raw_dataset =  load_tfrecords('test', sample=[0,1])
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row]), 'test 1'
        row+=1
        
        
        
        
        
    to_tfrecords(gen(),'test', size=3)
    raw_dataset =  load_tfrecords('test', sample=[1, 2])
    row = 0
    for vx, vy, vz in raw_dataset:
        assert (vx.numpy() == x[row+3]), 'test 1'
        assert (vy.numpy().astype('U13') == y[row+3]), 'test 1'
        row+=1
        
        