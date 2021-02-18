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
"""The code is written using the Keras Sequential API with a tf.GradientTape
training loop. This module implements the minmax game used to train a image-
conditioned GAN.

Generative Adversarial Networks (GANs) are one of the most interesting ideas in
computer science today. Two models are trained simultaneously by an adversarial
process. A generator("the artist") learns to create images that look real, while
a discriminator ("the art critic") learns to tell real images apart from fakes.

For more information about GANs see gan.py.

A conditional generative model p(x | c) can be obtained by adding c as input to
both G and D. Making the generation process dependent on an input data
distribution. This change allow image-conditional GANs to function as tools in
the field of image-to-image translation using paired data. A GAN tries to
predict the corresponding example from the target distribution using its
representation from the input data. Previous approacges have found it beneficial
to mix the GAN objective with a more traditional loss, such as L2 distance.
The discriminator's job remains unchanged, but the generator is tasked to not
only fool the discriminator but also to be near the ground truth output in an L2
sense.

Prior works have conditioned GANs on discrete labels, text and images.

(Paper: Image-to-image translation with conditional adversarial networks)
Without z, the net could still learn a mapping from x to y, but would produce
deterministic outputs, and therefore fail to match any distribution other than
a delta function. Past conditional GANs have acknowledged this and provided
Gaussian noise z as an input to the generator, in addition to x. In initial
experiments, we did not find this strategy effective – the generator simply
learned to ignore the noise. Instead, for our final models, we provide noise
only in the form of dropout, applied on several layers of our generator at both
training and test time. Despite the dropout noise, we observe only minor
stochasticity in the output of our nets. Designing conditional GANs that produce
highly stochastic output, and thereby capture the full entropy of the
conditional distributions they model, is an important question left open by the
present work.
"""
import logging
import os
import time
from datetime import datetime

import tensorflow as tf
from dnnlab.errors.dnnlab_exceptions import ModelNotCompiledError

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # FATAL
logging.getLogger("tensorflow").setLevel(logging.FATAL)


