from torchvision.transforms import Compose

def conditional_compose(*transform_list):
    """Creates a Compose transform out of all non-None entries, 
    which are simply discarded.

    This is useful for defining a search space over image transforms, so that
    the final transform is a composition of entries which can be [None, <some
    transform>] without requiring making many lists at once.
    """
    composition_list = filter(lambda x: x is not None, transform_list)
    return Compose(composition_list)
