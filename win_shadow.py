# coding=utf-8
from pynput import keyboard,mouse

import pyautogui as p
import time
import threading
import os
import shutil
import datetime
#保护措施，避免失控
p.FAILSAFE = True
#为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。
p.PAUSE = 0.25

class MyListener(threading.Thread):
    _stop_flag = False
    _pause_flag = False
    _runnig_flag = False
    lst  = []

    def __init__(self,file):
        threading.Thread.__init__(self)

        self.f = file

    def stop(self):
        self._stop_flag = True
        for t in self.lst:
            t.stop()

    def run(self):
        time.sleep(1)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.mouse_listener = mouse.Listener(on_click=self.on_click,on_scroll=self.on_scroll)
        self.lst = [self.keyboard_listener,self.mouse_listener]
        self._runnig_flag = True
        for t in self.lst:
            t.start()
        for t in self.lst:
            t.join()
    def on_press(self,key):

        try:
            if not isinstance(key,keyboard.Key):
                print('alphanumeric key {0} pressed'.format(key.char))
                # print(dir(key))
                f.writelines("keyboard,{0},{1},{2}\n".format(1,key.char,datetime.datetime.now().timestamp()))
            else:
                print('special key {0} pressed'.format(key))
                self.f.writelines("keyboard,{0},{1},{2}\n".format(0,key.name,datetime.datetime.now().timestamp()))

        except AttributeError:
            pass
        self.f.flush()

    def on_release(self,key):
        try:
            if not isinstance(key,keyboard.Key):
                print('alphanumeric key {0} released'.format(key.char))
                # print(dir(key))
                f.writelines("keyboard,{0},{1},{2}\n".format(2,key.char,datetime.datetime.now().timestamp()))
            else:
                print('special key {0} released'.format(key))
                self.f.writelines("keyboard,{0},{1},{2}\n".format(3,key.name,datetime.datetime.now().timestamp()))

        except AttributeError:
            pass
        self.f.flush()

    def on_move(self,x, y):
        print('Pointer moved to {0}'.format((x, y)))

    def on_click(self,x, y, button, pressed):
        print('{0} at {1}'.format( 'Pressed' if pressed else 'Released',(x, y)))
        self.f.writelines("mouse,{0},{1},{2},{3}\n".format(button.name+('_P' if pressed else '_R'),x,y,datetime.datetime.now().timestamp()))
        self.f.flush()


    def on_scroll(self,x, y, dx, dy):
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
        self.f.writelines("mouse,scroll,{0},{1},{2},{3},{4}\n".format(x,y,dx,dy,datetime.datetime.now().timestamp()))
        self.f.flush()

# m = Controller()-
def repeatMouseOps(ops):
    print(ops)
    ops_arr = ops.strip().split(",")
    name = ops_arr[1]
    if name== 'left_P' or name == "right_P":
        # p.click(int(ops_arr[2]),int(ops_arr[3]))
        p.mouseDown(int(ops_arr[2]),int(ops_arr[3]), button=name[:-2])
    elif name == "left_R" or name == 'right_R':
        # p.rightClick(int(ops_arr[2]),int(ops_arr[3]))
        p.mouseUp(int(ops_arr[2]),int(ops_arr[3]), button=name[:-2])
    elif name == 'middle':
        p.middleClick(int(ops_arr[2]),int(ops_arr[3]))
    elif name == 'scroll':
        p.moveTo(int(ops_arr[2]),int(ops_arr[3]))
        p.scroll(int(ops_arr[5]) * 120)
        # m.scroll(int(ops_arr[4]),int(ops_arr[5]))
    else:
        print("not known ops.....")

def repeatKeyboardOps(key_record):
    print(key_record)
    arrs = key_record.split(",")
    name = arrs[1]
    char = arrs[2]
    if name == '0' or name == '1':
        # p.typewrite(message=char,interval=0.01)
        p.keyDown(char)
    elif name == '3' or name == '2':
        p.keyUp(char)
    else:
        keys = char.split("$")
        cmd = "p.hotkey('"+"','".join(keys)+"')"
        exec(cmd)
        # pass
        # p.press(char)

def doShadow(file_name):
    time.sleep(2)
    stack = []
    stack2 = []
    with open(file_name,'r') as f:
        for i in f.readlines():
            print(i)
            stack.append(i.replace("_r","right").replace("_l","left"))
    while len(stack) > 0:
        i = stack.pop()
        if i.strip().startswith('mouse'):
            stack2.append(i)
        else:
            arrs = i.split(",")
            tp = arrs[1]
            name = arrs[2]

            if tp == '3':
                hotKey = []
                hotKey.append(arrs[2])
                v = stack.pop()
                arrs2 = v.split(",")
                while arrs2[1] != "0" and name != arrs2[2]:
                    if not arrs2[2] in hotKey:
                        hotKey.append(arrs2[2])
                    v = stack.pop()
                    arrs2 = v.split(",")
                stack2.append("keyboard,{0},{1},{2}\n".format('hot',"$".join(hotKey),arrs[3]))

    while len(stack2) > 0:
        i = stack2.pop()

        if i.strip().startswith('mouse'):
            repeatMouseOps(i.strip())
            time.sleep(1)
        else:
            repeatKeyboardOps(i.strip())


if __name__ == "__main__":
    path = "D://"
    file_name = "ops_log.txt"
    new_file_name = ""
    f = open(path + file_name,'w+')
    flag = True
    pause_flag = True
    name = 'Record'
    listener = MyListener(f)
    while flag:
        ac = p.confirm('Enter option.', buttons=[name, 'Repeat', 'Quit'])
        if ac == "Record":
            name = 'Stop Recording'
            listener.start()
            pause_flag = False

        elif ac == "Stop Recording":
            name = 'Record'
            listener.stop()
            f.close()
            pause_flag = True
            new_file_name = path + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+ ".txt"
            print(new_file_name)
            shutil.copy(os.path.join(path,file_name),new_file_name)
            f = open("D://ops_log.txt",'w')
            listener = MyListener(f)
        elif ac == 'Repeat':
            if not pause_flag:
                p.alert("listener is runing .....")
            else:
                if new_file_name == "":
                    import easygui
                    new_file_name = easygui.fileopenbox()
                    #new_file_name = p.prompt('input  ')
                doShadow(new_file_name)
        else:
            print("stop...")
            flag = False
            listener.stop()
    f.close()