class cGAN():
    """Implements a image-conditioned gan learning model.

    Typical usage example:

        generator -> keras.model with input layer = dim input data &
                     output same dim than target data.
        discriminator -> keras.model with two inputs:
                         1. input data
                         2. target data

        # Define forward path.
        gan = cGAN(generator, discriminator)

        # Define optimizer.
        cgan.compile(lr_gen=1e-4, lr_disc=1e-4)

        # Start training process.
        cgan.fit(x_domain, y_domain, EPOCHS, save_ckpt=5)

        # Export both models.
        gan.export()

        use gan.restore("relative_path_to_logs") to continue training after
        a break.

    Attributes:
        generator (keras.model): Keras NN to act as the generator.
        discriminator (keras.model): Keras NN to act as the discriminator.
        generator_optimizer (keras.optimizer): Optimization alg for generator.
        discriminator_optimizer (keras.optimizer): Optimization alg for disc.
        init_timestamp (str): Acts as a unique folder identifier.
        logdir (str): Top level logdir.
        tensorboard (str): Path to tensorboard summary files.
        ckpt_dir (str): Path to ckpt files.
        ckpt_manager (tf.train.CheckpointManager): Deletes old checkpoints.
        checkpoint (tf.train.Checkpoint): Groups trackable objects, saving and
            restoring them.
    """
    def __init__(
            self,
            generator,
            discriminator,
            l1_weight=100,
    ):
        """Takes two keras.models that take part in the minmax game.
        Both models define the hypothesis set to our learning model.

        Args:
            generator (keras.model): Keras NN to act as the generator.
            discriminator (keras.model): Keras NN to act as the discriminator.
            l1_weight (int, optional): Weight coefficient for l1 loss to total
                loss. Default value from the original paper.
        """
        self.generator = generator
        self.discriminator = discriminator
        self.l1_weight = l1_weight
        self.generator_optimizer = None
        self.discriminator_optimizer = None
        self.init_timestamp = "cGAN-" + datetime.now().strftime(
            "%d%m%Y-%H%M%S")
        self.logdir = os.path.join("logs", self.init_timestamp)
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        self.ckpt_manager = None
        self.checkpoint = None

    def compile(self, optimizer="adam", lr_gen=1e-4, lr_disc=1e-4):
        """Defines the optimization part of the learning algorithm to our
        learning model.

        Args:
            optimizer (str, optional): Optimizer. Defaults to "adam".
            lr_gen (Float, optional): Learning rate generator. Defaults to 1e4.
            lr_disc (Float, optional): Learning rate discriminator.
                Defaults to 1e4.
        """
        # TODO: more optimizer
        if optimizer == "adam":
            self.generator_optimizer = tf.keras.optimizers.Adam(lr_gen)
            self.discriminator_optimizer = tf.keras.optimizers.Adam(lr_disc)

        if self.checkpoint is None:
            self.checkpoint = tf.train.Checkpoint(
                generator_optimizer=self.generator_optimizer,
                discriminator_optimizer=self.discriminator_optimizer,
                generator=self.generator,
                discriminator=self.discriminator)
            self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                           self.ckpt_dir,
                                                           max_to_keep=5)

    def fit(self,
            source_domain,
            target_domain,
            epochs,
            batch_size,
            len_dataset,
            save_ckpt=5,
            verbose=1,
            max_outputs=2,
            initial_step=0,
            mlflow=False):
        """Trains both models for n EPOCHS. Saves ckpts every n EPOCHS.
        The training loop together with the optimization algorithm define the
        learning algorithm.

        Args:
            input_domain (tf.dataset): Images that generator sees as input with
                shape(None, width, height, depth).
            target_domain (tf.dataset): Images that generator tries to translate
            to with shape(None, width, height, depth).
            epochs (int): Number of epochs.
            save_ckpt (int): Save ckpts every n Epochs.
            verbose (int, optional): Keras Progbar verbose lvl. Defaults to 1.
            max_outputs (int, optional): Number of images shown in TB.
                Defaults to 2.
            initial_step (int): Step at which to start training. Useful for
                resuming a previous run.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """
        if self.generator_optimizer is None:
            raise ModelNotCompiledError("use conGAN.compile() first.")
        if mlflow:
            import mlflow  # pylint: disable=import-outside-toplevel

        # Retrace workaround @function signature only tensors.
        step = tf.Variable(initial_step, name="step", dtype=tf.int64)

        num_batches = len_dataset / batch_size
        # Keras Progbar
        progbar = tf.keras.utils.Progbar(target=num_batches, verbose=verbose)
        file_writer = tf.summary.create_file_writer(self.tensorboard)
        file_writer.set_as_default()

        # Iterate over all epochs.
        for epoch in range(epochs):
            step_float = 0
            start = time.time()
            for input_images, target_images in zip(source_domain,
                                                   target_domain):
                imgs = self.train_step(input_images, target_images, step,
                                       file_writer)
                # TODO Workaround. summary image & gpu usage
                with file_writer.as_default():  # pylint: disable=not-context-manager
                    tf.summary.image("source", imgs[0], step=step)
                    tf.summary.image("target", imgs[1], step=step)
                    tf.summary.image("fake_target", imgs[2], step=step)

                file_writer.flush()
                progbar.update(current=(step_float))
                step_float += 1
                step.assign(step + 1)

            # Save the model every n epochs
            if (epoch + 1) % save_ckpt == 0:
                ckpt_save_path = self.ckpt_manager.save()
                print("\nSaving checkpoint for epoch {} at {}".format(
                    epoch + 1, ckpt_save_path))

            print(" - Epoch {} finished in {} sec\n".format(
                epoch + 1, int(time.time() - start)))

    def restore(self, ckpt_path):
        """Restore model weights from the latest checkpoint.

        Args:
            ckpt_path (str): Relative path to ckpt files.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """

        restore_path = os.path.dirname(ckpt_path)
        self.logdir = restore_path
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        if self.ckpt_manager is None:
            raise ModelNotCompiledError("use conGAN.compile() first.")
        self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                       self.ckpt_dir,
                                                       max_to_keep=5)
        # if a checkpoint exists, restore the latest checkpoint.
        if self.ckpt_manager.latest_checkpoint:
            self.checkpoint.restore(self.ckpt_manager.latest_checkpoint)
            print("Latest checkpoint restored!!")
        else:
            print("Can not find ckpt files at {}".format(ckpt_path))

    def export(self, model_format="hdf5"):
        """Exports the trained models in hdf5 or SavedModel format.

        Args:
            model_format (str, optional): SavedModel or HDF5. Defaults to hdf5.
        """
        model_dir = os.path.join(self.logdir, "models")
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if model_format == "hdf5":
            self.generator.save(os.path.join(model_dir, "generator.h5"))
            self.discriminator.save(os.path.join(model_dir,
                                                 "discriminator.h5"))

        elif model_format == "SavedModel":
            self.generator.save(os.path.join(model_dir, "generator"))
            self.discriminator.save(os.path.join(model_dir, "discriminator"))

    @tf.function
    def train_step(self, source_images, target_images, step, file_writer):
        """Decorated function (@tf.function) that creates a callable tensorflow
        graph from a python function.
        """

        with file_writer.as_default():
            # Record gradients for generator and discriminator for each seperate
            # training step.
            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                fake_target = self.generator(source_images, training=True)
                disc_real_target = self.discriminator(
                    [source_images, target_images], training=True)
                disc_fake_target = self.discriminator(
                    [source_images, fake_target], training=True)

                gen_loss = self.generator_loss(disc_fake_target, fake_target,
                                               target_images, self.l1_weight)
                tf.summary.scalar("generator_loss", gen_loss, step=step)

                disc_loss = self.discriminator_loss(disc_real_target,
                                                    disc_fake_target)
                tf.summary.scalar("discriminator_loss", disc_loss, step=step)

            gradients_of_generator = gen_tape.gradient(
                gen_loss, self.generator.trainable_variables)
            # Compute the euclidean vector norm L2 for the gradients of the
            # generator.
            # GradientTape.gradient() returns a list of Tensors, one for each
            # element in sources. Returned structure is the same as the
            # structure of sources.
            gradient_norm_generator = tf.linalg.global_norm(
                gradients_of_generator)
            tf.summary.scalar("gen_gradient_norm_l2",
                              gradient_norm_generator,
                              step=step)

            gradients_of_discriminator = disc_tape.gradient(
                disc_loss, self.discriminator.trainable_variables)
            # Compute the euclidean vector norm L2 for the gradients of the
            # discriminator.
            gradient_norm_discriminator = tf.linalg.global_norm(
                gradients_of_discriminator)
            tf.summary.scalar("disc_gradient_norm_l2",
                              gradient_norm_discriminator,
                              step=step)

            self.generator_optimizer.apply_gradients(
                zip(gradients_of_generator,
                    self.generator.trainable_variables))
            self.discriminator_optimizer.apply_gradients(
                zip(gradients_of_discriminator,
                    self.discriminator.trainable_variables))
            imgs = [source_images, target_images, fake_target]
            # Piece of shit workaround.
            return imgs

    @staticmethod
    def discriminator_loss(real, fake):
        """This method quantifies how well the discriminator is able to
        distinguish real images from fakes. It compares the discriminator's
        predictions on real images to an array of 1s, and the discriminator's
        predictions on fake (generated) images to an array of 0s.

        Args:
            real_image: Image from the original dataset.
            generated_image: Images generated by the generator.
        """
        # This method returns a helper function to compute cross entropy loss.
        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        # Compares real images to tensors of 1 -> if real output 1s
        real_loss = cross_entropy(tf.ones_like(real), fake)
        # Compares generated images to tensors of 0 -> if generated output 0s
        fake_loss = cross_entropy(tf.zeros_like(fake), fake)

        total_loss = real_loss + fake_loss
        return total_loss

    @staticmethod
    def generator_loss(fake_output, gen_output, target, l1_weight):
        """The generator's loss quantifies how well it was able to trick the
           discriminator. Intuitively, if the generator is performing well, the
           discriminator will classify the generated images as real (or 1).
           Here, we will compare the discriminators decisions on the generated
           images to an array of 1s. In addition, the generated images are
           compared to the target images to bind the generators output closer
           to the target images.

        Args:
            fake_output: Prob. array of discriminator's performance on fake data
            gen_output: Generated images.
            target: Target images (ground truth).
        """
        # Additional term to GAN objective.
        l1_loss = tf.reduce_mean(tf.abs(target - gen_output))
        # This method returns a helper function to compute cross entropy loss.
        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        gan_loss = cross_entropy(tf.ones_like(fake_output), fake_output)

        total_loss = gan_loss + (l1_weight * l1_loss)
        return total_loss
