import sys
import ctypes
from PyQt6.QtWidgets import QApplication
import IOT_window as main_window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_id = 'Software_Engineer.POS_app.A1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    win = main_window.Window()
    win.showMaximized()
    sys.exit(app.exec())

