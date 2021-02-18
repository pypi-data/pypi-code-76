# Copyright 2019 Tobias Höfer
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
"""Create adversarial inputs formed by applying small but intentionally
worst-case perturbations to examples, such that the perturbed input results in
the model outputting an incorrect answer with high confidence.

Paper: https://arxiv.org/abs/1412.6572

This module implements a white box attack called fast gradient sign method to
generate adversarial examples.

The fast gradient sign method works by using the gradients of the neural network
to create an adversarial example. For an input image, the method uses the
gradients of the loss with respect to the input image to create a new image that
maximises the loss. This new image is called the adversarial image.

A perturbation is a matrix of [-1;0;+1] indicating the pixels value to create an
adversarial example. The idea is to multiply this matrix with a small but still
large enough value ɛ to fool the network.

    Adversarial_image = input_image + ɛ * perturbations.


Adversarial attacks can be categorized into white box and black box attacks.
White box attacks use the gradient of a model.
Black box attacks have no access to the gradient but use the models output.

Defense strategies:
-------------------
                ! Hiding the gradient doesn't work !

Adversarial examples generalize well and fool different learning models.
An intriguing aspect of adversarial examples is that an example generated for
one model is often misclassified by other models, even when they have different
architecures or were trained on dis- joint training sets. Moreover, when these
different models misclassify an adversarial example, they often agree with each
other on its class.

    1. Reactive Strategy: Define a second NN to act as a gateway model and
                          discards adversarial examples. This approach needs
                          double the infrastructure and is not ideal.

    2. Proactive Strategy: Use adversarial examples in the inner loop of the
                           training process to make the models more robust.
                           Adv. examples are also a great regularizer but this
                           approach has currently a tradeoff between stability
                           and accuracy.
"""
import logging
import os

import tensorflow as tf

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # FATAL
logging.getLogger("tensorflow").setLevel(logging.FATAL)


class FGSM():  # pylint: disable=too-few-public-methods
    """Implements fast gradient sign method (FGSM) to create adversarial
    examples.

        loss = tf.keras.losses.CategoricalCrossentropy()
        fgsm = FGSM(model, loss)
        perturbations = fgsm.create_adversarial_pattern(input_image,input_label)

        # Eps: Multiplier to ensure the perturbations are small.
        adv_x = image + eps*perturbations

fake_output
    Attributes:
        model (keras.model): NN to fool.
        loss: Loss used to train model.
    """
    def __init__(self, model, loss=None):
        self.model = model
        self.model.trainable = False
        if loss is None:
            # Default softmax + crossentropy.
            self.loss = tf.keras.losses.CategoricalCrossentropy()
        else:
            self.loss = loss

    def create_adversarial_pattern(self, input_image, input_label):
        """Calcualtes the signed gradient of the objective function with respect
        to the input image.

        Args:
            input_image (tensor, dtype=tf.float32): Tensor of shape=(1,x,y).
            input_label (tensor, dtype=tf.float32): Tensor of shape=(n_casses,)
                                                    one_hot_encoded!.

        Returns:
            signed_grad(tensor): Perturbations for a specific input image.
        """
        with tf.GradientTape() as tape:
            # Gradients with respect to the image.
            tape.watch(input_image)
            prediction = self.model(input_image)
            loss = self.loss(input_label, prediction)

        # Get the gradients of the loss w.r.t to the input image.
        gradient = tape.gradient(loss, input_image)
        # Get the sign of the gradients to create the perturbation
        signed_grad = tf.sign(gradient)
        return signed_grad
