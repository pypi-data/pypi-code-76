import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import *
from decimal import Decimal

def SynInt (O0OCkxQpwOO0CkxQpw0CkxQpw0 ,CkxQpw0CkxQpw000OCkxQpwOO0 ):
  OCkxQpw0O0JpWzACkxQpwO0 =[]
  OOO0CkxQpwO0OOCkxQpw0OO =[]
  OOCkxQpw00pQwkxQpwOOO0O =[]
  OO0CkxQpwCkxQpw0CkxQpw0O0O =[]
  OO0OCkxQpwOO0CkxQpwCkxQpw0 =len (O0OCkxQpwOO0CkxQpw0CkxQpw0 )
  OO0OCkxQpw0CkxQpwO0CkxQpw0 =CkxQpw0CkxQpw000OCkxQpwOO0 
  for HkMmZaEOOOCkxQpTTyXLmPz in list (range (0 ,OO0OCkxQpwOO0CkxQpwCkxQpw0 -CkxQpw0CkxQpw000OCkxQpwOO0 )):
    OO0OCkxQpwOIoZttSO0OO =O0OCkxQpwOO0CkxQpw0CkxQpw0 [HkMmZaEOOOCkxQpTTyXLmPz :(HkMmZaEOOOCkxQpTTyXLmPz +(CkxQpw0CkxQpw000OCkxQpwOO0 ))].mean ()
    OOOOCkxQpw000IoZttSO0 =O0OCkxQpwOO0CkxQpw0CkxQpw0 [(HkMmZaEOOOCkxQpTTyXLmPz +CkxQpw0CkxQpw000OCkxQpwOO0 ):(HkMmZaEOOOCkxQpTTyXLmPz +2 *CkxQpw0CkxQpw000OCkxQpwOO0 )].mean ()
    O0CkxQpwOO0OOCkxQpwOCkxQpw =(OOOOCkxQpw000IoZttSO0 -OO0OCkxQpwOIoZttSO0OO )
    OO0CkxQpw0OOO0CkxQpwCkxQpw =HkMmZaEOOOCkxQpTTyXLmPz +CkxQpw0CkxQpw000OCkxQpwOO0 
    OOCkxQpw00pQwkxQpwOOO0O .append (OO0CkxQpw0OOO0CkxQpwCkxQpw )
    OCkxQpw0O0JpWzACkxQpwO0 .append (O0CkxQpwOO0OOCkxQpwOCkxQpw )
    OOO0CkxQpwO0OOCkxQpw0OO .append (np .sum (OCkxQpw0O0JpWzACkxQpwO0 ))
  CkxQpwOO0OOJpWzAOCkxQpw =O0OCkxQpwOO0CkxQpw0CkxQpw0 [int (np .floor (.5 *CkxQpw0CkxQpw000OCkxQpwOO0 )):int (np .ceil (1.5 *CkxQpw0CkxQpw000OCkxQpwOO0 ))].mean ()
  JpWzACkxQpw00OCkxQpwCkxQpw =1 /CkxQpw0CkxQpw000OCkxQpwOO0 
  CkxQpw0OCkxQpwO0OJpWzAO =10000 
  OOO0OOO0CkxQpwpQwkxQpw0 =0 
  OCkxQpw0OCkxQpw00OCkxQpwOO =1 
  O0OJpWzAOCkxQpwOCkxQpw0 =1 
  CkxQpw0O0CkxQpw0OO0OOOO =100 
  for HkMmZaEOOOCkxQpTTyXLmPz in range (CkxQpw0OCkxQpwO0OJpWzAO ):
    CkxQpwHkMmZaEOOOOOCkxQpw0 =OOO0CkxQpwO0OOCkxQpw0OO [0 :OO0OCkxQpwOO0CkxQpwCkxQpw0 ]
    CkxQpwHkMmZaEOOOOOCkxQpw0 =np .multiply (CkxQpwHkMmZaEOOOOOCkxQpw0 ,JpWzACkxQpw00OCkxQpwCkxQpw )
    CkxQpwHkMmZaEOOOOOCkxQpw0 =list (map (lambda OO0CkxQpwO0CkxQpwO0OCkxQpw :OO0CkxQpwO0CkxQpwO0OCkxQpw +CkxQpwOO0OOJpWzAOCkxQpw ,CkxQpwHkMmZaEOOOOOCkxQpw0 ))
    O0OOCkxQpwOOJpWzAOO0 =np .subtract (O0OCkxQpwOO0CkxQpw0CkxQpw0 [(CkxQpw0CkxQpw000OCkxQpwOO0 ):(OO0OCkxQpwOO0CkxQpwCkxQpw0 )],CkxQpwHkMmZaEOOOOOCkxQpw0 [0 :OO0OCkxQpwOO0CkxQpwCkxQpw0 ])
    O0OOCkxQpwOOJpWzAOO0 =np .power (O0OOCkxQpwOOJpWzAOO0 ,2 )
    O0OCkxQpwOJpWzAO0CkxQpw =np .sum (O0OOCkxQpwOOJpWzAOO0 )
    O0CkxQpwOJpWzACkxQpwO0O =(2 /OO0OCkxQpwOO0CkxQpwCkxQpw0 )*O0OCkxQpwOJpWzAO0CkxQpw 
    if np .abs (CkxQpw0O0CkxQpw0OO0OOOO )<.000001 :
      break 
    CkxQpw0O0CkxQpw0OO0OOOO =np .abs (OCkxQpw0OCkxQpw00OCkxQpwOO )-np .abs (O0CkxQpwOJpWzACkxQpwO0O )
    if CkxQpw0O0CkxQpw0OO0OOOO <0 :
      O0OJpWzAOCkxQpwOCkxQpw0 =-O0OJpWzAOCkxQpwOCkxQpw0 
      OOO0OOO0CkxQpwpQwkxQpw0 =OOO0OOO0CkxQpwpQwkxQpw0 +HkMmZaEOOOCkxQpTTyXLmPz 
    O0O0JpWzAOIoZttSO0 =CkxQpwOO0OOJpWzAOCkxQpw -(CkxQpwOO0OOJpWzAOCkxQpw *(1 /(2 *OOO0OOO0CkxQpwpQwkxQpw0 +2 )))*O0OJpWzAOCkxQpwOCkxQpw0 
    OCkxQpw0OCkxQpw00OCkxQpwOO =O0CkxQpwOJpWzACkxQpwO0O 
    CkxQpwOO0OOJpWzAOCkxQpw =O0O0JpWzAOIoZttSO0 
    OO0CkxQpwCkxQpw0CkxQpw0O0O .append (O0CkxQpwOJpWzACkxQpwO0O )
  OOO0CkxQpwO0OOCkxQpw0OO =np .multiply (OOO0CkxQpwO0OOCkxQpw0OO ,JpWzACkxQpw00OCkxQpwCkxQpw )+CkxQpwOO0OOJpWzAOCkxQpw 
  O0CkxQpTTyXLmPz0OOCkxQpw =np .multiply (OCkxQpw0O0JpWzACkxQpwO0 ,JpWzACkxQpw00OCkxQpwCkxQpw )
  return (OOO0CkxQpwO0OOCkxQpw0OO ,O0CkxQpTTyXLmPz0OOCkxQpw ,OOCkxQpw00pQwkxQpwOOO0O ,OO0OCkxQpw0CkxQpwO0CkxQpw0 ,CkxQpwOO0OOJpWzAOCkxQpw )
