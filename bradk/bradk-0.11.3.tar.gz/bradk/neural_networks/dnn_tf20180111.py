
# coding: utf-8

# In[1]:


import tensorflow as tf
from tensorflow.python.framework import ops
import pickle
import numpy as np
import matplotlib.pyplot as plt
import time
get_ipython().magic('matplotlib inline')


# In[2]:


def random_mini_batches(X, Y, mini_batch_size = 64, seed = 0):
    np.random.seed(seed)            # To make your "random" minibatches the same as ours
    m = X.shape[1]                  # number of training examples
    mini_batches = []
    # Step 1: Shuffle (X, Y)
    permutation = np.random.permutation(m)
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation]
    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = max(1, m // mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, (k*mini_batch_size):((k+1)*mini_batch_size)]
        mini_batch_Y = shuffled_Y[:, (k*mini_batch_size):((k+1)*mini_batch_size)]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    if (m >= mini_batch_size) and (m % mini_batch_size != 0): # Handling the end case (last mini-batch < mini_batch_size)
        mini_batch_X = shuffled_X[:, (num_complete_minibatches*mini_batch_size):]
        mini_batch_Y = shuffled_Y[:, (num_complete_minibatches*mini_batch_size):]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    return mini_batches
def create_placeholders(n_x, n_y):
    X = tf.placeholder(tf.float32, shape=(n_x,None), name='X')
    Y = tf.placeholder(tf.float32, shape=(n_y,None), name='Y')
    return X, Y
def initialize_parameters(layerdims, seed = 1):
    tf.set_random_seed(seed)                   # so that your "random" numbers match ours
    parameters = {}
    for i in range(1, len(layerdims)):
        parameters["W%d"%i] = tf.get_variable("W%d"%i, [layerdims[i],layerdims[i-1]], initializer = tf.contrib.layers.xavier_initializer(seed = seed))
        parameters["b%d"%i] = tf.get_variable("b%d"%i, [layerdims[i],1], initializer = tf.zeros_initializer())
    return parameters
def forward_propagation(X, parameters, hpar):
    L = len(parameters) // 2 # 2 -> there are two groups: W's and b's
    units = {}
    units['Z1'] = tf.add(tf.matmul(parameters['W1'],X),parameters['b1'])
    for i in range(2, L+1):
        if hpar['activation_hidden_layers'] == 'sigmoid':
            units['A'+str(i-1)] = tf.nn.sigmoid(units['Z'+str(i-1)]) # sigmoidfunction
        elif hpar['activation_hidden_layers'] == 'tanh':
            units['A'+str(i-1)] = tf.nn.tanh(units['Z'+str(i-1)]) # tanh function
        elif hpar['activation_hidden_layers'] == 'relu':
            units['A'+str(i-1)] = tf.nn.relu(units['Z'+str(i-1)]) # ReLU function
        units['Z'+str(i)] = tf.add(tf.matmul(parameters['W'+str(i)], units['A'+str(i-1)]), parameters['b'+str(i)])
    ZL = units['Z'+str(L)]
    return ZL # output of the last LINEAR unit
def compute_cost(ZL, Y, hpar):
    logits = tf.transpose(ZL) # to fit the tensorflow requirement for tf.nn.softmax_cross_entropy_with_logits(...,...)
    labels = tf.transpose(Y) # to fit the tensorflow requirement for tf.nn.softmax_cross_entropy_with_logits(...,...)
    if hpar['activation_last_layer'] == 'sigmoid':
        cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = logits, labels = labels))
    elif hpar['activation_last_layer'] == 'softmax':
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = logits, labels = labels))
    return cost
def normalize_X_Y(X_train0, Y_train0, X_test0, Y_test0, hpar):
    if hpar['input_normalization'] == True:
        Xu = np.mean(X_train0, axis = 1, keepdims = True)
        Xs = np.std(X_train0, axis = 1, keepdims = True)
    else:
        Xu = np.zeros((X_train0.shape[0],1))
        Xs = np.full((X_train0.shape[0],1), 1.0)
    X_train = (X_train0 - Xu) / Xs
    Y_train = np.int64(Y_train0 > 0.5)
    X_test = (X_test0 - Xu) / Xs
    if len(Y_test0) != 0:
        Y_test = np.int64(Y_test0 > 0.5)
    else:
        Y_test = []
    return X_train, Xu, Xs, Y_train, X_test, Y_test
def denormalize_W1_b1(WW1, bb1, Xu, Xs):
    W1 = WW1 / Xs.T
    b1 = bb1 - np.dot(WW1, Xu / Xs)
    return W1, b1


# In[3]:


