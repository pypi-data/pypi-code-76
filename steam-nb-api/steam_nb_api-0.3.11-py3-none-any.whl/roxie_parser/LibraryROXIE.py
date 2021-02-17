import os

from bs4 import BeautifulSoup
import requests
import urllib
from urllib.request import urlopen


class LibraryROXIE:
    '''
        Class of libray of ROXIE magnet models
    '''

    def __init__(self, repositoryWebsite='http://roxie-lhc-magnets.web.cern.ch/roxie-LHC-magnets'):
        self.repositoryWebsite = repositoryWebsite
        self.targetFileTypes = ('.cadata', '.data', '.dat', '.iron', '.mod', '.bhdata', '.madata', '.map2d', '.cond2d')

        # by default, initialize the attribute self.targetSubfolders to the LHC magnet model repository
        self.setDefaultRepositoryLHC()

    def setTargetSubfolders(self, targetSubfolders: tuple):
        '''
            **Sets target folders**

            :param targetSubfolders: tuple of strings defining the paths of the target website subfolder
            :type targetSubfolders: tuple

            :return:
        '''
        self.targetSubfolders = targetSubfolders


    def setKeyFileTypes(self, targetFileTypes: tuple):
        '''
            **Sets target file types**

            :param targetFileTypes: tuple of strings defining the file types that will be downloaded
            :type targetFileTypes: tuple

            :return:
        '''
        self.targetFileTypes = targetFileTypes

    def setDefaultRepositoryLHC(self):
        '''
            **Sets target files for downloading from the official ROXIE LHC magnet model repository**
        '''

        # list update on 2 November 2019
        self.targetSubfolders = (
            'datab',
            'GENERALS',
            'HiLumi', 'HiLumi/D1/D1_2D', 'D1/D1_Roxie_Quench', 'HiLumi/D1/D_3D', 'HiLumi/D1/old/D1_3D', 'HiLumi/D2',
            'HiLumi/DS11T', 'HiLumi/DS11T/CERN_1in1', 'HiLumi/DS11T/CERN_1in1/2D/XSEC1/',
            'HiLumi/DS11T/CERN_2in1',
            'HiLumi/DS11T/FNAL_1in1', 'HiLumi/DS11T/FNAL_1in1/2D',
            'HiLumi/DS11T/FNAL_2in1',
            'HiLumi/DS11T/FNAL_mirror',
            'HiLumi/DS11T/MBHSP',
            'HiLumi/MCBRD', 'HiLumi/MKQXF',
            'HiLumi/MQXF', 'HiLumi/MQXF/2D', 'HiLumi/MQXF/3D',
            'HiLumi/Q4/Q4_Roxie_Quench', 'HiLumi/Q4/ROXIE_Files',
            'MB', 'MB/CrossSections', 'MB/CrossSections/CrossSection1', 'MB/CrossSections/CrossSection1/datab',
            'MB/CrossSections/CrossSection2', 'MB/CrossSections/CrossSection2/datab', 'MB/CrossSections/CrossSection3',
            'MB/CrossSections/CrossSection3/datab', 'MB/Geometries/Version_133C_148E',
            'MB/Geometries/Version_133C_148E_unsymmetric', 'MB/Geometries/Version_133C_148E_warm_data',
            'MB/Geometries/Version_136B_148E',
            'MBRB', 'MBRC', 'MBRS', 'MBW', 'MBX', 'MBXW', 'MBXW/Bmap', 'MCBC', 'MCBW', 'MCBX', 'MCBY',
            'MCDO', 'MCS', 'MCSOX', 'MCSTX', 'MO', 'MQ', 'MQM', 'MQM/3D/roxie_9_3', 'MQM/CrossTalk', 'MQSX', 'MQT-MQS',
            'MQTL', 'MQWA', 'MQWB', 'MQXA', 'MQXA/Glyn', 'MQXB',
            'MQXC', 'MQXC/Complete', 'MQXF', 'MQXF/2012-10', 'MQXF/2012-12', 'MQXF/2013-02', 'MQY', 'MQY/MQY/CrossTalk',
            'MQY/CrossTalk/8', 'MQY/CrossTalk/9', 'MSCB',
        )

        self.setTargetSubfolders(self.targetSubfolders)


    def setDefaultRepositoryRnD(self):
        '''
            **Sets target files for downloading from the official ROXIE R&D magnet model repository**
        '''

        # list update on 2 November 2019
        self.targetSubfolders = (
            'ERMC', 'ERMC/ERMC_nongraded', 'ERMC/ERMC_nongraded/2D', 'ERMC/ERMC_nongraded/3D',
            'ERMC/ERMC_nongraded/old',
            'FRESCA2',
            'HD_variants', 'HD_variants/HD2', 'HD_variants/HD2_A', 'HD_variants/HD2_A_Transient',
            'HD_variants/HD2_B', 'HD_variants/HD2_C', 'HD_variants/HD2_D', 'HD_variants/HD2_D2',
            'HD_variants/HD2_D3', 'HD_variants/HD2_E', 'HD_variants/HD2_F',
            'HQ',
            'MQT',
            'MQXC', 'MQXC/MQXC_2D', 'MQXC/MQXC_3D', 'MQXC/MQXC_3D/INNER', 'MQXC/MQXC_3D/OUTER',
            'MQXC/MQXC_3D/TOTAL',
            'RMC', 'RMC/RMC_QXF_PIT',
            'RMM', 'RMM/RMM_flared', 'RMM/RMM_graded', 'RMM/RMM_nongraded', 'RMM/RMM_nongraded/2D',
            'RMM/RMM_nongraded/3D', 'RMM/bhdata', 'RMM/cadata', 'RMM/iron',
            'SMC', 'SMC/SMC11T',
        )

        self.setTargetSubfolders(self.targetSubfolders)


    def makeLocalLibrary(self, outputFolder):
        '''
            **Makes a local copy of the ROXIE magnet model library**

            Function to copy from online repository all target file types of all target magnet models

            :param outputFolder: string defining the path of the local output folder
            :type outputFolder: string

            :return:
        '''

        print('Repository of ROXIE magnet models: {}'.format(self.repositoryWebsite))

        for subfolder in self.targetSubfolders:
            print('Subfolder {}'.format(subfolder))

            # if subfolder is not existing, make one
            localSubfolder = os.path.join(outputFolder, subfolder)
            if not os.path.exists(localSubfolder):
                os.makedirs(localSubfolder)
                print('New local folder generated: {}'.format(localSubfolder))

            r = requests.get(self.repositoryWebsite + '/' + subfolder)
            data = r.text
            soup = BeautifulSoup(data)

            allFilesInSubfolder = soup.find_all('a')

            for link in allFilesInSubfolder:
                onlineFileName = link.get('href')

                for targetFileType in self.targetFileTypes:
                    if targetFileType in onlineFileName:
                        fullFileOriginal = self.repositoryWebsite + '/' + subfolder + '/' + link.get('href')
                        fullFileOutput = os.path.join(outputFolder, subfolder, link.get('href'))

                        # download file
                        try:
                            urllib.request.urlretrieve(fullFileOriginal, fullFileOutput)
                        except:
                            print('*** Subfolder {}: - File: {} - PROBLEM'.format(subfolder, onlineFileName))
                            print('*** fullFileOriginal = {}'.format(fullFileOriginal))
                            print('*** fullFileOutput = {}'.format(fullFileOutput))

                        # check that the file was downloaded successfully
                        if os.path.isfile(fullFileOutput):
                            print('Subfolder {}: - File: {} - Successfully downloaded'.format(subfolder, onlineFileName))
                        else:
                            print('Subfolder {}: - File: {} - SKIPPED'.format(subfolder, onlineFileName))


    def printTargetFiles(self):
        '''
            **Prints the target files of the ROXIE magnet model library**

            Function to find and print from online repository all target file types of all target magnet models

            :return:
        '''

        print('Repository of ROXIE magnet models: {}'.format(self.repositoryWebsite))

        for subfolder in self.targetSubfolders:
            print('Subfolder {}'.format(subfolder))

            r = requests.get(self.repositoryWebsite + '/' + subfolder)
            data = r.text
            soup = BeautifulSoup(data)

            allFilesInSubfolder = soup.find_all('a')

            for link in allFilesInSubfolder:
                onlineFileName = link.get('href')
                for targetFileType in self.targetFileTypes:
                    if targetFileType in onlineFileName:
                        print('Subfolder {}: - File: {}'.format(subfolder, onlineFileName))