def SIproject (O0O0CkxQpwOO0O0HkMmZaE ,OO0CkxQpwOOCkxQpw0OCkxQpwO ,HkMmZaEO0OzGmjExCkxQpw0 ,OO0O0OCkxQpwOCkxQpwO0OO ):
  OOHkMmZaEOCkxQpwCkxQpw00O =len (HkMmZaEO0OzGmjExCkxQpw0 )
  (CkxQpwO0O0CkxQpw00OOO0O ,O0OCkxQpwCkxQpw000HkMmZaE ,OOO0CkxQpwCkxQpwOO0OOO0 ,OOIoZttSCkxQpwOOCkxQpw00 ,CkxQpw0OOO0OOCkxQpwO0OO )=SynInt (OO0CkxQpwOOCkxQpw0OCkxQpwO ,OO0O0OCkxQpwOCkxQpwO0OO )
  HkMmZaEO0CkxQpwOOOOCkxQpw =CkxQpwO0O0CkxQpw00OOO0O .min ()
  CkxQpw00JpWzAOOOCkxQpwO =CkxQpwO0O0CkxQpw00OOO0O .max ()
  HkMmZaEOOzGmjExCkxQpw0O =0 
  O0O0OCkxQpwCkxQpwO0CkxQpwO =len (CkxQpwO0O0CkxQpw00OOO0O )-2 *OO0O0OCkxQpwOCkxQpwO0OO 
  if O0O0OCkxQpwCkxQpwO0CkxQpwO <0 :
    O0O0OCkxQpwCkxQpwO0CkxQpwO =0 
  CkxQpw0OO0HkMmZaEOO0OO =CkxQpwO0O0CkxQpw00OOO0O [O0O0OCkxQpwCkxQpwO0CkxQpwO :len (CkxQpwO0O0CkxQpw00OOO0O )-2 ].mean ()
  O0O0OOOOOOOCkxQpwOO0 =CkxQpwO0O0CkxQpw00OOO0O [len (CkxQpwO0O0CkxQpw00OOO0O )-1 ]
  OO0CkxQpw0OOOCkxQpw0000 =(O0O0OOOOOOOCkxQpwOO0 -CkxQpw0OO0HkMmZaEOO0OO )/OO0O0OCkxQpwOCkxQpwO0OO 
  OCkxQpw0IoZttSO0CkxQpwO0 =HkMmZaEO0OzGmjExCkxQpw0 [len (HkMmZaEO0OzGmjExCkxQpw0 )-1 ]
  OOO0CkxQpwOO0CkxQpwCkxQpw0 =[]
  OOOOCkxQpwOOOCkxQpwO0OO =[]
  OIoZttSCkxQpw0OCkxQpw0O0 =[]
  CkxQpTTyXLmPzOOOOOOOO =[]
  for O0JpWzAOOOOOOCkxQpw0 in list (range (0 ,ceil (OO0O0OCkxQpwOCkxQpwO0OO +1 ))):
    OO0CkxQpwzGmjExCkxQpwOO0 =OCkxQpw0IoZttSO0CkxQpwO0 +O0JpWzAOOOOOOCkxQpw0 +1 
    if O0JpWzAOOOOOOCkxQpw0 ==0 :
      CkxQpw0IoZttSOCkxQpw0CkxQpw =O0O0CkxQpwOO0O0HkMmZaE [len (O0O0CkxQpwOO0O0HkMmZaE )-1 ]
      O0CkxQpwCkxQpw000OO0O0O =O0O0OOOOOOOCkxQpwOO0 
      CkxQpw0IoZttSOCkxQpw0CkxQpw =CkxQpw0IoZttSOCkxQpw0CkxQpw +O0CkxQpwCkxQpw000OO0O0O 
    elif (O0O0OOO0OCkxQpw00O0O <=CkxQpw00JpWzAOOOCkxQpwO and O0O0OOO0OCkxQpw00O0O >=HkMmZaEO0CkxQpwOOOOCkxQpw )and HkMmZaEOOzGmjExCkxQpw0O ==0 :
      O0CkxQpwCkxQpw000OO0O0O =O0JpWzAOOOOOOCkxQpw0 *OO0CkxQpw0OOOCkxQpw0000 +O0O0OOOOOOOCkxQpwOO0 
      CkxQpw0IoZttSOCkxQpw0CkxQpw =CkxQpw0IoZttSOCkxQpw0CkxQpw +O0CkxQpwCkxQpw000OO0O0O 
    elif HkMmZaEOOzGmjExCkxQpw0O ==1 :
      O0CkxQpwCkxQpw000OO0O0O =-1 *np .abs (OO0CkxQpw0OOOCkxQpw0000 )+O0O0OOO0OCkxQpw00O0O 
      CkxQpw0IoZttSOCkxQpw0CkxQpw =CkxQpw0IoZttSOCkxQpw0CkxQpw +O0CkxQpwCkxQpw000OO0O0O 
    elif HkMmZaEOOzGmjExCkxQpw0O ==-1 :
      O0CkxQpwCkxQpw000OO0O0O =np .abs (OO0CkxQpw0OOOCkxQpw0000 )+O0O0OOO0OCkxQpw00O0O 
      CkxQpw0IoZttSOCkxQpw0CkxQpw =CkxQpw0IoZttSOCkxQpw0CkxQpw +O0CkxQpwCkxQpw000OO0O0O 
    OOO0CkxQpwOO0CkxQpwCkxQpw0 .append (CkxQpw0IoZttSOCkxQpw0CkxQpw )
    OOOOCkxQpwOOOCkxQpwO0OO .append (O0CkxQpwCkxQpw000OO0O0O )
    HkMmZaEO0OzGmjExCkxQpw0 .append (OO0CkxQpwzGmjExCkxQpwOO0 )
    OIoZttSCkxQpw0OCkxQpw0O0 .append (CkxQpw0IoZttSOCkxQpw0CkxQpw )
    CkxQpTTyXLmPzOOOOOOOO .append (O0CkxQpwCkxQpw000OO0O0O )
    O0O0OOO0OCkxQpw00O0O =OOOOCkxQpwOOOCkxQpwO0OO [len (OOOOCkxQpwOOOCkxQpwO0OO )-1 ]
    if O0O0OOO0OCkxQpw00O0O >CkxQpw00JpWzAOOOCkxQpwO :
        HkMmZaEOOzGmjExCkxQpw0O =1 
    if O0O0OOO0OCkxQpw00O0O <HkMmZaEO0CkxQpwOOOOCkxQpw :
        HkMmZaEOOzGmjExCkxQpw0O =-1 
  O0O0CkxQpwOO0O0HkMmZaE =np .concatenate ((O0O0CkxQpwOO0O0HkMmZaE ,OOO0CkxQpwOO0CkxQpwCkxQpw0 ),axis =0 )
  OO0CkxQpwOOCkxQpw0OCkxQpwO =np .concatenate ((OO0CkxQpwOOCkxQpw0OCkxQpwO ,OOOOCkxQpwOOOCkxQpwO0OO ),axis =0 )
  OCkxQpw0000O0HkMmZaEO0 =HkMmZaEO0OzGmjExCkxQpw0 [0 :OOHkMmZaEOCkxQpwCkxQpw00O ]
  return (O0O0CkxQpwOO0O0HkMmZaE ,OO0CkxQpwOOCkxQpw0OCkxQpwO ,HkMmZaEO0OzGmjExCkxQpw0 ,OCkxQpw0000O0HkMmZaEO0 )
