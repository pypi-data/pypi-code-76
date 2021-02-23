def train_decorator(algorithm_id: str, main: bool = False):
    def do_train(f):
        _algorithm_id = f.__name__ if algorithm_id is None else algorithm_id
        setattr(f, "_is_train_func", True)
        setattr(f, "_algorithm_id", _algorithm_id)
        setattr(f, "_is_main", main)
        return f

    return do_train


def predict_decorator(algorithm_id: str, main: bool = False):
    def do_predict(f):
        _algorithm_id = f.__name__ if algorithm_id is None else algorithm_id
        setattr(f, "_is_predict_func", True)
        setattr(f, "_algorithm_id", _algorithm_id)
        setattr(f, "_is_main", main)
        return f

    return do_predict


def pipeline_decorator(pipeline_id: str):
    def do_pipeline(f):
        setattr(f, "_is_pipeline_func", True)

        return f

    return do_pipeline
