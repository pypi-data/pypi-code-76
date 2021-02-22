import csv
from matplotlib import dates
import datetime as dt
import numpy as np
import pandas as pd
import sys
import matplotlib
matplotlib.use('TkAgg')
sys.path.insert(0, "../")
from interface_multi import c4gl_interface_soundings,get_record_yaml
from class4gl import class4gl_input, data_global,class4gl,units
#from sklearn.metrics import mean_squared_error
import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn.apionly as sns
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
from scipy.stats import pearsonr                                                
from matplotlib import ticker
from interface_multi import c4gl_interface_soundings,get_record_yaml
import os

c4gldata = {}

path_forcing = "/data/gent/vo/000/gvo00090/D2D/data/SOUNDINGS/GOAMAZON6/"
path_experiments = "/user/data/gent/gvo000/gvo00090/D2D/data/GOAMAZON6/"
path_corr = "/user/data/gent/gvo000/gvo00090/D2D/data/GOAMAZON/CAMPAIGN_CORR_INPUT/"
exp = 'BASE_ITER'
c4gldata[exp] = c4gl_interface_soundings( \
                  path_experiments+'/'+exp+'/',\
                  path_forcing+'/',\
                  None,\
                  refetch_records=False,\
                  obs_filter = False,\
                  tendencies_revised = False
                ) 

data = c4gldata[exp]

# select goamazon station
data.sel_station(STNID=90002)
# c4gldata[exp].next_record(-2)
obs_all = pd.read_csv('/user/data/gent/gvo000/gvo00090/EXT/archive/GOAMAZON/Pierre_AWS_Fluxos_2014_fluxes.csv')
obs_all["date"] = pd.Series([dt.datetime(2014,1,1)+dt.timedelta(seconds=((doy - 1.)*24.+4.)*3600.) for idoy,doy in obs_all.DOY.iteritems()])
obs_all["ldate"] = pd.Series([dt.datetime(2014,1,1)+dt.timedelta(seconds=((doy - 1.)*24.)*3600.) for idoy,doy in obs_all.DOY.iteritems()])

for idoy,doy in obs_all.DOY.iteritems():
    print(idoy,doy)

num_records = data.frames['profiles']['records_current_station_ini'].shape[0]



mod = []
obs = []
# select = [1,2,3,4,5,6,7,13]
select = range(num_records)
sel = 0

if (select[0]) > 0:
    data.next_record( (select[0]) - sel)
    
os.system('mkdir -p '+path_corr)
fn_ini_corr = []
file_ini_corr = []
cors = ['ORIG','EF','CC','EFCC']
for corr in cors:
    path_corr_exp = path_corr+'/'+corr+'/'
    os.system('mkdir -p '+path_corr_exp)
    fn_ini_corr.append(path_corr_exp+'/90002_ini.yaml')
    file_ini_corr.append(open(fn_ini_corr[-1],'w'))
    print(path_corr_exp)


