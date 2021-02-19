# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import cv2

def show(img):
    plt.figure(figsize=(8, 8))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if np.max(img) == 1:
        plt.imshow(img, vmin = 0, vmax = 1)
    else:
        plt.imshow(img, vmin = 0, vmax = 255)
    plt.gray()
    plt.show()
    plt.close()
    print()

def resize(img, window_size):
    #サイズ取得
    h, w = img.shape[:2]
    #目標サイズにリサイズ
    if h < w:
        w_aim = window_size
        h_aim = int(h * window_size / w)
        rate = w / window_size
    else:
        h_aim = window_size
        w_aim = int(w * window_size / h)
        rate = h / window_size
    img = cv2.resize(img, (w_aim, h_aim), interpolation = cv2.INTER_CUBIC)
    
    print('------------------------------------')
    print('resizing in window size ({}, {})'.format(w_aim, h_aim))
    print('(w, h) = ({}, {})'.format(w, h))
    print('(w, h) = ({}, {})'.format(w_aim, h_aim))
    return img, rate

class pointlist():
    def __init__(self):
        self.points = []
        self.L = []
        self.R = []
        self.state = None

    def add(self, x, y, LR):
        self.points.append([x, y])
        if LR == 'L':
            self.L.append([x, y])
            self.state = 'L'
        if LR == 'R':
            self.R.append([x, y])
            self.state = 'R'
        print('points[{}] = ({}, {})'.format(len(self.points) - 1, x, y))

