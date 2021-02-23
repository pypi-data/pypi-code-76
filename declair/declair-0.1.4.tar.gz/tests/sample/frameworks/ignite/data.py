# Needs to load data from:
# https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html#sklearn.datasets.load_digits

from sklearn.datasets import load_digits
from torch.utils.data import Dataset
from torchvision import transforms

from declair.frameworks.ignite.data import get_split_loaders as declair_get_split_loaders

# This is an ordinary PyTorch dataset definition
class DigitsDataset(Dataset):
    """The sklearn digits dataset in PyTorch form."""
    def __init__(self, transform=None):
        data = load_digits()
        self.images = data['images'].astype('float32')
        self.labels = data['target']
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        if self.transform:
            image = self.transform(image)
        label = self.labels[idx]
        return image, label

def get_split_loaders(batch_size, seed=42, dataset_params=None):
    return declair_get_split_loaders(DigitsDataset, batch_size,
        dataset_params=dataset_params, seed=seed,
                             splits=(0.7, 0.9))

def rotation_transform(max_degrees):
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.RandomRotation(max_degrees),
        transforms.ToTensor()
    ])