for j,i in enumerate(select):
    sel = i
    mod.append(pd.DataFrame())
    for var in ['H','LE','Swin','Swout','Swin_cs']:
        temp = data.frames['profiles']['record_yaml_end_mod'].out.__dict__[var]
        temp = (temp[:-1] + temp[1:])/2.
        mod[-1][var] = temp

    #mod[-1] = pd.DataFrame(mod[-1][:-1]+ mod[-1][1:])[:-1]/2.
    
    mod[-1]['date'] = \
        [data.frames['profiles']['record_yaml_ini'].pars.datetime_daylight + \
         dt.timedelta(hours= time - \
                      data.frames['profiles']['record_yaml_end_mod'].out.time[0]) \
         for time in data.frames['profiles']['record_yaml_end_mod'].out.time[:-1]]
    mod[-1]['ldate'] = \
        [data.frames['profiles']['record_yaml_ini'].pars.ldatetime_daylight + \
         dt.timedelta(hours= time - \
                      data.frames['profiles']['record_yaml_end_mod'].out.time[0]) \
         for time in data.frames['profiles']['record_yaml_end_mod'].out.time[:-1]]
                        
    obs.append( pd.DataFrame(obs_all[\
                  (obs_all['date'] >= mod[-1]['date'].iloc[0]) & \
                  (obs_all['date'] <= mod[-1]['date'].iloc[-1])  \
                 ]))


    # ax.xaxis.set_major_locator(dates.HourLocator)
    if ((len(obs[-1]) > 3.) and \
       (np.mean(~np.isnan(obs[-1].LE)) > 0.50) and \
        (np.mean(~np.isnan(obs[-1].H )) > 0.50)):
        EF_campaign = obs[-1].LE.mean()/(obs[-1].H.mean() + obs[-1].LE.mean())
    else:
        EF_campaign = data.frames['profiles']['record_yaml_ini'].pars.EF
    if ((len(obs[-1]) > 10.) and \
        (np.mean(~np.isnan(obs[-1].ROC_in)) > 0.50)          
        ):
        cc_campaign = np.min((1.,
                              np.max((0.,(1.- obs[-1].ROC_in.mean()/mod[-1].Swin_cs.mean())/0.4))
                             ))
    else:
        cc_campaign = data.frames['profiles']['record_yaml_ini'].pars.cc
        
    
    print(cc_campaign)

    if (\
        (len(obs[-1]) > 4.) and \
        (np.mean(~np.isnan(obs[-1].LE)) > 0.30) and \
        (np.mean(~np.isnan(obs[-1].H )) > 0.30) and \
        (np.mean(~np.isnan(obs[-1].ROC_in)) > 0.30) \
       ):

        data.frames['profiles']['record_yaml_ini'].dump(file_ini_corr[cors.index('ORIG')])
        
        EF_orig = data.frames['profiles']['record_yaml_ini'].pars.EF
        data.frames['profiles']['record_yaml_ini'].pars.EF = float(EF_campaign)
        data.frames['profiles']['record_yaml_ini'].dump(file_ini_corr[cors.index('EF')])
        
        data.frames['profiles']['record_yaml_ini'].pars.EF = EF_orig
        data.frames['profiles']['record_yaml_ini'].pars.cc = float(cc_campaign)
        data.frames['profiles']['record_yaml_ini'].dump(file_ini_corr[cors.index('CC')])
        
        data.frames['profiles']['record_yaml_ini'].pars.EF = float(EF_campaign)
        data.frames['profiles']['record_yaml_ini'].dump(file_ini_corr[cors.index('EFCC')])
    else:
        mod.pop(-1)
        obs.pop(-1)
        print('I popped '+str(sel))
        
        
    if j+1 < len(select):

        data.next_record(select[j+1] - sel)

for icorr,corr in enumerate(cors): 
    file_ini_corr[icorr].close()
    
from matplotlib import pyplot as plt
fig = plt.figure(figsize=(9,6))
for j,i in enumerate(mod):
    columns = 4
    if j == 0:   
        ax = fig.add_subplot(np.ceil((len(mod)/columns)),columns,j+1)
    else:
        ax = fig.add_subplot(np.ceil((len(mod)/columns)),columns,j+1,sharey=axprev)

    ax.plot(obs[j].ldate,obs[j].H,'rx')
    ax.plot(mod[j].ldate,mod[j].H,'r-')
    ax.plot(obs[j].ldate,obs[j].LE,'gx')
    ax.plot(mod[j].ldate,mod[j].LE,'g-')
    ax.plot(mod[j].ldate,mod[j].Swin,'y-')
    ax.plot(mod[j].ldate,-mod[j].Swout,'m-')
    ax.plot(obs[j].ldate,obs[j].ROC_in,'yx')
    ax.plot(obs[j].ldate,- obs[j].ROC_re,'mx')
    
    ax.set_ylim((-150.,1000.))
    ax.set_xlim((dt.datetime.combine(mod[j].ldate[0].date(),dt.time(hour=5)),
                dt.datetime.combine(mod[j].ldate[0].date(),dt.time(hour=19)))
                )
    xfmt = dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation= 70 )
    
    if j < len(mod)-columns:
        ax.set_xticks([])
    #if np.mod(j,columns) != 0:
    #    ax.set_yticks([])
    ax.set_title(mod[j].ldate[0].strftime("%Y/%m/%d"))
    axprev = ax

fig.subplots_adjust(top=0.95,bottom=0.1,left=0.1,right=0.977,hspace=0.215,wspace=0.15)
fig.show()

