import tkinter

window = tkinter.Tk() 
label = tkinter.Label(window, text = "サンプル") 
label.pack()    # --- (1) 
button = tkinter.Button(window, text = "ボタンです。押しても何も起きません") 
button.pack() 
 
window.mainloop() 