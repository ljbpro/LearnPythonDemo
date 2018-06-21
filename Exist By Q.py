import threading
from msvcrt import getch

isExist = False

def keyEventMonitoring():
    global isExist
    while(True):
        key = ord(getch())
        if(key == 113):
            # [q]キー押下イベント
            isExist = True

def doSometing():
    n = 0
    while isExist == False:
        print(n)
        n = n + 1
    
    exit()

def main():
    # 監視関数起動
    t1 = threading.Thread(target=keyEventMonitoring)
    t1.setDaemon(True)
    t1.start()

    # 事務処理関数起動
    doSometing()

if __name__ == '__main__':
    main()