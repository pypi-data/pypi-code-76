#############################################################
#
#  Author: Sebastian Maurice, PhD
#  Copyright by Sebastian Maurice 2018
#  All rights reserved.
#  Email: Sebastian.maurice@gmail.com
#
#############################################################

import imp
import json, urllib
import requests
import maads
import urllib.request
import os


#maads = imp.load_source('maads','sendfiles.py')

    
def dotraining(maadstoken,thefile,autofeature,removeoutliers,hasseasonality,dependentvariable,url,throttle=-1,theserverlocalname='',summer='6,7,8',winter='12,1,2,3',shoulder='4,5,9,10,11',trainingpercentage=75,retrainingdays=0,retraindeploy=0,shuffle=0,username='',passw='',company='',email=''):
#   rmsg=maads.uploadcsvfortraining(thefile,username,passw,autofeature,removeoutliers,hasseasonality,dependentvariable,company,email,url,summer,winter,shoulder,trainingpercentage)
   #print(rmsg)
   if autofeature != -1 and autofeature != 1 and autofeature != 0:
      return "ERROR: Incorrect autofeature value: 1,0,-1"
   if removeoutliers != 1 and removeoutliers != 0:
      return "ERROR: Incorrect removeoutlier value value: 1,0"
   if hasseasonality != 1 and hasseasonality != 0:
      return "ERROR: Incorrect hasseasonality value value: 1,0"
      
   if trainingpercentage<40 or trainingpercentage>100:
      return "ERROR: Incorrect training percentage value: Must be between 40 and 100, inclusive"
   if hasseasonality:
      if len(summer)==0 or len(winter)==0 or len(shoulder)==0:
         return "ERROR: Summer, Winter and Shoulder must contain month values."
      if len(summer)>0:
         ss=summer.split(",")
         for i in ss:
            if int(i)<1 or int(i)>12:
               return "ERROR: Summer months: Months must be between 1 and 12."
      if len(winter)>0:
         ss=winter.split(",")
         for i in ss:
            if int(i)<1 or int(i)>12:
               return "ERROR: Winter months: Months must be between 1 and 12."
      if len(shoulder)>0:
         ss=shoulder.split(",")
         for i in ss:
            if int(i)<1 or int(i)>12:
               return "ERROR: Shoulder months: Months must be between 1 and 12."

   if  retrainingdays<0:
      return "ERROR: Invalid retraining day."
   else:
      retrainingdays=int(retrainingdays)

   if  retraindeploy<0 or retraindeploy>1:
      return "ERROR: Invalid retraining deploy: must be 0 or 1."
   else:
      retraindeploy=int(retraindeploy)
      
   rmsg=maads.uploadcsvfortraining(maadstoken,thefile,autofeature,removeoutliers,hasseasonality,dependentvariable,url,throttle,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy,shuffle,theserverlocalname,username,passw,company,email)
   rms=rmsg.split(":")[0]
   rms=rms.lstrip('\n')
   rms=rms.rstrip('\n')
   rms=rms.strip()
   if rms.lower()=='error':
        #print(thedata)
      return rmsg
    
   if rmsg.find("FEATURECOMPLETE:")!=-1:
      fn=rmsg[18:]
      url = "%s" % (fn)
      #print(url)
      base=os.path.basename(thefile)
      floc=os.path.splitext(base)[0]
      if len(os.path.dirname(thefile))>0:
          localname=os.path.dirname(thefile)+ "/" +floc +"_features.csv"
      else:
          localname=floc +"_features.csv"
          
      #print(localname)
      urllib.request.urlretrieve(url, localname)
      return "Feature file retrieved:" + localname
   try:
     pkeylist=rmsg.splitlines()
   #print(pkeylist)
     pkeyname=pkeylist[3]
   except Exception as e:
     return "ERROR: There was an error.  Likely the file is too large or it is not properly formatted.  Check max filesize on server." 
   #print(pkeyname)
   
   pkey=pkeyname[5:]
   #print(pkey)
   base=os.path.basename(thefile)
   floc=os.path.splitext(base)[0]
##   if len(os.path.dirname(thefile))>0:
##      localpdf=os.path.dirname(thefile)+ "/" +floc +"_REPORT.pdf"
##      localpred=os.path.dirname(thefile)+ "/" +floc +"_PREDICTION.csv"
##      localfeat=os.path.dirname(thefile)+ "/" +floc +"_FEATURES.csv"
##   else:
   localpdf=floc +"_REPORT.pdf"
   localpred=floc +"_PREDICTION.csv"
   localfeat=floc +"_FEATURES.csv"
      
   a=url.split("/")
   a=a[:-1]
   b='/'.join(a)
   
   try:   
      remotepdf="%s.pdf" % (pkey)
      url = "%s/pdfreports/%s" % (b,remotepdf)
      #print(url)
      urllib.request.urlretrieve(url, localpdf)
   except Exception as e:
      a=1
      print("Cannot download remotefile: %s TO %s" % (url,localpdf))
   
   #Prediction Data
   try:
      remotepred="%s.csv" % (pkey)
      url = "%s/csvuploads/%s" % (b,remotepred)
      #print(url)
      urllib.request.urlretrieve(url, localpred)
   except Exception as e:
      a=1
      print("Cannot download remotefile: %s TO %s" % (url,localpred))


   if autofeature==1:
      try:
         remotefeat="%s_.csv" % (pkey)
         url = "%s/autofeatures/%s" % (b,remotefeat)
         urllib.request.urlretrieve(url, localfeat)
      except Exception as e:
         a=1
         print("Cannot download remotefile: %s TO %s" % (url,localfeat))
      
   return rmsg

def dopredictions(maadstoken,attr,pkey,thefile,url,username='',passw='',company='',email=''):
   rmsg=maads.getpredictions(maadstoken,attr,pkey,thefile,url,username,passw,company,email)
   #print(rmsg)
   return rmsg


