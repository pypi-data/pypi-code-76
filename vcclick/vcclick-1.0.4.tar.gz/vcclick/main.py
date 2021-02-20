import numpy as np #line:2
from copy import deepcopy #line:3
import matplotlib .pyplot as plt #line:4
import cv2 #line:5
def show (O0OO00OOO000000OO ):#line:7
    plt .figure (figsize =(8 ,8 ))#line:8
    if np .max (O0OO00OOO000000OO )==1 :#line:10
        plt .imshow (O0OO00OOO000000OO ,vmin =0 ,vmax =1 )#line:11
    else :#line:12
        plt .imshow (O0OO00OOO000000OO ,vmin =0 ,vmax =255 )#line:13
    plt .gray ()#line:14
    plt .show ()#line:15
    plt .close ()#line:16
    print ()#line:17
def resize (OO00O00O00OO00OOO ,O000O00000O00O0O0 ):#line:19
    O0O0000OO00O0OO0O ,O0000OOOO0OOO00O0 =OO00O00O00OO00OOO .shape [:2 ]#line:21
    if O0O0000OO00O0OO0O <O0000OOOO0OOO00O0 :#line:23
        O00OO00OO0O000O0O =O000O00000O00O0O0 #line:24
        O00OOO000OO00O00O =int (O0O0000OO00O0OO0O *O000O00000O00O0O0 /O0000OOOO0OOO00O0 )#line:25
        OO0OO0O0O00OO0O0O =O0000OOOO0OOO00O0 /O000O00000O00O0O0 #line:26
    else :#line:27
        O00OOO000OO00O00O =O000O00000O00O0O0 #line:28
        O00OO00OO0O000O0O =int (O0000OOOO0OOO00O0 *O000O00000O00O0O0 /O0O0000OO00O0OO0O )#line:29
        OO0OO0O0O00OO0O0O =O0O0000OO00O0OO0O /O000O00000O00O0O0 #line:30
    OO00O00O00OO00OOO =cv2 .resize (OO00O00O00OO00OOO ,(O00OO00OO0O000O0O ,O00OOO000OO00O00O ),interpolation =cv2 .INTER_CUBIC )#line:31
    print ('------------------------------------')#line:33
    print ('resizing in window size ({}, {})'.format (O00OO00OO0O000O0O ,O00OOO000OO00O00O ))#line:34
    print ('(w, h) = ({}, {})'.format (O0000OOOO0OOO00O0 ,O0O0000OO00O0OO0O ))#line:35
    print ('(w, h) = ({}, {})'.format (O00OO00OO0O000O0O ,O00OOO000OO00O00O ))#line:36
    return OO00O00O00OO00OOO ,OO0OO0O0O00OO0O0O #line:37
class pointlist ():#line:39
    def __init__ (OO0O0O0O00O000O00 ):#line:40
        OO0O0O0O00O000O00 .points =[]#line:41
        OO0O0O0O00O000O00 .L =[]#line:42
        OO0O0O0O00O000O00 .R =[]#line:43
        OO0O0O0O00O000O00 .state =None #line:44
    def add (O0000000O0000O0O0 ,O0O0000O0O00OO0OO ,O0000OOOO00OO00O0 ,O00OO00O0O0OOO00O ):#line:46
        O0000000O0000O0O0 .points .append ([O0O0000O0O00OO0OO ,O0000OOOO00OO00O0 ])#line:47
        if O00OO00O0O0OOO00O =='L':#line:48
            O0000000O0000O0O0 .L .append ([O0O0000O0O00OO0OO ,O0000OOOO00OO00O0 ])#line:49
            O0000000O0000O0O0 .state ='L'#line:50
        if O00OO00O0O0OOO00O =='R':#line:51
            O0000000O0000O0O0 .R .append ([O0O0000O0O00OO0OO ,O0000OOOO00OO00O0 ])#line:52
            O0000000O0000O0O0 .state ='R'#line:53
        print ('points[{}] = ({}, {})'.format (len (O0000000O0000O0O0 .points )-1 ,O0O0000O0O00OO0OO ,O0000OOOO00OO00O0 ))#line:54