def SIforecast (CkxQpwOOOOJpWzAHkMmZaE ,OO0OOOJpWzAOHkMmZaE ,OJpWzACkxQpw0O0CkxQpwO0 ,spec_index ="auto"):
  OOO0CkxQpwOOCkxQpwO0CkxQpw =np .array (CkxQpwOOOOJpWzAHkMmZaE ).reshape (len (CkxQpwOOOOJpWzAHkMmZaE ))
  CkxQpwOO0OCkxQpwOOJpWzA =np .empty ((0 ,3 ),int )
  CkxQpwCkxQpwwTUuSbBU0OCkxQpw =list (range (3 ,(OO0OOOJpWzAOHkMmZaE +3 ),1 ))
  OOHkMmZaECkxQpwOCkxQpw000 =len (CkxQpwCkxQpwwTUuSbBU0OCkxQpw )
  for O0O0OCkxQpwOOOIoZttSO in list (range (0 ,OOHkMmZaECkxQpwOCkxQpw000 )):
    O0CkxQpw0O0CkxQpw0IoZttS =[]
    O0OOCkxQpwOOCkxQpw0OCkxQpw =[]
    O0OCkxQpwCkxQpwCkxQpw00000 =[]
    OO0O0CkxQpw0OO0O0CkxQpw =CkxQpwCkxQpwwTUuSbBU0OCkxQpw [O0O0OCkxQpwOOOIoZttSO ]
    (O0OCkxQpwJpWzAOIoZttS ,CkxQpwOCkxQpwHkMmZaEHkMmZaE ,OOzGmjExCkxQpwO0O0OOO ,OHkMmZaEOOO0OCkxQpwOOO ,OCkxQpwOOOOCkxQpw0O0OOO )=SynInt (OOO0CkxQpwOOCkxQpwO0CkxQpw ,OO0O0CkxQpw0OO0O0CkxQpw )
    JpWzAOO0CkxQpwO0CkxQpwO =len (O0OCkxQpwJpWzAOIoZttS )-1 
    for OOzGmjExCkxQpwCkxQpw0O0O in list (range ((spec_index ),(JpWzAOO0CkxQpwO0CkxQpwO +1 ),1 )):
      CkxQpw0O0HkMmZaEO0OOO0 =OOzGmjExCkxQpwCkxQpw0O0O 
      if spec_index ==0 :
        OJpWzACkxQpw0O0CkxQpwO0 =0 
      (OHkMmZaECkxQpw000OO0O0 ,CkxQpw0OOOCkxQpw0O0OOOO ,O0OCkxQpwOCkxQpwOOCkxQpw00 ,O0O0CkxQpw00O0CkxQpwOOO )=SIproject (O0OCkxQpwJpWzAOIoZttS [(CkxQpw0O0HkMmZaEO0OOO0 -OJpWzACkxQpw0O0CkxQpwO0 ):CkxQpw0O0HkMmZaEO0OOO0 ],CkxQpwOCkxQpwHkMmZaEHkMmZaE [(CkxQpw0O0HkMmZaEO0OOO0 -OJpWzACkxQpw0O0CkxQpwO0 ):CkxQpw0O0HkMmZaEO0OOO0 ],OOzGmjExCkxQpwO0O0OOO [(CkxQpw0O0HkMmZaEO0OOO0 -OJpWzACkxQpw0O0CkxQpwO0 ):CkxQpw0O0HkMmZaEO0OOO0 ],OO0O0CkxQpw0OO0O0CkxQpw )
      O0CkxQpw0O0CkxQpw0IoZttS .append (OHkMmZaECkxQpw000OO0O0 [len (OHkMmZaECkxQpw000OO0O0 )-1 ])
      OCkxQpwOOCkxQpwO0CkxQpw0OO =np .array (O0CkxQpw0O0CkxQpw0IoZttS )
      O0OCkxQpwCkxQpwCkxQpw00000 .append (O0OCkxQpwOCkxQpwOOCkxQpw00 [len (O0OCkxQpwOCkxQpwOOCkxQpw00 )-1 ])
      O0OOCkxQpwOOCkxQpw0OCkxQpw .append (OO0O0CkxQpw0OO0O0CkxQpw )
      O0OCkxQpw0CkxQpwOCkxQpwCkxQpw =np .array ((O0OCkxQpwCkxQpwCkxQpw00000 ,OCkxQpwOOCkxQpwO0CkxQpw0OO ,O0OOCkxQpwOOCkxQpw0OCkxQpw )).transpose ()
    CkxQpwOO0OCkxQpwOOJpWzA =np .concatenate ((CkxQpwOO0OCkxQpwOOJpWzA ,O0OCkxQpw0CkxQpwOCkxQpwCkxQpw ),axis =0 )
  CkxQpwCkxQpw0pQwkxQpw0CkxQpw0 =pd .DataFrame (CkxQpwOO0OCkxQpwOOJpWzA )
  return (CkxQpwCkxQpw0pQwkxQpw0CkxQpw0 )
