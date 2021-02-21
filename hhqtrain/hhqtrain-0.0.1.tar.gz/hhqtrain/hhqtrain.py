import numpy as np
import detect_mfcc_plot
import scipy.stats as st
import os
import datetime
def train(norfile_list, falfile_list, envfile_list, nor_per_time, mfcc_n, now_chdir):
    norfilenum = len(norfile_list)
    falfilenum = len(falfile_list)
    envfilenum = len(envfile_list)

    nor_gauss_all = np.empty((norfilenum, (mfcc_n + 1), 2), dtype=float)
    fal_gauss_all = np.empty((falfilenum, (mfcc_n + 1), 2), dtype=float)
    env_gauss_all = np.empty((envfilenum, (mfcc_n + 1), 2), dtype=float)
    detect_time = np.empty((1, 1, 1), dtype=float)
    detect_time[0][0][0] = nor_per_time[0]

    for x in range(norfilenum):

        gauss_list_all_T = []
        nor_fft_feature_list = []
        filename = norfile_list[x]
        os.chdir(filename)
        wav_files = os.listdir()

        for wav_file in wav_files:
            fft_ = detect_mfcc_plot.wav_mfcc(wav_file, mfcc_n)
            nor_fft_feature_list.append(fft_)
        nor_fft_feature_array = np.asarray(nor_fft_feature_list)  # 将list转为array，方便以后处理

        for p in range(mfcc_n):
            temp = nor_fft_feature_array[:, p]
            mean = np.mean(temp)
            std = np.std(temp)
            nor_gauss_all[x][p][0] = mean
            nor_gauss_all[x][p][1] = std
            gauss_list = []
            for m in range(len(wav_files)):
                gauss = st.norm.pdf(temp[m], nor_gauss_all[x][p][0], nor_gauss_all[x][p][1])
                gauss_list.append(gauss)
            gauss_list_all_T.append(gauss_list)
        gauss_list_all_T = np.asarray(gauss_list_all_T)
        gauss_list_all = gauss_list_all_T.T
        #print(gauss_list_all.shape)
        mean_list = []
        for i in range(len(gauss_list_all)):
            mean = np.mean(gauss_list_all[i])
            mean_list.append(mean)
        nor_gauss_all[x][mfcc_n][0] = np.mean(mean_list)
        nor_gauss_all[x][mfcc_n][1] = np.std(mean_list)

    for x in range(falfilenum):
        gauss_list_all_T = []
        fal_fft_feature_list = []
        filename = falfile_list[x]
        os.chdir(filename)
        wav_files = os.listdir()

        for wav_file in wav_files:
            fft_ = detect_mfcc_plot.wav_mfcc(wav_file, mfcc_n)
            fal_fft_feature_list.append(fft_)
        fal_fft_feature_array = np.asarray(fal_fft_feature_list)  # 将list转为array，方便以后处理

        for p in range(mfcc_n):
            temp = fal_fft_feature_array[:, p]
            mean = np.mean(temp)
            std = np.std(temp)
            fal_gauss_all[x][p][0] = mean
            fal_gauss_all[x][p][1] = std
            gauss_list = []
            for m in range(len(wav_files)):
                gauss = st.norm.pdf(temp[m], fal_gauss_all[x][p][0], fal_gauss_all[x][p][1])
                gauss_list.append(gauss)
            gauss_list_all_T.append(gauss_list)
        gauss_list_all_T = np.asarray(gauss_list_all_T)
        gauss_list_all = gauss_list_all_T.T
        mean_list = []
        for i in range(len(gauss_list_all)):
            mean = np.mean(gauss_list_all[i])
            mean_list.append(mean)
        fal_gauss_all[x][mfcc_n][0] = np.mean(mean_list)
        fal_gauss_all[x][mfcc_n][1] = np.std(mean_list)

    for x in range(envfilenum):
        gauss_list_all_T = []
        env_fft_feature_list = []
        filename = envfile_list[x]
        os.chdir(filename)
        wav_files = os.listdir()

        for wav_file in wav_files:
            fft_ = detect_mfcc_plot.wav_mfcc(wav_file, mfcc_n)
            env_fft_feature_list.append(fft_)
        env_fft_feature_array = np.asarray(env_fft_feature_list)  # 将list转为array，方便以后处理

        for p in range(mfcc_n):
            temp = env_fft_feature_array[:, p]
            mean = np.mean(temp)
            std = np.std(temp)
            env_gauss_all[x][p][0] = mean
            env_gauss_all[x][p][1] = std
            gauss_list = []
            for m in range(len(wav_files)):
                gauss = st.norm.pdf(temp[m], env_gauss_all[x][p][0], env_gauss_all[x][p][1])
                gauss_list.append(gauss)
            gauss_list_all_T.append(gauss_list)
        gauss_list_all_T = np.asarray(gauss_list_all_T)
        gauss_list_all = gauss_list_all_T.T
        mean_list = []
        for i in range(len(gauss_list_all)):
            mean = np.mean(gauss_list_all[i])
            mean_list.append(mean)
        env_gauss_all[x][mfcc_n][0] = np.mean(mean_list)
        env_gauss_all[x][mfcc_n][1] = np.std(mean_list)

    os.chdir(now_chdir)
    file_name = './model'
    word_name = os.path.exists(file_name)
    if not word_name:
        os.makedirs(file_name)
    modeldir = now_chdir + '\model'
    os.chdir(modeldir)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')
    file_name = 'model' + now_time + '.npy'
    np.save(file=file_name, arr=(nor_gauss_all, fal_gauss_all, env_gauss_all, detect_time))
