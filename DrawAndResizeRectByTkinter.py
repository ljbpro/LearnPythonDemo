import os, fnmatch

from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk

folder_path = ""
imageFileNameList = []
firstDrawFlag = True
firstDragInFirstDraw = True
mouseDragingFlag = False
resizeMode = 0
startPointX = 0
startPointY = 0
endPointX = 0
endPointY = 0
cursorType = ""
displayImageIndex = 0

root = Tk()
root.title(u"create label bbox")
root.geometry("600x600")

fileFrame = Frame(root,bd=0,relief="ridge")
folderPathTitleLabel = Label(master=fileFrame,text="フォルダー：")
folderPathEntry = Entry(master=fileFrame,width=40)
browseButton = Button(master=fileFrame,text="フォルダー選択")

canvasFrame = Frame(root,bd=0,relief="ridge")
canvas = Canvas(canvasFrame, width = 600, height = 480, bd = 0, bg = '#F5F5DC')

nextPrevBtnFrame = Frame(root,bd=0,relief="ridge")
prevButton = Button(master=nextPrevBtnFrame,text="Prev")
nextButton = Button(master=nextPrevBtnFrame,text="Next")

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
    global firstDrawFlag
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
    global firstDrawFlag
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
    global firstDrawFlag
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

def on_next_button_click(event):
    global displayImageIndex
    global imageFileNameList
    if(displayImageIndex < len(imageFileNameList) - 1):
        displayImageIndex = displayImageIndex + 1
        displayImage(imageFileNameList[displayImageIndex])

def getFileNameListFromPath(folderPath):
    global imageFileNameList
    # 初期化
    imageFileNameList = []
    displayImageIndex = 0

    # 取得値設定
    listOfFiles = os.listdir(folderPath)  
    pattern = "*.jpg"
    for fileName in listOfFiles:  
        if fnmatch.fnmatch(fileName, pattern):
            imageFileNameList.append(folderPath + "/" + fileName)

def displayImage(fileName):
    imageFile = ImageTk.PhotoImage(Image.open(fileName))
    canvas.image = imageFile
    canvas.create_image(0,0,anchor='nw',image=imageFile)
    #canvas.coords("canvasImage",0,0,anchor='nw',image=imageFile)

def main():
    canvas.bind("<Motion>", on_mouse_motion)
    canvas.bind("<Button-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    browseButton.bind("<Button-1>", on_browse_button_click)
    prevButton.bind("<Button-1>", on_prev_button_click)
    nextButton.bind("<Button-1>", on_next_button_click)

    fileFrame.pack(fill="x")
    folderPathTitleLabel.pack(side="left")
    folderPathEntry.pack(side="left")
    browseButton.pack(side="left")

    canvasFrame.pack(fill="x")
    canvas.pack(side="left")

    nextPrevBtnFrame.pack(fill="x")
    prevButton.pack(side="right")
    nextButton.pack(side="right")

    root.mainloop()
 
if __name__ == '__main__':
    main()