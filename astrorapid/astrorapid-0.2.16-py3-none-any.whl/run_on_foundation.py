#@title Get Foundation DR1 data and plot examples
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from astrorapid.process_light_curves import InputLightCurve
import astrorapid.helpers as helpers

passbands = ['g', 'r', 'i', 'z']

# Get filenames
data_filenames = os.listdir('../data/Foundation_DR1-master/Foundation_DR1')

light_curves = {}
light_curve_list = []

for s, data_filename in enumerate(data_filenames):
    data_filepath = os.path.join("../data/Foundation_DR1-master/Foundation_DR1", data_filename)
    if os.path.splitext(data_filepath)[-1] != '.txt':
        continue

    # Get Header data
    linecount = 0
    header = {}
    with open(data_filepath, "r") as fp:
        while True:
            line = fp.readline()
            linecount += 1
            if line[0] == "#" or line == "\n":
                continue
            if line[:3] == 'OBS' or not line:
                break
            key, val = line.replace("\n",'').split(":")
            header[key] = val
    objid = header["SNID"].strip()
    ra = float(header["RA"].strip().split("deg")[0])
    dec = float(header["DECL"].strip().split("deg")[0])
    mwebv = float(header["MWEBV"].split("+")[0])
    redshift = float(header["REDSHIFT_FINAL"].split("+")[0])
    peakmjd = float(header["SEARCH_PEAKMJD"])
    print(f"objid: {objid}, ra: {ra}, dec: {dec}, mwebv: {mwebv}, peakmjd: {peakmjd}")

    # Get Photometric Data
    data = pd.read_csv(data_filepath, skiprows=linecount-2, skipfooter=1, delim_whitespace=True)
    # print(data)
    mjd = data["MJD"].values
    passband = data["FLT"]
    flux = data["FLUXCAL"]
    fluxerr = data["FLUXCALERR"]
    photflag = np.zeros(len(mjd))
    photflag[mjd < peakmjd] = 0
    photflag[mjd > peakmjd] = 4096
    peakmjd_idx = helpers.find_nearest(mjd, peakmjd)
    photflag[peakmjd_idx] = 6144
    maxflux = max(flux)#flux[peakmjd_idx]

    light_curve_info1 = (mjd, flux, fluxerr, passband, photflag, ra, dec, objid, redshift, mwebv)
    light_curve_list += [light_curve_info1]

    # inputlightcurve = InputLightCurve(mjd, flux, fluxerr, passband, photflag,
    #                                   ra, dec, objid, redshift, mwebv,
    #                                   known_redshift=True,
    #                                   training_set_parameters={'class_number': "PS1",
    #                                                           'peakmjd': peakmjd},
    #                                   calculate_t0=False)

    # lc = inputlightcurve.preprocess_light_curve()


    # # Limit to only -80 to 70 days around trigger
    # masktimes = (lc['time'] >= -70) & (lc['time'] <= 80)
    # lc = lc[masktimes]
    # light_curves[objid] = lc

    # font = {'family': 'normal',
    #         'size': 12}

    # matplotlib.rc('font', **font)
    # color = {'g': 'tab:green', 'r': "tab:red", 'i': "tab:purple", 'z': "tab:brown"}

    # lc = light_curves[objid]
    # plt.figure()
    # for pb in passbands:
    #     pbmask = lc['passband'] == pb
    #     plt.errorbar(lc['time'][pbmask], lc['flux'][pbmask], yerr=lc['fluxErr'][pbmask], fmt='.', label=pb, color=color[pb])
    #     plt.xlim(-70, 80)
    #     plt.ylim(top=1.5*maxflux)
    #     plt.legend()

    # fit_gaussian_process(lc, objid, passbands, plot=True, extrapolate=False, bad_loglike_thresh=-500)
    # plt.show()

from astrorapid.classify import Classify

# Classify Light curves
classification = Classify(model_name='PS1_known_redshift_Ia_CC_SLSN')#known_redshift=True, model_filepath='training_set_files/Figures/PS1_test_epochs30_dropout0.2_speclabels1/keras_model.hdf5', passbands=('g', 'r', 'i', 'z'), class_names=('SLSN', 'II', 'IIn', 'Ia', 'Ibc'))

predictions, time_steps = classification.get_predictions(light_curve_list)
# print(predictions)

