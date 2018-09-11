import os, fnmatch
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk
from operator import itemgetter

folder_path = ""
imageFileNameList = []
coordinateAndClassInfoList = []
firstDragInFirstDraw = True
mouseDragingFlag = False
resizeMode = 0
startPointX = 0
startPointY = 0
endPointX = 0
endPointY = 0
cursorType = ""
displayImageIndex = 0

ITEMS = ['1. circle', '2. multilateralstar', '3. semicircle']
MAPPING = {'1. circle' : 0, '2. multilateralstar' : 1, '3. semicircle' : 2}

root = Tk()
root.title(u"create label bbox")
root.geometry("640x600")

fileFrame = Frame(root,bd=0,relief="ridge")
folderPathTitleLabel = Label(master=fileFrame,text="フォルダー：")
folderPathEntry = Entry(master=fileFrame,width=40)
browseButton = Button(master=fileFrame,text="フォルダー選択")

classlabel=tkinter.StringVar()
classnames=ttk.Combobox(fileFrame,textvariable=classlabel,state = 'readonly', values = ITEMS)
classnames.current(0)

canvasFrame = Frame(root,bd=0,relief="ridge")
canvas = Canvas(canvasFrame, width = 640, height = 480, bd = 0, bg = '#F5F5DC')

nextPrevBtnFrame = Frame(root,bd=0,relief="ridge")
prevButton = Button(master=nextPrevBtnFrame,text="Prev")
nextButton = Button(master=nextPrevBtnFrame,text="Next")
OKButton = Button(master=nextPrevBtnFrame,text="Getting Coordinate and class information") # addition get coordinate button

def on_mouse_motion(event):
    global mouseDragingFlag
    global resizeMode
    global cursorType
    global startPointX
    global startPointY
    global endPointX
    global endPointY

    x = event.x
    y = event.y

    if mouseDragingFlag == False:
        cursorType = "arrow"
        if(abs(x-startPointX) < 5 and abs(y-endPointY) <5):
            resizeMode = 1
            cursorType = "crosshair"
        elif(abs(x-startPointX) < 5 and abs(y-endPointY) >5 and abs(y-startPointY) >5):
            resizeMode = 14
            cursorType = "sb_h_double_arrow"
        elif(abs(x-startPointX) < 5 and abs(y-startPointY) <5):
            resizeMode = 4
            cursorType = "crosshair"
        elif(abs(x-startPointX) > 5 and abs(y-startPointY) <5 and abs(x-endPointX) > 5):
            resizeMode = 34
            cursorType = "sb_v_double_arrow"
        elif(abs(x-endPointX) < 5 and abs(y-startPointY) <5):
            resizeMode = 3
            cursorType = "crosshair"
        elif(abs(x-endPointX) < 5 and abs(y-startPointY) > 5 and abs(y-endPointY) > 5):
            resizeMode = 23
            cursorType = "sb_h_double_arrow"
        elif(abs(x-endPointX) < 5 and abs(y-endPointY) <5):
            resizeMode = 2
            cursorType = "crosshair"
        elif(abs(x-endPointX) > 5 and abs(y-endPointY) <5 and abs(x- startPointX) > 5):
            resizeMode = 12
            cursorType = "sb_v_double_arrow"
        else:
            resizeMode = 0
            cursorType = "arrow"

        # カーソル設定
        canvas.configure(cursor=cursorType)

def on_mouse_drag(event):
    global firstDragInFirstDraw
    global mouseDragingFlag
    global resizeMode
    global startPointX
    global startPointY
    global endPointX
    global endPointY

    x = event.x
    y = event.y

    if(x > 600 or x <= 1):
        return

    if(y > 480 or y <= 1):
        return

    # 描く中フラグ更新
    mouseDragingFlag = True
    
    if resizeMode == 0:
        # 変数を更新
        endPointX = x
        endPointY = y

        # 範囲を描く
        if firstDragInFirstDraw == True:
            firstDragInFirstDraw = False
            canvas.create_rectangle(startPointX, startPointY, endPointX, endPointY, tag="canvasRect",outline="red")
        else:
            canvas.coords("canvasRect",startPointX, startPointY, endPointX, endPointY)
        
        # カーソル設定
        canvas.configure(cursor="crosshair")

    else:
        # 枠を調整
        if resizeMode == 1:
            startPointX = x
            endPointY = y
        elif resizeMode == 14:
            startPointX = x
        elif resizeMode == 4:
            startPointX = x
            startPointY = y
        elif resizeMode == 34:
            startPointY = y
        elif resizeMode == 3:
            endPointX = x
            startPointY = y
        elif resizeMode == 23:
            endPointX = x
        elif resizeMode == 2:
            endPointX = x
            endPointY = y
        elif resizeMode == 12:
            endPointY = y

        canvas.coords("canvasRect",startPointX, startPointY, endPointX, endPointY)

def on_mouse_press(event):
    global startPointX
    global startPointY
    global endPointX
    global endPointY

    x = event.x
    y = event.y

    if resizeMode == 0:
        startPointX = x
        startPointY = y
        endPointX = x
        endPointY = y

def on_mouse_release(event):
    global mouseDragingFlag

    # カーソル設定
    canvas.configure(cursor='arrow')

    # Mouse Drawingフラグ制御解除
    mouseDragingFlag = False

def on_browse_button_click(event):
    global folder_path
    filename = filedialog.askdirectory()
    folder_path = filename
    folderPathEntry.insert(END,folder_path)

    # ファイル名取得
    getFileNameListFromPath(folder_path)

    # 初期表示
    displayImage(imageFileNameList[0])

