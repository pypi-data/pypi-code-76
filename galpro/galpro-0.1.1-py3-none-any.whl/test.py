import numpy as np
from galpro.model import Model
import time

x_train = np.load('/Users/sunil/Desktop/PhD/Projects/Joint PDFs using RF/Analysis/Data/X_train_deep.npy')
x_test = np.load('/Users/sunil/Desktop/PhD/Projects/Joint PDFs using RF/Analysis/Data/X_test_deep.npy')
y_train = np.load('/Users/sunil/Desktop/PhD/Projects/Joint PDFs using RF/Analysis/Data/y_train_deep.npy')
y_test = np.load('/Users/sunil/Desktop/PhD/Projects/Joint PDFs using RF/Analysis/Data/y_test_deep.npy')

mag = np.arange(14, 28)
lup = np.arange(0, 14)
Input = lup


# 2d
x_train = np.delete(x_train, Input, axis=1)
x_test = np.delete(x_test, Input, axis=1)
y_train = y_train
y_test = y_test
target_features = ['$z$', '$\log(M_{\star} / M_{\odot})$']

# [:10000].repeat(100, axis=0)

print(y_test.shape)


'''
# 1d
y_train = y_train[:, 0]
y_test = y_test[:, 0]

target_features = ['$z$']
'''



'''
# nd
y_train = np.c_[y_train, x_train[:, 4]]
y_test = np.c_[y_test, x_test[:, 4]]
x_train = np.delete(x_train, 4, axis=1)
x_test = np.delete(x_test, 4, axis=1)

target_features = ['$z$', '$M$', '$g-r$']
'''

'''
x_train = np.load('/Users/sunil/Desktop/PhD/Projects/Dark Sirens/data/x_train.npy')
x_test = np.load('/Users/sunil/Desktop/PhD/Projects/Dark Sirens/data/x_target_GW190412.npy')
y_train = np.load('/Users/sunil/Desktop/PhD/Projects/Dark Sirens/data/y_train.npy')
y_test = np.load('/Users/sunil/Desktop/PhD/Projects/Dark Sirens/data/x_target_GW190412.npy')
'''

#start = time.time()
model = Model(model_name='model', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test,
              save_model=True, target_features=target_features)
model.point_estimate(save_estimates=True, make_plots=False)

#posterior = model.posterior(save_posteriors=True, make_plots=False, on_the_fly=False)
#finish = time.time()
#print(finish-start)

'''
posterior = model.posterior(save_posteriors=False, make_plots=False, on_the_fly=True)
#start = time.time()
for i in np.arange(x_test.shape[0]):
    next(posterior)

finish = time.time()
print(finish-start)
'''


#model.plot_marginal(show=False, save=True)
#model.end()
#finish = time.time()

#model.validate(save_validation=True, make_plots=True)
"""print(validation['pits'])
print(validation['marginal_calibration'])
print(validation['coppits'])
print(validation['kendall_calibration'])"""
model.plot_scatter(show=True, save=True)
#model.plot_marginal(show=True, save=False)
#model.plot_joint(show=False, save=True)
#model.plot_corner(show=False, save=True)

#model.plot_pit(show=True, save=True)
#model.plot_coppit(show=False, save=True)
#model.plot_marginal_calibration(show=True, save=False)
#model.plot_kendall_calibration(show=False, save=True)

"""
sample_leafs = self.model.apply(self.x_test[sample].reshape(1, self.model.n_features_))[0]
"""

