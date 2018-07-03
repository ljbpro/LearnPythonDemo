import argparse
import matplotlib.pyplot as plt
import numpy as np
import chainer
import cv2
import threading
import time

from chainercv.datasets import voc_bbox_label_names
from chainercv.links import SSD300
from chainercv.links import SSD512
from chainercv import utils
from chainercv.visualizations import vis_bbox
from PIL import Image, ImageDraw, ImageFont

class SsdByCamera:

    def __init__(self, interval):
        self.analysisTimeInterval = interval
        self.frames = 0
        self.isExit = False
        self.fig, (self.imageAx, self.analysisAx) = plt.subplots(2, 1)

    def on_close(self,event):
        event.canvas.figure.axes[0].has_been_closed = True
        self.isExit = True

    def on_process(self,event):
        if event.key == 'q':
            self.isExit = True

    def grab_frame(self,cap):
        ret,frame = cap.read()
        return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    def convert_pilimg_for_chainercv(self,pilimg):
        """ pilimg(RGBのカラー画像とする)を、ChainerCVが扱える形式に変換 """ 
        img = np.asarray(pilimg, dtype=np.uint8)
        # transpose (H, W, C) -> (C, H, W)
        return img.transpose((2, 0, 1))

    def doSsd(self):

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--model', choices=('ssd300', 'ssd512'), default='ssd300')
        parser.add_argument('--gpu', type=int, default=-1)
        parser.add_argument('--pretrained-model', default='voc0712')
        #parser.add_argument('image')
        args = parser.parse_args()

        if args.model == 'ssd300':
            model = SSD300(
                n_fg_class=len(voc_bbox_label_names),
                pretrained_model=args.pretrained_model)
        elif args.model == 'ssd512':
            model = SSD512(
                n_fg_class=len(voc_bbox_label_names),
                pretrained_model=args.pretrained_model)

        if args.gpu >= 0:
            chainer.cuda.get_device_from_id(args.gpu).use()
            model.to_gpu()
    
        cap1 = cv2.VideoCapture(0)

        # 初期設定
        self.imageAx.has_been_closed = False
        self.imageAx.get_xaxis().set_visible(False)
        self.imageAx.get_yaxis().set_visible(False)
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.fig.canvas.mpl_connect('key_press_event', self.on_process)

        # 統計スレッド起動
        analysisThread = threading.Thread(target=self.doAnalysis)
        analysisThread.setDaemon(True)
        analysisThread.start()

        while self.isExit == False:
            im2 = self.convert_pilimg_for_chainercv(self.grab_frame(cap1))
            bboxes, labels, scores = model.predict([im2])
            bbox, label, score = bboxes[0], labels[0], scores[0]
            self.imageAx.clear()  
            self.imageAx = vis_bbox(im2, bbox, label, score, label_names=voc_bbox_label_names,ax=self.imageAx)
            self.frames = self.frames + 1
            plt.pause(0.0001)
    
        plt.show()
        exit()

    def doAnalysis(self):

        analysisX = []
        analysisY = []
        analysisTimes = 0
        sumFrames = 0

        while(True):
            if(analysisTimes != 0):
                analysisX.append(self.analysisTimeInterval*analysisTimes)
                analysisY.append(self.frames)
                self.analysisAx.clear()
                self.analysisAx.plot(analysisX,analysisY)
                sumFrames = sumFrames + self.frames
                self.analysisAx.set_title('Fps:' + str(sumFrames/(self.analysisTimeInterval*analysisTimes)))
                self.analysisAx.set_ylabel('Frames')
                self.analysisAx.set_xlabel('Time')
                self.analysisAx.grid()

            analysisTimes = analysisTimes + 1
            self.frames = 0
            time.sleep(self.analysisTimeInterval)

if __name__ == '__main__':
    ssd = SsdByCamera(10)
    ssd.doSsd()