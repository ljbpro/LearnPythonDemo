import argparse
import matplotlib.pyplot as plt

import chainer

import os, fnmatch

from chainercv.datasets import voc_bbox_label_names
from chainercv.links import SSD300
from chainercv.links import SSD512
from chainercv import utils
from chainercv.visualizations import vis_bbox

doSSDImageIndex = 0
trueInfoList = []
fig, imageAx = plt.subplots(1, 1)
trueInfoFilePath = "/Users/ljbzylpro/Desktop/list.txt"
imageFileFolderPath = "/Users/ljbzylpro/Desktop/Image"

def main():
    fig.canvas.mpl_connect('key_press_event', on_process)
    getTrueInfoList()
    doSSD(trueInfoList[doSSDImageIndex][0])
    plt.show()

def on_process(event):
    global doSSDImageIndex
    if event.key == 'left':
        if doSSDImageIndex > 0:
            doSSDImageIndex = doSSDImageIndex -1
            doSSD(trueInfoList[doSSDImageIndex][0])
    elif event.key == 'right':
        if doSSDImageIndex < len(trueInfoList) -1:
            doSSDImageIndex = doSSDImageIndex +1
            doSSD(trueInfoList[doSSDImageIndex][0])

def doSSD(imageName):
    global imageAx
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

    img = utils.read_image(imageFileFolderPath + "/" + imageName, color=True)
    bboxes, labels, scores = model.predict([img])
    bbox, label, score = bboxes[0], labels[0], scores[0]

    # 正しい情報
    label_true = trueInfoList[doSSDImageIndex][1]
    x1_true = trueInfoList[doSSDImageIndex][2]
    y1_true = trueInfoList[doSSDImageIndex][3]
    x2_true = trueInfoList[doSSDImageIndex][4]
    y2_true = trueInfoList[doSSDImageIndex][5]

    imageAx.clear()  
    imageAx = vis_bbox(img, bbox, label, score, label_names=voc_bbox_label_names,ax=imageAx)
    plt.pause(0.0001)

def getTrueInfoList():
    global trueInfoList
    with open(trueInfoFilePath,'r') as f:
        data=f.readlines()

        for line in data:
            text = line.replace('\n','')
            text = text.replace('\r','')
            tmplineArray = text.split(' ')
            trueInfoList.append(tmplineArray)

if __name__ == '__main__':
    main()