def convert_to_one_hot(labels, C):
    C = tf.constant(C, name='C') # Create a tf.constant equal to C (depth), name it 'C'. (approx. 1 line)
    one_hot_matrix = tf.one_hot(labels.squeeze(), C, axis=0)
    sess = tf.Session()
    one_hot = sess.run(one_hot_matrix)
    sess.close()
    return one_hot
def train(X_train0, Y_train0, X_test0, Y_test0, hpar):
    print('> Deep Neural Network (tensorflow) started ...')
    X_train, Xu, Xs, Y_train, X_test, Y_test = normalize_X_Y(X_train0, Y_train0, X_test0, Y_test0, hpar)
    print('>> X_train shape = '+str(X_train.shape))
    print('>> Y_train shape = '+str(Y_train.shape))
    print('>> X_test shape = '+str(X_test.shape if len(X_test)!=0 else X_test))
    print('>> Y_test shape = '+str(Y_test.shape if len(Y_test)!=0 else Y_test))
    print(">> the number of training data = " + str(X_train.shape[1]))
    print(">> the number of test data = " + str(X_test.shape[1] if len(X_test)!=0 else X_test))
    layerdims = [X_train.shape[0]] + hpar['hidden_layer_dims'] + [Y_train.shape[0]]
    print('>> the number of units of layers = '+str(layerdims))
    print(">> the number of epochs = " + str(hpar['num_epochs']))
    print(">> learning rate = " + str(hpar['learning_rate']))
    print(">> activation function of hidden layers = " + hpar['activation_hidden_layers'])
    print(">> activation function of the last layer = " + hpar['activation_last_layer'])
    print(">> mini batch size = " + str(hpar['minibatch_size']))
    print(">> optimizer = " + hpar['optimizer'])
    print(">> input normalization = " + str(hpar['input_normalization']))
    print(">> global random seed = " + str(hpar['global_random_seed']))
    #------------------------------------------------------------------------------------
    ops.reset_default_graph()                         # to be able to rerun the model without overwriting tf variables
    tf.set_random_seed(hpar['global_random_seed'])                             # to keep consistent results
#    seed = 3                                          # to keep consistent results
    seed = hpar['global_random_seed']
    (n_x, m) = X_train.shape                          # (n_x: input size, m : number of examples in the train set)
    n_y = Y_train.shape[0]                            # n_y : output size
    costs = []                                        # To keep track of the cost
    
    X, Y = create_placeholders(n_x, n_y) # Create Placeholders of shape (n_x, n_y)
    parameters = initialize_parameters(layerdims, hpar['global_random_seed']) # Initialize parameters
    ZL = forward_propagation(X, parameters, hpar) # Forward propagation: Build the forward propagation in the tensorflow graph
    cost = compute_cost(ZL, Y, hpar) # Cost function: Add cost function to tensorflow graph
    if hpar['optimizer'] == 'gradient descent':
        optimizer = tf.train.GradientDescentOptimizer(learning_rate = hpar['learning_rate']).minimize(cost) # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.
    elif hpar['optimizer'] == 'momentum':
        optimizer = tf.train.MomentumOptimizer(learning_rate = hpar['learning_rate']).minimize(cost) # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.
    elif hpar['optimizer'] == 'adam':
        optimizer = tf.train.AdamOptimizer(learning_rate = hpar['learning_rate']).minimize(cost) # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.
    init = tf.global_variables_initializer() # Initialize all the variables
    
    with tf.Session() as sess: # Start the session to compute the tensorflow graph
        sess.run(init) # Run the initialization
        tic = time.time()
#        for epoch in range(0, hpar['num_epochs']): # Do the training loop        
        for epoch in range(1, hpar['num_epochs']+1): # Do the training loop
            epoch_cost = 0.                       # Defines a cost related to an epoch
            num_minibatches = max(1, int(m / hpar['minibatch_size'])) # number of minibatches of size minibatch_size in the train set
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, hpar['minibatch_size'], seed)

            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch # Select a minibatch
                # IMPORTANT: The line that runs the graph on a minibatch.
                _ , minibatch_cost = sess.run([optimizer, cost], feed_dict={X:minibatch_X, Y:minibatch_Y}) # Run the session to execute the "optimizer" and the "cost", the feedict should contain a minibatch for (X,Y).
#                epoch_cost += minibatch_cost / num_minibatches
                epoch_cost += minibatch_cost * (minibatch_X.shape[1] / m)
            costs.append(epoch_cost)
            # Print the cost every epoch
