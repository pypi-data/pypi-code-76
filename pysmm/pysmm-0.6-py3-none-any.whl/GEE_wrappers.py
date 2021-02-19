from __future__ import print_function
import ee
import numpy as np
import datetime as dt
import math
import time
import os
# import matplotlib.pyplot as plt
# import pytesmo.time_series.anomaly as anomaly
# from pytesmo.time_series.plotting import plot_clim_anom
# from sklearn.linear_model import LinearRegression
# from pytesmo.temporal_matching import df_match
# import pandas as pd
# from pysmm.utils import gdrive
# import pickle


# class GEE_pt(object):
#     """Class to create an interface with GEE for the extraction of parameter time series
#
#         Attributes:
#             lon: longitude in decimal degrees
#             lat: latitude in decimal degrees
#             workdir: path to a directory to save output e.g. time-series plots
#             buffer: radius of the time-series footprint
#         """
#
#     def __init__(self, lon, lat, workdir, buffer=20):
#         ee.Reset()
#         ee.Initialize()
#         self.lon = lon
#         self.lat = lat
#         self.buffer = buffer
#         self.workdir = workdir
#
#         # Placeholders
#         self.S1TS = None
#         self.ASPE = None
#         self.SLOP = None
#         self.ELEV = None
#         self.LC = None
#
#     def slope_correction(self, collection, elevation, model, buffer=0):
#         '''This function applies the slope correction on a collection of Sentinel-1 data
#
#            :param collection: ee.Collection of Sentinel-1
#            :param elevation: ee.Image of DEM
#            :param model: model to be applied (volume/surface)
#            :param buffer: buffer in meters for layover/shadow amsk
#
#             :returns: ee.Image
#         '''
#
#         def _volumetric_model_SCF(theta_iRad, alpha_rRad):
#             '''Code for calculation of volumetric model SCF
#
#             :param theta_iRad: ee.Image of incidence angle in radians
#             :param alpha_rRad: ee.Image of slope steepness in range
#
#             :returns: ee.Image
#             '''
#
#             # create a 90 degree image in radians
#             ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)
#
#             # model
#             nominator = (ninetyRad.subtract(theta_iRad).add(alpha_rRad)).tan()
#             denominator = (ninetyRad.subtract(theta_iRad)).tan()
#             return nominator.divide(denominator)
#
#         def _surface_model_SCF(theta_iRad, alpha_rRad, alpha_azRad):
#             '''Code for calculation of direct model SCF
#
#             :param theta_iRad: ee.Image of incidence angle in radians
#             :param alpha_rRad: ee.Image of slope steepness in range
#             :param alpha_azRad: ee.Image of slope steepness in azimuth
#
#             :returns: ee.Image
#             '''
#
#             # create a 90 degree image in radians
#             ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)
#
#             # model
#             nominator = (ninetyRad.subtract(theta_iRad)).cos()
#             denominator = (alpha_azRad.cos()
#                            .multiply((ninetyRad.subtract(theta_iRad).add(alpha_rRad)).cos()))
#
#             return nominator.divide(denominator)
#
#         def _erode(image, distance):
#             '''Buffer function for raster
#
#             :param image: ee.Image that shoudl be buffered
#             :param distance: distance of buffer in meters
#
#             :returns: ee.Image
#             '''
#
#             d = (image.Not().unmask(1)
#                  .fastDistanceTransform(30).sqrt()
#                  .multiply(ee.Image.pixelArea().sqrt()))
#
#             return image.updateMask(d.gt(distance))
#
#         def _masking(alpha_rRad, theta_iRad, buffer):
#             '''Masking of layover and shadow
#
#
#             :param alpha_rRad: ee.Image of slope steepness in range
#             :param theta_iRad: ee.Image of incidence angle in radians
#             :param buffer: buffer in meters
#
#             :returns: ee.Image
#             '''
#             # layover, where slope > radar viewing angle
#             layover = alpha_rRad.lt(theta_iRad).rename('layover')
#
#             # shadow
#             ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)
#             shadow = alpha_rRad.gt(ee.Image.constant(-1).multiply(ninetyRad.subtract(theta_iRad))).rename('shadow')
#
#             # add buffer to layover and shadow
#             if buffer > 0:
#                 layover = _erode(layover, buffer)
#                 shadow = _erode(shadow, buffer)
#
#                 # combine layover and shadow
#             no_data_mask = layover.And(shadow).rename('no_data_mask')
#
#             return layover.addBands(shadow).addBands(no_data_mask)
#
#         def _correct(image):
#             '''This function applies the slope correction and adds layover and shadow masks
#
#             '''
#
#             # get the image geometry and projection
#             geom = image.geometry()
#             proj = image.select(1).projection()
#
#             # calculate the look direction
#             heading = (ee.Terrain.aspect(image.select('angle'))
#                        .reduceRegion(ee.Reducer.mean(), geom, 1000)
#                        .get('aspect'))
#
#             # Sigma0 to Power of input image
#             sigma0Pow = ee.Image.constant(10).pow(image.divide(10.0))
#
#             # the numbering follows the article chapters
#             # 2.1.1 Radar geometry
#             theta_iRad = image.select('angle').multiply(np.pi / 180)
#             phi_iRad = ee.Image.constant(heading).multiply(np.pi / 180)
#
#             # 2.1.2 Terrain geometry
#             alpha_sRad = ee.Terrain.slope(elevation).select('slope').multiply(np.pi / 180).setDefaultProjection(
#                 proj).clip(
#                 geom)
#             phi_sRad = ee.Terrain.aspect(elevation).select('aspect').multiply(np.pi / 180).setDefaultProjection(
#                 proj).clip(
#                 geom)
#
#             # we get the height, for export
#             height = elevation.setDefaultProjection(proj).clip(geom)
#
#             # 2.1.3 Model geometry
#             # reduce to 3 angle
#             phi_rRad = phi_iRad.subtract(phi_sRad)
#
#             # slope steepness in range (eq. 2)
#             alpha_rRad = (alpha_sRad.tan().multiply(phi_rRad.cos())).atan()
#
#             # slope steepness in azimuth (eq 3)
#             alpha_azRad = (alpha_sRad.tan().multiply(phi_rRad.sin())).atan()
#
#             # local incidence angle (eq. 4)
#             theta_liaRad = (alpha_azRad.cos().multiply((theta_iRad.subtract(alpha_rRad)).cos())).acos()
#             theta_liaDeg = theta_liaRad.multiply(180 / np.pi)
#
#             # 2.2
#             # Gamma_nought
#             gamma0 = sigma0Pow.divide(theta_iRad.cos())
#             gamma0dB = ee.Image.constant(10).multiply(gamma0.log10()).select(['VV', 'VH'], ['VV_gamma0', 'VH_gamma0'])
#             ratio_gamma = (gamma0dB.select('VV_gamma0')
#                            .subtract(gamma0dB.select('VH_gamma0'))
#                            .rename('ratio_gamma0'))
#
#             if model == 'volume':
#                 scf = _volumetric_model_SCF(theta_iRad, alpha_rRad)
#
#             if model == 'surface':
#                 scf = _surface_model_SCF(theta_iRad, alpha_rRad, alpha_azRad)
#
#             # apply model for Gamm0_f
#             gamma0_flat = gamma0.divide(scf)
#             gamma0_flatDB = (ee.Image.constant(10)
#                              .multiply(gamma0_flat.log10())
#                              .select(['VV', 'VH'], ['VV_gamma0flat', 'VH_gamma0flat'])
#                              )
#
#             masks = _masking(alpha_rRad, theta_iRad, buffer)
#
#             # calculate the ratio for RGB vis
#             ratio_flat = (gamma0_flatDB.select('VV_gamma0flat')
#                           .subtract(gamma0_flatDB.select('VH_gamma0flat'))
#                           .rename('ratio_gamma0flat')
#                           )
#
#             if model == 'surface':
#                 gamma0_flatDB = gamma0_flatDB.rename(['VV_gamma0surf', 'VH_gamma0surf'])
#
#             if model == 'volume':
#                 gamma0_flatDB = gamma0_flatDB.rename(['VV_gamma0vol', 'VH_gamma0vol'])
#
#             return (image.rename(['VV_sigma0', 'VH_sigma0', 'incAngle'])
#                     .addBands(gamma0dB)
#                     .addBands(ratio_gamma)
#                     .addBands(gamma0_flatDB)
#                     .addBands(ratio_flat)
#                     .addBands(alpha_rRad.rename('alpha_rRad'))
#                     .addBands(alpha_azRad.rename('alpha_azRad'))
#                     .addBands(phi_sRad.rename('aspect'))
#                     .addBands(alpha_sRad.rename('slope'))
#                     .addBands(theta_iRad.rename('theta_iRad'))
#                     .addBands(theta_liaRad.rename('theta_liaRad'))
#                     .addBands(masks)
#                     .addBands(height.rename('elevation'))
#                     )
#
#             # run and return correction
#
#         return collection.map(_correct, opt_dropNulls=True)
#
#     def multitemporalDespeckle(self, images, radius, units, opt_timeWindow=None):
#         def mapMeanSpace(i):
#             reducer = ee.Reducer.mean()
#             kernel = ee.Kernel.square(radius, units)
#             mean = i.reduceNeighborhood(reducer, kernel).rename(bandNamesMean)
#             ratio = i.divide(mean).rename(bandNamesRatio)
#             return (i.addBands(mean).addBands(ratio))
#
#         if opt_timeWindow == None:
#             timeWindow = dict(before=-3, after=3, units='month')
#         else:
#             timeWindow = opt_timeWindow
#
#         bandNames = ee.Image(images.first()).bandNames()
#         bandNamesMean = bandNames.map(lambda b: ee.String(b).cat('_mean'))
#         bandNamesRatio = bandNames.map(lambda b: ee.String(b).cat('_ratio'))
#
#         # compute spatial average for all images
#         meanSpace = images.map(mapMeanSpace)
#
#         # computes a multi-temporal despeckle function for a single image
#
#         def multitemporalDespeckleSingle(image):
#             t = image.date()
#             fro = t.advance(ee.Number(timeWindow['before']), timeWindow['units'])
#             to = t.advance(ee.Number(timeWindow['after']), timeWindow['units'])
#
#             meanSpace2 = ee.ImageCollection(meanSpace).select(bandNamesRatio).filterDate(fro, to) \
#                 .filter(ee.Filter.eq('relativeOrbitNumber_start', image.get('relativeOrbitNumber_start')))
#
#             b = image.select(bandNamesMean)
#
#             return (b.multiply(meanSpace2.sum()).divide(meanSpace2.count()).rename(bandNames)).set('system:time_start',
#                                                                                                    image.get(
#                                                                                                        'system:time_start'))
#
#         return meanSpace.map(multitemporalDespeckleSingle)
#
#     def _s1_track_ts(self, filtered_collection,
#                      track_nr,
#                      dual_pol,
#                      varmask,
#                      returnLIA,
#                      masksnow,
#                      tempfilter,
#                      radcor=False):
#         def getAzimuth(f):
#             coords = ee.Array(f.geometry().coordinates().get(0)).transpose()
#             crdLons = ee.List(coords.toList().get(0))
#             crdLats = ee.List(coords.toList().get(1))
#             minLon = crdLons.sort().get(0)
#             maxLon = crdLons.sort().get(-1)
#             minLat = crdLats.sort().get(0)
#             maxLat = crdLats.sort().get(-1)
#             azimuth = ee.Number(crdLons.get(crdLats.indexOf(minLat))).subtract(minLon).atan2(ee.Number(crdLats
#                 .get(
#                 crdLons.indexOf(minLon))).subtract(minLat)).multiply(180.0 / math.pi).add(180.0)
#             return ee.Feature(ee.Geometry.LineString([crdLons.get(crdLats.indexOf(maxLat)), maxLat,
#                                                       minLon, crdLats.get(crdLons.indexOf(minLon))]),
#                               {'azimuth': azimuth}).copyProperties(f)
#
#         def getLIA(imCollection):
#             # function to calculate the local incidence angle, based on azimuth angle and srtm
#             srtm = ee.Image("USGS/SRTMGL1_003")
#             srtm_slope = ee.Terrain.slope(srtm)
#             srtm_aspect = ee.Terrain.aspect(srtm)
#
#             # tmpImg = ee.Image(imCollection.first())
#             tmpImg = imCollection
#
#             inc = tmpImg.select('angle')
#             azimuth = getAzimuth(tmpImg).get('azimuth')
#             srtm_slope_proj = srtm_slope.multiply(
#                 ee.Image.constant(azimuth).subtract(9.0).subtract(srtm_aspect).multiply(math.pi / 180).cos())
#             lia = inc.subtract(ee.Image.constant(90).subtract(ee.Image.constant(90).subtract(srtm_slope_proj))).abs()
#
#             return tmpImg.addBands(ee.Image(lia.select(['angle'], ['lia'])))
#             # s = srtm_slope.multiply(ee.Image.constant(277).subtract(srtm_aspect).multiply(math.pi / 180).cos())
#             # lia = inc.subtract(ee.Image.constant(90).subtract(ee.Image.constant(90).subtract(s))).abs()
#
#             # return ee.Image(lia.select(['angle'], ['lia']).reproject(srtm.projection()))
#
#         def miscMask(image):
#             # masking of low and high db values as well as areas affected by geometry distortion
#             tmp = ee.Image(image)
#
#             # mask pixels
#             vv = tmp.select('VV')
#             if dual_pol == True:
#                 vh = tmp.select('VH')
#                 maskvh = vh.gte(-25).bitwiseAnd(vh.lt(0))  # was -25 and 0
#             lia = tmp.select('lia')
#             maskvv = vv.gte(-25).bitwiseAnd(vv.lt(0))
#             masklia1 = lia.gt(20)  # angle 10
#             masklia2 = lia.lt(45)  # angle 50
#             masklia = masklia1.bitwiseAnd(masklia2)
#
#             if dual_pol == True:
#                 mask = maskvv.bitwiseAnd(maskvh)
#             else:
#                 mask = maskvv
#             mask = mask.bitwiseAnd(masklia)
#             # mask = mask.bitwiseAnd(maskslope)
#             tmp = tmp.updateMask(mask)
#
#             return (tmp)
#
#         def toln(image):
#             tmp = ee.Image(image)
#
#             # Convert to linear
#             vv = ee.Image(10).pow(tmp.select('VV').divide(10))
#             if dual_pol == True:
#                 vh = ee.Image(10).pow(tmp.select('VH').divide(10))
#
#             # Convert to ln
#             out = vv.log()
#             if dual_pol == True:
#                 out = out.addBands(vh.log())
#                 out = out.select(['constant', 'constant_1'], ['VV', 'VH'])
#             else:
#                 out = out.select(['constant'], ['VV'])
#
#             return out.set('system:time_start', tmp.get('system:time_start'))
#
#         def applyvarmask(image):
#             tmp = ee.Image(image)
#             tmp = tmp.updateMask(varmask)
#
#             return (tmp)
#
#         def tolin(image):
#             tmp = ee.Image(image)
#
#             # Convert to linear
#             vh = ee.Image(10).pow(tmp.select('VH').divide(10))
#
#             # Output
#             out = vh.select(['constant'], ['VH'])
#
#             return out.set('system:time_start', tmp.get('system:time_start'))
#
#         def tolin_dual(image):
#             tmp = ee.Image(image)
#             if dual_pol == True:
#                 lin = ee.Image(10).pow(tmp.divide(10))  # .select(['constant', 'constant_1'], ['VV', 'VH'])
#             else:
#                 lin = ee.Image(10).pow(tmp.divide(10))  # .select(['constant'], ['VV'])
#
#             return lin.set('system:time_start', tmp.get('system:time_start'))
#
#         def todb(image):
#             tmp = ee.Image(image)
#
#             return ee.Image(10).multiply(tmp.log10()).set('system:time_start', tmp.get('system:time_start'))
#
#         def applysnowmask(image):
#             tmp = ee.Image(image)
#             sdiff = tmp.select('VH').subtract(snowref)
#             wetsnowmap = sdiff.lte(-2.6)  # .focal_mode(100, 'square', 'meters', 3)
#
#             return (tmp.updateMask(wetsnowmap.eq(0)))
#
#         def createAvg(image):
#             # average pixels within the time-series foot print
#             gee_roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#             tmp = ee.Image(image)
#
#             # Conver to linear before averaging
#             tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VV_sigma0').divide(10)))
#             tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VV_gamma0').divide(10)))
#             tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VV_gamma0vol').divide(10)))
#             tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VV_gamma0surf').divide(10)))
#             if dual_pol == True:
#                 tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VH_sigma0').divide(10)))
#                 tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VH_gamma0').divide(10)))
#                 tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VH_gamma0vol').divide(10)))
#                 tmp = tmp.addBands(ee.Image(10).pow(tmp.select('VH_gamma0surf').divide(10)))
#                 tmp = tmp.select(['constant', 'constant_1', 'constant_2', 'constant_3', 'constant_4',
#                                   'constant_5', 'constant_6', 'constant_7', 'incAngle', 'theta_liaRad'],
#                                  ['VV_sigma0', 'VV_gamma0', 'VV_gamma0vol', 'VV_gamma0surf',
#                                   'VH_sigma0', 'VH_gamma0', 'VH_gamma0vol', 'VH_gamma0surf', 'angle', 'lia'])
#             else:
#                 tmp = tmp.select(['constant', 'constant_1', 'constant_2', 'constant_3',
#                                   'incAngle', 'theta_liaRad'],
#                                  ['VV_sigma0', 'VV_gamma0', 'VV_gamma0vol', 'VV_gamma0surf',
#                                   'angle', 'lia'])
#
#             reduced_img_data = tmp.reduceRegion(ee.Reducer.mean(), gee_roi, 10)
#             totcount = ee.Image(1).reduceRegion(ee.Reducer.count(), gee_roi, 10)
#             pcount = tmp.reduceRegion(ee.Reducer.count(), gee_roi, 10)
#             return ee.Feature(None, {'result': reduced_img_data, 'count': pcount, 'totcount': totcount})
#
#         def cliptoroi(image):
#             # average pixels within the time-series foot print
#             gee_roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#             return image.clip(gee_roi)
#
#         def apply_no_data_mask(image):
#             return image.updateMask(image.select('no_data_mask'))
#
#         #  filter for track
#         gee_s1_track_fltd = filtered_collection.filterMetadata('relativeOrbitNumber_start', 'equals', int(track_nr))
#
#
#         # gee_s1_track_fltd = gee_s1_track_fltd.map(cliptoroi)
#         # paths to dem
#         dem = 'USGS/SRTMGL1_003'
#
#         # list of models
#         model = 'volume'
#         gee_s1_track_fltd_vol = self.slope_correction(gee_s1_track_fltd,
#                                                  ee.Image(dem),
#                                                  model)
#
#         model = 'surface'
#         gee_s1_track_fltd_surf = self.slope_correction(gee_s1_track_fltd,
#                                                   ee.Image(dem),
#                                                   model)
#
#         # combine results based on volume and surface backscattering
#         gee_s1_track_fltd = gee_s1_track_fltd_surf.combine(gee_s1_track_fltd_vol, overwrite=True)
#
#         gee_s1_track_fltd = gee_s1_track_fltd.map(apply_no_data_mask)
#
#         if varmask == True:
#             # mask pixels with low temporal variability
#             # compute temporal statistics
#             gee_s1_ln = gee_s1_track_fltd.map(toln)
#             k2vv = ee.Image(gee_s1_ln.select('VV').reduce(ee.Reducer.stdDev()))
#             if dual_pol == True:
#                 k2vh = ee.Image(gee_s1_ln.select('VH').reduce(ee.Reducer.stdDev()))
#                 varmask = k2vv.gt(0.4).And(k2vh.gt(0.4))
#             else:
#                 varmask = k2vv.gt(0.4)
#             gee_s1_track_fltd = gee_s1_track_fltd.map(applyvarmask)
#
#         if tempfilter == True:
#             # apply a temporal speckle filter
#             radius = 3
#             units = 'pixels'
#             gee_s1_linear = gee_s1_track_fltd.map(tolin_dual)
#             gee_s1_dspckld_vv = self.multitemporalDespeckle(gee_s1_linear.select('VV'), radius, units,
#                                                        {'before': -12, 'after': 12, 'units': 'month'})
#             gee_s1_dspckld_vv = gee_s1_dspckld_vv.map(todb).select(['constant'], ['VV'])
#             if dual_pol == True:
#                 gee_s1_dspckld_vh = self.multitemporalDespeckle(gee_s1_linear.select('VH'), radius, units,
#                                                            {'before': -12, 'after': 12, 'units': 'month'})
#                 gee_s1_dspckld_vh = gee_s1_dspckld_vh.map(todb).select(['constant'], ['VH'])
#             if dual_pol == False:
#                 gee_s1_track_fltd = gee_s1_dspckld_vv.combine(gee_s1_track_fltd.select('angle')) \
#                     .combine(gee_s1_track_fltd.select('lia'))
#             else:
#                 gee_s1_track_fltd = gee_s1_dspckld_vv.combine(gee_s1_dspckld_vh) \
#                     .combine(gee_s1_track_fltd.select('angle')) \
#                     .combine(gee_s1_track_fltd.select('lia'))
#
#         # create average for buffer area - i.e. compute time-series
#         gee_s1_mapped = gee_s1_track_fltd.map(createAvg)
#         tmp = gee_s1_mapped.getInfo()
#         # get vv
#         vv_sig0 = 10 * np.log10(
#             np.array([x['properties']['result']['VV_sigma0'] for x in tmp['features']], dtype=np.float))
#         vv_g0 = 10 * np.log10(
#             np.array([x['properties']['result']['VV_gamma0'] for x in tmp['features']], dtype=np.float)
#         )
#         vv_g0vol = 10 * np.log10(
#             np.array([x['properties']['result']['VV_gamma0vol'] for x in tmp['features']], dtype=np.float)
#         )
#         vv_g0surf = 10 * np.log10(
#             np.array([x['properties']['result']['VV_gamma0surf'] for x in tmp['features']], dtype=np.float)
#         )
#
#         ge_dates = np.array([dt.datetime.strptime(x['id'][17:32], '%Y%m%dT%H%M%S') for x in tmp['features']])
#
#         if dual_pol == True:
#             # get vh
#             vh_sig0 = 10 * np.log10(
#                 np.array([x['properties']['result']['VH_sigma0'] for x in tmp['features']], dtype=np.float))
#             vh_g0 = 10 * np.log10(
#                 np.array([x['properties']['result']['VH_gamma0'] for x in tmp['features']], dtype=np.float)
#             )
#             vh_g0vol = 10 * np.log10(
#                 np.array([x['properties']['result']['VH_gamma0vol'] for x in tmp['features']], dtype=np.float)
#             )
#             vh_g0surf = 10 * np.log10(
#                 np.array([x['properties']['result']['VH_gamma0surf'] for x in tmp['features']], dtype=np.float)
#             )
#             if masksnow == True:
#                 vh_sig0_lin = np.array([x['properties']['result']['VH_sigma0'] for x in tmp['features']],
#                                        dtype=np.float)
#                 snowref = 10 * np.log10(np.mean(vh_sig0_lin[vh_sig0_lin > np.percentile(vh_sig0_lin, 5)]))
#                 snowmask = np.where(vh_sig0 - snowref > -2.6)
#                 vh_sig0 = vh_sig0[snowmask]
#                 vv_sig0 = vv_sig0[snowmask]
#                 ge_dates = ge_dates[snowmask]
#
#         if returnLIA == True:
#             # get lia
#             lia = np.array([x['properties']['result']['lia'] for x in tmp['features']], dtype=np.float)
#         else:
#             # get angle
#             lia = np.array([x['properties']['result']['angle'] for x in tmp['features']], dtype=np.float)
#
#         # get val_count - i.e. compute the fraction of valid pixels within the footprint
#         val_count = np.array(
#             [np.float(x['properties']['count']['VV_sigma0']) / np.float(x['properties']['totcount']['constant']) for x
#              in
#              tmp['features']], dtype=np.float)
#
#         if masksnow == True:
#             val_count = val_count[snowmask]
#
#         if self.buffer <= 100:
#             valid = np.where(val_count > 0.01)
#         else:
#             valid = np.where(val_count > 0.1)
#         vv_sig0 = vv_sig0[valid]
#         vv_g0 = vv_g0[valid]
#         vv_g0vol = vv_g0vol[valid]
#         vv_g0surf = vv_g0surf[valid]
#         if dual_pol == True:
#             vh_sig0 = vh_sig0[valid]
#             vh_g0 = vh_g0[valid]
#             vh_g0vol = vh_g0vol[valid]
#             vh_g0surf = vh_g0surf[valid]
#         lia = lia[valid]
#         ge_dates = ge_dates[valid]
#
#         if dual_pol == True:
#             return (pd.DataFrame({'vv_sig0': vv_sig0, 'vh_sig0': vh_sig0, 'lia': lia,
#                                   'vv_g0': vv_g0, 'vv_g0vol': vv_g0vol, 'vv_g0surf': vv_g0surf,
#                                   'vh_g0': vh_g0, 'vh_g0vol': vh_g0vol, 'vh_g0surf': vh_g0surf},
#                                  index=ge_dates))
#         else:
#             return (pd.DataFrame({'vv_sig0': vv_sig0, 'lia': lia,
#                                   'vv_g0': vv_g0, 'vv_g0vol': vv_g0vol, 'vv_g0surf': vv_g0surf},
#                                  index=ge_dates))
#
#     def extr_LC(self, prod='Globcover'):
#         # select prod='Globcover', 'Corine', 'USGS' (North America only for USGS)
#         if prod == 'Globcover':
#             lc_image = ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3").select('landcover')
#         elif prod == 'Corine':
#             lc_image = ee.Image('users/felixgreifeneder/corine')
#         elif prod == 'USGS':
#             lc_image = ee.Image(ee.ImageCollection("USGS/NLCD").toList(100).get(-1))
#         elif prod == 'Copernicus':
#             copernicus_collection = ee.ImageCollection('COPERNICUS/Landcover/100m/Proba-V/Global')
#             copernicus_image = ee.Image(copernicus_collection.toList(100).get(0))
#             roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#             class_info = {'classid': copernicus_image.select('discrete_classification').reduceRegion(ee.Reducer.mode(),
#                                                                                                      roi).getInfo()[
#                 'discrete_classification'],
#                           'forestType': copernicus_image.select('forest_type').reduceRegion(ee.Reducer.mean(),
#                                                                                             roi).getInfo()[
#                               'forest_type'],
#                           'bare': copernicus_image.select('bare-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                              roi).getInfo()[
#                               'bare-coverfraction'],
#                           'crops': copernicus_image.select('crops-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                                roi).getInfo()[
#                               'crops-coverfraction'],
#                           'grass': copernicus_image.select('grass-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                                roi).getInfo()[
#                               'grass-coverfraction'],
#                           'moss': copernicus_image.select('moss-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                              roi).getInfo()[
#                               'moss-coverfraction'],
#                           'shrub': copernicus_image.select('shrub-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                                roi).getInfo()[
#                               'shrub-coverfraction'],
#                           'tree': copernicus_image.select('tree-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                              roi).getInfo()[
#                               'tree-coverfraction'],
#                           'urban': copernicus_image.select('urban-coverfraction').reduceRegion(ee.Reducer.mean(),
#                                                                                                roi).getInfo()[
#                               'urban-coverfraction'],
#                           'waterp': copernicus_image.select('water-permanent-coverfraction').reduceRegion(
#                               ee.Reducer.mean(), roi).getInfo()['water-permanent-coverfraction'],
#                           'waters': copernicus_image.select('water-seasonal-coverfraction').reduceRegion(
#                               ee.Reducer.mean(), roi).getInfo()['water-seasonal-coverfraction']}
#             self.LC = class_info
#             return
#         else:
#             print('Unknown land-cover product')
#             return
#
#         roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#         lc = lc_image.reduceRegion(ee.Reducer.mode(), roi).getInfo()
#         self.LC = lc['landcover']
#
#     def extr_MODIS_MOD13Q1(self):
#         # extract time-series of the MODIS product MOD13Q1
#
#         def createAvg(image):
#             gee_roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#
#             # mask image
#             immask = image.select('SummaryQA').eq(ee.Image(0))
#             image = image.updateMask(immask)
#
#             reduced_img_data = image.reduceRegion(ee.Reducer.median(), gee_roi, 30)
#             return ee.Feature(None, {'result': reduced_img_data})
#
#         # load collection
#         gee_l8_collection = ee.ImageCollection('MODIS/006/MOD13Q1')
#
#         # filter collection
#         gee_roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#         gee_l8_fltd = gee_l8_collection.filterBounds(gee_roi)
#
#         # extract time series
#         gee_l8_mpd = gee_l8_fltd.map(createAvg)
#         tmp = gee_l8_mpd.getInfo()
#
#         EVI = np.array([x['properties']['result']['EVI'] for x in tmp['features']], dtype=np.float)
#
#         ge_dates = np.array([dt.datetime.strptime(x['id'], '%Y_%m_%d') for x in tmp['features']])
#
#         valid = np.where(np.isfinite(EVI))
#
#         # cut out invalid values
#         EVI = EVI[valid]
#         ge_dates = ge_dates[valid]
#
#         return (pd.Series(EVI, index=ge_dates, name='EVI'))
#
#     def extr_GLDAS_SM(self, yearlist=None):
#         # get time series of GLDAS 0 to 10 cm soil moisture
#
#         def createAvg(image):
#             gee_roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#
#             reduced_img_data = image.reduceRegion(ee.Reducer.median(), gee_roi, 30, tileScale=4)
#             return ee.Feature(None, {'result': reduced_img_data})
#
#         if yearlist == None:
#             # yearlist = range(1987,2018)
#             yearlist = range(2011, 2018)
#
#         SM_list = list()
#
#         for iyear in yearlist:
#             # ee.Reset()
#             # ee.Initialize()
#             print(iyear)
#             # load collection
#             if iyear < 2000:
#                 GLDAS_collection = ee.ImageCollection('NASA/GLDAS/V20/NOAH/G025/T3H').select('SoilMoi0_10cm_inst')
#             else:
#                 GLDAS_collection = ee.ImageCollection('NASA/GLDAS/V021/NOAH/G025/T3H').select('SoilMoi0_10cm_inst')
#             GLDAS_collection = GLDAS_collection.filterDate(str(iyear) + '-01-01', str(iyear) + '-12-31')
#             GLDAS_collection = GLDAS_collection.filter(ee.Filter.calendarRange(16, 18, 'hour'))
#
#             # clip
#             roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#             GLDAS_collection = GLDAS_collection.map(lambda image: image.clip(roi))
#
#             # extract time series
#             time_series = GLDAS_collection.map(createAvg)
#             tmp = time_series.getInfo()
#
#             SM = np.array([x['properties']['result']['SoilMoi0_10cm_inst'] for x in tmp['features']], dtype=np.float)
#
#             ge_dates = np.array([dt.datetime.strptime(x['id'], 'A%Y%m%d_%H%M') for x in tmp['features']])
#
#             valid = np.where(np.isfinite(SM))
#
#             # cut out invalid values
#             SM = SM[valid]
#             ge_dates = ge_dates[valid]
#
#             SM_series = pd.Series(SM, index=ge_dates, copy=True, name='GLDAS')
#
#             SM_list.append(SM_series)
#
#         return (pd.concat(SM_list))
#
#     def extr_GLDAS_date(self, date):
#         doi = ee.Date(date)
#         gldas = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
#             .select(['SoilMoi0_10cm_inst', 'CanopInt_inst']) \
#             .filterDate(doi, doi.advance(3, 'hour'))
#
#         gldas_img = ee.Image(gldas.first())
#         roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#         try:
#             return (gldas_img.reduceRegion(ee.Reducer.median(), roi, 50).getInfo())
#         except:
#             return {'SoilMoi0_10cm_inst': np.nan, 'CanopInt_inst': np.nan}
#
#     def extr_terrain(self):
#         roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#         elev = ee.Image("CGIAR/SRTM90_V4").reduceRegion(ee.Reducer.median(), roi).getInfo()
#         aspe = ee.Terrain.aspect(ee.Image("CGIAR/SRTM90_V4")).reduceRegion(ee.Reducer.median(), roi).getInfo()
#         slop = ee.Terrain.slope(ee.Image("CGIAR/SRTM90_V4")).reduceRegion(ee.Reducer.median(), roi).getInfo()
#         self.ELEV = elev['elevation']
#         self.ASPE = aspe['aspect']
#         self.SLOP = slop['slope']
#
#     def extr_S1(self,
#                 maskwinter=False,
#                 lcmask=False,
#                 globcover_mask=False,
#                 trackflt=None,
#                 masksnow=False,
#                 varmask=False,
#                 ssmcor=None,
#                 dual_pol=True,
#                 desc=False,
#                 tempfilter=False,
#                 returnLIA=False,
#                 datefilter=None,
#                 S1B=False,
#                 treemask=False,
#                 radcor=False):
#         # extract filtered Sentinel-1 backscatter time-series
#         def mask_lc(image):
#             tmp = ee.Image(image)
#
#             # load land cover info
#             corine = ee.Image('users/felixgreifeneder/corine')
#
#             # create lc mask
#             valLClist = [10, 11, 12, 13, 18, 19, 20, 21, 26, 27, 28, 29]
#
#             lcmask = corine.eq(valLClist[0]).bitwiseOr(corine.eq(valLClist[1])) \
#                 .bitwiseOr(corine.eq(valLClist[2])) \
#                 .bitwiseOr(corine.eq(valLClist[3])) \
#                 .bitwiseOr(corine.eq(valLClist[4])) \
#                 .bitwiseOr(corine.eq(valLClist[5])) \
#                 .bitwiseOr(corine.eq(valLClist[6])) \
#                 .bitwiseOr(corine.eq(valLClist[7])) \
#                 .bitwiseOr(corine.eq(valLClist[8])) \
#                 .bitwiseOr(corine.eq(valLClist[9])) \
#                 .bitwiseOr(corine.eq(valLClist[10])) \
#                 .bitwiseOr(corine.eq(valLClist[11]))
#
#             tmp = tmp.updateMask(lcmask)
#
#             return tmp
#
#         def mask_lc_globcover(image):
#             tmp = ee.Image(image)
#
#             # load lc
#             glbcvr = ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3").select('landcover')
#
#             valLClist = [11, 14, 20, 30, 120, 140, 150]
#
#             lcmask = glbcvr.eq(valLClist[0]) \
#                 .bitwiseOr(glbcvr.eq(valLClist[1])) \
#                 .bitwiseOr(glbcvr.eq(valLClist[2])) \
#                 .bitwiseOr(glbcvr.eq(valLClist[3])) \
#                 .bitwiseOr(glbcvr.eq(valLClist[4])) \
#                 .bitwiseOr(glbcvr.eq(valLClist[5])) \
#                 .bitwiseOr(glbcvr.eq(valLClist[6]))
#
#             tmp = tmp.updateMask(lcmask)
#
#             return tmp
#
#         def mask_tree_cover(image):
#
#             copernicus_collection = ee.ImageCollection('COPERNICUS/Landcover/100m/Proba-V/Global')
#             copernicus_image = ee.Image(copernicus_collection.toList(1000).get(0))
#             treemask = copernicus_image.select('tree-coverfraction').clip(gee_roi).lte(20)
#
#             # load lc
#             glbcvr = ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3").select('landcover')
#             # mask water
#             watermask = copernicus_image.select('discrete_classification').neq(80)
#             return image.updateMask(treemask.And(watermask))
#
#         def addRefSM(image):
#             tmp = ee.Image(image)
#             img_date = ee.Date(tmp.get('system:time_start'))
#             RefSMtmp = RefSMcollection.filterDate(img_date.format('Y-M-d'))
#             current_ssm = ee.ImageCollection(RefSMtmp).toList(10).get(0)
#
#             out_image = tmp.addBands(ee.Image(current_ssm))
#
#             return (out_image)
#
#         def s1_simplyfy_date(image):
#             return (image.set('system:time_start', ee.Date(ee.Date(image.get('system:time_start')).format('Y-M-d'))))
#
#         def applyCorrelationMask(image):
#             mask = ssm_vv_cor.select('correlation').gt(0.1)
#             return (image.updateMask(mask))
#
#         import timeit
#
#         tic = timeit.default_timer()
#
#         # load S1 data
#         gee_s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')  # .map(setresample)
#
#         # filter collection
#         gee_roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#
#         gee_s1_filtered = gee_s1_collection.filter(ee.Filter.eq('instrumentMode', 'IW')) \
#             .filterBounds(gee_roi) \
#             .filter(ee.Filter.listContains('transmitterReceiverPolarisation',
#                                            'VV'))
#
#         if S1B == False:
#             gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('platform_number', 'A'))
#
#         if datefilter is not None:
#             gee_s1_filtered = gee_s1_filtered.filterDate(datefilter[0], datefilter[1])
#
#         if desc == False:
#             # Select only acquisition from ascending tracks
#             gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
#         # else:
#         #    gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
#
#         if dual_pol == True:
#             # select only acquisitions with VV AND VH
#             gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
#
#         if maskwinter == True:
#             # Mask winter based on the DOY
#             gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.dayOfYear(121, 304))
#
#         if trackflt is not None:
#             # Select only data from a specific S1 track
#             if isinstance(trackflt, list):
#                 gee_s1_filtered = gee_s1_filtered.filter(
#                     ee.Filter.inList(ee.List(trackflt), 'relativeOrbitNumber_start'))
#             else:
#                 gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('relativeOrbitNumber_start', trackflt))
#
#         if lcmask == True:
#             # Mask pixels based on Corine land-cover
#             gee_s1_filtered = gee_s1_filtered.map(mask_lc)
#
#         if globcover_mask == True:
#             # Mask pixels based on the Globcover land-cover classification
#             gee_s1_filtered = gee_s1_filtered.map(mask_lc_globcover)
#
#         if treemask == True:
#             gee_s1_filtered = gee_s1_filtered.map(mask_tree_cover)
#
#         if ssmcor is not None:
#             # Mask pixels with a low correlation toe coarse resolution soil moisture
#             # Mostly relevant if aggregating over a larger area
#             RefSMlist = list()
#             ssmcor = ssmcor.resample('D').mean().dropna()
#             ssmcor = ssmcor.astype(np.float)
#             for i in range(len(ssmcor)):
#                 ssm_img = ee.Image(ssmcor[i]).clip(gee_roi).float()
#                 ssm_img = ssm_img.set('system:time_start', ssmcor.index[i])
#                 RefSMlist.append(ssm_img)
#             RefSMcollection = ee.ImageCollection(RefSMlist)
#
#             # prepare the join
#             s1_joined = gee_s1_filtered.map(s1_simplyfy_date)
#             join_filter = ee.Filter.equals(leftField='system:time_start', rightField='system:time_start')
#             simple_join = ee.Join.simple()
#             s1_joined = simple_join.apply(s1_joined, RefSMcollection, join_filter)
#
#             # create ssm reference SM, image collection
#             s1_plus_RefSM = ee.ImageCollection(s1_joined.map(addRefSM, True))
#             ssm_vv_cor = s1_plus_RefSM.select(['VV', 'constant']).reduce(ee.Reducer.pearsonsCorrelation())
#             gee_s1_filtered = gee_s1_filtered.map(applyCorrelationMask)
#
#         # get the track numbers
#         tmp = gee_s1_filtered.getInfo()
#         track_series = np.array([x['properties']['relativeOrbitNumber_start'] for x in tmp['features']])
#         dir_series = np.array([x['properties']['orbitProperties_pass'] for x in tmp['features']])
#         available_tracks, uidx = np.unique(track_series, return_index=True)
#         available_directions = dir_series[uidx]
#         # create dict with orbit directions
#         available_directions = pd.Series(np.where(available_directions == 'ASCENDING', 1, 0), index=available_tracks)
#
#         print('Extracting data from ' + str(len(available_tracks)) + ' Sentinel-1 tracks...')
#         print(available_tracks)
#
#         out_dict = {}
#
#         for track_nr in available_tracks:
#             out_dict[str(int(track_nr))] = self._s1_track_ts(gee_s1_filtered,
#                                                              track_nr,
#                                                              dual_pol,
#                                                              varmask,
#                                                              returnLIA,
#                                                              masksnow,
#                                                              tempfilter,
#                                                              radcor)
#
#         toc = timeit.default_timer()
#
#         print('Time-series extraction finished in ' + "{:10.2f}".format(toc - tic) + 'seconds')
#
#         self.S1TS = out_dict
#
#     def extr_SM(self,
#                 tracknr=None,
#                 masksnow=False,
#                 tempfilter=True,
#                 calc_anomalies=False):
#
#         if self.S1TS == None:
#             # get S1 time-series
#             self.extr_S1(maskwinter=False,
#                          trackflt=tracknr,
#                          masksnow=masksnow,
#                          tempfilter=tempfilter,
#                          desc=True,
#                          radcor=True,
#                          returnLIA=True,
#                          S1B=True)
#
#         s1_ts = self.S1TS
#
#         # load SVR model
#         modelpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SVRmodel.p')
#         MLmodel = pickle.load(open(modelpath, 'rb'))
#
#         # extract land cover
#         self.extr_LC()
#         # extract terrain information
#         self.extr_terrain()
#
#         # check if one of the found tracks contains valid data
#         empty = 0
#         for track_id in s1_ts.keys():
#             if len(s1_ts[track_id]) == 0:
#                 empty = 1
#         if empty == 1:
#             print('No valid data was found')
#             return None
#
#         # create ts stack
#         cntr = 0
#         sm_estimated = list()
#         anom_estimated = list()
#         for track_id in s1_ts.keys():
#             # extract model attributes
#             reg_model1 = (MLmodel[0], MLmodel[1])
#             reg_model2 = (MLmodel[2], MLmodel[3])
#
#             # calculate k1,...,kN and sig0m
#             s1_ts[track_id].dropna(axis=0, how='any')
#             temp_ts1 = s1_ts[track_id]['sig0']
#             temp_ts2 = s1_ts[track_id]['sig02']
#             temp_tslia = s1_ts[track_id]['lia']
#
#             ts_length = len(temp_ts1)
#
#             if ts_length < 10:
#                 print('Estimation for track #' + str(track_id) + ' not possible - time-series too short')
#                 continue
#
#             temp_ts1_lin = np.power(10, temp_ts1 / 10.)
#             temp_ts2_lin = np.power(10, temp_ts2 / 10.)
#             meanVV = np.mean(temp_ts1_lin)
#             meanVH = np.mean(temp_ts2_lin)
#             k1VV = np.mean(np.log(temp_ts1_lin))
#             k1VH = np.mean(np.log(temp_ts2_lin))
#             k2VV = np.std(np.log(temp_ts1_lin))
#             k2VH = np.std(np.log(temp_ts1_lin))
#
#             # get gldas
#             gldas_series = pd.Series(index=s1_ts[track_id].index)
#             for i in gldas_series.index:
#                 gldas_tmp = self.extr_GLDAS_date(i.strftime('%Y-%m-%d'))
#                 gldas_series[i] = gldas_tmp['SoilMoi0_10cm_inst']
#
#             # check for nans in the gldas time-series
#             valid2 = np.where(np.isfinite(gldas_series) & np.isfinite(gldas_series))
#
#             fmat_tmp1 = np.array([k1VV, k1VH, k2VV, k2VH, self.LC, np.mean(temp_tslia), self.ASPE,
#                                   gldas_series.median()])  # , aspe, slop, elev, gldas_series.mean()])
#
#             fmat_tmp2 = np.hstack(((temp_ts1_lin - meanVV).values.reshape(ts_length, 1),
#                                    (temp_ts2_lin - meanVH).values.reshape(ts_length, 1),
#                                    (gldas_series - gldas_series.mean()).values.reshape(ts_length, 1)))
#
#             # apply masks to dates and fmat
#             fmat_tmp2 = fmat_tmp2[valid2, :]
#             dates = s1_ts[track_id].index[valid2]
#             # fmat_tmp2 = fmat_tmp2[0]
#
#             nn_model1 = reg_model1[0]
#             nn_scaler1 = reg_model1[1]
#             nn_model2 = reg_model2[0]
#             nn_scaler2 = reg_model2[1]
#             fvect1 = nn_scaler1.transform(fmat_tmp1.reshape(1, -1))
#             fvect2 = nn_scaler2.transform(fmat_tmp2.squeeze())
#
#             avg_ssm_estimated_tmp = nn_model1.predict(fvect1)
#             diff_ssm_estimated_tmp = nn_model2.predict(fvect2)
#             ssm_estimated_tmp = pd.Series((diff_ssm_estimated_tmp + avg_ssm_estimated_tmp) * 100, index=dates,
#                                           name='S1')
#             ssm_estimated_tmp = ssm_estimated_tmp[~ssm_estimated_tmp.index.duplicated(keep='first')]
#
#             sm_estimated.append(ssm_estimated_tmp.copy())
#
#             if calc_anomalies == True:
#                 # get GLDAS timeseries
#                 gldas_ts = self.extr_GLDAS_SM()
#
#                 # correct GLDAS for local variations
#                 gldas_ts_matched = df_match(ssm_estimated_tmp, gldas_ts, window=0.5)
#                 gldas_s1 = pd.concat([ssm_estimated_tmp, gldas_ts_matched['GLDAS']], axis=1, join='inner').dropna()
#                 lin_fit = LinearRegression()
#                 lin_fit.fit(gldas_s1['GLDAS'].values.reshape(-1, 1), gldas_s1['S1'].values)
#                 # calibrate GLDAS
#                 gldas_tmp = lin_fit.predict(gldas_ts.values.reshape(-1, 1))
#                 gldas_ts = pd.Series(gldas_tmp, index=gldas_ts.index)
#
#                 # calculate climatology
#                 gldas_clim = anomaly.calc_climatology(gldas_ts, moving_avg_clim=30)
#                 gldas_clim = pd.DataFrame(pd.Series(gldas_clim, name='S1'))
#                 # calculate anomaly
#                 anom_estimated_tmp = pd.Series(
#                     [ssm_estimated_tmp[dateI] - gldas_clim['S1'][dateI.dayofyear] for dateI in ssm_estimated_tmp.index],
#                     index=ssm_estimated_tmp.index,
#                     dtype=np.float64)
#                 anom_estimated.append(anom_estimated_tmp.copy())
#
#         sm_estimated = pd.concat(sm_estimated)
#         sm_estimated.sort_index(inplace=True)
#         if calc_anomalies == True:
#             anom_estimated = pd.concat(anom_estimated)
#             anom_estimated.sort_index(inplace=True)
#
#         if calc_anomalies == False:
#             return sm_estimated
#         else:
#             return pd.DataFrame({'S1SM': sm_estimated, 'ANOM': anom_estimated}, index=sm_estimated.index)
#
#     def extr_SM_GBR(self,
#                     tracknr=None,
#                     masksnow=False,
#                     tempfilter=False,
#                     calc_anomalies=False):
#         if self.S1TS == None:
#             # get S1 time-series
#             self.extr_S1(maskwinter=False,
#                          trackflt=tracknr,
#                          masksnow=masksnow,
#                          tempfilter=tempfilter,
#                          desc=True,
#                          radcor=True,
#                          returnLIA=True,
#                          S1B=True)
#
#         s1_ts = self.S1TS
#
#         # load SVR model
#         modelpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'no_GLDAS_GBRmlmodel_1step.p')
#         MLmodel = pickle.load(open(modelpath, 'rb'))
#
#         # extract land cover
#         self.extr_LC()
#
#         # check if one of the found tracks contains valid data
#         empty = 0
#         for track_id in s1_ts.keys():
#             if len(s1_ts[track_id]) == 0:
#                 empty = 1
#         if empty == 1:
#             print('No valid data was found')
#             return None
#
#         # create ts stack
#         cntr = 0
#         sm_estimated = list()
#         anom_estimated = list()
#         for track_id in s1_ts.keys():
#             # extract model attributes
#             reg_model1 = (MLmodel[0], MLmodel[1])
#             reg_model2 = (MLmodel[2], MLmodel[3])
#
#             # calculate k1,...,kN and sig0m
#             s1_ts[track_id].dropna(axis=0, how='any')
#             g0vol_ts = s1_ts[track_id]['vv_g0vol']
#             g0surf_ts = s1_ts[track_id]['vv_g0surf']
#
#             ts_length = len(g0vol_ts)
#
#             if ts_length < 10:
#                 print('Estimation for track #' + str(track_id) + ' not possible - time-series too short')
#                 continue
#
#             g0vol_ts_lin = np.power(10, g0vol_ts / 10.)
#             g0surf_ts_lin = np.power(10, g0surf_ts / 10.)
#             med_vol = np.median(g0vol_ts_lin)
#             med_surf = np.median(g0surf_ts_lin)
#
#             # get gldas
#             gldas_swe = pd.Series(index=s1_ts[track_id].index)
#             gldas_soilt = pd.Series(index=s1_ts[track_id].index)
#             for i in gldas_swe.index:
#                 gldas_tmp = self.extr_GLDAS_date(i.strftime('%Y-%m-%d'))
#                 gldas_swe[i] = gldas_tmp['SWE_inst']
#                 gldas_soilt[i] = gldas_tmp['SoilTMP0_10cm_inst']
#
#             # check for nans in the gldas time-series
#             valid2 = np.where(np.isfinite(gldas_series) & np.isfinite(gldas_series))
#
#             fmat_tmp1 = np.array([k1VV, k1VH, k2VV, k2VH, self.LC, np.mean(temp_tslia), self.ASPE,
#                                   gldas_series.median()])  # , aspe, slop, elev, gldas_series.mean()])
#
#             fmat_tmp2 = np.hstack(((temp_ts1_lin - meanVV).values.reshape(ts_length, 1),
#                                    (temp_ts2_lin - meanVH).values.reshape(ts_length, 1),
#                                    (gldas_series - gldas_series.mean()).values.reshape(ts_length, 1)))
#
#             # apply masks to dates and fmat
#             fmat_tmp2 = fmat_tmp2[valid2, :]
#             dates = s1_ts[track_id].index[valid2]
#             # fmat_tmp2 = fmat_tmp2[0]
#
#             nn_model1 = reg_model1[0]
#             nn_scaler1 = reg_model1[1]
#             nn_model2 = reg_model2[0]
#             nn_scaler2 = reg_model2[1]
#             fvect1 = nn_scaler1.transform(fmat_tmp1.reshape(1, -1))
#             fvect2 = nn_scaler2.transform(fmat_tmp2.squeeze())
#
#             avg_ssm_estimated_tmp = nn_model1.predict(fvect1)
#             diff_ssm_estimated_tmp = nn_model2.predict(fvect2)
#             ssm_estimated_tmp = pd.Series((diff_ssm_estimated_tmp + avg_ssm_estimated_tmp) * 100, index=dates,
#                                           name='S1')
#             ssm_estimated_tmp = ssm_estimated_tmp[~ssm_estimated_tmp.index.duplicated(keep='first')]
#
#             sm_estimated.append(ssm_estimated_tmp.copy())
#
#             if calc_anomalies == True:
#                 # get GLDAS timeseries
#                 gldas_ts = self.extr_GLDAS_SM()
#
#                 # correct GLDAS for local variations
#                 gldas_ts_matched = df_match(ssm_estimated_tmp, gldas_ts, window=0.5)
#                 gldas_s1 = pd.concat([ssm_estimated_tmp, gldas_ts_matched['GLDAS']], axis=1, join='inner').dropna()
#                 lin_fit = LinearRegression()
#                 lin_fit.fit(gldas_s1['GLDAS'].values.reshape(-1, 1), gldas_s1['S1'].values)
#                 # calibrate GLDAS
#                 gldas_tmp = lin_fit.predict(gldas_ts.values.reshape(-1, 1))
#                 gldas_ts = pd.Series(gldas_tmp, index=gldas_ts.index)
#
#                 # calculate climatology
#                 gldas_clim = anomaly.calc_climatology(gldas_ts, moving_avg_clim=30)
#                 gldas_clim = pd.DataFrame(pd.Series(gldas_clim, name='S1'))
#                 # calculate anomaly
#                 anom_estimated_tmp = pd.Series(
#                     [ssm_estimated_tmp[dateI] - gldas_clim['S1'][dateI.dayofyear] for dateI in ssm_estimated_tmp.index],
#                     index=ssm_estimated_tmp.index,
#                     dtype=np.float64)
#                 anom_estimated.append(anom_estimated_tmp.copy())
#
#         sm_estimated = pd.concat(sm_estimated)
#         sm_estimated.sort_index(inplace=True)
#         if calc_anomalies == True:
#             anom_estimated = pd.concat(anom_estimated)
#             anom_estimated.sort_index(inplace=True)
#
#         if calc_anomalies == False:
#             return sm_estimated
#         else:
#             return pd.DataFrame({'S1SM': sm_estimated, 'ANOM': anom_estimated}, index=sm_estimated.index)
#
#     def get_s1_dates(self, tracknr=None, dualpol=True):
#         # get the S1 acquisition dates
#         # load S1 data
#         gee_s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')
#
#         # construct roi
#         roi = ee.Geometry.Point(self.lon, self.lat).buffer(self.buffer)
#
#         # ASCENDING acquisitions
#         gee_s1_filtered = gee_s1_collection.filter(ee.Filter.eq('instrumentMode', 'IW')) \
#             .filterBounds(roi) \
#             .filter(ee.Filter.eq('platform_number', 'A')) \
#             .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
#             .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
#
#         if dualpol == True:
#             gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
#
#         if tracknr is not None:
#             gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('relativeOrbitNumber_start', tracknr))
#
#         # create a list of availalbel dates
#         tmp = gee_s1_filtered.getInfo()
#         tmp_ids = [x['properties']['system:index'] for x in tmp['features']]
#         dates = np.array([dt.date(year=int(x[17:21]), month=int(x[21:23]), day=int(x[23:25])) for x in tmp_ids])
#
#         return (dates)


