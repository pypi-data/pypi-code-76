"""
Contains the video class the provides the main video related functionality
"""

import numpy as np
import OrcFxAPI as ofx

from . import DEFAULT_WIDTH, DEFAULT_HEIGHT


class Video:
    """
    Record videos from orcaflex simulations. Provides a wrapper around the AVI
    functionality from the orcaflex API
    """

    codec_map = {ofx.gmWireFrame: "MRLE", ofx.gmShaded: "XVID"}

    @classmethod
    def avi_from_ofx(
        cls,
        model,
        file_path,
        start_time,
        end_time,
        width=None,
        height=None,
        codec=None,
        view_parameters=None,
    ):
        """
        Create an .avi video file from an orcaflex model. Wrapper around
        `ofx.AVIFile` and related methods from the orcaflex API to create a
        video saved locally

        :param model            An instance of OrcFxAPI.Model
        :param file_path        The path to the .avi file to create
        :param start_time       The start time in the model to start recording
        :param end_time         The end time in the model to stop the recording
        :param width            The width of the video in pixels. Default 400
        :param height           The height of the video in pixels. Default 400
        :param codec            The codec of the video. Values accepted from
                                the OrcFxAPI are "MRLE" and "XVID".
                                Defaults  the codec that corresponds to the
                                default GraphicsMode
        :param view_parameters  An optional instance of OrcFxAPI viewParameters
        """
        interval = model["General"].ActualLogSampleInterval
        width = width or DEFAULT_WIDTH
        height = height or DEFAULT_HEIGHT
        if codec is None:
            if view_parameters is None:
                codec = cls.codec_map[model.defaultViewParameters.GraphicsMode]
            else:
                codec = cls.codec_map[view_parameters.GraphicsMode]
        avi_file = ofx.AVIFile(
            filename=file_path,
            codec=codec,
            interval=interval,
            width=width,
            height=height,
        )
        draw_time_arr = np.linspace(
            start=start_time,
            stop=end_time,
            num=int(round((end_time - start_time) / interval, 0)) + 1,
        )
        for draw_time in draw_time_arr:
            avi_file.AddFrame(model, draw_time, viewParameters=view_parameters)
        avi_file.Close()