# Plot light curve and classification vs time of the light curves at the specified indexes
classification.plot_light_curves_and_classifications(indexes_to_plot=(0,1,4,6))
# classification.plot_classification_animation(indexes_to_plot=(0,1,4,6))


# Plot light curve and classification vs time of the light curves

CLASS_COLOR = {'Pre-explosion': 'grey', 'SNIa-norm': 'tab:green', 'SNIbc': 'tab:orange', 'SNII': 'tab:blue',
               'SNIa-91bg': 'tab:red', 'SNIa-x': 'tab:purple', 'point-Ia': 'tab:brown', 'Kilonova': '#aaffc3',
               'SLSN-I': 'tab:olive', 'PISN': 'tab:cyan', 'ILOT': '#FF1493', 'CART': 'navy', 'TDE': 'tab:pink',
               'AGN': 'bisque', 'Ia': 'tab:green', 'SLSN': 'tab:olive', 'II': 'tab:blue', 'IIn': 'tab:brown',
               'Ibc': 'tab:orange', 'CC': 'blue'}
PB_COLOR = {'u': 'tab:blue', 'g': 'tab:blue', 'r': 'tab:orange', 'i': 'm', 'z': 'k', 'Y': 'y'}

import matplotlib
from matplotlib.ticker import MaxNLocator
font = {'family': 'normal',
        'size': 12}
matplotlib.rc('font', **font)
class_names =  list(classification.class_names)

best_classes = []
best_classes_notpreexplosion = []
best_classes_last = []
for idx, prediction in enumerate(predictions):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6.5, 7.5), num="classification_vs_time_{}".format(idx), sharex=True)
    lc_data = classification.orig_lc[idx]
    argmax = classification.timesX[idx].argmax() + 1
    objid = classification.objids[idx]
    print(objid, len(predictions))
    used_passbands = [pb for pb in classification.passbands if pb in lc_data['passband']]
    for pbidx, pb in enumerate(used_passbands):
        pbmask = lc_data['passband'] == pb
        ax1.errorbar(lc_data[pbmask]['time'], lc_data[pbmask]['flux'], yerr=lc_data[pbmask]['fluxErr'], fmt='o', label=pb, c=PB_COLOR[pb], lw=2, markersize=3)
        ax1.plot(classification.timesX[idx][:argmax], classification.X[idx][:, pbidx][:argmax], c=PB_COLOR[pb], lw=2)
    new_t = np.concatenate([lc_data[lc_data['passband'] == pb]['time'].data for pb in used_passbands])
    new_t = np.sort(new_t[~np.isnan(new_t)])
    new_y_predict = []
    for classnum, classname in enumerate(class_names):
        new_y_predict.append(np.interp(new_t, classification.timesX[idx][:argmax], classification.y_predict[idx][:, classnum][:argmax]))
    for classnum, classname in enumerate(class_names):
        ax2.plot(new_t, new_y_predict[classnum], '-', label=classname, color=CLASS_COLOR[classname], linewidth=2,)
    ax1.legend(frameon=True, fontsize=12)
    ax2.legend(frameon=True, fontsize=12)
    ax2.set_xlabel("Days since trigger (rest frame)")  # , fontsize=18)
    ax1.set_ylabel("Relative Flux")  # , fontsize=15)
    ax2.set_ylabel("Class Probability")  # , fontsize=18)
    ax2.set_ylim(0, 1)
    ax1.set_xlim(left=min(new_t))  # ax1.set_xlim(-70, 80)
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=6, prune='upper'))  # added
    plt.tight_layout()
    fig.subplots_adjust(hspace=0)
    ax1.set_title(f"{objid}")
    plt.show()
    plt.close()

    best_probs_class = np.max(classification.y_predict[idx], axis=0)
    best_class = class_names[np.argmax(best_probs_class)]
    print(best_class, best_probs_class)
    best_classes.append(best_class)
    best_classes_notpreexplosion.append(class_names[np.argmax(best_probs_class[:-1])])
    best_classes_last.append(class_names[np.argmax(classification.y_predict[idx][argmax-1][:-1])])

print(np.unique(best_classes, return_counts=True))
# for bc, bccount in zip(*np.unique(best_classes, return_counts=True)):
#     print(f"{bc}: {bccount}, {round(100*bccount/len(predictions),1)}%")
# for bc, bccount in zip(*np.unique(best_classes_notpreexplosion, return_counts=True)):
#     print(f"{bc}: {bccount}, {round(100*bccount/len(predictions),1)}%")