class vcclick:
    def __init__(self):
        pass
    def __del__(self):
        pass
    
    def get_draw(self, return_size='original'):
        if return_size == 'original':
            self.img_draw_original = cv2.resize(self.img_draw, self.img_original.shape[:2][::-1], interpolation = cv2.INTER_CUBIC)
            return self.img_draw_original
        else:
            return self.img_draw
        
    def get_mask(self, return_size='original'):
        if self.mode == 'single':
            if return_size == 'original':
                mask = np.zeros(self.img_original.shape, int)
                contours = np.array(self.points.points) * self.rate
                contours = contours.astype(int)
                cv2.fillConvexPoly(mask, points=contours, color=(1, 1, 1))
            else:
                mask = np.zeros(self.img.shape, int)
                contours = np.array(self.points.points)
                cv2.fillConvexPoly(mask, points=contours, color=(1, 1, 1))
        if self.mode == 'multi':
            if return_size == 'original':
                mask = np.zeros(self.img_original.shape, int)
                #複数の多角形を描画
                for points_tmp in self.points_set:
                    contours = np.array(points_tmp) * self.rate
                    contours = contours.astype(int)
                    cv2.fillConvexPoly(mask, points=contours, color=(1, 1, 1))
            else:
                mask = np.zeros(self.img.shape, int)
                #複数の多角形を描画
                for points_tmp in self.points_set:
                    contours = np.array(points_tmp)
                    cv2.fillConvexPoly(mask, points=contours, color=(1, 1, 1))
        mask = np.sum(mask, axis=2) == 3
        return mask

    def single(self, img_original, window_size=1000,
                                   guide=(0, 255, 0),
                                   marker=(255, 0, 0),
                                   line=(0, 255, 0),
                                   return_size='original'):
        #設定１
        self.img_original = np.array(img_original)
        self.window_size = window_size
        assert guide == None or len(guide) == 3
        assert marker == None or len(marker) == 3
        assert line == None or len(line) == 3
        self.guide = guide[::-1] if guide != None else None
        self.marker = marker[::-1] if marker != None else None
        self.line = line[::-1] if line != None else None
        self.points = pointlist()
        self.points_set = []
        self.wname = 'aaa'
        
        #サイズ変更
        self.img, self.rate = resize(self.img_original, self.window_size)
        #設定２
        self.h, self.w = self.img.shape[:2]
        self.img_draw = deepcopy(self.img)
        
        #準備
        self.mode = 'single'
        cv2.namedWindow(self.wname)
        cv2.setMouseCallback(self.wname, self.start)
        #開始
        cv2.imshow(self.wname, self.img)
        cv2.waitKey()
        
        #元サイズに変換
        if return_size == 'original':
            print('return in original size {}'.format(self.img_original.shape[:2][::-1]))
            print('------------------------------------')
            return np.array(self.points.points) * self.rate
        else:
            print('return in window size {}'.format(self.img.shape[:2][::-1]))
            return np.array(self.points.points)
    
    def multi(self, img_original, window_size=1000,
                                  guide=(0, 255, 0),
                                  marker=(255, 0, 0),
                                  line=(0, 255, 0),
                                  return_size='original'):
        #設定１
        self.img_original = np.array(img_original)
        self.window_size = window_size
        assert guide == None or len(guide) == 3
        assert marker == None or len(marker) == 3
        assert line == None or len(line) == 3
        self.guide = guide[::-1] if guide != None else None
        self.marker = marker[::-1] if marker != None else None
        self.line = line[::-1] if line != None else None
        self.points = pointlist()
        self.points_set = []
        self.wname = 'aaa'
        
        #サイズ変更
        self.img, self.rate = resize(self.img_original, self.window_size)
        #設定２
        self.h, self.w = self.img.shape[:2]
        self.img_draw = deepcopy(self.img)
        
        #準備
        self.mode = 'multi'
        cv2.namedWindow(self.wname)
        cv2.setMouseCallback(self.wname, self.start)
        #開始
        cv2.imshow(self.wname, self.img)
        cv2.waitKey()
        
        #元サイズに変換
        if return_size == 'original':
            print('return in original size {}'.format(self.img_original.shape[:2][::-1]))
            print('------------------------------------')
            ret_set = deepcopy(self.points_set)
            for i in range(len(ret_set)):
                ret_set[i] = np.array(ret_set[i]) * self.rate
            return ret_set
        else:
            print('return in window size {}'.format(self.img.shape[:2][::-1]))
            ret_set = deepcopy(self.points_set)
            for i in range(len(ret_set)):
                ret_set[i] = np.array(ret_set[i])
            return self.points_set
        
    
    def start(self, event, x, y, flag, params):
        #カーソル移動
        if event == cv2.EVENT_MOUSEMOVE:
            #コピー
            img_tmp = deepcopy(self.img_draw)
            #ガイド線１
            if self.guide != None:
                cv2.line(img_tmp, (x, 0), (x, self.h - 1), self.guide)
                cv2.line(img_tmp, (0, y), (self.w - 1, y), self.guide)
            #ガイド線２
            if self.points.state == 'L':
                if self.guide != None:
                    x_before, y_before = self.points.L[-1]
                    cv2.line(img_tmp, (x_before, y_before), (x, y), self.guide)
            #表示
            cv2.imshow(self.wname, img_tmp)

        #左クリック
        if event == cv2.EVENT_LBUTTONDOWN:
            #Lのあとの場合、継続
            if self.points.state == 'L':
                #円を描画
                cv2.circle(self.img_draw, (x, y), 4, self.marker, 1)
                #最後のL点と結ぶ
                if self.line != None:
                    x_before, y_before = self.points.L[-1]
                    cv2.line(self.img_draw, (x_before, y_before), (x, y), self.line)
                #追加
                self.points.add(x, y, 'L')
                #表示
                cv2.imshow(self.wname, self.img_draw)
            #そうでない場合、ここからスタート
            else:
                #追加
                self.points.add(x, y, 'L')
                #円を描画
                cv2.circle(self.img_draw, (x, y), 8, self.marker, 1)
                #表示
                cv2.imshow(self.wname, self.img_draw)

        #右クリック
        if event == cv2.EVENT_RBUTTONDOWN:
            #Lのあとの場合、線を閉じる
            if self.points.state == 'L':
                #円を描画
                cv2.circle(self.img_draw, (x, y), 8, self.marker, 1)
                #最後のL点と結ぶ
                if self.line != None:
                    x_before, y_before = self.points.L[-1]
                    cv2.line(self.img_draw, (x_before, y_before), (x, y), self.line)
                #追加
                self.points.add(x, y, 'R')
                #表示
                cv2.imshow(self.wname, self.img_draw)
                
                #マルチなら区切る
                if self.mode == 'multi':
                    self.points_set.append(self.points.points)
                    self.points = pointlist()
            
            #そうでない場合、無効
            else:
                pass
            
            #シングルなら終了
            if self.mode == 'single':
                cv2.destroyAllWindows()


if __name__ == '__main__':
    #ファイル名
    file_name = 'yoko.JPG'
    #file_name = 'tate.JPG'
    
    #画面上の表示サイズ
    #size_max = 1000
    
    #読み込み
    img = cv2.imread(file_name)
    show(img)
    
    #
    aaa = vcclick()
    points = aaa.multi(img, window_size=1000, guide=None)
    print(points)
    show(aaa.get_draw())
    show(aaa.get_mask())

    
    
    





