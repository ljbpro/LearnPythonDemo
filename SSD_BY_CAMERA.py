import argparse
import matplotlib.pyplot as plt
import numpy as np
import chainer
import cv2

from chainercv.datasets import voc_bbox_label_names
from chainercv.links import SSD300
from chainercv.links import SSD512
from chainercv import utils
from chainercv.visualizations import vis_bbox
from PIL import Image, ImageDraw, ImageFont

# Global変数定義
isExist = False

def keyEventMonitoring():
    global isExist
    while(True):
        key = ord(getch())
        if(key == 113):
            # [q]キー押下イベント
            isExist = True

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

def convert_pilimg_for_chainercv(pilimg):
    """ pilimg(RGBのカラー画像とする)を、ChainerCVが扱える形式に変換 """ 
    img = np.asarray(pilimg, dtype=np.uint8)
    # transpose (H, W, C) -> (C, H, W)
    return img.transpose((2, 0, 1))

def main():
    # 監視関数起動
    t1 = threading.Thread(target=keyEventMonitoring)
    t1.setDaemon(True)
    t1.start()

    # 事務処理開始
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
    imageAx = None

    while(isExist == False):
        im2 = convert_pilimg_for_chainercv(grab_frame(cap1))
        bboxes, labels, scores = model.predict([im2])
        bbox, label, score = bboxes[0], labels[0], scores[0]
        if imageAx is not None:
            imageAx.clear()
            imageAx.get_xaxis().set_visible(False)
            imageAx.get_yaxis().set_visible(False)
        imageAx = vis_bbox(im2, bbox, label, score, label_names=voc_bbox_label_names,ax=imageAx)
        plt.pause(0.2)
    
    plt.show()
    cap1.release()
    exit()

if __name__ == '__main__':
    main()