def on_prev_button_click(event):
    global displayImageIndex
    global imageFileNameList
    if(displayImageIndex > 0):
        displayImageIndex = displayImageIndex -1
        displayImage(imageFileNameList[displayImageIndex])
        # 矩形をクリア
        clearRect()
        # 処理済み情報再表示
        reDisplayCoordinateAndClassInfo()

def on_next_button_click(event):
    global displayImageIndex
    global imageFileNameList
    if(displayImageIndex < len(imageFileNameList) - 1):
        displayImageIndex = displayImageIndex + 1
        displayImage(imageFileNameList[displayImageIndex])
        # 矩形をクリア
        clearRect()
        # 処理済み情報再表示
        reDisplayCoordinateAndClassInfo()

def getFileNameListFromPath(folderPath):
    global imageFileNameList
    global displayImageIndex

    # 初期化
    imageFileNameList = []
    displayImageIndex = 0

    # 取得値設定
    listOfFiles = os.listdir(folderPath)  
    pattern = "*.jpg"
    for fileName in sorted(listOfFiles):  
        if fnmatch.fnmatch(fileName, pattern):
            imageFileNameList.append(fileName)

def displayImage(fileName):
    imageFile = ImageTk.PhotoImage(Image.open(folder_path + "/" + fileName))
    canvas.image = imageFile
    canvas.create_image(0,0,anchor='nw',image=imageFile)

def get_coordinate_click(event):
    global coordinateAndClassInfoList
    # 出力情報作成
    coordinateAndClassInfo = [imageFileNameList[displayImageIndex],MAPPING[classnames.get()],startPointX,startPointY,endPointX,endPointY]

    # 情報追加
    if len(coordinateAndClassInfoList) == 0:
        coordinateAndClassInfoList.append(coordinateAndClassInfo)
    else:
        isExist = False
        for index, item in enumerate(coordinateAndClassInfoList):
            if(item[0] == coordinateAndClassInfo[0]):
                isExist = True
                coordinateAndClassInfoList[index] = coordinateAndClassInfo

        if isExist == False:
            coordinateAndClassInfoList.append(coordinateAndClassInfo)

    # 情報出力
    outPutCoordinateAndClassInfo()

def select_class(event):
    print(classnames.get())

def reDisplayCoordinateAndClassInfo():
    global firstDragInFirstDraw
    global startPointX
    global startPointY
    global endPointX
    global endPointY

    reDisplayImageName = imageFileNameList[displayImageIndex]
    if(len(coordinateAndClassInfoList) > 0):
        for item in coordinateAndClassInfoList:
            if(item[0] == reDisplayImageName):
                classnames.current(item[1])
                startPointX = item[2]
                startPointY = item[3]
                endPointX = item[4]
                endPointY = item[5]
                firstDragInFirstDraw = False
                canvas.create_rectangle(startPointX, startPointY, endPointX, endPointY, tag="canvasRect",outline="red")


def outPutCoordinateAndClassInfo():
    global coordinateAndClassInfoList
    # 出力パス
    outPutFilePath = folder_path + "/" + "Result.txt"
    # 出力内容
    outPutInfo = ""
    # ソート
    coordinateAndClassInfoList.sort(key=itemgetter(0))
    print(coordinateAndClassInfoList)

    for index, item in enumerate(coordinateAndClassInfoList):
        outPutInfoItem = ""
        outPutInfoItem = outPutInfoItem + item[0] + " "
        outPutInfoItem = outPutInfoItem + str(item[1]) + " "
        outPutInfoItem = outPutInfoItem + str(item[2]) + " "
        outPutInfoItem = outPutInfoItem + str(item[3]) + " "
        outPutInfoItem = outPutInfoItem + str(item[4]) + " "
        outPutInfoItem = outPutInfoItem + str(item[5])

        outPutInfo = outPutInfo + outPutInfoItem
        if(index < len(coordinateAndClassInfoList) - 1):
            outPutInfo = outPutInfo + "\n"

    # 出力
    with open(outPutFilePath, mode='w') as f:
        f.write(outPutInfo)

def clearRect():
    global firstDragInFirstDraw
    global startPointX
    global startPointY
    global endPointX
    global endPointY
    global resizeMode

    # 初期化
    firstDragInFirstDraw = True
    
    # 矩形をクリア
    canvas.delete("canvasRect")
    startPointX = 0
    startPointY = 0
    endPointX = 0
    endPointY = 0
    resizeMode = 0

def main():
    canvas.bind("<Motion>", on_mouse_motion)
    canvas.bind("<Button-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    browseButton.bind("<Button-1>", on_browse_button_click)
    prevButton.bind("<Button-1>", on_prev_button_click)
    nextButton.bind("<Button-1>", on_next_button_click)
    OKButton.bind("<Button-1>", get_coordinate_click)  # addation get coordinate
    classnames.bind("<<ComboboxSelected>>",select_class)

    fileFrame.pack(fill="x")
    folderPathTitleLabel.pack(side="left")
    folderPathEntry.pack(side="left")
    browseButton.pack(side="left")
    classnames.pack(side="right") # addation class 

    canvasFrame.pack(fill="x")
    canvas.pack(side="left")

    nextPrevBtnFrame.pack(fill="x")
    prevButton.pack(side="right")
    nextButton.pack(side="right")
    OKButton.pack(side="left") # addation get coordinate botton

    root.mainloop()
 
if __name__ == '__main__':
    main()