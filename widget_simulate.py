# coding: utf-8
from PyQt5 import QtCore, QtWidgets
from utils import AbstractFunction
from ui_design.simulate import Ui_Form as __Form


class WidgetScanButton(QtWidgets.QDialog, __Form, AbstractFunction):
    sig_scan = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WidgetScanButton, self).__init__(parent, flags=QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.btn_scan.clicked.connect(self.sig_scan.emit)
        self.setWindowTitle('模拟按钮')


