import random

from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler

def get_shuffled_split_indices(dsize, splits, shuffle_seed=42):
    """Returns a list of lists of indices such that the indices are randomly
    sampled from the range(0, dsize) and each of these lists is of length
    corresponding to a fraction of the dataset between the end of the previous
    split and the beginning of the next.

    Example:

    >>> get_shuffled_split_indices(10, [0.5], shuffle_seed=42)
    [[7, 3, 2, 8, 5], [6, 9, 4, 0, 1]]

    >>> get_shuffled_split_indices(10, [0.3, 0.5], shuffle_seed=42)
    [[7, 3, 2], [8, 5], [6, 9, 4, 0, 1]]

    >>> get_shuffled_split_indices(10, [0.3, 0.5], shuffle_seed=55)
    [[6, 4, 8], [9, 0], [7, 5, 2, 3, 1]]


    Args:
        dsize (int): maximum index
        splits (list of floats): strictly increasing list of floats from 0 to 1.
            Defines how to divide the indices
        shuffle_seed (hashable object): seed for the shuffling
    """
    last_split = 0
    for s in splits:
        if s <= last_split:
            raise ValueError("Splits must be strictly increasing")
        last_split = s
    indices = list(range(dsize))
    random.seed(shuffle_seed)
    random.shuffle(indices)

    split_locs = [int(s * dsize) for s in splits]
    split_indices = []
    begin = 0
    end = 0
    for i in range(len(split_locs)):
        if i == 0:
            begin = 0
            end = split_locs[i]
        else:
            begin = split_locs[i-1]
            end = split_locs[i]
        split_indices.append(indices[begin:end])
    split_indices.append(indices[end:])
    return split_indices

def get_datasets_from_params(dataset_class, dataset_params):
    """Returns a train, validation and test dataset given a 
    class to call and dictionary of parameters. 

    The parameter dictionary can contain keys with parameters
    explicitly for train, validation or test datasets if assigned
    to a key "__train__", "__validation__" or "__test__".
    """
    special_keys = ["__train__", "__validation__", "__test__"]
    params_for_all = {
        key: value for key, value in dataset_params.items()
        if not key in special_keys}
    datasets = []
    default_dataset = None
    for key in special_keys:
        params = {**params_for_all, **dataset_params.get(key, {})}
        if params == params_for_all:
            if default_dataset is None:
                default_dataset = dataset_class(**params)
            datasets.append(default_dataset)
        else:
            datasets.append(dataset_class(**params))
    return datasets

def get_split_loaders(dataset_class, batch_size, 
                      dataset_params=None, splits=(0.7, 0.9), seed=42):
    """Returns three dataset loaders which receive a portion of the data
    decided by the `splits` argument:
     - one for training data with `splits[0]` total fraction of data
     - one for validation data with `splits[1] - splits[0]` total fraction of
       data
     - one for testing data with `1 - splits[1]` total fraction of data
    Furthermore, the data samples contained in each of these portions are
    randomly decided based on the seed.

    The `dataset_params` argument is a dictionary which is forwarded to the
    Dataset constructor.
    """
    if not (splits[0] < splits[1] and splits[0] >= 0 and splits[1] <= 1):
        raise ValueError("Invalid dataset splitting points")

    dataset_params = dataset_params if dataset_params else {}
    train_dataset, val_dataset, test_dataset = get_datasets_from_params(
        dataset_class, dataset_params)
    # Strong assumption that 
    # len(train_dataset) == len(val_dataset) == len(test_dataset)
    indices_list = get_shuffled_split_indices(
        len(train_dataset), splits, shuffle_seed=seed)
    train_sampler, val_sampler, test_sampler = [
        SubsetRandomSampler(indices) for indices in indices_list]
    train_loader = DataLoader(train_dataset, batch_size=batch_size,
                              sampler=train_sampler)
    val_loader = DataLoader(val_dataset, batch_size=batch_size,
                            sampler=val_sampler)
    test_loader = DataLoader(test_dataset, batch_size=batch_size,
                             sampler=test_sampler)
    return train_loader, val_loader, test_loader