#            if hpar['print_cost'] > 0 and epoch % hpar['print_cost'] == 0:
            if hpar['print_cost'] > 0 and ((epoch == 1) or (epoch % hpar['print_cost'] == 0) or (epoch == hpar['num_epochs'])):
                toc = time.time()
                print (">> epoch =  %i; cost = %f; time = %f sec" % (epoch, epoch_cost, toc-tic))
                tic = time.time()
        ## plot the cost
        #plt.plot(np.squeeze(costs))
        #plt.ylabel('cost')
        #plt.xlabel('iterations (per tens)')
        #plt.title("Learning rate =" + str(hpar['learning_rate']))
        #plt.show()
        # lets save the parameters in a variable
        parameters = sess.run(parameters)
        #print(">> Parameters have been trained!")
        # Calculate the correct predictions
        #correct_prediction = tf.equal(tf.argmax(ZL), tf.argmax(Y))
        ## Calculate accuracy on the test set
        #accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        #print(">> Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        #print(">> Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))
    Yp_train, accuracy_train = predict(X_train, Y_train, parameters, hpar)
    Yp_test, accuracy_test = predict(X_test, Y_test, parameters, hpar)
    print(">> Train Accuracy:" + str(accuracy_train))
    print(">> Test Accuracy:" + str(accuracy_test))
    parameters['W1'], parameters['b1'] = denormalize_W1_b1(parameters['W1'], parameters['b1'], Xu, Xs) # denormalization
    print('> Deep Neural Network (tensorflow) ended ...')
    dout = {'parameters': parameters,
            'costs': costs,
            'Yp_train': Yp_train,
            'Yp_test': Yp_test}
    return dout
