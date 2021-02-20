import numpy as np #line:2
from copy import deepcopy #line:3
import matplotlib .pyplot as plt #line:4
import cv2 #line:5
def show (O0OO0OO0000O0O0O0 ):#line:7
    plt .figure (figsize =(8 ,8 ))#line:8
    if np .max (O0OO0OO0000O0O0O0 )==1 :#line:10
        plt .imshow (O0OO0OO0000O0O0O0 ,vmin =0 ,vmax =1 )#line:11
    else :#line:12
        plt .imshow (O0OO0OO0000O0O0O0 ,vmin =0 ,vmax =255 )#line:13
    plt .gray ()#line:14
    plt .show ()#line:15
    plt .close ()#line:16
    print ()#line:17
def resize (O0O000O000OOOOO00 ,OOOOOOO00O0O00O0O ):#line:19
    OO00O0OOOO0O0O0OO ,O0000O0000O000O0O =O0O000O000OOOOO00 .shape [:2 ]#line:21
    if OO00O0OOOO0O0O0OO <O0000O0000O000O0O :#line:23
        OOOO00O0OO000OO0O =OOOOOOO00O0O00O0O #line:24
        OOOOO000OO0000O0O =int (OO00O0OOOO0O0O0OO *OOOOOOO00O0O00O0O /O0000O0000O000O0O )#line:25
        O00O0OOOOO0O0OO0O =O0000O0000O000O0O /OOOOOOO00O0O00O0O #line:26
    else :#line:27
        OOOOO000OO0000O0O =OOOOOOO00O0O00O0O #line:28
        OOOO00O0OO000OO0O =int (O0000O0000O000O0O *OOOOOOO00O0O00O0O /OO00O0OOOO0O0O0OO )#line:29
        O00O0OOOOO0O0OO0O =OO00O0OOOO0O0O0OO /OOOOOOO00O0O00O0O #line:30
    O0O000O000OOOOO00 =cv2 .resize (O0O000O000OOOOO00 ,(OOOO00O0OO000OO0O ,OOOOO000OO0000O0O ),interpolation =cv2 .INTER_CUBIC )#line:31
    print ('------------------------------------')#line:33
    print ('resizing in window size ({}, {})'.format (OOOO00O0OO000OO0O ,OOOOO000OO0000O0O ))#line:34
    print ('(w, h) = ({}, {})'.format (O0000O0000O000O0O ,OO00O0OOOO0O0O0OO ))#line:35
    print ('(w, h) = ({}, {})'.format (OOOO00O0OO000OO0O ,OOOOO000OO0000O0O ))#line:36
    return O0O000O000OOOOO00 ,O00O0OOOOO0O0OO0O #line:37
class pointlist ():#line:39
    def __init__ (OOOOOO0OOO0OOOOOO ):#line:40
        OOOOOO0OOO0OOOOOO .points =[]#line:41
        OOOOOO0OOO0OOOOOO .L =[]#line:42
        OOOOOO0OOO0OOOOOO .R =[]#line:43
        OOOOOO0OOO0OOOOOO .state =None #line:44
    def add (OO000OOO00OOO0OOO ,O0OO0OOOO0O000OO0 ,O0OOO00OO00O0O0O0 ,O00O0O000O000OO00 ):#line:46
        OO000OOO00OOO0OOO .points .append ([O0OO0OOOO0O000OO0 ,O0OOO00OO00O0O0O0 ])#line:47
        if O00O0O000O000OO00 =='L':#line:48
            OO000OOO00OOO0OOO .L .append ([O0OO0OOOO0O000OO0 ,O0OOO00OO00O0O0O0 ])#line:49
            OO000OOO00OOO0OOO .state ='L'#line:50
        if O00O0O000O000OO00 =='R':#line:51
            OO000OOO00OOO0OOO .R .append ([O0OO0OOOO0O000OO0 ,O0OOO00OO00O0O0O0 ])#line:52
            OO000OOO00OOO0OOO .state ='R'#line:53
        print ('points[{}] = ({}, {})'.format (len (OO000OOO00OOO0OOO .points )-1 ,O0OO0OOOO0O000OO0 ,O0OOO00OO00O0O0O0 ))#line:54