def aggProcess (O0O0OOJpWzAOIoZttS ,OO0OCkxQpw00OOOOOCkxQpw ,CkxQpwOOOOCkxQpwCkxQpw00OO ):
  CkxQpwOJpWzAO0OOO0O0 =O0O0OOJpWzAOIoZttS 
  CkxQpw0pQwkxQpw0wTUuSbBUO =O0O0OOJpWzAOIoZttS ['index'].unique ()
  O0CkxQpwOOOOCkxQpw0CkxQpwO =list (range (0 ,len (CkxQpw0pQwkxQpw0wTUuSbBUO )))
  O0CkxQpwOOJpWzACkxQpwOO =[]
  OOOOOOCkxQpwO0OOO0O0 =[]
  OCkxQpwOCkxQpw00OO0OCkxQpw =[]
  O0CkxQpwCkxQpw0OCkxQpwCkxQpw0 =[]
  JpWzAOO0O0OOO0OOO =[]
  OOO0JpWzACkxQpwOO0O0 =[]
  OOCkxQpwCkxQpw0CkxQpw0000O =[]
  OOJpWzACkxQpwCkxQpwOO0O =1 
  for OCkxQpw0OCkxQpwCkxQpw0000O in O0CkxQpwOOOOCkxQpw0CkxQpwO :
    OHkMmZaEO0CkxQpw0000OO =CkxQpwOJpWzAO0OOO0O0 .loc [CkxQpwOJpWzAO0OOO0O0 ['index']==CkxQpw0pQwkxQpw0wTUuSbBUO [OCkxQpw0OCkxQpwCkxQpw0000O ]]
    OCkxQpwCkxQpw0OHkMmZaEOO0 =np .max (OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz'])
    OOJpWzACkxQpwOOHkMmZaE =np .min (OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz'])
    CkxQpwOO0OOHkMmZaEOO0O =np .mean (OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz'])
    O0OOCkxQpw0OCkxQpw0OOOO =len (OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz'])
    try :
      OOO0CkxQpwCkxQpwO0OCkxQpw0 =OO0OCkxQpw00OOOOOCkxQpw ['sdata'].loc [OO0OCkxQpw00OOOOOCkxQpw ['index_a']==CkxQpw0pQwkxQpw0wTUuSbBUO [OCkxQpw0OCkxQpwCkxQpw0000O ]].values [0 ]
      O0CkxQpwOIoZttSCkxQpwO0O =len (OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz'].loc [OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz']<OOO0CkxQpwCkxQpwO0OCkxQpw0 ].values )/O0OOCkxQpw0OCkxQpw0OOOO 
    except :
      OOJpWzACkxQpwCkxQpwOO0O =OOJpWzACkxQpwCkxQpwOO0O +1 /(10 *CkxQpwOOOOCkxQpwCkxQpw00OO )
      O0CkxQpwOIoZttSCkxQpwO0O =.5 -(.5 -O0CkxQpwOIoZttSCkxQpwO0O )/(OOJpWzACkxQpwCkxQpwOO0O )
    OOCkxQpwCkxQpwO0CkxQpw000O =OHkMmZaEO0CkxQpw0000OO ['xOzLptTHz'].quantile (O0CkxQpwOIoZttSCkxQpwO0O )
    O0CkxQpwOOJpWzACkxQpwOO .append (CkxQpw0pQwkxQpw0wTUuSbBUO [OCkxQpw0OCkxQpwCkxQpw0000O ])
    OOOOOOCkxQpwO0OOO0O0 .append (O0OOCkxQpw0OCkxQpw0OOOO )
    OCkxQpwOCkxQpw00OO0OCkxQpw .append (O0CkxQpwOIoZttSCkxQpwO0O )
    O0CkxQpwCkxQpw0OCkxQpwCkxQpw0 .append (OOCkxQpwCkxQpwO0CkxQpw000O )
    JpWzAOO0O0OOO0OOO .append (OCkxQpwCkxQpw0OHkMmZaEOO0 )
    OOO0JpWzACkxQpwOO0O0 .append (OOJpWzACkxQpwOOHkMmZaE )
    OOCkxQpwCkxQpw0CkxQpw0000O .append (CkxQpwOO0OOHkMmZaEOO0O )
  OCkxQpwCkxQpwOOCkxQpwO0OOO =np .array ((O0CkxQpwOOJpWzACkxQpwOO ,OOOOOOCkxQpwO0OOO0O0 ,OCkxQpwOCkxQpw00OO0OCkxQpw ,O0CkxQpwCkxQpw0OCkxQpwCkxQpw0 ,JpWzAOO0O0OOO0OOO ,OOO0JpWzACkxQpwOO0O0 ,OOCkxQpwCkxQpw0CkxQpw0000O )).transpose ()
  OO0HkMmZaECkxQpw0OOO0O =pd .DataFrame (OCkxQpwCkxQpwOOCkxQpwO0OOO )
  OO0HkMmZaECkxQpw0OOO0O =OO0HkMmZaECkxQpw0OOO0O .rename (columns ={0 :"index_f",1 :"cindex",2 :"pval",3 :"forecast",4 :"upperbound",5 :"lowerbound",6 :"mprojection"})
  return OO0HkMmZaECkxQpw0OOO0O 
def generate_forecast (OCkxQpTTyXLmPzwTUuSbBUO ,OOHkMmZaECkxQpwO0CkxQpw00 ,OO0CkxQpw0CkxQpw00000O0 ):
  O0CkxQpw000IoZttSOOO0 =OCkxQpTTyXLmPzwTUuSbBUO 
  O0CkxQpw000IoZttSOOO0 ['index_a']=np .arange (O0CkxQpw000IoZttSOOO0 .shape [0 ])+1 
  CkxQpw0JpWzAO0OCkxQpwO0 =O0CkxQpw000IoZttSOOO0 ['sdata']
  OCkxQpwO0OCkxQpwO0OCkxQpwO =(2 *OOHkMmZaECkxQpwO0CkxQpw00 )
  OOO0CkxQpw0CkxQpwwTUuSbBU =len (CkxQpw0JpWzAO0OCkxQpwO0 )-OCkxQpwO0OCkxQpwO0OCkxQpwO -10 
  OOOCkxQpwwTUuSbBU0O0OO =SIforecast (CkxQpw0JpWzAO0OCkxQpwO0 ,OOHkMmZaECkxQpwO0CkxQpw00 ,OCkxQpwO0OCkxQpwO0OCkxQpwO ,OOO0CkxQpw0CkxQpwwTUuSbBU )
  OOOCkxQpwwTUuSbBU0O0OO .columns =["index","xOzLptTHz","wQew0jVsd"]
  O0HkMmZaECkxQpwCkxQpwCkxQpw0 =aggProcess (OOOCkxQpwwTUuSbBU0O0OO ,O0CkxQpw000IoZttSOOO0 ,OOHkMmZaECkxQpwO0CkxQpw00 )
  O0HkMmZaECkxQpwCkxQpwCkxQpw0 ['cat_id']=OO0CkxQpw0CkxQpw00000O0 
  OOOOOCkxQpw0OOO0O0OO =np .max (O0CkxQpw000IoZttSOOO0 ["index_a"])
  OCkxQpw000OCkxQpwOCkxQpw00 =np .max (O0CkxQpw000IoZttSOOO0 ["date"])
  OIoZttSCkxQpw000O0CkxQpw ="d"
  O0CkxQpw0OOJpWzAO0OO =pd .Series (pd .period_range (OCkxQpw000OCkxQpwOCkxQpw00 ,freq =OIoZttSCkxQpw000O0CkxQpw ,periods =OOHkMmZaECkxQpwO0CkxQpw00 +1 ).to_timestamp ())[1 :]
  OCkxQpw000OCkxQpwpQwkxQpw0 =pd .Series (list (range (OOOOOCkxQpw0OOO0O0OO +1 ,OOOOOCkxQpw0OOO0O0OO +OOHkMmZaECkxQpwO0CkxQpw00 +1 )))
  OOCkxQpw000O0OCkxQpw00O ={'index_a':OCkxQpw000OCkxQpwpQwkxQpw0 .reset_index (drop =True ),'date':O0CkxQpw0OOJpWzAO0OO .reset_index (drop =True )}
  OOCkxQpwOOOOOOOOOCkxQpw =pd .DataFrame (OOCkxQpw000O0OCkxQpw00O )
  CkxQpw0OCkxQpwOOCkxQpw00O0 =O0CkxQpw000IoZttSOOO0 .append ([OOCkxQpwOOOOOOOOOCkxQpw ])
  CkxQpw0OCkxQpwOOCkxQpw00O0 ['cat_id']=OO0CkxQpw0CkxQpw00000O0 
  return (O0CkxQpw000IoZttSOOO0 ,O0HkMmZaECkxQpwCkxQpwCkxQpw0 )
def simple_si_forecast (O0CkxQpw0CkxQpwOCkxQpwOOO0 ,OOCkxQpw0IoZttSOOCkxQpwO ,O0OCkxQpw0000OCkxQpw000 ):
  OCkxQpwOCkxQpwCkxQpw0CkxQpw0O =O0CkxQpw0CkxQpwOCkxQpwOOO0 
  OCkxQpwOCkxQpwCkxQpw0CkxQpw0O ['index_a']=np .arange (OCkxQpwOCkxQpwCkxQpw0CkxQpw0O .shape [0 ])+1 
  OCkxQpw0OOCkxQpwHkMmZaEOO =O0CkxQpw0CkxQpwOCkxQpwOOO0 ['sdata']
  CkxQpw00O0JpWzACkxQpw0O =OOCkxQpw0IoZttSOOCkxQpwO 
  (O0OCkxQpw0000pQwkxQpwO0 ,OOOOCkxQpwO0O0OCkxQpwOO ,CkxQpw0CkxQpw00000OCkxQpw0 ,O0JpWzAOCkxQpwOHkMmZaE ,O0OCkxQpwCkxQpw0pQwkxQpw00 )=SynInt (OCkxQpw0OOCkxQpwHkMmZaEOO ,CkxQpw00O0JpWzACkxQpw0O )
  (OOCkxQpw00O0OOCkxQpwO0O ,CkxQpwO0OCkxQpwOOOOCkxQpw0 ,OCkxQpw00O0CkxQpwCkxQpw00O ,CkxQpw0CkxQpw00000OCkxQpw0 )=SIproject (O0OCkxQpw0000pQwkxQpwO0 ,OOOOCkxQpwO0O0OCkxQpwOO ,CkxQpw0CkxQpw00000OCkxQpw0 ,CkxQpw00O0JpWzACkxQpw0O )
  CkxQpw0OCkxQpw000JpWzAO =pd .DataFrame ({'Ix':OCkxQpw00O0CkxQpwCkxQpw00O ,'SI':OOCkxQpw00O0OOCkxQpwO0O ,'SD':CkxQpwO0OCkxQpwOOOOCkxQpw0 })
  CkxQpw0OCkxQpw000JpWzAO ["sVal"]=O0JpWzAOCkxQpwOHkMmZaE 
  CkxQpw0OCkxQpw000JpWzAO ["cat_id"]=O0OCkxQpw0000OCkxQpw000 
  CkxQpw0pQwkxQpw0HkMmZaEOO =np .max (OCkxQpwOCkxQpwCkxQpw0CkxQpw0O ["index_a"])
  O0OCkxQpwpQwkxQpTTyXLmPz =np .max (OCkxQpwOCkxQpwCkxQpw0CkxQpw0O ["date"])
  OCkxQpw0OO0OOOOOOCkxQpw ="d"
  O0OOCkxQpwCkxQpwCkxQpwO0OO =pd .Series (pd .period_range (O0OCkxQpwpQwkxQpTTyXLmPz ,freq =OCkxQpw0OO0OOOOOOCkxQpw ,periods =OOCkxQpw0IoZttSOOCkxQpwO +1 ).to_timestamp ())[1 :]
  CkxQpw000O0OCkxQpw0000O =pd .Series (list (range (CkxQpw0pQwkxQpw0HkMmZaEOO +1 ,CkxQpw0pQwkxQpw0HkMmZaEOO +OOCkxQpw0IoZttSOOCkxQpwO +1 )))
  OHkMmZaECkxQpwO0CkxQpw000 ={'index_a':CkxQpw000O0OCkxQpw0000O .reset_index (drop =True ),'date':O0OOCkxQpwCkxQpwCkxQpwO0OO .reset_index (drop =True )}
  OCkxQpw00O0OCkxQpwO0OOO =pd .DataFrame (OHkMmZaECkxQpwO0CkxQpw000 )
  O0CkxQpw0OCkxQpwOCkxQpwOO0 =OCkxQpwOCkxQpwCkxQpw0CkxQpw0O .append ([OCkxQpw00O0OCkxQpwO0OOO ])
  O0CkxQpw0OCkxQpwOCkxQpwOO0 ['cat_id']=O0OCkxQpw0000OCkxQpw000 
  return (CkxQpw0OCkxQpw000JpWzAO ,O0CkxQpw0OCkxQpwOCkxQpwOO0 )