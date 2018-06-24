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

# 設定値
analysisTimeInterval = 10

# Global変数
frames = 0
isExit = False

fig, (imageAx, analysisAx) = plt.subplots(2, 1)

def on_close(event):
    global isExit
    event.canvas.figure.axes[0].has_been_closed = True
    isExit = True

def on_process(event):
    global isExit
    if event.key == 'q':
        isExit = True

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

def convert_pilimg_for_chainercv(pilimg):
    """ pilimg(RGBのカラー画像とする)を、ChainerCVが扱える形式に変換 """ 
    img = np.asarray(pilimg, dtype=np.uint8)
    # transpose (H, W, C) -> (C, H, W)
    return img.transpose((2, 0, 1))

def main():
    global isExit
    global imageAx
    global frames

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
    imageAx.has_been_closed = False
    imageAx.get_xaxis().set_visible(False)
    imageAx.get_yaxis().set_visible(False)
    fig.canvas.mpl_connect('close_event', on_close)
    fig.canvas.mpl_connect('key_press_event', on_process)

    # 統計スレッド起動
    analysisThread = threading.Thread(target=doAnalysis)
    analysisThread.setDaemon(True)
    analysisThread.start()

    while isExit == False:
        im2 = convert_pilimg_for_chainercv(grab_frame(cap1))
        bboxes, labels, scores = model.predict([im2])
        bbox, label, score = bboxes[0], labels[0], scores[0]
        imageAx.clear()  
        imageAx = vis_bbox(im2, bbox, label, score, label_names=voc_bbox_label_names,ax=imageAx)
        frames = frames + 1
        plt.pause(0.0001)
    
    plt.show()
    exit()

def doAnalysis():
    global analysisAx
    global frames

    analysisX = []
    analysisY = []
    analysisTimes = 0
    sumFrames = 0

    while(True):
        if(analysisTimes != 0):
            analysisX.append(analysisTimeInterval*analysisTimes)
            analysisY.append(frames)
            analysisAx.clear()
            analysisAx.plot(analysisX,analysisY)
            sumFrames = sumFrames + frames
            analysisAx.set_title('Fps:' + str(sumFrames/(analysisTimeInterval*analysisTimes)))
            analysisAx.set_ylabel('Frames')
            analysisAx.set_xlabel('Time')
            analysisAx.grid()

        analysisTimes = analysisTimes + 1
        frames = 0
        time.sleep(analysisTimeInterval)

if __name__ == '__main__':
    main()