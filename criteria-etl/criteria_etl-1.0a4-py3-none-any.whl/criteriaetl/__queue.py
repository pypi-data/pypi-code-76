# utils/save_func.py
def protected_save(save_func, *args, ask_before_save=True):
    """
    Wrapper for saving outputs
    Parameters
    ----------
    save_func : callable
        It saves the output. Its first argument needs to be
        `to_save_object`.
    args : optional,
        Positional argumets to be passed to `save_func`. The second
        argument (if any) is assumed to be the path where the file will
        be stored.
    ask_before_save : bool or None.
        If True, it asks for input to confirm saving. If False, it does
        not ask for confirmation. If None it will not save the output.
    """
    if ask_before_save is None:
        print('skip saving')
        return None
    save = True

    print(f'trying to save at: {args[1]}') if len(args) > 1 else None
    if ask_before_save:
        save &= (input('confirm saving? (y/n)') == 'y')

    if save:
        print('saving')
        save_func(*args)
    else:
        print('not saved')


# transformers/columns_base.py
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
class PandasColumnTransformer(ColumnTransformer):
    def _hstack(self, Xs):
        """Stacks Xs horizontally.
        This allows subclasses to control the stacking behavior, while reusing
        everything else from ColumnTransformer.
        Parameters
        ----------
        Xs : List of numpy arrays or DataFrames
        """
        if isinstance(Xs[0], pd.DataFrame):
            return pd.concat(Xs, axis = 'columns', copy=False)
        else:
            Xs = [f.toarray() if sparse.issparse(f) else f for f in Xs]
            return np.hstack(Xs)