class vcclick :#line:56
    def __init__ (OO00O0O0OO0O0OOO0 ):#line:57
        pass #line:58
    def __del__ (O00000O000O0O00OO ):#line:59
        pass #line:60
    def get_draw (OOOOOO0O00OOOO0OO ,return_size ='original'):#line:62
        if return_size =='original':#line:63
            OOOOOO0O00OOOO0OO .img_draw_original =cv2 .resize (OOOOOO0O00OOOO0OO .img_draw ,OOOOOO0O00OOOO0OO .img_original .shape [:2 ][::-1 ],interpolation =cv2 .INTER_CUBIC )#line:64
            return OOOOOO0O00OOOO0OO .img_draw_original #line:65
        else :#line:66
            return OOOOOO0O00OOOO0OO .img_draw #line:67
    def get_mask (OOO000OOOO00O0000 ,return_size ='original'):#line:69
        if OOO000OOOO00O0000 .mode =='single':#line:70
            if return_size =='original':#line:71
                O000O0O000OOOOO00 =np .zeros (OOO000OOOO00O0000 .img_original .shape ,int )#line:72
                O0O00OO00OOO0OOO0 =np .array (OOO000OOOO00O0000 .points .points )*OOO000OOOO00O0000 .rate #line:73
                O0O00OO00OOO0OOO0 =O0O00OO00OOO0OOO0 .astype (int )#line:74
                cv2 .fillConvexPoly (O000O0O000OOOOO00 ,points =O0O00OO00OOO0OOO0 ,color =(1 ,1 ,1 ))#line:75
            else :#line:76
                O000O0O000OOOOO00 =np .zeros (OOO000OOOO00O0000 .img .shape ,int )#line:77
                O0O00OO00OOO0OOO0 =np .array (OOO000OOOO00O0000 .points .points )#line:78
                cv2 .fillConvexPoly (O000O0O000OOOOO00 ,points =O0O00OO00OOO0OOO0 ,color =(1 ,1 ,1 ))#line:79
        if OOO000OOOO00O0000 .mode =='multi':#line:80
            if return_size =='original':#line:81
                O000O0O000OOOOO00 =np .zeros (OOO000OOOO00O0000 .img_original .shape ,int )#line:82
                for OOOOOOO0OOO00O0O0 in OOO000OOOO00O0000 .points_set :#line:84
                    O0O00OO00OOO0OOO0 =np .array (OOOOOOO0OOO00O0O0 )*OOO000OOOO00O0000 .rate #line:85
                    O0O00OO00OOO0OOO0 =O0O00OO00OOO0OOO0 .astype (int )#line:86
                    cv2 .fillConvexPoly (O000O0O000OOOOO00 ,points =O0O00OO00OOO0OOO0 ,color =(1 ,1 ,1 ))#line:87
            else :#line:88
                O000O0O000OOOOO00 =np .zeros (OOO000OOOO00O0000 .img .shape ,int )#line:89
                for OOOOOOO0OOO00O0O0 in OOO000OOOO00O0000 .points_set :#line:91
                    O0O00OO00OOO0OOO0 =np .array (OOOOOOO0OOO00O0O0 )#line:92
                    cv2 .fillConvexPoly (O000O0O000OOOOO00 ,points =O0O00OO00OOO0OOO0 ,color =(1 ,1 ,1 ))#line:93
        O000O0O000OOOOO00 =np .sum (O000O0O000OOOOO00 ,axis =2 )==3 #line:94
        return O000O0O000OOOOO00 #line:95
    def single (OO0O0O0O000O00O00 ,OO0OOOOOO000OOO00 ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:101
        OO0O0O0O000O00O00 .img_original =np .array (OO0OOOOOO000OOO00 )#line:103
        OO0O0O0O000O00O00 .window_size =window_size #line:104
        assert guide ==None or len (guide )==3 #line:105
        assert marker ==None or len (marker )==3 #line:106
        assert line ==None or len (line )==3 #line:107
        OO0O0O0O000O00O00 .guide =guide [::-1 ]if guide !=None else None #line:108
        OO0O0O0O000O00O00 .marker =marker [::-1 ]if marker !=None else None #line:109
        OO0O0O0O000O00O00 .line =line [::-1 ]if line !=None else None #line:110
        OO0O0O0O000O00O00 .points =pointlist ()#line:111
        OO0O0O0O000O00O00 .points_set =[]#line:112
        OO0O0O0O000O00O00 .wname ='aaa'#line:113
        OO0O0O0O000O00O00 .img ,OO0O0O0O000O00O00 .rate =resize (OO0O0O0O000O00O00 .img_original ,OO0O0O0O000O00O00 .window_size )#line:116
        OO0O0O0O000O00O00 .h ,OO0O0O0O000O00O00 .w =OO0O0O0O000O00O00 .img .shape [:2 ]#line:118
        OO0O0O0O000O00O00 .img_draw =deepcopy (OO0O0O0O000O00O00 .img )#line:119
        OO0O0O0O000O00O00 .mode ='single'#line:122
        cv2 .namedWindow (OO0O0O0O000O00O00 .wname )#line:123
        cv2 .setMouseCallback (OO0O0O0O000O00O00 .wname ,OO0O0O0O000O00O00 .start )#line:124
        cv2 .imshow (OO0O0O0O000O00O00 .wname ,OO0O0O0O000O00O00 .img )#line:126
        cv2 .waitKey ()#line:127
        if return_size =='original':#line:130
            print ('return in original size {}'.format (OO0O0O0O000O00O00 .img_original .shape [:2 ][::-1 ]))#line:131
            print ('------------------------------------')#line:132
            return np .array (OO0O0O0O000O00O00 .points .points )*OO0O0O0O000O00O00 .rate #line:133
        else :#line:134
            print ('return in window size {}'.format (OO0O0O0O000O00O00 .img .shape [:2 ][::-1 ]))#line:135
            return np .array (OO0O0O0O000O00O00 .points .points )#line:136
    def multi (O0OO0OOOOOOO0OO0O ,O000O00O00OOOOOOO ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:142
        O0OO0OOOOOOO0OO0O .img_original =np .array (O000O00O00OOOOOOO )#line:144
        O0OO0OOOOOOO0OO0O .window_size =window_size #line:145
        assert guide ==None or len (guide )==3 #line:146
        assert marker ==None or len (marker )==3 #line:147
        assert line ==None or len (line )==3 #line:148
        O0OO0OOOOOOO0OO0O .guide =guide [::-1 ]if guide !=None else None #line:149
        O0OO0OOOOOOO0OO0O .marker =marker [::-1 ]if marker !=None else None #line:150
        O0OO0OOOOOOO0OO0O .line =line [::-1 ]if line !=None else None #line:151
        O0OO0OOOOOOO0OO0O .points =pointlist ()#line:152
        O0OO0OOOOOOO0OO0O .points_set =[]#line:153
        O0OO0OOOOOOO0OO0O .wname ='aaa'#line:154
        O0OO0OOOOOOO0OO0O .img ,O0OO0OOOOOOO0OO0O .rate =resize (O0OO0OOOOOOO0OO0O .img_original ,O0OO0OOOOOOO0OO0O .window_size )#line:157
        O0OO0OOOOOOO0OO0O .h ,O0OO0OOOOOOO0OO0O .w =O0OO0OOOOOOO0OO0O .img .shape [:2 ]#line:159
        O0OO0OOOOOOO0OO0O .img_draw =deepcopy (O0OO0OOOOOOO0OO0O .img )#line:160
        O0OO0OOOOOOO0OO0O .mode ='multi'#line:163
        cv2 .namedWindow (O0OO0OOOOOOO0OO0O .wname )#line:164
        cv2 .setMouseCallback (O0OO0OOOOOOO0OO0O .wname ,O0OO0OOOOOOO0OO0O .start )#line:165
        cv2 .imshow (O0OO0OOOOOOO0OO0O .wname ,O0OO0OOOOOOO0OO0O .img )#line:167
        cv2 .waitKey ()#line:168
        if return_size =='original':#line:171
            print ('return in original size {}'.format (O0OO0OOOOOOO0OO0O .img_original .shape [:2 ][::-1 ]))#line:172
            print ('------------------------------------')#line:173
            OOOO00O000O000O00 =deepcopy (O0OO0OOOOOOO0OO0O .points_set )#line:174
            for O00O00O00OOO0O000 in range (len (OOOO00O000O000O00 )):#line:175
                OOOO00O000O000O00 [O00O00O00OOO0O000 ]=np .array (OOOO00O000O000O00 [O00O00O00OOO0O000 ])*O0OO0OOOOOOO0OO0O .rate #line:176
            return OOOO00O000O000O00 #line:177
        else :#line:178
            print ('return in window size {}'.format (O0OO0OOOOOOO0OO0O .img .shape [:2 ][::-1 ]))#line:179
            OOOO00O000O000O00 =deepcopy (O0OO0OOOOOOO0OO0O .points_set )#line:180
            for O00O00O00OOO0O000 in range (len (OOOO00O000O000O00 )):#line:181
                OOOO00O000O000O00 [O00O00O00OOO0O000 ]=np .array (OOOO00O000O000O00 [O00O00O00OOO0O000 ])#line:182
            return O0OO0OOOOOOO0OO0O .points_set #line:183
    def start (OO0OO00OO000O0000 ,OO00O00O00O00O000 ,OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ,O00O000OO0OOOO0O0 ,OOO00000O0O000OO0 ):#line:186
        if OO00O00O00O00O000 ==cv2 .EVENT_MOUSEMOVE :#line:188
            OOOO0O0O0O000OOOO =deepcopy (OO0OO00OO000O0000 .img_draw )#line:190
            if OO0OO00OO000O0000 .guide !=None :#line:192
                cv2 .line (OOOO0O0O0O000OOOO ,(OOOOOOOO0OO00O0OO ,0 ),(OOOOOOOO0OO00O0OO ,OO0OO00OO000O0000 .h -1 ),OO0OO00OO000O0000 .guide )#line:193
                cv2 .line (OOOO0O0O0O000OOOO ,(0 ,OO000O00OOO0O0000 ),(OO0OO00OO000O0000 .w -1 ,OO000O00OOO0O0000 ),OO0OO00OO000O0000 .guide )#line:194
            if OO0OO00OO000O0000 .points .state =='L':#line:196
                if OO0OO00OO000O0000 .line !=None :#line:197
                    OO0000O00O0OOO0OO ,OOO0O0OOO0O000000 =OO0OO00OO000O0000 .points .L [-1 ]#line:198
                    cv2 .line (OOOO0O0O0O000OOOO ,(OO0000O00O0OOO0OO ,OOO0O0OOO0O000000 ),(OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ),OO0OO00OO000O0000 .guide )#line:199
            cv2 .imshow (OO0OO00OO000O0000 .wname ,OOOO0O0O0O000OOOO )#line:201
        if OO00O00O00O00O000 ==cv2 .EVENT_LBUTTONDOWN :#line:204
            if OO0OO00OO000O0000 .points .state =='L':#line:206
                cv2 .circle (OO0OO00OO000O0000 .img_draw ,(OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ),4 ,OO0OO00OO000O0000 .marker ,1 )#line:208
                if OO0OO00OO000O0000 .line !=None :#line:210
                    OO0000O00O0OOO0OO ,OOO0O0OOO0O000000 =OO0OO00OO000O0000 .points .L [-1 ]#line:211
                    cv2 .line (OO0OO00OO000O0000 .img_draw ,(OO0000O00O0OOO0OO ,OOO0O0OOO0O000000 ),(OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ),OO0OO00OO000O0000 .line )#line:212
                OO0OO00OO000O0000 .points .add (OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ,'L')#line:214
                cv2 .imshow (OO0OO00OO000O0000 .wname ,OO0OO00OO000O0000 .img_draw )#line:216
            else :#line:218
                OO0OO00OO000O0000 .points .add (OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ,'L')#line:220
                cv2 .circle (OO0OO00OO000O0000 .img_draw ,(OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ),8 ,OO0OO00OO000O0000 .marker ,1 )#line:222
                cv2 .imshow (OO0OO00OO000O0000 .wname ,OO0OO00OO000O0000 .img_draw )#line:224
        if OO00O00O00O00O000 ==cv2 .EVENT_RBUTTONDOWN :#line:227
            if OO0OO00OO000O0000 .points .state =='L':#line:229
                cv2 .circle (OO0OO00OO000O0000 .img_draw ,(OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ),8 ,OO0OO00OO000O0000 .marker ,1 )#line:231
                if OO0OO00OO000O0000 .line !=None :#line:233
                    OO0000O00O0OOO0OO ,OOO0O0OOO0O000000 =OO0OO00OO000O0000 .points .L [-1 ]#line:234
                    cv2 .line (OO0OO00OO000O0000 .img_draw ,(OO0000O00O0OOO0OO ,OOO0O0OOO0O000000 ),(OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ),OO0OO00OO000O0000 .line )#line:235
                OO0OO00OO000O0000 .points .add (OOOOOOOO0OO00O0OO ,OO000O00OOO0O0000 ,'R')#line:237
                cv2 .imshow (OO0OO00OO000O0000 .wname ,OO0OO00OO000O0000 .img_draw )#line:239
                if OO0OO00OO000O0000 .mode =='multi':#line:242
                    OO0OO00OO000O0000 .points_set .append (OO0OO00OO000O0000 .points .points )#line:243
                    OO0OO00OO000O0000 .points =pointlist ()#line:244
            else :#line:247
                pass #line:248
            if OO0OO00OO000O0000 .mode =='single':#line:251
                cv2 .destroyAllWindows ()#line:252
if __name__ =='__main__':#line:255
    file_name ='yoko.JPG'#line:257
    img =cv2 .imread (file_name )#line:264
    show (img )#line:265
    aaa =vcclick ()#line:268
    points =aaa .multi (img ,window_size =1000 ,line =None )#line:269
    print (points )#line:270
    show (aaa .get_draw ())#line:271
    show (aaa .get_mask ())#line:272
