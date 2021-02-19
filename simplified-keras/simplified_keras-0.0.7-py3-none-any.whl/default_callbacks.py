import tensorflow.keras.callbacks as clb


def get_default_callbacks(model_path, monitor='val_acc', base_patience=3, lr_reduce_factor=0.5, min_lr=1e-7, verbose=1):
    return [
        clb.ReduceLROnPlateau(monitor=monitor, factor=lr_reduce_factor, min_lr=min_lr, patience=base_patience, verbose=verbose),
        clb.EarlyStopping(monitor=monitor, patience=(2 * base_patience + 1), verbose=verbose),
        clb.ModelCheckpoint(monitor=monitor, filepath=model_path, save_best_only=True, verbose=verbose)
    ]