class GEE_extent(object):
    """Class to create an interface with GEE for the extraction of arrays

        Attributes:
            minlon: minimum longitude in decimal degrees
            minlat: minumum latitude in decimal degress
            maxlon: maximum longitude in decimal degrees
            maxlat: maximum latitude in decimal degrees
            workdir: path to directory for exported files
            sampling: sampling of exported grids
        """

    def __init__(self, minlon, minlat, maxlon, maxlat, workdir, sampling=20):
        """Return a new GEE extent object"""
        ee.Reset()
        ee.Initialize()

        # construct roi
        roi = ee.Geometry.Polygon([[minlon, minlat], [minlon, maxlat],
                                   [maxlon, maxlat], [maxlon, minlat],
                                   [minlon, minlat]])

        self.roi = roi
        self.MINLON = minlon
        self.MINLAT = minlat
        self.sampling = sampling
        self.workdir = workdir

        # Placeholders
        self.S1_SIG0_VV_db = None
        self.S1_G0VOL_VV_db = None
        self.S1_G0SURF_VV_db = None
        self.S1_ANGLE = None
        self.S1_LIA = None
        self.K1VV = None
        self.K2VV = None
        self.K3VV = None
        self.K4VV = None
        self.K1G0VV_V = None
        self.K2G0VV_V = None
        self.K3G0VV_V = None
        self.K4G0VV_V = None
        self.K1G0VV_S = None
        self.K2G0VV_S = None
        self.K3G0VV_S = None
        self.K4G0VV_S = None
        self.S1MEAN_VV = None
        self.S1STD_VV = None
        self.S1G0VOLMEAN_VV = None
        self.S1G0VOLSTD_VV = None
        self.S1G0SURFMEAN_VV = None
        self.S1G0SURFSTD_VV = None
        self.S1_DATE = None
        self.S1_SIG0_VH_db = None
        self.S1_G0VOL_VH_db = None
        self.S1_G0SURF_VH_db = None
        self.K1VH = None
        self.K2VH = None
        self.K3VH = None
        self.K4VH = None
        self.K1G0VH_V = None
        self.K2G0VH_V = None
        self.K3G0VH_V = None
        self.K4G0VH_V = None
        self.K1G0VH_S = None
        self.K2G0VH_S = None
        self.K3G0VH_S = None
        self.K4G0VH_S = None
        self.S1MEAN_VH = None
        self.S1STD_VH = None
        self.S1G0VOLMEAN_VH = None
        self.S1G0VOLSTD_VH = None
        self.S1G0SURFMEAN_VH = None
        self.S1G0SURFSTD_VH = None
        self.ESTIMATED_SM = None
        self.GLDAS_IMG = None
        self.GLDAS_MEAN = None
        self.LAND_COVER = None
        self.TERRAIN = None
        self.L8_IMG = None
        self.L8_MEAN = None
        self.L8_MASK = None
        self.TREE_COVER = None
        self.LAST_GLDAS = dt.datetime.today()  # temporary
        self.LC_ID = None
        self.FOREST_TYPE = None
        self.BARE_COVER = None
        self.CROPS_COVER = None
        self.GRASS_COVER = None
        self.MOSS_COVER = None
        self.SHRUB_COVER = None
        self.TREE_COVER = None
        self.URBAN_COVER = None
        self.WATERP_COVER = None
        self.WATERS_COVER = None
        self.SAND = None
        self.CLAY = None
        self.BULK = None
        self.EVI_IMG = None
        self.EVI_MEAN = None
        self.OVERWRITE = None

    def _multitemporalDespeckle(self, images, radius, units, opt_timeWindow=None):
        """Function for multi-temporal despeckling"""

        def mapMeanSpace(i):
            reducer = ee.Reducer.mean()
            kernel = ee.Kernel.square(radius, units)
            mean = i.reduceNeighborhood(reducer, kernel).rename(bandNamesMean)
            ratio = i.divide(mean).rename(bandNamesRatio)
            return (i.addBands(mean).addBands(ratio))

        if opt_timeWindow == None:
            timeWindow = dict(before=-3, after=3, units='month')
        else:
            timeWindow = opt_timeWindow

        bandNames = ee.Image(images.first()).bandNames()
        bandNamesMean = bandNames.map(lambda b: ee.String(b).cat('_mean'))
        bandNamesRatio = bandNames.map(lambda b: ee.String(b).cat('_ratio'))

        # compute spatial average for all images
        meanSpace = images.map(mapMeanSpace)

        # computes a multi-temporal despeckle function for a single image

        def multitemporalDespeckleSingle(image):
            t = image.date()
            fro = t.advance(ee.Number(timeWindow['before']), timeWindow['units'])
            to = t.advance(ee.Number(timeWindow['after']), timeWindow['units'])

            meanSpace2 = ee.ImageCollection(meanSpace).select(bandNamesRatio).filterDate(fro, to) \
                .filter(ee.Filter.eq('relativeOrbitNumber_start', image.get('relativeOrbitNumber_start')))

            b = image.select(bandNamesMean)

            return (b.multiply(meanSpace2.sum()).divide(meanSpace2.count()).rename(bandNames)).set('system:time_start',
                                                                                                   image.get(
                                                                                                       'system:time_start'))

        return meanSpace.map(multitemporalDespeckleSingle)

    def _slope_correction(self, collection, elevation, model, buffer=0):
        """This function applies the slope correction on a collection of Sentinel-1 data

           :param collection: ee.Collection of Sentinel-1
           :param elevation: ee.Image of DEM
           :param model: model to be applied (volume/surface)
           :param buffer: buffer in meters for layover/shadow amsk

            :returns: ee.Image
        """

        def _volumetric_model_SCF(theta_iRad, alpha_rRad):
            '''Code for calculation of volumetric model SCF

            :param theta_iRad: ee.Image of incidence angle in radians
            :param alpha_rRad: ee.Image of slope steepness in range

            :returns: ee.Image
            '''

            # create a 90 degree image in radians
            ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)

            # model
            nominator = (ninetyRad.subtract(theta_iRad).add(alpha_rRad)).tan()
            denominator = (ninetyRad.subtract(theta_iRad)).tan()
            return nominator.divide(denominator)

        def _surface_model_SCF(theta_iRad, alpha_rRad, alpha_azRad):
            '''Code for calculation of direct model SCF

            :param theta_iRad: ee.Image of incidence angle in radians
            :param alpha_rRad: ee.Image of slope steepness in range
            :param alpha_azRad: ee.Image of slope steepness in azimuth

            :returns: ee.Image
            '''

            # create a 90 degree image in radians
            ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)

            # model
            nominator = (ninetyRad.subtract(theta_iRad)).cos()
            denominator = (alpha_azRad.cos()
                           .multiply((ninetyRad.subtract(theta_iRad).add(alpha_rRad)).cos()))

            return nominator.divide(denominator)

        def _erode(image, distance):
            '''Buffer function for raster

            :param image: ee.Image that shoudl be buffered
            :param distance: distance of buffer in meters

            :returns: ee.Image
            '''

            d = (image.Not().unmask(1)
                 .fastDistanceTransform(30).sqrt()
                 .multiply(ee.Image.pixelArea().sqrt()))

            return image.updateMask(d.gt(distance))

        def _masking(alpha_rRad, theta_iRad, buffer):
            '''Masking of layover and shadow


            :param alpha_rRad: ee.Image of slope steepness in range
            :param theta_iRad: ee.Image of incidence angle in radians
            :param buffer: buffer in meters

            :returns: ee.Image
            '''
            # layover, where slope > radar viewing angle
            layover = alpha_rRad.lt(theta_iRad).rename('layover')

            # shadow
            ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)
            shadow = alpha_rRad.gt(ee.Image.constant(-1).multiply(ninetyRad.subtract(theta_iRad))).rename('shadow')

            # add buffer to layover and shadow
            if buffer > 0:
                layover = _erode(layover, buffer)
                shadow = _erode(shadow, buffer)

                # combine layover and shadow
            no_data_mask = layover.And(shadow).rename('no_data_mask')

            return layover.addBands(shadow).addBands(no_data_mask)

        def _correct(image):
            '''This function applies the slope correction and adds layover and shadow masks

            '''

            # get the image geometry and projection
            geom = image.geometry()
            proj = image.select(1).projection()

            # calculate the look direction
            heading = (ee.Terrain.aspect(image.select('angle'))
                       .reduceRegion(ee.Reducer.mean(), geom, 1000, tileScale=4)
                       .get('aspect'))

            # Sigma0 to Power of input image
            sigma0Pow = ee.Image.constant(10).pow(image.divide(10.0))

            # the numbering follows the article chapters
            # 2.1.1 Radar geometry
            theta_iRad = image.select('angle').multiply(np.pi / 180)
            phi_iRad = ee.Image.constant(heading).multiply(np.pi / 180)

            # 2.1.2 Terrain geometry
            alpha_sRad = ee.Terrain.slope(elevation).select('slope').multiply(np.pi / 180).setDefaultProjection(
                proj).clip(
                geom)
            phi_sRad = ee.Terrain.aspect(elevation).select('aspect').multiply(np.pi / 180).setDefaultProjection(
                proj).clip(
                geom)

            # we get the height, for export
            height = elevation.setDefaultProjection(proj).clip(geom)

            # 2.1.3 Model geometry
            # reduce to 3 angle
            phi_rRad = phi_iRad.subtract(phi_sRad)

            # slope steepness in range (eq. 2)
            alpha_rRad = (alpha_sRad.tan().multiply(phi_rRad.cos())).atan()

            # slope steepness in azimuth (eq 3)
            alpha_azRad = (alpha_sRad.tan().multiply(phi_rRad.sin())).atan()

            # local incidence angle (eq. 4)
            theta_liaRad = (alpha_azRad.cos().multiply((theta_iRad.subtract(alpha_rRad)).cos())).acos()
            theta_liaDeg = theta_liaRad.multiply(180 / np.pi)

            # 2.2
            # Gamma_nought
            gamma0 = sigma0Pow.divide(theta_iRad.cos())
            gamma0dB = ee.Image.constant(10).multiply(gamma0.log10()).select(['VV', 'VH'], ['VV_gamma0', 'VH_gamma0'])
            ratio_gamma = (gamma0dB.select('VV_gamma0')
                           .subtract(gamma0dB.select('VH_gamma0'))
                           .rename('ratio_gamma0'))

            if model == 'volume':
                scf = _volumetric_model_SCF(theta_iRad, alpha_rRad)

            if model == 'surface':
                scf = _surface_model_SCF(theta_iRad, alpha_rRad, alpha_azRad)

            # apply model for Gamm0_f
            gamma0_flat = gamma0.divide(scf)
            gamma0_flatDB = (ee.Image.constant(10)
                             .multiply(gamma0_flat.log10())
                             .select(['VV', 'VH'], ['VV_gamma0flat', 'VH_gamma0flat'])
                             )

            masks = _masking(alpha_rRad, theta_iRad, buffer)

            # calculate the ratio for RGB vis
            ratio_flat = (gamma0_flatDB.select('VV_gamma0flat')
                          .subtract(gamma0_flatDB.select('VH_gamma0flat'))
                          .rename('ratio_gamma0flat')
                          )

            if model == 'surface':
                gamma0_flatDB = gamma0_flatDB.rename(['VV_gamma0surf', 'VH_gamma0surf'])

            if model == 'volume':
                gamma0_flatDB = gamma0_flatDB.rename(['VV_gamma0vol', 'VH_gamma0vol'])

            return (image.rename(['VV_sigma0', 'VH_sigma0', 'incAngle'])
                    .addBands(gamma0dB)
                    .addBands(ratio_gamma)
                    .addBands(gamma0_flatDB)
                    .addBands(ratio_flat)
                    .addBands(alpha_rRad.rename('alpha_rRad'))
                    .addBands(alpha_azRad.rename('alpha_azRad'))
                    .addBands(phi_sRad.rename('aspect'))
                    .addBands(alpha_sRad.rename('slope'))
                    .addBands(theta_iRad.rename('theta_iRad'))
                    .addBands(theta_liaRad.rename('theta_liaRad'))
                    .addBands(masks)
                    .addBands(height.rename('elevation'))
                    )

            # run and return correction

        return collection.map(_correct, opt_dropNulls=True)

    def init_SM_retrieval(self, year, month, day, hour=12, minute=0, track=None, overwrite=False):
        # initiate all datasets for the retrieval of soil moisture
        self.get_copernicus_lc()

        self.get_S1_tmp_collection(year, month, day, hour, minute,
                                   mask_copernicuslc=True,
                                   trackflt=int(track),
                                   ascending=False)

        self.match_evi()
        self.match_l8()
        # self.match_gldas()

        self.get_l8()

        self.get_modis_evi()

        self.get_S1(tempfilter=False,
                    mask_snow_frozen_GLDAS=False)

        self.get_sand_content()
        # self.get_clay_content()
        self.get_bulk_density()

        self.OVERWRITE = overwrite

    def get_S1(self,
               tempfilter=False,
               tempfilter_radius=7,
               mask_snow_frozen_GLDAS=False):
        """Retrieve the S1 image for a given day from GEE and apply specific filters.
           Assigns outputs to respective instance attributes

        """

        def tolin(image):

            tmp = ee.Image(image)

            # Covert to linear
            out = ee.Image(10).pow(tmp.select('VV_gamma0vol').divide(10))
            # rename
            out = out.select(['constant'], ['VV_gamma0vol'])

            return out.set('system:time_start', tmp.get('system:time_start'))

        def todb(image):

            tmp = ee.Image(image)

            return ee.Image(10).multiply(tmp.log10()).set('system:time_start', tmp.get('system:time_start'))

        def create_gldas_snow_frozen_mask(image):
            s1 = ee.Image(image.get('primary'))
            gldas = ee.Image(image.get('secondary'))

            mask = ee.Image(gldas.expression("(b('SWE_inst') < 3) && (b('SoilTMP0_10cm_inst') > 275) ? 1 : 0"))

            return s1.updateMask(mask)

        def mask_evi(image):
            s1 = ee.Image(image.get('primary'))
            evi = ee.Image(image.get('secondary'))
            return s1.updateMask(evi.select(0).mask())

        gee_s1_filtered = self.S1_reference_stack

        if mask_snow_frozen_GLDAS:
            # mask snow frozen from GLDAS and ndvi from
            gldas_filt = ee.Filter.equals(leftField='system:time_start', rightField='system:time_start')
            innjoin = ee.Join.inner()
            joined_s1_gldas = innjoin.apply(gee_s1_filtered, self.GLDAS_STACK, gldas_filt)

            gee_s1_filtered = ee.ImageCollection(joined_s1_gldas.map(create_gldas_snow_frozen_mask))

        # mask evi
        evi_filt = ee.Filter.equals(leftField='system:time_start', rightField='system:time_start')
        innjoin2 = ee.Join.inner()
        joined_s1_evi = innjoin2.apply(gee_s1_filtered, self.EVI_STACK, evi_filt)
        gee_s1_filtered = ee.ImageCollection(joined_s1_evi.map(mask_evi, opt_dropNulls=True))

        # filter
        def getddist(image):
            return image.set(
                'dateDist', ee.Number(image.get('system:time_start')).subtract(
                    ee.Date(doi.strftime('%Y-%m-%dT%H:%M:%S')).millis()).abs()
            )

        # select pixels with the smalles time gap to doi and mosaic spatially
        doi = self.S1_DATE
        s1_selected = ee.Image(gee_s1_filtered.map(getddist).sort('dateDist').first())
        s1_g0vol = s1_selected.select(['VV_gamma0vol', 'VH_gamma0vol'])

        if tempfilter == True:
            # despeckle
            radius = tempfilter_radius
            units = 'pixels'
            gee_s1_linear = gee_s1_filtered.map(tolin)
            gee_s1_dspckld_vv = self._multitemporalDespeckle(gee_s1_linear.select('VV'), radius, units,
                                                             {'before': -12, 'after': 12, 'units': 'month'})
            gee_s1_dspckld_vv = gee_s1_dspckld_vv.map(todb)
            gee_s1_fltrd_vv = gee_s1_dspckld_vv.filterDate(date_selected.strftime('%Y-%m-%d'),
                                                           (date_selected + dt.timedelta(days=1)).strftime('%Y-%m-%d'))
            s1_sig0_vv = gee_s1_fltrd_vv.mosaic()

            s1_sig0 = s1_sig0_vv.select(['constant'], ['VV'])

        # extract information
        s1_g0vol_vv = s1_g0vol.select('VV_gamma0vol')

        # calculate statistical moments
        gee_s1_filtered = gee_s1_filtered.filterDate(str(doi.year) + '-01-01', str(doi.year) + '-12-31').select('VV_gamma0vol')
        gee_s1_lin = gee_s1_filtered.map(tolin)

        # check if median was alread computed
        tmpcoords = self.roi.getInfo()['coordinates']
        mean_asset_path = 's1med_' + str(abs(tmpcoords[0][0][0])) + \
                          '_' + str(abs(tmpcoords[0][0][1])) + '_' + \
                          str(abs(tmpcoords[0][2][0])) + \
                          '_' + str(abs(tmpcoords[0][2][1])) + \
                          '_' + str(self.sampling) + '_' + str(self.TRACK_NR) + '_' + str(doi.year)
        mean_asset_path = mean_asset_path.replace('.', '')
        mean_gvv_v = ee.Image('users/felixgreifeneder/' + mean_asset_path)
        try:
            mean_gvv_v.getInfo()
            print('S1 median exists')
        except:
            # compute median
            mean_gvv_v = ee.Image(gee_s1_lin.select('VV_gamma0vol').reduce(ee.Reducer.median(), parallelScale=16))

            # export asset
            self.GEE_2_disk(raster=mean_gvv_v, name=mean_asset_path, timeout=False)
            mean_gvv_v = ee.Image('users/felixgreifeneder/' + mean_asset_path)

        # std_gvv_v = ee.Image(gee_s1_lin.select('VV_gamma0vol').reduce(ee.Reducer.stdDev(), parallelScale=24))
        # g0 - surf
        # k1gvv_s = ee.Image(gee_s1_ln.select('VV_gamma0surf').reduce(ee.Reducer.mean(), parallelScale=24))
        # k2gvv_s = ee.Image(gee_s1_ln.select('VV_gamma0surf').reduce(ee.Reducer.stdDev(), parallelScale=24))
        # k3gvv_s = ee.Image(gee_s1_ln.select('VV_gamma0surf').reduce(ee.Reducer.skew(), parallelScale=24))
        # k4gvv_s = ee.Image(gee_s1_ln.select('VV_gamma0surf').reduce(ee.Reducer.kurtosis(), parallelScale=24))
        # mean_gvv_s = ee.Image(gee_s1_lin.select('VV_gamma0surf').reduce(ee.Reducer.mean(), parallelScale=24))
        # std_gvv_s = ee.Image(gee_s1_lin.select('VV_gamma0surf').reduce(ee.Reducer.stdDev(), parallelScale=24))

        # if dualpol == True:
        #     # s0
        #     k1vh = ee.Image(gee_s1_ln.select('VH_sigma0').reduce(ee.Reducer.mean(), parallelScale=24))
        #     k2vh = ee.Image(gee_s1_ln.select('VH_sigma0').reduce(ee.Reducer.stdDev(), parallelScale=24))
        #     k3vh = ee.Image(gee_s1_ln.select('VH_sigma0').reduce(ee.Reducer.skew(), parallelScale=24))
        #     k4vh = ee.Image(gee_s1_ln.select('VH_sigma0').reduce(ee.Reducer.kurtosis(), parallelScale=24))
        #     mean_vh = ee.Image(gee_s1_lin.select('VH_sigma0').reduce(ee.Reducer.mean(), parallelScale=24))
        #     std_vh = ee.Image(gee_s1_lin.select('VH_sigma0').reduce(ee.Reducer.stdDev(), parallelScale=24))
        #     # g0 - vol
        #     k1gvh_v = ee.Image(gee_s1_ln.select('VH_gamma0vol').reduce(ee.Reducer.mean(), parallelScale=24))
        #     k2gvh_v = ee.Image(gee_s1_ln.select('VH_gamma0vol').reduce(ee.Reducer.stdDev(), parallelScale=24))
        #     k3gvh_v = ee.Image(gee_s1_ln.select('VH_gamma0vol').reduce(ee.Reducer.skew(), parallelScale=24))
        #     k4gvh_v = ee.Image(gee_s1_ln.select('VH_gamma0vol').reduce(ee.Reducer.kurtosis(), parallelScale=24))
        #     mean_gvh_v = ee.Image(gee_s1_lin.select('VH_gamma0vol').reduce(ee.Reducer.mean(), parallelScale=24))
        #     std_gvh_v = ee.Image(gee_s1_lin.select('VH_gamma0vol').reduce(ee.Reducer.stdDev(), parallelScale=24))
        #     # g0 - surf
        #     k1gvh_s = ee.Image(gee_s1_ln.select('VH_gamma0surf').reduce(ee.Reducer.mean(), parallelScale=24))
        #     k2gvh_s = ee.Image(gee_s1_ln.select('VH_gamma0surf').reduce(ee.Reducer.stdDev(), parallelScale=24))
        #     k3gvh_s = ee.Image(gee_s1_ln.select('VH_gamma0surf').reduce(ee.Reducer.skew(), parallelScale=24))
        #     k4gvh_s = ee.Image(gee_s1_ln.select('VH_gamma0surf').reduce(ee.Reducer.kurtosis(), parallelScale=24))
        #     mean_gvh_s = ee.Image(gee_s1_lin.select('VH_gamma0surf').reduce(ee.Reducer.mean(), parallelScale=24))
        #     std_gvh_s = ee.Image(gee_s1_lin.select('VH_gamma0surf').reduce(ee.Reducer.stdDev(), parallelScale=24))

        # export
        # self.S1_SIG0_VV_db = s1_sig0_vv
        self.S1_G0VOL_VV_db = s1_g0vol_vv
        self.S1G0VOLMEAN_VV = ee.Image(10).multiply(mean_gvv_v.log10()).copyProperties(mean_gvv_v)

    def estimate_SM_GBR_1step(self):
        # load GBR models
        from pysmm.no_GLDAS_decisiontree_GEE__1step import tree as GBR_tree
        import sys

        g0_v_vv = self.S1_G0VOL_VV_db
        dg0_v_vv = g0_v_vv.subtract(self.S1G0VOLMEAN_VV)
        crops = self.CROPS_COVER
        grass = self.GRASS_COVER
        moss = self.MOSS_COVER
        l8b4 = self.L8_IMG.select('B4')
        l8b4med = self.L8_MEAN.select('B4_median')
        l8b5 = self.L8_IMG.select('B5')
        l8b5med = self.L8_MEAN.select('B5_median')
        l8b11 = self.L8_IMG.select('B11')
        l8b11med = self.L8_MEAN.select('B11_median')
        ndvi = self.EVI_IMG
        ndvi_med = self.EVI_MEAN
        bulk = self.BULK
        sand = self.SAND

        input_image1 = ee.Image([dg0_v_vv.toFloat(),
                                 crops.toFloat(),
                                 grass.toFloat(),
                                 moss.toFloat(),
                                 l8b4.toFloat(),
                                 l8b4med.toFloat(),
                                 l8b5.toFloat(),
                                 l8b5med.toFloat(),
                                 l8b11.toFloat(),
                                 l8b11med.toFloat(),
                                 ndvi.toFloat(),
                                 ndvi_med.toFloat(),
                                 bulk.toFloat(),
                                 sand.toFloat()])

        input_image1 = input_image1.rename(['dg0_v_vv', 'crops', 'grass', 'moss', 'l8b4', 'l8b4_med', 'l8b5',
                                            'l8b5_med', 'l8b11', 'l8b11_med', 'ndvi', 'ndvi_med', 'bulk', 'sand'])

        ipt_img_mask1 = input_image1.mask().reduce(ee.Reducer.allNonZero())

        combined_mask = ipt_img_mask1

        input_image1 = input_image1.updateMask(ee.Image(combined_mask))

        sys.setrecursionlimit(5000)
        estimated_smc = GBR_tree(input_image1)
        estimated_smc = estimated_smc.updateMask(combined_mask)

        # mask negative values
        estimated_smc = estimated_smc.updateMask(estimated_smc.gt(0))

        ## scaling
        estimated_smc = estimated_smc.multiply(100).round().int8()

        self.ESTIMATED_SM = estimated_smc.rename(['ESTIMATED_SM']).set({'system:time_start':
                                                                       ee.Date(self.S1_DATE.strftime('%Y-%m-%dT%H:%M:%S')).millis(),
                                                                       's1tracknr': int(self.TRACK_NR)})
        self.ESTIMATED_MEAN_SM = None

    def get_S1_dates(self, tracknr=None, dualpol=True, ascending=True, start='2014-01-01', stop='2020-01-01'):
        # load S1 data
        gee_s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')

        # ASCENDING acquisitions
        gee_s1_filtered = gee_s1_collection.filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .filterBounds(self.roi) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filterDate(start, opt_end=stop)

        if ascending == True:
            # Consider only image from ascending orbits
            gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))

        if dualpol == True:
            gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))

        if tracknr is not None:
            if (type(tracknr)) == list:
                gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.inList('relativeOrbitNumber_start', tracknr))
            else:
                gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('relativeOrbitNumber_start', tracknr))

        # create a list of availalbel dates
        tmp = gee_s1_filtered.getInfo()
        tmp_ids = [x['properties']['system:index'] for x in tmp['features']]

        dates = np.array(
            [dt.datetime(int(x[17:21]), int(x[21:23]), int(x[23:25]), hour=int(x[26:28]), minute=int(x[28:30])) for x in
             tmp_ids])
        orbits = np.array([x['properties']['relativeOrbitNumber_start'] for x in tmp['features']])

        return dates, orbits

    def get_S1_tmp_collection(self, year, month, day, hour, minute, trackflt=None, dualpol=True, ascending=False,
                              mask_copernicuslc=False):
        def mosaicByDate(imcol):
            def xf(d):
                d = ee.Date(d)
                im = imcol.filterDate(d, d.advance(1, "day")).mosaic()
                return im.set("system:time_start", d.millis(), "system:id", d.format("YYYY-MM-dd"))

            imlist = imcol.toList(imcol.size())
            unique_dates = imlist.map(lambda x: ee.Image(x).date().format("YYYY-MM-dd")).distinct()
            mosaic_imlist = unique_dates.map(xf)
            return ee.ImageCollection(mosaic_imlist)

        def mask_lc_copernicus(image):
            copernicus_collection = ee.ImageCollection('COPERNICUS/Landcover/100m/Proba-V/Global')
            copernicus_image = ee.Image(copernicus_collection.toList(1000).get(0)).select('discrete_classification').setDefaultProjection(image.select(1).projection()).clip(image.geometry())

            valLClist = [20, 30, 40, 60, 125, 126, 121, 122, 123, 124]

            lcmask = copernicus_image.eq(valLClist[0]).bitwiseOr(copernicus_image.eq(valLClist[1])) \
                .bitwiseOr(copernicus_image.eq(valLClist[2])) \
                .bitwiseOr(copernicus_image.eq(valLClist[3])) \
                .bitwiseOr(copernicus_image.eq(valLClist[4])) \
                .bitwiseOr(copernicus_image.eq(valLClist[5])) \
                .bitwiseOr(copernicus_image.eq(valLClist[6])) \
                .bitwiseOr(copernicus_image.eq(valLClist[7])) \
                .bitwiseOr(copernicus_image.eq(valLClist[8])) \
                .bitwiseOr(copernicus_image.eq(valLClist[9]))
            maskimg = ee.Image.cat([lcmask,
                                    lcmask,
                                    image.select('angle').mask()])

            #tmp = ee.Image(image)
            #tmp = tmp.updateMask(lcmask)

            return image.updateMask(maskimg)

        gee_s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')

        # Filter the image collection
        gee_s1_filtered = gee_s1_collection.filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .filterBounds(self.roi) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \

        if ascending:
            # Consider only image from ascending orbits
            gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))

        if dualpol:
            # Consider only dual-pol scenes
            gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))

        if trackflt is not None:
            # Specify track
            gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.eq('relativeOrbitNumber_start', trackflt))

        if mask_copernicuslc:
            gee_s1_filtered = gee_s1_filtered.map(mask_lc_copernicus)


        # filter
        def getddist(image):
            return image.set(
                'dateDist', ee.Number(image.get('system:time_start')).subtract(
                ee.Date(doi.strftime('%Y-%m-%dT%H:%M:%S')).millis()).abs()
                             )

        # select pixels with the smalles time gap to doi and mosaic spatially
        doi = dt.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        s1_selected = ee.Image(gee_s1_filtered.map(getddist).sort('dateDist').first())

        self.S1_DATE = dt.datetime.strptime(s1_selected.date().format('yyyy-MM-dd HH:mm:ss').getInfo(), '%Y-%m-%d %H:%M:%S')

        # get the track number
        s1_sig0_info = s1_selected.getInfo()
        track_nr = s1_sig0_info['properties']['relativeOrbitNumber_start']
        self.TRACK_NR = track_nr
        self.ORBIT = s1_sig0_info['properties']['orbitProperties_pass']

        # only uses images of the same track
        gee_s1_filtered = gee_s1_filtered.filterMetadata('relativeOrbitNumber_start', 'equals', track_nr)

        # calculate g0
        # paths to dem
        dem = 'USGS/SRTMGL1_003'

        # list of models
        model = 'volume'
        gee_s1_fltd_vol = self._slope_correction(gee_s1_filtered,
                                                 ee.Image(dem),
                                                 model)

        gee_s1_filtered = gee_s1_fltd_vol

        # apply no data mask
        def mask_no_data(image):
            return image.updateMask(image.select('no_data_mask'))

        gee_s1_filtered = gee_s1_filtered.map(mask_no_data)

        # self.S1_reference_stack = mosaicByDate(gee_s1_filtered)
        self.S1_reference_stack = mosaicByDate(gee_s1_filtered)

    def get_available_S1_tracks(self, dualpol=True):
        # load S1 data
        gee_s1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')

        # ASCENDING acquisitions
        gee_s1_filtered = gee_s1_collection.filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .filterBounds(self.roi) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
        #           .filter(ee.Filter.eq('platform_number', 'A')) \

        if dualpol == True:
            gee_s1_filtered = gee_s1_filtered.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))

        # create a list of availalbel dates
        tmp = gee_s1_filtered.getInfo()
        tmp_tracks = [x['properties']['relativeOrbitNumber_start'] for x in tmp['features']]
        tracks = np.unique(tmp_tracks)

        return tracks

    def check_gldas_availability(self, year, month, day):
        gldas_test = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
            .select('SoilMoi0_10cm_inst')
        last_gldas = dt.datetime.strptime(gldas_test.aggregate_max('system:index').getInfo(),
                                          "A%Y%m%d_%H%M")
        self.LAST_GLDAS = last_gldas
        doi = dt.date(year=year, month=month, day=day)
        return last_gldas.date() > doi

    def get_gldas(self, date=None):
        # get GLDAS, date can be passed as a string or copied from the extracted S1 scene
        if date is None:
            doi = ee.Date(self.S1_DATE.strftime(format='%Y-%m-%d'))

        # check if Sentinel-1 was retrieved and date is available
        if hasattr(self, 'S1_DATE'):
            gldas_mean = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                .select('SoilMoi0_10cm_inst') \
                .filterDate('2014-10-01', dt.datetime.today().strftime('%Y-%m-%d')) \
                .filter(ee.Filter.calendarRange(self.S1_DATE.hour, self.S1_DATE.hour + 3, field='hour')) \
                .reduce(ee.Reducer.median())
        else:
            gldas_mean = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                .select('SoilMoi0_10cm_inst') \
                .filterDate('2014-10-01', dt.datetime.today().strftime('%Y-%m-%d')) \
                .reduce(ee.Reducer.median())

        gldas_mean = ee.Image(gldas_mean).resample().clip(self.roi)

        # gldas = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
        #     .select('SoilMoi0_10cm_inst') \
        #     .filterDate(doi, doi.advance(3, 'hour'))
        #
        # if gldas.size().getInfo() == 0:
        #     print('No GLDAS product for specified date')
        #     gldas_test = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
        #                             .select('SoilMoi0_10cm_inst')
        #     last_gldas = gldas_test.aggregate_max('system:index').getInfo()
        #     print('ID of latest available product: ' + last_gldas)
        #     self.GLDAS_IMG = None
        #     self.GLDAS_MEAN = None
        #     return
        #
        # gldas_img = ee.Image(gldas.first()).resample().clip(self.roi)
        gldas_img = gldas_mean

        try:
            self.GLDAS_IMG = gldas_img
            self.GLDAS_MEAN = gldas_mean
        except:
            return None

    def match_l8(self):

        def mask(image):
            # clouds
            def getQABits(image, start, end, newName):
                pattern = 0
                for i in range(start, end + 1):
                    pattern = pattern + int(math.pow(2, i))

                return image.select([0], [newName]).bitwiseAnd(pattern).rightShift(start)

            def cloud_shadows(image):
                QA = image.select('pixel_qa')
                return getQABits(QA, 3, 3, 'Cloud_shadows').eq(0)

            def clouds(image):
                QA = image.select('pixel_qa')
                return getQABits(QA, 5, 5, 'Cloud').eq(0)

            # frozen soil / snow
            def frzn(image):
                doi = ee.Date(image.get('system:time_start'))
                snow = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                    .select('SWE_inst') \
                    .filterDate(doi, doi.advance(3, 'hour'))

                snow_img = ee.Image(snow.first()).resample().clip(self.roi)

                snow_mask = snow_img.expression('(b(0) < 3) ? 1 : 0')

                fs = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                    .select('SoilTMP0_10cm_inst') \
                    .filterDate(doi, doi.advance(3, 'hour'))

                fs_img = ee.Image(fs.first()).resample().clip(self.roi)

                fs_mask = fs_img.expression('(b(0) > 275) ? 1 : 0')

                return snow_mask.And(fs_mask)

            image = image.updateMask(cloud_shadows(image))
            image = image.updateMask(clouds(image))
            # image = image.updateMask(frzn(image))

            # # radiometric saturation
            # image = image.updateMask(image.select('radsat_qa').eq(2))
            return image.clip(self.roi)

        gee_l8_collection_all = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')

        # apply landsat mask
        gee_l8_collection_all = gee_l8_collection_all.map(mask).select(['B4', 'B5', 'B11'])

        def date_mosaic(image):

            def addDate(image2):
                date_img = ee.Image(image2.date().difference(imdate, 'second')).abs().float().rename(
                    ['Ddate']).multiply(-1)
                return image2.addBands(date_img)

            imdate = image.date()

            gee_l8_date = gee_l8_collection_all.filterDate(imdate.advance(-40, 'day'),
                                                           imdate.advance(40, 'day'))
            gee_l8_date = gee_l8_date.map(addDate)
            gee_l8_date = gee_l8_date.qualityMosaic('Ddate').float()

            return gee_l8_date.set('system:time_start', imdate.millis())

        self.L8_STACK = self.S1_reference_stack.map(date_mosaic)
        # self.L8_STACK = gee_l8_collection_all

    def match_evi(self):

        def mask(image):
            # mask image
            immask = image.select('SummaryQA').eq(ee.Image(0))
            evimask = image.select('EVI').lte(5000)
            image = image.updateMask(immask).updateMask(evimask)

            return image.clip(self.roi)

        # load collection
        evi_collection = ee.ImageCollection('MODIS/006/MOD13Q1').map(mask).select('EVI')

        def date_mosaic(image):
            def addDate(image2):
                date_img = ee.Image(image2.date().difference(imdate, 'second')).abs().float().rename(
                    ['Ddate']).multiply(-1)
                return image2.addBands(date_img)

            imdate = image.date()

            gee_evi_date = evi_collection.filterDate(imdate.advance(-40, 'day'),
                                                     imdate.advance(40, 'day'))
            gee_evi_date = gee_evi_date.map(addDate)
            gee_evi_date = gee_evi_date.qualityMosaic('Ddate').float()

            return gee_evi_date.set('system:time_start', imdate.millis())

        self.EVI_STACK = self.S1_reference_stack.map(date_mosaic)

    def match_gldas(self):

        def mask(image):
            return image.clip(self.roi)

        # load collection
        gl_collection = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
            .select(['SoilTMP0_10cm_inst', 'SWE_inst']) \
            .filterDate('2014-01-01', dt.datetime.today().strftime('%Y-%m-%d')).map(mask)

        def date_map(image):

            imdate = image.date()

            # filter
            def getddist(image2):
                return image2.set(
                    'dateDist', ee.Number(image2.get('system:time_start')).subtract(
                        imdate.millis()).abs()
                )

            # select the image with the smalles time gap
            gl_collection_date = gl_collection.filterDate(imdate.advance(-5, 'day'),
                                                          imdate.advance(5, 'day'))
            gee_gl_date = ee.Image(gl_collection_date.map(getddist).sort('dateDist').first())

            return gee_gl_date.set('system:time_start', imdate.millis())

        self.GLDAS_STACK = self.S1_reference_stack.map(date_map)

    def get_l8(self, date=None):
        # get Landsat-8, date can be passed as a string or copied from the extracted S1 scene

        def mask(image):
            # clouds
            def getQABits(image, start, end, newName):
                pattern = 0
                for i in range(start, end + 1):
                    pattern = pattern + int(math.pow(2, i))

                return image.select([0], [newName]).bitwiseAnd(pattern).rightShift(start)

            def cloud_shadows(image):
                QA = image.select('pixel_qa')
                return getQABits(QA, 3, 3, 'Cloud_shadows').eq(0)

            def clouds(image):
                QA = image.select('pixel_qa')
                return getQABits(QA, 5, 5, 'Cloud').eq(0)

            # frozen soil / snow
            def frzn(image):
                doi = ee.Date(image.get('system:time_start'))
                snow = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                    .select('SWE_inst') \
                    .filterDate(doi, doi.advance(3, 'hour'))

                snow_img = ee.Image(snow.first()).resample().clip(self.roi)

                snow_mask = snow_img.expression('(b(0) < 3) ? 1 : 0')

                fs = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                    .select('SoilTMP0_10cm_inst') \
                    .filterDate(doi, doi.advance(3, 'hour'))

                fs_img = ee.Image(fs.first()).resample().clip(self.roi)

                fs_mask = fs_img.expression('(b(0) > 275) ? 1 : 0')

                return snow_mask.And(fs_mask)

            image = image.updateMask(cloud_shadows(image))
            image = image.updateMask(clouds(image))
            # image = image.updateMask(frzn(image))

            # # radiometric saturation
            # image = image.updateMask(image.select('radsat_qa').eq(2))
            return image.clip(self.roi)

        gee_l8_collection_all = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')

        # apply landsat mask
        gee_l8_collection = gee_l8_collection_all.map(mask).select(['B4', 'B5', 'B11'])

        if date is None:
            doi = self.S1_DATE
        else:
            doi = date

        # check if median was alread computed
        tmpcoords = self.roi.getInfo()['coordinates']
        mean_asset_path = 'l8med_' + str(abs(tmpcoords[0][0][0])) + \
                          '_' + str(abs(tmpcoords[0][0][1])) + '_' + \
                          str(abs(tmpcoords[0][2][0])) + \
                          '_' + str(abs(tmpcoords[0][2][1])) + \
                          '_' + str(self.sampling) + '_' + str(doi.year)
        mean_asset_path = mean_asset_path.replace('.', '')
        gee_l8_mean = ee.Image('users/felixgreifeneder/' + mean_asset_path)
        try:
            gee_l8_mean.getInfo()
            print('L8 median exists')
        except:
            # compute median
            gee_l8_mean = gee_l8_collection.filterDate(str(doi.year) + '-01-01', str(doi.year) + '-12-31') \
                .reduce(ee.Reducer.median(), parallelScale=16)

            #export asset
            self.GEE_2_disk(raster=gee_l8_mean, name=mean_asset_path, timeout=False)
            gee_l8_mean = ee.Image('users/felixgreifeneder/' + mean_asset_path)

        def addDate(image2):
            date_img = ee.Image(image2.date().difference(doi.strftime('%Y-%m-%dT%H:%M:%S'), 'second')).abs().float().rename(
                ['Ddate']).multiply(-1)
            return image2.addBands(date_img)

        # create mosaic for the doi
        gee_l8_date = gee_l8_collection_all.filterDate((doi - dt.timedelta(days=40)).strftime('%Y-%m-%d'),
                                                       (doi + dt.timedelta(days=40)).strftime('%Y-%m-%d'))
        gee_l8_date = gee_l8_date.map(addDate)
        gee_l8_date = gee_l8_date.qualityMosaic('Ddate').float()

        gee_l8_date.set('system:time_start', ee.Date(doi.strftime('%Y-%m-%dT%H:%M:%S')).millis())

        #outimg = gee_l8_mosaic.clip(self.roi)

        try:
            self.L8_IMG = gee_l8_date
            self.L8_MEAN = gee_l8_mean
            self.L8_DDATE = gee_l8_date.select('Ddate').clip(self.roi).multiply(-1)
            self.L8_MASK = self.L8_IMG.mask().reduce(ee.Reducer.allNonZero(), parallelScale=8)
        except:
            return None

    def get_terrain(self):
        # get SRTM data
        elev = ee.Image("CGIAR/SRTM90_V4").select('elevation').clip(self.roi).resample()
        aspe = ee.Terrain.aspect(ee.Image("CGIAR/SRTM90_V4")).select('aspect').clip(self.roi).resample()
        slop = ee.Terrain.slope(ee.Image("CGIAR/SRTM90_V4")).select('slope').clip(self.roi).resample()
        self.TERRAIN = (elev, aspe, slop)

    def get_modis_evi(self, date=None):

        def create_gldas_snow_frozen_mask(image):
            evi = ee.Image(image.get('primary'))
            gldas = ee.Image(image.get('secondary'))

            mask = ee.Image(gldas.expression("(b('SWE_inst') < 3) && (b('SoilTMP0_10cm_inst') > 275) ? 1 : 0"))

            return evi.updateMask(mask)

        def mask(image):
            # mask image
            immask = image.select('SummaryQA').eq(ee.Image(0))
            evimask = image.select('EVI').lte(5000)
            image = image.updateMask(immask).updateMask(evimask)

            return image.clip(self.roi)

        # load collection
        evi_collection = ee.ImageCollection('MODIS/006/MOD13Q1').map(mask).select('EVI')

        if date is None:
            doi = self.S1_DATE

        # mask snow frozen from GLDAS and ndvi from
        # join gldas and l8 collections as well as
        # gldas_filt = ee.Filter.equals(leftField='system:time_start', rightField='system:time_start')
        # innjoin = ee.Join.inner()
        # joined_evi_gldas = innjoin.apply(evi_collection, self.GLDAS_STACK, gldas_filt)
        #
        # evi_collection = ee.ImageCollection(joined_evi_gldas.map(create_gldas_snow_frozen_mask))

        # check if median was already calculated
        tmpcoords = self.roi.getInfo()['coordinates']
        mean_asset_path = 'evimed_' + str(abs(tmpcoords[0][0][0])) + \
                          '_' + str(abs(tmpcoords[0][0][1])) + '_' + \
                          str(abs(tmpcoords[0][2][0])) + \
                          '_' + str(abs(tmpcoords[0][2][1])) + \
                          '_' + str(self.sampling) + '_' + str(doi.year)
        mean_asset_path = mean_asset_path.replace('.', '')
        evi_mean = ee.Image('users/felixgreifeneder/' + mean_asset_path)
        try:
            evi_mean.getInfo()
            print('EVI median exists')
        except:
            # compute avg
            evi_mean = evi_collection.filterDate(str(doi.year) + '-01-01', str(doi.year) + '-12-31') \
                .reduce(ee.Reducer.median(), parallelScale=16)

            # export asset
            self.GEE_2_disk(raster=evi_mean, name=mean_asset_path, timeout=False)
            evi_mean = ee.Image('users/felixgreifeneder/' + mean_asset_path)

        # fiter
        # filter
        def addDate(image2):
            date_img = ee.Image(image2.date().difference(doi.strftime('%Y-%m-%dT%H:%M:%S'), 'second')).abs().float().rename(
                ['Ddate']).multiply(-1)
            return image2.addBands(date_img)

        gee_evi_date = evi_collection.filterDate((doi - dt.timedelta(days=30)).strftime('%Y-%m-%d'),
                                                 (doi + dt.timedelta(days=30)).strftime('%Y-%m-%d'))
        gee_evi_date = gee_evi_date.map(addDate)
        gee_evi_date = gee_evi_date.qualityMosaic('Ddate').float()

        gee_evi_date.set('system:time_start',  ee.Date(doi.strftime('%Y-%m-%dT%H:%M:%S')).millis())

        try:
            self.EVI_IMG = gee_evi_date.select('EVI').clip(self.roi)
            self.EVI_MEAN = evi_mean.select('EVI_median')
        except:
            return None

    def get_bulk_density(self):
        bulkimg = ee.Image("OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02").select('b0')
        self.BULK = bulkimg.resample()

    def get_clay_content(self):
        clayimg = ee.Image("OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02").select('b0')
        self.CLAY = clayimg.resample()

    def get_sand_content(self):
        sandimg = ee.Image("OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02").select('b0')
        self.SAND = sandimg.resample()

    def get_copernicus_lc(self):

        copernicus_collection = ee.ImageCollection('COPERNICUS/Landcover/100m/Proba-V/Global')
        copernicus_image = ee.Image(copernicus_collection.toList(1000).get(0))
        self.LC_ID = copernicus_image.select('discrete_classification')
        self.FOREST_TYPE = copernicus_image.select('forest_type')
        self.BARE_COVER = copernicus_image.select('bare-coverfraction').resample()
        self.CROPS_COVER = copernicus_image.select('crops-coverfraction').resample()
        self.GRASS_COVER = copernicus_image.select('grass-coverfraction').resample()
        self.MOSS_COVER = copernicus_image.select('moss-coverfraction').resample()
        self.SHRUB_COVER = copernicus_image.select('shrub-coverfraction').resample()
        self.TREE_COVER = copernicus_image.select('tree-coverfraction').resample()
        self.URBAN_COVER = copernicus_image.select('urban-coverfraction').resample()
        self.WATERP_COVER = copernicus_image.select('water-permanent-coverfraction').resample()
        self.WATERS_COVER = copernicus_image.select('water-seasonal-coverfraction').resample()

    def GEE_2_asset(self, outdir=None, raster='ESTIMATED_SM', name='SM', timeout=True):
        # Export GEE rasters as asset - specify raster as string

        if isinstance(raster, str):
            geds = self.__getattribute__(raster)
        else:
            geds = raster

        if outdir is None:
            outdir = self.workdir

        try:
            file_avail = ee.Image('users/felixgreifeneder/' + outdir + '/' + name)
            file_avail.getInfo()
            if self.OVERWRITE:
                os.system('earthengine rm users/felixgreifeneder/' + outdir + '/' + name)
                raise NameError(name + ' will be overwritten')
            else:
                print(name + 'already exists')
                return
        except:
            file_exp = ee.batch.Export.image.toAsset(image=geds, description='fileexp' + name,
                                                     assetId='users/felixgreifeneder/' + outdir + '/' + name,
                                                     region=self.roi.getInfo()['coordinates'],
                                                     scale=self.sampling,
                                                     maxPixels=1000000000000)

            file_exp.start()

            start = time.time()

            while file_exp.active():
                time.sleep(2)
                if timeout and (time.time() - start) > 4800:
                    success = 0
                    break
            else:
                print('Export completed')
