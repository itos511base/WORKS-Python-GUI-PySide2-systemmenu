import sys
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget

import ctypes.wintypes
import win32con
import win32gui

#システムメニュー(タスクバーを右クリックで出るメニュー)にアイテムを追加して、項目クリックを検出するテストコード

class Ui(QWidget):
    
    #system menu 項目ID
    SELFMENUID_0 = 100
    SELFMENUID_1 = 101
    SELFMENUID_2 = 102
    
    def __init__(self, *args, **kwargs):
        super(Ui, self).__init__(*args, **kwargs)
        self.ui = CustomQUiLoader().load('untitled.ui', None) #was uic.loadUi
        
        self.ui.setWindowTitle('System menu test with .ui')
        self.Form = self.ui #as 'Form' of base widget
        #self.pushButton = self.ui.pushButton #dummy
        
        self.ui.parent=self
        
        #システムメニューに項目を追加する
        #hwnd = win32gui.GetForegroundWindow()
        #hwnd = win32gui.FindWindow(None, 'Form')  #この時点でwindowは生成されていないので使えない → ui.show()の後だと使える
        self.ui.hwnd = self.ui.winId()
        if self.ui.hwnd:
            hmenu = win32gui.GetSystemMenu(self.ui.hwnd, False)
            if hmenu:
                win32gui.AppendMenu(hmenu, win32con.MF_SEPARATOR, 0, '')
                win32gui.AppendMenu(hmenu, win32con.MF_STRING, self.SELFMENUID_0, f'New Menu Item ({self.SELFMENUID_0})')
                win32gui.AppendMenu(hmenu, win32con.MF_STRING, self.SELFMENUID_1, f'New Menu Item ({self.SELFMENUID_1})')
                win32gui.AppendMenu(hmenu, win32con.MF_STRING, self.SELFMENUID_2, f'New Menu Item ({self.SELFMENUID_2})')

    def show(self):
        self.ui.show()
    
    #override 'nativeEvent' handler of window
    #https://doc.qt.io/qt-6/qwindow.html#nativeEvent
    #https://github.com/PyQt5/PyQt/blob/master/Demo/NativeEvent.py
    #※CustomQUiLoader()した場合はハンドラが呼ばれるウィジット(Formクラス)はこことは別で生成される。
    #  nativeEventはそちらでオーバーライドする必要があるので、カスタムローダー内のFormクラス生成でオーバーライドしている。
    #  ここの関数は、そのオーバーライド関数から呼ばしている。
    def nativeEvent_cb(self, eventType, message): #callback from CustomQWidget.nativeEvent
        if eventType == "windows_generic_MSG": #message from Qt
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message==win32con.WM_SYSCOMMAND:
                #print(f'message=WM_SYSCOMMAND({win32con.WM_SYSCOMMAND}), wParam={msg.wParam}')
                if msg.wParam==self.SELFMENUID_0: #参考としてswicth～case風に書く
                    print(f'Your select: New Menu Item ({self.SELFMENUID_0})')
                    return (True, 0)
                elif msg.wParam==self.SELFMENUID_1:
                    print(f'Your select: New Menu Item ({self.SELFMENUID_1})')
                    return (True, 0)
                elif msg.wParam==self.SELFMENUID_2:
                    print(f'Your select: New Menu Item ({self.SELFMENUID_2})')
                    return (True, 0)  #イベントが処理された場合にのみ true を返す必要があります。
        return (False, 0)


class CustomQUiLoader(QUiLoader):
    def createWidget(self, className, parent=None, name=''):
        if className == 'CustomQWidget':
            ret = CustomQWidget(parent)
            ret.setObjectName(name)
            return ret
        return super().createWidget(className, parent, name)

class CustomQWidget(QWidget):
    parent:QWidget = None
    hwnd:int = 0
    
    #override 'nativeEvent' handler of window
    #https://doc.qt.io/qt-6/qwindow.html#nativeEvent
    #https://github.com/PyQt5/PyQt/blob/master/Demo/NativeEvent.py         
    def nativeEvent(self, eventType, message):
        retval, result = super(CustomQWidget, self).nativeEvent(eventType, message)
        if self.parent!=None:
            return self.parent.nativeEvent_cb(eventType, message) #callback
        return (retval, result)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
