# Copyright 2019 Kevin Hirschmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import os 
import glob
import random
import tensorflow as tf 

class PerClassBatchSampler:
    """Retrieves N samples from K classes, total batch size B = N * K.
    Used for TripletMining and OnlineTripletLoss.
    """

    def __init__(self, data_path, num_classes: int, num_samples: int):
        self.all_images = self.generate_all_images_dict(data_path)
        self.batch_size = num_classes * num_samples
        self.num_classes = num_classes
        self.num_samples = num_samples

    
    def generate_all_images_dict(self, data_path):
        """Generate a dictionary between a label and all of the corresponding images.

        Args:
            data_path (string): path to the image folder

        Returns:
            all_images_to_label ({label: [images]}, {string: [strings]}): dictonary - all image_path for one label
        """

        all_images_to_label = {}

        labels = os.listdir(data_path)
        # MacOS specific subfolder which is used for the Finder
        if '.DS_Store' in labels: 
            labels.remove(".DS_Store")

        label_folders = [os.path.abspath(os.path.join(data_path, i)) for i in labels]

        # convert string labels to int values
        # better to handle during input pipeline because data is converted to bytes
        labels = [i for i in range(len(labels))]

        i = 0
        for label_folder in label_folders:
            files = os.listdir(label_folder)
            files = [os.path.abspath(os.path.join(label_folder, i)) for i in files]

            all_images_to_label[labels[i]] = files
            i += 1
        
        self.num_images = sum(len(v) for v in all_images_to_label.values())

        return all_images_to_label


    def get_data(self):
        """Sampling/Iteration function for tf.data.Dataset.from_generator.
        """
        count = 0
        while count + self.batch_size < self.num_images:
            class_labels = random.sample(self.all_images.keys(), self.num_classes)

            images = []
            labels = []
            for class_label in class_labels:
                labels += ([class_label] * self.num_samples)
                samples = random.sample(self.all_images[class_label], self.num_samples)
                images += samples
            
            count += self.batch_size

            yield images, labels



class TripletDataset:
    """Custom Datset class for use of PerClassBatchSampler
    With this Triplet Mining can be applied.

    The Datafolder/-set should have the following structure:
    - class 1
        - img1_class1
        - img2_class1
        - ...
    - class 2
        - img1_class2
        - img2_class2
        - ...
    - class 3
        - img1_class3
        - img2_class3
        - ...
    - ...

    """

    def __init__(self, data_path, num_classes, num_samples, target_size=[128,128]):
        self.data_path = data_path
        self.num_classes = num_classes
        self.num_samples = num_samples
        self.batch_size = num_classes * num_samples
        self.target_size = target_size

        self.sampler = PerClassBatchSampler(data_path=data_path,
                        num_classes=num_classes, num_samples=num_samples)

        self.next_sample = self.build_iterator(self.sampler)

    def build_iterator(self, sampler):
        """Build an iteratable dataset with use of a custom sampler for triplet networks.

        Args:
            sampler: data sampler to produce triplets of samples

        Returns:
            dataset (tf.Dataset): tf.Dataset for training/validation/testing

        """
        prefetch_buffer = 5
        # let’s tensorflow know that it’s going to be fed by our pythonic generator.
        # we need to specify the types of the outputs that the generator is going to generate
        dataset = tf.data.Dataset.from_generator(self.sampler.get_data,
                output_types=(tf.string, tf.int16))

        # with map(...) set up all the tasks necessary 
        # to get from the generator input (file names) to tensors and labels
        # this is now a dataset of decoded (images, labels) pairs
        dataset = dataset.map(self._read_image_and_resize)
        dataset = dataset.cache()

        return dataset # this gets fed into model.fit(...) as data



    def _read_image_and_resize(self, images, labels):
        """Read an image and resize it to a given target size. 
        This function is properly used in combination with tf.Dataset's "map"-function.

        Args:
            images (string): filenames of images
            labels (string): label names

        Returns:
            mapped_images (tf.tensor): read and resized images
            labels (tf.tensor): corresponding labels
        """
        mapped_images = []
        mapped_labels = []
        for i in range(self.batch_size):
            bits = tf.io.read_file(images[i]) # read file as bytes
            image = tf.io.decode_image(bits) # decode bytes as images

            label = labels[i]# extract label

            # let tensorflow know that the loaded images have unknown dimensions, 
            # and 3 color channels (rgb)
            image.set_shape([None, None, 3])

            # resize to model input size
            image_resized = tf.image.resize(image, self.target_size)
            mapped_images.append(image_resized)
            mapped_labels.append(label)
            
        # return images and labels
        return mapped_images, mapped_labels



def create_dataset(data_path, num_classes, num_samples, target_size=[128,128]):
    """Create a TripletDataset with internal use of tf.Dataset for running the triplet network.

    Args:
        data_path (string): path to the directory where the images are
        num_classes (int): number of classes which are sampled for one batch
        num_samples (int): number of samples per class which are sampled for one batch
        target_size ([int, int]): prefered size of images

    Returns:
        dataset (TripletDataset): dataset used for traning/running the triplet network
    """
    dataset = TripletDataset(data_path, num_classes, num_samples, target_size=[128,128])
    return dataset.next_sample 