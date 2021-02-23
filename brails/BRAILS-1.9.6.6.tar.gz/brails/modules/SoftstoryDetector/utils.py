import json 
import xmltodict 
import glob
import os
import subprocess
import numpy as np
import xml.etree.ElementTree as ET
import pandas as pd

def processcvat(xmlfiles, namemap):

    imgPath = []
    xtl = []
    ytl = []
    xbr = []
    ybr = []
    use = []
    security = []
    material = []
    condition = []
    completeness = []
    width = []
    height = []
    
    for f in xmlfiles:
        
        with open(f) as xml_file:
            fstr = xml_file.read()
            
            if namemap:
                for k in namemap:
                    fstr = fstr.replace(k, namemap[k])
            
            j = xmltodict.parse(fstr)
            
            imgs = j['annotations']['image']
            for img in imgs:
                name = img['@name']
                w = img['@width']
                h = img['@height']
                
                try:
                    bs = img['box']

                    for b in bs:
                            
                        xtl.append(b['@xtl'])
                        ytl.append(b['@ytl'])
                        xbr.append(b['@xbr'])
                        ybr.append(b['@ybr'])
                        attributes = b['attribute']
                        imgPath.append(name)
                        width.append(w)
                        height.append(h)
                        thisatt = {}
                        for att in attributes:
                            attName = att['@name']
                            attValue = att['#text']
                            thisatt[attName] = attValue
                        use.append(thisatt['use'])
                        security.append(thisatt['security'])
                        material.append(thisatt['material'])
                        condition.append(thisatt['condition'])
                        completeness.append(thisatt['completeness'])

                except: pass
                
                try:
                    
                    xtl.append(bs['@xtl'])
                    ytl.append(bs['@ytl'])
                    xbr.append(bs['@xbr'])
                    ybr.append(bs['@ybr'])


                    attributes = bs['attribute']
                    imgPath.append(name)
                    width.append(w)
                    height.append(h)
                    thisatt = {}
                    for att in attributes:
                        attName = att['@name']
                        attValue = att['#text']
                        thisatt[attName] = attValue
                    use.append(thisatt['use'])
                    security.append(thisatt['security'])
                    material.append(thisatt['material'])
                    condition.append(thisatt['condition'])
                    completeness.append(thisatt['completeness'])

                except: pass
                
          
    df = pd.DataFrame(list(zip(imgPath,width,height,xtl,ytl,xbr,ybr, material,use,condition,security,completeness)), columns =['imgPath','width','height','xtl','ytl','xbr','ybr', 'material','use','condition','security','completeness'])

    return df
