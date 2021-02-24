import numpy as np


def macro_pixels_mapping(source_shape, target_shape):
    """
    Computes indices of the macro pixels as a 2D zoom in of the source.
    Returns an array of the same shape as source_shape, with each element being
    a list of 2D coordinates in the target space
    """
    if np.greater(source_shape, target_shape).any():
        raise ValueError("source doesn't fit in target")

    # determine macropixel's side size
    # increment it until macro_shape doesn't fit
    side = 1
    while True:
        macro_shape = np.multiply(source_shape, side + 1)
        if np.greater(macro_shape, target_shape).any():
            # one of the dimensions is too big
            break
        side += 1

    # build coordinates of a single macro-pixel
    # ex: for side=2, sample coords is an array of (0,0), (0,1), (1,0), (1,1)
    sample = []
    for i in range(side):
        for j in range(side):
            sample.append([i, j])
    sample = np.asarray(sample)

    #  generate all the others coordinates in mapping
    mapping = np.zeros(source_shape + sample.shape, dtype=np.int)
    for i in range(source_shape[0]):
        for j in range(source_shape[1]):
            # offset is added to sample macro-pixel
            offset = [i*side, j*side]
            mapping[i, j] = np.add(sample,  offset)

    return mapping


def lined_mapping(n_source, target_shape):
    """
    Builds a mapping from a 1D vector of size n_source in a 2D target space,
    with each vector element being represented as a line in the
    target space.

    mapping is a n_features elements array, with each elements being
    an array of 2 coordinates in the target space
    """
    # px_size is the size of one "pixel" in the target space
    px_size = int(np.floor(np.prod(target_shape) / n_source))

    # Generate mapping
    mapping = np.zeros((n_source,) + (px_size, 2), dtype=np.int)

    major = target_shape[1]

    # convert 1D to 2D coordinates in the target space
    def coords_conv(x): return [x // major, x % major]

    offset = 0
    for i in range(n_source):
        # this is 1d coords
        coords = range(offset, offset + px_size)
        # convert to 2D with a map, and place into mapping
        mapping[i] = np.asarray(list(map(coords_conv, coords)))
        offset += n_source

    return mapping


def sample_test(source, target_shape, mapping):
    # sample source array, alternating 0 and 1
    x = np.zeros(np.prod(source), dtype=np.uint8)
    x[::2] = 1
    # reshape if features is 2D
    x = x.reshape(source)

    formatted_x = np.ones(target_shape, dtype=np.uint8)

    if len(x.shape) == 2:
        for i in range(source[0]):
            for j in range(source[1]):
                # Mapping is a list of coordinates in the destination space
                for coord in mapping[i, j]:
                    formatted_x[tuple(coord)] = x[i, j]

    if len(x.shape) == 1:
        for i in range(source):
            for coord in mapping[i]:
                formatted_x[tuple(coord)] = x[i]

    return x, formatted_x


def show(x, formatted_x, plot=True):
    print("This is source array:\n", x)
    print("This is translated array into {} space: \n".format(formatted_x.shape), formatted_x)

    if plot:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(ncols=2)
        if len(x.shape) == 1:
            x = [x]
        axes[0].imshow(x, cmap='gray')
        axes[0].set_title('original')
        axes[1].imshow(formatted_x, cmap='gray')
        axes[1].set_title('formatted')
        plt.show()


if __name__=="__main__":
    # features can be 1D or 2D. When 2D it means that we want to display an image on the DMD
    source_2d = (20, 30)
    source_1d = 70
    target_shape_ = (80, 60)

    macro = macro_pixels_mapping(source_2d, target_shape_)
    lined = lined_mapping(source_1d, target_shape_)

    # X is source (feature vector), formatted_X is target (DMD)
    x1, formatted_x1 = sample_test(source_2d, target_shape_, macro)
    x2, formatted_x2 = sample_test(source_1d, target_shape_, lined)
    show(x1, formatted_x1)
    show(x2, formatted_x2)
