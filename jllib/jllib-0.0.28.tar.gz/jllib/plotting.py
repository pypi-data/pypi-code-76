import numpy as np
import os

def plot_keras_history(history, name='', acc='acc'):
    """Plots keras history."""
    import matplotlib.pyplot as plt

    try:
        training_acc = history.history[acc]
        validation_acc = history.history['val_' + acc]
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(len(training_acc))

        plt.ylim(0, 1)
        plt.plot(epochs, training_acc, 'tab:blue', label='Training acc')
        plt.plot(epochs, validation_acc, 'tab:orange', label='Validation acc')
        plt.title('Training and validation accuracy  ' + name)
        plt.legend()

        plt.figure()

        plt.plot(epochs, loss, 'tab:green', label='Training loss')
        plt.plot(epochs, val_loss, 'tab:red', label='Validation loss')
        plt.title('Training and validation loss  ' + name)
        plt.legend()
        plt.show()
        plt.close()
        return training_acc, validation_acc
    except KeyError:
        # When validation_split is not used, do this:
        training_acc = history.history[acc]
        loss = history.history['loss']

        epochs = range(len(training_acc))

        plt.ylim(0, 1)
        plt.plot(epochs, training_acc, label='Training acc', c='tab:blue')
        plt.plot(epochs, loss, label='Training loss', c='tab:orange')
        plt.title('Training accuracy and training loss  ' + name)
        plt.legend()
        plt.show()
        plt.close()
        return training_acc


def plot_history_df(history, path, name='', acc='acc'):
    """Plots keras history."""
    import matplotlib.pyplot as plt
    import os

    training_acc = history[acc]
    validation_acc = history['val_' + acc]
    loss = history['loss']
    val_loss = history['val_loss']

    epochs = range(len(training_acc))

    plt.ylim(0, 1)
    plt.plot(epochs, training_acc, 'tab:blue', label='Training acc')
    plt.plot(epochs, validation_acc, 'tab:orange', label='Validation acc')
    plt.title('Training and validation accuracy ' + name)
    plt.legend()
    plt.savefig(os.path.dirname(path) + '/history_acc.pdf')
    #plt.show()
    plt.close()

    plt.figure()

    plt.plot(epochs, loss, 'tab:green', label='Training loss')
    plt.plot(epochs, val_loss, 'tab:red', label='Validation loss')
    plt.title('Training and validation loss ' + name)
    plt.legend()
    plt.savefig(os.path.dirname(path) + '/history_loss.pdf')
    #plt.show()
    plt.close()
    return training_acc, validation_acc


def plot_confusion_matrix(cm,
                          target_names,
                          path,
                          title='Confusion Matrix',
                          cmap=None,
                          normalize=True,
                          fname='/confusion-matrix.pdf'):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    fname:        filename.

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(12, 10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True class')
    plt.xlabel('Predicted class\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.savefig(path + fname, bbox_inches='tight')
    #plt.show()
    plt.close()


def do_cm(X: np.ndarray, Y_labels: np.ndarray, model):
    from sklearn.metrics import classification_report, confusion_matrix

    assert isinstance(X, np.ndarray), 'Param `X` must be np.ndarray but is ' + str(type(X))
    assert isinstance(Y_labels, np.ndarray), 'Param `Y_labels` must be np.ndarray but is ' + str(type(Y_labels))

    assert X.shape[0] == Y_labels.shape[0]

    #Confution Matrix and Classification Report
    Y_pred = model.model.predict(X)
    y_pred = np.argmax(Y_pred, axis=1)
    Y_labels = np.argmax(Y_labels, axis=1)
    #print(y_pred, len(y_pred))
    cm = confusion_matrix(Y_labels, y_pred)

    with open(os.path.dirname(model.output_directory) + '/classification-report.txt', 'w') as f:
        f.write('Classification Report\n')
        f.write(classification_report(Y_labels, y_pred))

    plot_confusion_matrix(cm, set(Y_labels), os.path.dirname(model.output_directory), normalize=False)


def do_cm_reduce_window_slices(a_np: np.ndarray, b_np: np.ndarray, model_output_directory):
    from sklearn.metrics import classification_report, confusion_matrix

    assert isinstance(a_np, np.ndarray), 'Param `a_np` must be np.ndarray but is ' + str(type(a_np))
    assert isinstance(b_np, np.ndarray), 'Param `b_np` must be np.ndarray but is ' + str(type(b_np))

    assert a_np.shape[0] == b_np.shape[0]

    #Confution Matrix and Classification Report
    cm = confusion_matrix(a_np, b_np)

    with open(os.path.dirname(model_output_directory) + '/classification-report-reduced-window-slices.txt', 'w') as f:
        f.write('Classification Report\n')
        f.write(classification_report(a_np, b_np))

    plot_confusion_matrix(cm,
                          set(a_np),
                          os.path.dirname(model_output_directory),
                          normalize=False,
                          fname='/confusion-matrix-reduced-window-slices.pdf')
