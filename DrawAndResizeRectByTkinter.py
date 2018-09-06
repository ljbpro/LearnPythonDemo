import tkinter

firstDrawFlag = True
firstDragInFirstDraw = True
mouseDragingFlag = False
resizeMode = 0
startPointX = 0
startPointY = 0
endPointX = 0
endPointY = 0
cursorType = ""

root = tkinter.Tk()
root.title(u"TkinterのCanvasを使ってみる")
root.geometry("800x600")
canvas = tkinter.Canvas(root, width = 600, height = 480, bd = 0, bg = '#F5F5DC')
canvas.place(x=0, y=0)

def on_mouse_motion(event):
    global firstDrawFlag
    global mouseDragingFlag
    global resizeMode
    global cursorType
    global startPointX
    global startPointY
    global endPointX
    global endPointY

    x = event.x
    y = event.y

    if firstDrawFlag == False and mouseDragingFlag == False:
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
    
    if firstDrawFlag == True:
        # 変数を更新
        endPointX = x
        endPointY = y

        # 範囲を描く
        if firstDragInFirstDraw == True:
            firstDragInFirstDraw = False
            canvas.create_rectangle(startPointX, startPointY, endPointX, endPointY, tag="canvasRect")
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

    if firstDrawFlag == True:
        startPointX = x
        startPointY = y
        endPointX = x
        endPointY = y

def on_mouse_release(event):
    global firstDrawFlag
    global mouseDragingFlag

    # カーソル設定
    canvas.configure(cursor='arrow')

    if (firstDrawFlag == True and mouseDragingFlag == True):
        firstDrawFlag = False

    # Mouse Drawingフラグ制御解除
    mouseDragingFlag = False

def main():
    canvas.bind("<Motion>", on_mouse_motion)
    canvas.bind("<Button-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)
    canvas.pack()
    root.mainloop()
 
if __name__ == '__main__':
    main()