def predict(X_data, Y_data, parameters, hpar):
    para = {}
    for i in range(1, (len(parameters) // 2) + 1):
        para['W%d'%i] = tf.constant(parameters['W%d'%i], dtype = tf.float32)
        para['b%d'%i] = tf.constant(parameters['b%d'%i], dtype = tf.float32)
    xx = tf.constant(X_data, dtype = tf.float32)
    zl = forward_propagation(xx, para, hpar)
    sess = tf.Session()
    if hpar['activation_last_layer'] == 'sigmoid':
        al = tf.nn.sigmoid(zl)
        AL = sess.run(al)
        Yp = np.int64(AL > 0.5)
        YY = np.int64(Y_data > 0.5)
        accuracy = np.mean(np.all(YY == Yp, axis=0))
    elif hpar['activation_last_layer'] == 'softmax':
        ZL = sess.run(zl)
        YL = np.argmax(ZL, axis = 0)
        YY = np.argmax(Y_data, axis = 0)
        accuracy = np.mean(np.int64(YY == YL))
        Yp = convert_to_one_hot(YL, Y_data.shape[0])
    sess.close()
    return Yp, accuracy


# In[4]:


if False:
    M = 1000   # the number of samples
    np.random.seed(1)
    X = np.random.rand(2, M)
    Y = np.zeros((1, M))
    #Y[0, (X[1,:] - X[0,:] + 0.3) > 0 ] = 1  # line
    #Y[0, (X[0,:]**2 + X[1,:]**2 - 0.7**2) > 0 ] = 1  # semi-circle
    #Y[0, ((X[0,:]-0.5)**2 + (X[1,:]-0.5)**2 - 0.3**2) > 0] = 1  # circle
    #Y[0, (((X[0,:]-0.5)/0.4)**2 + ((X[1,:]-0.2)/0.05)**2 - 1) > 0] = 1  # ellipse
    Y[0, ((((X[0,:]-0.5)/0.4)**2 + ((X[1,:]-0.2)/0.05)**2 - 1) > 0) & (((X[0,:]-0.7)**2 + (X[1,:]-0.7)**2 - 0.1**2) > 0)] = 1  # ellipse & circle
    #-----------------------------------------------------------------
    rn = np.random.permutation(M)
    NofT = int(M * 0.7) # number of train samples
    X_train = X[:,rn[0:NofT]]
    Y_train = Y[:,rn[0:NofT]]
    X_test = X[:,rn[NofT:]]
    Y_test = Y[:,rn[NofT:]]
    #-----------------------------------------------------------------
    hpar = {}
    hpar['hidden_layer_dims'] = [10,5,2]
    hpar['activation_hidden_layers'] = ['sigmoid', 'tanh', 'relu'][1]
    hpar['activation_last_layer'] = ['sigmoid', 'softmax'][0]
    hpar['learning_rate'] = 0.1
    hpar['num_epochs'] = 10000
    hpar['minibatch_size'] = 999999
    hpar['optimizer'] = ["gradient descent", "momentum", "adam"][0]
    hpar['print_cost'] = 1000 # print epoch step; no print when it is zero
    hpar['input_normalization'] = True
    hpar['global_random_seed'] = 1
    dout = train(X_train, Y_train, X_test, Y_test, hpar)
    #-----------------------------------------------------------------
    Yp_train, accuracy_train = predict(X_train, Y_train, dout['parameters'], hpar)
    Yp_test, accuracy_test = predict(X_test, Y_test, dout['parameters'], hpar)
    print("- Train Accuracy:" + str(accuracy_train))
    print("- Test Accuracy:" + str(accuracy_test))  


# In[5]:


if False:
    M = 1000   # the number of samples
    np.random.seed(1)
    X = np.random.rand(2, M)
    Y = np.zeros((1, M))
    #Y[0, (X[1,:] - X[0,:] + 0.3) > 0 ] = 1  # line
    #Y[0, (X[0,:]**2 + X[1,:]**2 - 0.7**2) > 0 ] = 1  # semi-circle
    #Y[0, ((X[0,:]-0.5)**2 + (X[1,:]-0.5)**2 - 0.3**2) > 0] = 1  # circle
    #Y[0, (((X[0,:]-0.5)/0.4)**2 + ((X[1,:]-0.2)/0.05)**2 - 1) > 0] = 1  # ellipse
    Y[0, ((((X[0,:]-0.5)/0.4)**2 + ((X[1,:]-0.2)/0.05)**2 - 1) > 0) & (((X[0,:]-0.7)**2 + (X[1,:]-0.7)**2 - 0.1**2) > 0)] = 1  # ellipse & circle
    #-----------------------------------------------------------------
    rn = np.random.permutation(M)
    NofT = int(M * 0.7) # number of train samples
    X_train = X[:,rn[0:NofT]]
    Y_train = Y[:,rn[0:NofT]]
    X_test = X[:,rn[NofT:]]
    Y_test = Y[:,rn[NofT:]]
    #-----------------------------------------------------------------
    hpar = {}
    hpar['hidden_layer_dims'] = [10,5,2]
    hpar['activation_hidden_layers'] = ['sigmoid', 'tanh', 'relu'][2]
    hpar['activation_last_layer'] = ['sigmoid', 'softmax'][0]
    hpar['learning_rate'] = 0.001
    hpar['num_epochs'] = 2000
    hpar['minibatch_size'] = 64
    hpar['optimizer'] = ["gradient descent", "momentum", "adam"][2]
    hpar['print_cost'] = 1000 # print epoch step; no print when it is zero
    hpar['input_normalization'] = True
    hpar['global_random_seed'] = 1
    dout = train(X_train, Y_train, X_test, Y_test, hpar)
    #-----------------------------------------------------------------
    Yp_train, accuracy_train = predict(X_train, Y_train, dout['parameters'], hpar)
    Yp_test, accuracy_test = predict(X_test, Y_test, dout['parameters'], hpar)
    print("- Train Accuracy:" + str(accuracy_train))
    print("- Test Accuracy:" + str(accuracy_test))      


# In[6]:


if False:
    dataset_file_path = './dataset/coursera_SIGNS_dataset/dataset_(X_train, Y_train, X_test, Y_test).pckl'
    f = open(dataset_file_path, 'rb')
    (X_train_orig, Y_train_orig, X_test_orig, Y_test_orig) = pickle.load(f)
    f.close()
    classes = np.array([0,1,2,3,4,5])
    #-------------------------------------------------------
    # Example of a picture
    #index = 0
    #plt.imshow(X_train_orig[index])
    #print ("y = " + str(np.squeeze(Y_train_orig[:, index])))
    #-------------------------------------------------------
    # Flatten the training and test images
    X_train_flatten = X_train_orig.reshape(X_train_orig.shape[0], -1).T
    X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
    # Normalize image vectors
    X_train = X_train_flatten/255.
    X_test = X_test_flatten/255.
    # Convert training and test labels to one hot matrices
    Y_train = convert_to_one_hot(Y_train_orig, 6)
    Y_test = convert_to_one_hot(Y_test_orig, 6)
    #-----------------------------------------------------------------------------------
    hpar = {}
    hpar['hidden_layer_dims'] = [25,12]
    hpar['activation_hidden_layers'] = ['sigmoid', 'tanh', 'relu'][2]
    hpar['activation_last_layer'] = ['sigmoid', 'softmax'][1]
    hpar['learning_rate'] = 0.0001
    hpar['num_epochs'] = 1500
    hpar['minibatch_size'] = 32
    hpar['optimizer'] = ["gradient descent", "momentum", "adam"][2]
    hpar['print_cost'] = 100 # print epoch step; no print when it is zero
    hpar['input_normalization'] = False
    hpar['global_random_seed'] = 1
    dout = train(X_train, Y_train, X_test, Y_test, hpar)
    #-----------------------------------------------------------------
    Yp_train, accuracy_train = predict(X_train, Y_train, dout['parameters'], hpar)
    Yp_test, accuracy_test = predict(X_test, Y_test, dout['parameters'], hpar)
    print("- Train Accuracy:" + str(accuracy_train))
    print("- Test Accuracy:" + str(accuracy_test))      


# In[ ]:




