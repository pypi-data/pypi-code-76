import time

from lightonml.internal.controller import LinearController
from lightonml.internal.device import OpuDevice
from lightonml.internal.types import PhotonicCoreType


class LinearOpuDevice(OpuDevice):
    """Interface to Linear OPU hardware resources: device and controller"""
    core_type = PhotonicCoreType.lazuli

    def __init__(self, opu_type: str, frametime_us: int,
                 exposure_us: int, low_value, start_with_low, port,
                 min_delta_transforms_ms, name="opu"):
        self.min_delta_transforms_ms = min_delta_transforms_ms
        assert opu_type != "type1", "Unsupported OPU type"

        super().__init__(opu_type, frametime_us, exposure_us,  name=name,
                         sequence_nb_prelim=0)
        self.controller = LinearController(1024, exposure_us, low_value,
                                           start_with_low, port, self.verbose)
        # End time of latest transform, to make sure they respect minimum time between two
        self._transform_last = 0.

    # Override exposure with sending value to controller as well
    @property
    def exposure_us(self):
        return super().exposure_us

    @exposure_us.setter
    def exposure_us(self, value):
        if self.controller.exposure_us != value:
            self.controller.exposure_us = value
        # We want to set upper class property but sadly we can't say
        # super().exposure_us = value :(
        # See https://stackoverflow.com/questions/10810369/

        # noinspection PyArgumentList
        OpuDevice.exposure_us.fset(self, value)

    @property
    def transform_size(self):
        """Number of vectors in the transform.
        This is the user transform size, so for Lazuli, half of the raw total batch"""
        return self.controller.batch_size

    @transform_size.setter
    def transform_size(self, value):
        if self.controller.batch_size != value:
            self.controller.batch_size = value

    def transform_wait(self):
        """Make sure we wait for at least min_delta_transforms between successive transforms"""
        if self._transform_last:
            # Prevent successive transforms time being too short
            delta = time.perf_counter() - self._transform_last
            # Convert to seconds
            min_delta = self.min_delta_transforms_ms / 1000.
            if delta < min_delta:
                # Need to wait. Apply an additional 10% security time
                sleep_time = 1.1 * (min_delta - delta)
                self._debug(f"Sleeping for {1000. * sleep_time:.1f} ms")
                time.sleep(sleep_time)
            # In anyways check back that min_delta between transforms is respected
            assert time.perf_counter() - self._transform_last >= min_delta

    def transform_finished(self):
        """To be called at the end of the transform by user code"""
        self._transform_last = time.perf_counter()

    def open(self):
        if self.active:
            return
        # Open the device first, since it has a guard again concurrent use
        super().open()
        self.controller.open()

    def close(self):
        self.controller.close()
        super().close()