class vcclick :#line:56
    def __init__ (OO0OO00OOO00O0OO0 ):#line:57
        pass #line:58
    def __del__ (O00O000OO000O0OO0 ):#line:59
        pass #line:60
    def get_draw (OOOO0OO00O0OOO00O ,return_size ='original'):#line:62
        if return_size =='original':#line:63
            OOOO0OO00O0OOO00O .img_draw_original =cv2 .resize (OOOO0OO00O0OOO00O .img_draw ,OOOO0OO00O0OOO00O .img_original .shape [:2 ][::-1 ],interpolation =cv2 .INTER_CUBIC )#line:64
            return OOOO0OO00O0OOO00O .img_draw_original #line:65
        else :#line:66
            return OOOO0OO00O0OOO00O .img_draw #line:67
    def get_mask (OOOOO0OO00O0OOO00 ,return_size ='original'):#line:69
        if OOOOO0OO00O0OOO00 .mode =='single':#line:70
            if return_size =='original':#line:71
                OOOO0O000OOOOOO0O =np .zeros (OOOOO0OO00O0OOO00 .img_original .shape ,int )#line:72
                OO000OOO00OOO0OO0 =np .array (OOOOO0OO00O0OOO00 .points .points )*OOOOO0OO00O0OOO00 .rate #line:73
                OO000OOO00OOO0OO0 =OO000OOO00OOO0OO0 .astype (int )#line:74
                cv2 .fillConvexPoly (OOOO0O000OOOOOO0O ,points =OO000OOO00OOO0OO0 ,color =(1 ,1 ,1 ))#line:75
            else :#line:76
                OOOO0O000OOOOOO0O =np .zeros (OOOOO0OO00O0OOO00 .img .shape ,int )#line:77
                OO000OOO00OOO0OO0 =np .array (OOOOO0OO00O0OOO00 .points .points )#line:78
                cv2 .fillConvexPoly (OOOO0O000OOOOOO0O ,points =OO000OOO00OOO0OO0 ,color =(1 ,1 ,1 ))#line:79
        if OOOOO0OO00O0OOO00 .mode =='multi':#line:80
            if return_size =='original':#line:81
                OOOO0O000OOOOOO0O =np .zeros (OOOOO0OO00O0OOO00 .img_original .shape ,int )#line:82
                for O0OOOO0O0OO0O0000 in OOOOO0OO00O0OOO00 .points_set :#line:84
                    OO000OOO00OOO0OO0 =np .array (O0OOOO0O0OO0O0000 )*OOOOO0OO00O0OOO00 .rate #line:85
                    OO000OOO00OOO0OO0 =OO000OOO00OOO0OO0 .astype (int )#line:86
                    cv2 .fillConvexPoly (OOOO0O000OOOOOO0O ,points =OO000OOO00OOO0OO0 ,color =(1 ,1 ,1 ))#line:87
            else :#line:88
                OOOO0O000OOOOOO0O =np .zeros (OOOOO0OO00O0OOO00 .img .shape ,int )#line:89
                for O0OOOO0O0OO0O0000 in OOOOO0OO00O0OOO00 .points_set :#line:91
                    OO000OOO00OOO0OO0 =np .array (O0OOOO0O0OO0O0000 )#line:92
                    cv2 .fillConvexPoly (OOOO0O000OOOOOO0O ,points =OO000OOO00OOO0OO0 ,color =(1 ,1 ,1 ))#line:93
        OOOO0O000OOOOOO0O =np .sum (OOOO0O000OOOOOO0O ,axis =2 )==3 #line:94
        return OOOO0O000OOOOOO0O #line:95
    def single (O0000OOOO0O0OO00O ,O00O000OO00OOO0O0 ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:101
        O0000OOOO0O0OO00O .img_original =np .array (O00O000OO00OOO0O0 )#line:103
        O0000OOOO0O0OO00O .window_size =window_size #line:104
        assert guide ==None or len (guide )==3 #line:105
        assert marker ==None or len (marker )==3 #line:106
        assert line ==None or len (line )==3 #line:107
        O0000OOOO0O0OO00O .guide =guide [::-1 ]if guide !=None else None #line:108
        O0000OOOO0O0OO00O .marker =marker [::-1 ]if marker !=None else None #line:109
        O0000OOOO0O0OO00O .line =line [::-1 ]if line !=None else None #line:110
        O0000OOOO0O0OO00O .points =pointlist ()#line:111
        O0000OOOO0O0OO00O .points_set =[]#line:112
        O0000OOOO0O0OO00O .wname ='aaa'#line:113
        O0000OOOO0O0OO00O .img ,O0000OOOO0O0OO00O .rate =resize (O0000OOOO0O0OO00O .img_original ,O0000OOOO0O0OO00O .window_size )#line:116
        O0000OOOO0O0OO00O .h ,O0000OOOO0O0OO00O .w =O0000OOOO0O0OO00O .img .shape [:2 ]#line:118
        O0000OOOO0O0OO00O .img_draw =deepcopy (O0000OOOO0O0OO00O .img )#line:119
        O0000OOOO0O0OO00O .mode ='single'#line:122
        cv2 .namedWindow (O0000OOOO0O0OO00O .wname )#line:123
        cv2 .setMouseCallback (O0000OOOO0O0OO00O .wname ,O0000OOOO0O0OO00O .start )#line:124
        cv2 .imshow (O0000OOOO0O0OO00O .wname ,O0000OOOO0O0OO00O .img )#line:126
        cv2 .waitKey ()#line:127
        if return_size =='original':#line:130
            print ('return in original size {}'.format (O0000OOOO0O0OO00O .img_original .shape [:2 ][::-1 ]))#line:131
            print ('------------------------------------')#line:132
            return np .array (O0000OOOO0O0OO00O .points .points )*O0000OOOO0O0OO00O .rate #line:133
        else :#line:134
            print ('return in window size {}'.format (O0000OOOO0O0OO00O .img .shape [:2 ][::-1 ]))#line:135
            return np .array (O0000OOOO0O0OO00O .points .points )#line:136
    def multi (O00OOO0OOOO0OOOOO ,O00OOO0OOO00O0O00 ,window_size =1000 ,guide =(0 ,255 ,0 ),marker =(255 ,0 ,0 ),line =(0 ,255 ,0 ),return_size ='original'):#line:142
        O00OOO0OOOO0OOOOO .img_original =np .array (O00OOO0OOO00O0O00 )#line:144
        O00OOO0OOOO0OOOOO .window_size =window_size #line:145
        assert guide ==None or len (guide )==3 #line:146
        assert marker ==None or len (marker )==3 #line:147
        assert line ==None or len (line )==3 #line:148
        O00OOO0OOOO0OOOOO .guide =guide [::-1 ]if guide !=None else None #line:149
        O00OOO0OOOO0OOOOO .marker =marker [::-1 ]if marker !=None else None #line:150
        O00OOO0OOOO0OOOOO .line =line [::-1 ]if line !=None else None #line:151
        O00OOO0OOOO0OOOOO .points =pointlist ()#line:152
        O00OOO0OOOO0OOOOO .points_set =[]#line:153
        O00OOO0OOOO0OOOOO .wname ='aaa'#line:154
        O00OOO0OOOO0OOOOO .img ,O00OOO0OOOO0OOOOO .rate =resize (O00OOO0OOOO0OOOOO .img_original ,O00OOO0OOOO0OOOOO .window_size )#line:157
        O00OOO0OOOO0OOOOO .h ,O00OOO0OOOO0OOOOO .w =O00OOO0OOOO0OOOOO .img .shape [:2 ]#line:159
        O00OOO0OOOO0OOOOO .img_draw =deepcopy (O00OOO0OOOO0OOOOO .img )#line:160
        O00OOO0OOOO0OOOOO .mode ='multi'#line:163
        cv2 .namedWindow (O00OOO0OOOO0OOOOO .wname )#line:164
        cv2 .setMouseCallback (O00OOO0OOOO0OOOOO .wname ,O00OOO0OOOO0OOOOO .start )#line:165
        cv2 .imshow (O00OOO0OOOO0OOOOO .wname ,O00OOO0OOOO0OOOOO .img )#line:167
        cv2 .waitKey ()#line:168
        if return_size =='original':#line:171
            print ('return in original size {}'.format (O00OOO0OOOO0OOOOO .img_original .shape [:2 ][::-1 ]))#line:172
            print ('------------------------------------')#line:173
            O00OO00O0OOO00000 =deepcopy (O00OOO0OOOO0OOOOO .points_set )#line:174
            for O0OO0O0O000OO0OOO in range (len (O00OO00O0OOO00000 )):#line:175
                O00OO00O0OOO00000 [O0OO0O0O000OO0OOO ]=np .array (O00OO00O0OOO00000 [O0OO0O0O000OO0OOO ])*O00OOO0OOOO0OOOOO .rate #line:176
            return O00OO00O0OOO00000 #line:177
        else :#line:178
            print ('return in window size {}'.format (O00OOO0OOOO0OOOOO .img .shape [:2 ][::-1 ]))#line:179
            O00OO00O0OOO00000 =deepcopy (O00OOO0OOOO0OOOOO .points_set )#line:180
            for O0OO0O0O000OO0OOO in range (len (O00OO00O0OOO00000 )):#line:181
                O00OO00O0OOO00000 [O0OO0O0O000OO0OOO ]=np .array (O00OO00O0OOO00000 [O0OO0O0O000OO0OOO ])#line:182
            return O00OOO0OOOO0OOOOO .points_set #line:183
    def start (O00O0O000000O00OO ,O0OOO00O0O0OO00OO ,OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ,O0OOO000O000O0O00 ,OO0O00O00O0O0OO0O ):#line:186
        if O0OOO00O0O0OO00OO ==cv2 .EVENT_MOUSEMOVE :#line:188
            O0OO00O0000000O0O =deepcopy (O00O0O000000O00OO .img_draw )#line:190
            if O00O0O000000O00OO .guide !=None :#line:192
                cv2 .line (O0OO00O0000000O0O ,(OO0OO0O0O0OO00O00 ,0 ),(OO0OO0O0O0OO00O00 ,O00O0O000000O00OO .h -1 ),O00O0O000000O00OO .guide )#line:193
                cv2 .line (O0OO00O0000000O0O ,(0 ,OOO0OO0OO0OO0O000 ),(O00O0O000000O00OO .w -1 ,OOO0OO0OO0OO0O000 ),O00O0O000000O00OO .guide )#line:194
            if O00O0O000000O00OO .points .state =='L':#line:196
                if O00O0O000000O00OO .line !=None :#line:197
                    OOO000000OOO00000 ,OO000O00O0O0O0000 =O00O0O000000O00OO .points .L [-1 ]#line:198
                    cv2 .line (O0OO00O0000000O0O ,(OOO000000OOO00000 ,OO000O00O0O0O0000 ),(OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ),O00O0O000000O00OO .guide )#line:199
            cv2 .imshow (O00O0O000000O00OO .wname ,O0OO00O0000000O0O )#line:201
        if O0OOO00O0O0OO00OO ==cv2 .EVENT_LBUTTONDOWN :#line:204
            if O00O0O000000O00OO .points .state =='L':#line:206
                cv2 .circle (O00O0O000000O00OO .img_draw ,(OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ),4 ,O00O0O000000O00OO .marker ,1 )#line:208
                if O00O0O000000O00OO .line !=None :#line:210
                    OOO000000OOO00000 ,OO000O00O0O0O0000 =O00O0O000000O00OO .points .L [-1 ]#line:211
                    cv2 .line (O00O0O000000O00OO .img_draw ,(OOO000000OOO00000 ,OO000O00O0O0O0000 ),(OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ),O00O0O000000O00OO .line )#line:212
                O00O0O000000O00OO .points .add (OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ,'L')#line:214
                cv2 .imshow (O00O0O000000O00OO .wname ,O00O0O000000O00OO .img_draw )#line:216
            else :#line:218
                O00O0O000000O00OO .points .add (OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ,'L')#line:220
                cv2 .circle (O00O0O000000O00OO .img_draw ,(OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ),4 ,O00O0O000000O00OO .marker ,1 )#line:222
                cv2 .imshow (O00O0O000000O00OO .wname ,O00O0O000000O00OO .img_draw )#line:224
        if O0OOO00O0O0OO00OO ==cv2 .EVENT_RBUTTONDOWN :#line:227
            if O00O0O000000O00OO .points .state =='L':#line:229
                cv2 .circle (O00O0O000000O00OO .img_draw ,(OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ),4 ,O00O0O000000O00OO .marker ,1 )#line:231
                if O00O0O000000O00OO .line !=None :#line:233
                    OOO000000OOO00000 ,OO000O00O0O0O0000 =O00O0O000000O00OO .points .L [-1 ]#line:234
                    cv2 .line (O00O0O000000O00OO .img_draw ,(OOO000000OOO00000 ,OO000O00O0O0O0000 ),(OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ),O00O0O000000O00OO .line )#line:235
                O00O0O000000O00OO .points .add (OO0OO0O0O0OO00O00 ,OOO0OO0OO0OO0O000 ,'R')#line:237
                cv2 .imshow (O00O0O000000O00OO .wname ,O00O0O000000O00OO .img_draw )#line:239
                if O00O0O000000O00OO .mode =='multi':#line:242
                    O00O0O000000O00OO .points_set .append (O00O0O000000O00OO .points .points )#line:243
                    O00O0O000000O00OO .points =pointlist ()#line:244
            else :#line:247
                pass #line:248
            if O00O0O000000O00OO .mode =='single':#line:251
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
