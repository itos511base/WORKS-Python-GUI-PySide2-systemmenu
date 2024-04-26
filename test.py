import sys
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

import ctypes.wintypes
import win32con
import win32gui

#システムメニュー(タスクバーを右クリックで出るメニュー)にアイテムを追加して、項目クリックを検出するテストコード

class Ui(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Ui, self).__init__(*args, **kwargs)
        
        self.setWindowFlags(Qt.Window)
        self.resize(400, 300)
        self.setWindowTitle('System menu test')
        
    #override 'NativeEvent' handler of window
    #https://doc.qt.io/qt-6/qwindow.html#nativeEvent
    #https://github.com/PyQt5/PyQt/blob/master/Demo/NativeEvent.py         
    def nativeEvent(self, eventType, message):
        retval, result = super(Ui, self).nativeEvent(eventType, message)
        
        if eventType == "windows_generic_MSG": #message from Qt
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message==win32con.WM_SYSCOMMAND:
                print(f'message=WM_SYSCOMMAND({win32con.WM_SYSCOMMAND}), wParam={msg.wParam}')
                return (False, 0)
        
        return retval, result
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Ui()
    w.show()

    #システムメニューに項目を追加する
    #hwnd = win32gui.GetForegroundWindow ()
    hwnd = win32gui.FindWindow(None, 'System menu test')
    #hwnd = win32gui.FindWindow(None,'無題 - メモ帳') #他のアプリに項目を追加することもできる
    #print(win32gui.GetWindowText(self.hwnd))
    hmenu = win32gui.GetSystemMenu(hwnd, False)
    win32gui.AppendMenu(hmenu, win32con.MF_SEPARATOR, 0, '')
    win32gui.AppendMenu(hmenu, win32con.MF_STRING, 100, 'New Menu Item (100)')   #どうやってイベントをハンドルするの？(いわゆるWNDPROCコールバック)
    win32gui.AppendMenu(hmenu, win32con.MF_STRING, 101, 'New Menu Item (101)')
    win32gui.AppendMenu(hmenu, win32con.MF_STRING, 102, 'New Menu Item (102)')

    sys.exit(app.exec_())
