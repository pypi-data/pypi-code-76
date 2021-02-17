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
training loop. This module implements the minmax game used to train a cylce GAN.

Generative Adversarial Networks (GANs) are one of the most interesting ideas in
computer science today. Two models are trained simultaneously by an adversarial
process. A generator("the artist") learns to create images that look real, while
a discriminator ("the art critic") learns to tell real images apart from fakes.
"""
import os
import time
from datetime import datetime

import tensorflow as tf
from dnnlab.errors.dnnlab_exceptions import ModelNotCompiledError


class CycleGAN():
    """Implements a cylce gan learning model.

    Attributes:
        generator_target (keras.model): Generates target images from source.
        generator_source(keras.model): Generates source images from targets.
        discriminator_target (keras.model): Compares fake targets to real ones.
        discriminator_source(keras.model): Compares fake sources to real ones.
        generator_target_optimizer (keras.optimizer): Optimization alg for
            generator_target.
        generator_source_optimizer (keras.optimizer): Optimization alg for
            generator_source.
        discriminator_target_optimizer (keras.optimizer): Optimization alg for
            discriminator_target.
        discriminator_source_optimizer (keras.optimizer): Optimization alg for
            discriminator_source.
        init_timestamp (str): Acts as a unique folder identifier.
        logdir (str): Top level logdir.
        tensorboard (str): Path to tensorboard summary files.
        ckpt_dir (str): Path to ckpt files.
        ckpt_manager (tf.train.CheckpointManager): Deletes old checkpoints.
        checkpoint (tf.train.Checkpoint): Groups trackable objects, saving and
            restoring them.
    """
    def __init__(self,
                 generator_target,
                 generator_source,
                 discriminator_target,
                 discriminator_source,
                 alpha_disc=0.5,
                 alpha_identity=0.5,
                 lambda_cycle=10):
        """Takes four keras.models that take part in the cycling gan game.

        Args:
            generator_target (keras.model): Generates target imgs from sources.
            generator_source(keras.model): Generates source imgs from targets.
            discriminator_target(keras.model): Compares fake/real targets.
            discriminator_source(keras.model): Compares fake/real sources.
        """
        self.generator_target = generator_target
        self.generator_source = generator_source
        self.discriminator_target = discriminator_target
        self.discriminator_source = discriminator_source
        self.alpha_disc = alpha_disc
        self.alpha_identity = alpha_identity
        self.lambda_cycle = lambda_cycle
        self.generator_target_optimizer = None
        self.generator_source_optimizer = None
        self.discriminator_target_optimizer = None
        self.discriminator_source_optimizer = None
        self.init_timestamp = "CycleGAN-" + datetime.now().strftime(
            "%d%m%Y-%H%M%S")
        self.logdir = os.path.join("logs", self.init_timestamp)
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        self.ckpt_manager = None
        self.checkpoint = None

    def compile(self,
                optimizer="adam",
                lr_gen_target=1e-4,
                lr_gen_source=1e-4,
                lr_disc_target=1e-4,
                lr_disc_source=1e-4):
        """Defines the optimization part of the learning algorithm to our
        learning model.

        Args:
            optimizer (str, optional): [description]. Defaults to "adam".
            lr_gen_g ([type], optional): [description]. Defaults to 1e4.
            lr_gen_f ([type], optional): [description]. Defaults to 1e4.
            lr_disc_y ([type], optional): [description]. Defaults to 1e4.
            lr_disc_x ([type], optional): [description]. Defaults to 1e4.
        """
        if optimizer == "adam":
            self.generator_target_optimizer = tf.keras.optimizers.Adam(
                lr_gen_target)
            self.generator_source_optimizer = tf.keras.optimizers.Adam(
                lr_gen_source)
            self.discriminator_target_optimizer = tf.keras.optimizers.Adam(
                lr_disc_target)
            self.discriminator_source_optimizer = tf.keras.optimizers.Adam(
                lr_disc_source)

        if self.checkpoint is None:
            self.checkpoint = tf.train.Checkpoint(
                generator_target=self.generator_target,
                generator_source=self.generator_source,
                discriminator_target=self.discriminator_target,
                discriminator_source=self.discriminator_source,
                generator_target_optimizer=self.generator_target_optimizer,
                generator_source_optimizer=self.generator_source_optimizer,
                discriminator_target_optimizer=self.
                discriminator_target_optimizer,
                discriminator_source_optimizer=self.
                discriminator_source_optimizer)
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
        """Trains all four models for n EPOCHS. Saves ckpts every n EPOCHS.
        The training loop together with the optimization algorithm define the
        learning algorithm.

        Args:
            source_domain (tf.dataset): Images that generator sees as source
                with shape(None, width, height, depth).
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
        if self.generator_target_optimizer is None:
            raise ModelNotCompiledError("use CycleGAN.compile() first.")
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
            for source_images, target_images in zip(source_domain,
                                                    target_domain):
                imgs = self.train_step(source_images, target_images, step,
                                       file_writer)

                # TODO Workaround. summary image & gpu usage
                with file_writer.as_default():  # pylint: disable=not-context-manager
                    tf.summary.image("source", imgs[0], step=step)
                    tf.summary.image("target", imgs[1], step=step)
                    tf.summary.image("fake_source", imgs[2], step=step)
                    tf.summary.image("fake_target", imgs[3], step=step)
                    tf.summary.image("cycled_source", imgs[4], step=step)
                    tf.summary.image("cycled_target", imgs[5], step=step)

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
            raise ModelNotCompiledError("use cycleGAN.compile() first.")
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
            self.generator_target.save(
                os.path.join(model_dir, "generator_target.h5"))
            self.generator_source.save(
                os.path.join(model_dir, "generator_source.h5"))
            self.discriminator_target.save(
                os.path.join(model_dir, "discriminator_target.h5"))
            self.discriminator_source.save(
                os.path.join(model_dir, "discriminator_source.h5"))

        elif model_format == "SavedModel":
            self.generator_target.save(
                os.path.join(model_dir, "generator_target"))
            self.generator_source.save(
                os.path.join(model_dir, "generator_source"))
            self.discriminator_target.save(
                os.path.join(model_dir, "discriminator_target"))
            self.discriminator_source.save(
                os.path.join(model_dir, "discriminator_source"))

    @tf.function
    def train_step(self, source_images, target_images, step, file_writer):
        """Decorated function (@tf.function) that creates a callable tensorflow
        graph from a python function.
        """
        with file_writer.as_default():
            # Record gradients for generator and discriminator for each seperate
            # training step.
            with tf.GradientTape(persistent=True) as tape:
                # Forward cycle consistency loss.
                # Source -> Target (single)
                fake_target = self.generator_target(source_images,
                                                    training=True)
                # Source -> Target -> Source (cycle)
                cycled_source = self.generator_source(fake_target,
                                                      training=True)

                # Backward cycle consistency loss.
                # Target -> Source (single)
                fake_source = self.generator_source(target_images,
                                                    training=True)
                # Target -> Source -> Target (cycle)
                cycled_target = self.generator_target(fake_source,
                                                      training=True)

                # Identity loss.
                same_source = self.generator_source(source_images,
                                                    training=True)
                same_target = self.generator_target(target_images,
                                                    training=True)

                # Detect real images.
                disc_real_source = self.discriminator_source(source_images,
                                                             training=True)
                disc_real_target = self.discriminator_target(target_images,
                                                             training=True)

                # Detect fake images.
                disc_fake_source = self.discriminator_source(fake_source,
                                                             training=True)
                disc_fake_target = self.discriminator_target(fake_target,
                                                             training=True)

                # Calculate the adversarial loss.
                gen_target_loss = self.generator_loss(disc_fake_target)
                gen_source_loss = self.generator_loss(disc_fake_source)

                # Calculate the cycle consistency loss.
                total_cycle_loss = self.cycle_consistency_loss(
                    source_images,
                    cycled_source) + self.cycle_consistency_loss(
                        target_images, cycled_target)

                # Total generator loss = adversarial + cycle + identity
                total_gen_target_loss = gen_target_loss + \
                    self.lambda_cycle * total_cycle_loss + \
                    self.identity_loss(target_images, same_target,
                                       self.alpha_identity)

                total_gen_source_loss = gen_source_loss + \
                    self.lambda_cycle * total_cycle_loss + \
                    self.identity_loss(source_images, same_source,
                                       self.alpha_identity)

                tf.summary.scalar("gen_target_loss",
                                  total_gen_target_loss,
                                  step=step)
                tf.summary.scalar("gen_source_loss",
                                  total_gen_source_loss,
                                  step=step)

                # Total discriminator loss.
                disc_source_loss = self.discriminator_loss(
                    disc_real_source, disc_fake_source, self.alpha_disc)
                disc_target_loss = self.discriminator_loss(
                    disc_real_target, disc_fake_target, self.alpha_disc)
                tf.summary.scalar("disc_source_loss",
                                  disc_source_loss,
                                  step=step)
                tf.summary.scalar("disc_target_loss",
                                  disc_target_loss,
                                  step=step)

            gradients_of_generator_target = tape.gradient(
                total_gen_target_loss,
                self.generator_target.trainable_variables)
            gradients_of_generator_source = tape.gradient(
                total_gen_source_loss,
                self.generator_source.trainable_variables)
            gradients_of_discriminator_target = tape.gradient(
                disc_target_loss,
                self.discriminator_target.trainable_variables)
            gradients_of_discriminator_source = tape.gradient(
                disc_source_loss,
                self.discriminator_source.trainable_variables)

            self.generator_target_optimizer.apply_gradients(
                zip(gradients_of_generator_target,
                    self.generator_target.trainable_variables))
            self.generator_source_optimizer.apply_gradients(
                zip(gradients_of_generator_source,
                    self.generator_source.trainable_variables))
            self.discriminator_target_optimizer.apply_gradients(
                zip(gradients_of_discriminator_target,
                    self.discriminator_target.trainable_variables))
            self.discriminator_source_optimizer.apply_gradients(
                zip(gradients_of_discriminator_source,
                    self.discriminator_source.trainable_variables))

            imgs = [
                source_images, target_images, fake_source, fake_target,
                cycled_source, cycled_target
            ]
            # Piece of shit workaround.
            return imgs

    @staticmethod
    def discriminator_loss(real, fake, alpha_disc):
        """This method quantifies how well the discriminator is able to
        distinguish real images from fakes. It compares the discriminator's
        predictions on real images to an array of 1s, and the discriminator's
        predictions on fake (generated) images to an array of 0s.

        Args:
            real_image ([type]): [description]
            generated_image ([type]): [description]
        """
        # TODO mean least square loss for stability.
        # This method returns a helper function to compute cross entropy loss.
        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        # Compares real images to tensors of 1 -> if real output 1s
        real_loss = cross_entropy(tf.ones_like(real), real)
        # Compares generated images to tensors of 0 -> if generated output 0s
        fake_loss = cross_entropy(tf.zeros_like(fake), fake)

        total_loss = alpha_disc * (real_loss + fake_loss)
        return total_loss

    @staticmethod
    def generator_loss(disc_decision):
        """The generator's loss quantifies how well it was able to trick the
           discriminator. Intuitively, if the generator is performing well, the
           discriminator will classify the fake images as real (or 1).
           Here, we will compare the discriminators decisions on the generated
           images to an array of 1s.
        """
        # TODO mean least square loss for stability.
        # least_squared_loss = tf.keras.losses.MeanSquaredError()
        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        return cross_entropy(tf.ones_like(disc_decision), disc_decision)

    @staticmethod
    def cycle_consistency_loss(real_image, cycled_image):
        """Cycle consistency means the result should be close to the original
        source. For example, if one translates a sentence from English to French
        and then translates it back from French to English, then the resulting
        sentence should be the same as the original sentence.
        """
        # Calculate mean absolute error between orig and cycled.
        return tf.reduce_mean(tf.abs(real_image - cycled_image))

    @staticmethod
    def identity_loss(real_image, same_image, alpha_identity):
        """[summary]
        """
        loss = alpha_identity * (tf.reduce_mean(
            tf.abs(real_image - same_image)))
        return loss
