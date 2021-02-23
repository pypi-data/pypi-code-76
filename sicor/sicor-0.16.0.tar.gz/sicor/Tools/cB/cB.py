import logging
import numpy as np

from sicor.Mask import S2Mask
from sicor.Tools import majority_mask_filter


class S2cB(object):
    def __init__(self, cb_clf, mask_legend, clf_to_col, processing_tiles=11, logger=None):

        self.logger = logger or logging.getLogger(__name__)

        self.cb_clf = cb_clf
        self.mask_legend = mask_legend
        self.clf_to_col = clf_to_col
        self.processing_tiles = processing_tiles

        self.S2_MSI_channels = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11',
                                'B12']

        unique_channel_list = []
        for clf_ids in cb_clf.mk_clf.classifiers_id:
            unique_channel_list += list(clf_ids)
        self.unique_channel_ids = np.unique(unique_channel_list)
        self.unique_channel_str = [self.S2_MSI_channels[ii] for ii in self.unique_channel_ids]

    def __mk_nv__(self, data):

        if hasattr(self.cb_clf, "nvc"):
            bf = self.cb_clf.mk_clf(data.reshape((-1, data.shape[-1])))
            nv = self.cb_clf.nvc.predict(bf).reshape(data.shape[:2])
            nv[nv < 0] = 0
            nv[nv > 0] = 1
            return np.array(nv, dtype=np.uint8)
        else:
            return None

    def __call__(self, img, target_resolution=None, majority_filter_options=None, nodata_value=255):
        if img.target_resolution is None:

            channel_ids = np.unique([item for sublist in self.cb_clf.mk_clf.classifiers_id_full for item in sublist])
            cb_channels = [self.cb_clf.mk_clf.id2name[channel_id] for channel_id in channel_ids]
            self.cb_clf.mk_clf.adjust_classifier_ids(full_bands=self.cb_clf.mk_clf.id2name,
                                                     band_lists=cb_channels)
            data = img.image_subsample(channels=cb_channels, target_resolution=target_resolution)

            nv = self.__mk_nv__(data)

            good_data = img.nodata[target_resolution] == np.False_
            bad_values = img.nodata[target_resolution]

            mask_shape = [img.metadata["spatial_samplings"][target_resolution][ii] for ii in ["NCOLS", "NROWS"]]
            mask_array = np.empty(mask_shape, dtype=np.float32)
            mask_conf = np.empty(mask_shape, dtype=np.float32)

            mask_array[:] = np.nan
            mask_conf[:] = np.nan

            if self.processing_tiles == 0:
                mask_array[good_data], mask_conf[good_data] = self.cb_clf.predict_and_conf(
                    data[good_data, :], bad_data_value=nodata_value)
            else:
                line_segs = np.linspace(0, mask_shape[0], self.processing_tiles, dtype=int)
                for ii, (i1, i2) in enumerate(zip(line_segs[:-1], line_segs[1:])):
                    self.logger.info("Processing lines segment %i of %i -> %i:%i" %
                                     (ii + 1, self.processing_tiles, i1, i2))

                    ma, mc = self.cb_clf.predict_and_conf(
                        data[i1:i2, :, :][good_data[i1:i2, :], :], bad_data_value=nodata_value)
                    maf = np.empty(good_data[i1:i2, :].shape, dtype=np.float32)
                    mcf = np.empty(good_data[i1:i2, :].shape, dtype=np.float32)
                    maf[:] = np.nan
                    mcf[:] = np.nan

                    maf[good_data[i1:i2, :]], mcf[good_data[i1:i2, :]] = ma, mc
                    mask_array[i1:i2, :], mask_conf[i1:i2, :] = maf, mcf

        else:
            if target_resolution is not None:
                raise ValueError("target_resolution should only be given if target_resolution=None for the S2 image.")

            self.cb_clf.mk_clf.adjust_classifier_ids(full_bands=img.full_band_list,
                                                     band_lists=img.band_list)
            if self.processing_tiles == 0:
                mask_array, mask_conf = self.cb_clf.predict_and_conf(img.data, bad_data_value=nodata_value)
                mask_array = np.array(mask_array, dtype=float)
                mask_conf = np.array(mask_conf, dtype=float)
            else:
                mask_array = np.empty(img.data.shape[:2], dtype=np.float32)
                mask_conf = np.empty(img.data.shape[:2], dtype=np.float32)
                mask_array[:] = np.nan
                mask_conf[:] = np.nan

                line_segs = np.linspace(0, img.data.shape[0], self.processing_tiles, dtype=int)
                for ii, (i1, i2) in enumerate(zip(line_segs[:-1], line_segs[1:])):
                    self.logger.info(
                        "Processing lines segment %i of %i -> %i:%i" % (ii + 1, self.processing_tiles, i1, i2))
                    mask_array[i1:i2, :], mask_conf[i1:i2, :] = self.cb_clf.predict_and_conf(
                        img.data[i1:i2, :, :], bad_data_value=nodata_value)

            bad_values = np.sum(np.isnan(img.data), axis=2) != 0

            nv = self.__mk_nv__(img.data)

        # conversion to final data type
        mask_array = np.array(mask_array, dtype=np.uint8)
        mask_array[bad_values] = nodata_value
        mask_conf[bad_values] = nodata_value
        if nv is not None:
            nv[bad_values] = nodata_value

        if majority_filter_options is not None:
            self.logger.info("Applying majority filter:%s" % str(majority_filter_options))
            if type(majority_filter_options) is dict:
                mask_array = majority_mask_filter(mask_array, **majority_filter_options)
            else:
                for opts in majority_filter_options:
                    mask_array = majority_mask_filter(mask_array, **opts)

        uvals = np.unique(mask_array)  # unique values
        avals = list(self.cb_clf.classes) + [nodata_value]  # allows values are class ids and the nodata_value
        for uval in uvals:
            if uval not in avals:
                raise ValueError("Value:%f encountered in mask array which is now allowed." % float(uval))

        gc = img.metadata["spatial_samplings"][target_resolution] if target_resolution is not None else None
        return S2Mask(img=img, mask_array=mask_array, clf_to_col=self.clf_to_col, novelty=nv,
                      mask_legend=self.mask_legend, mask_confidence_array=mask_conf, geo_coding=gc)
