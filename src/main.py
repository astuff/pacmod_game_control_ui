#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/calib_fenoglio/sb_joy_qt/src/joy_stick/src/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtCore import *

from qnode import JoyGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1039, 635)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))

        self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 1001, 551))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setMargin(11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))

        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setMargin(11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))

        self.Steering_Label = QtGui.QLabel(self.verticalLayoutWidget)
        self.Steering_Label.setObjectName(_fromUtf8("Steering_Label"))
        self.verticalLayout_6.addWidget(self.Steering_Label, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.steering_image = QtGui.QLabel(self.verticalLayoutWidget)
        self.steering_image.setText(_fromUtf8(""))
        self.steering_image.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")))
        self.steering_image.setObjectName(_fromUtf8("steering_image"))
        self.verticalLayout_6.addWidget(self.steering_image, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)

        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setMargin(11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))

        self.Active_Indicator = QtGui.QLabel(self.verticalLayoutWidget)
        self.Active_Indicator.setStyleSheet(_fromUtf8("QLabel { background-color: Red }"))
        self.Active_Indicator.setText(_fromUtf8(""))
        self.Active_Indicator.setObjectName(_fromUtf8("Active_Indicator"))
        self.verticalLayout_4.addWidget(self.Active_Indicator)

        self.Override_Indicator = QtGui.QLabel(self.verticalLayoutWidget)
        self.Override_Indicator.setStyleSheet(_fromUtf8("QLabel { background-color: Red }"))
        self.Override_Indicator.setText(_fromUtf8(""))
        self.Override_Indicator.setObjectName(_fromUtf8("Override_Indicator"))
        self.verticalLayout_4.addWidget(self.Override_Indicator)

        self.TimeoutIndicator = QtGui.QLabel(self.verticalLayoutWidget)
        self.TimeoutIndicator.setStyleSheet(_fromUtf8("QLabel { background-color: Red }"))
        self.TimeoutIndicator.setText(_fromUtf8(""))
        self.TimeoutIndicator.setObjectName(_fromUtf8("TimeoutIndicator"))
        self.verticalLayout_4.addWidget(self.TimeoutIndicator)

        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.PACMod = QtGui.QLabel(self.verticalLayoutWidget)
        self.PACMod.setObjectName(_fromUtf8("PACMod"))
        self.verticalLayout_3.addWidget(self.PACMod)

        self.Override = QtGui.QLabel(self.verticalLayoutWidget)
        self.Override.setObjectName(_fromUtf8("Override"))
        self.verticalLayout_3.addWidget(self.Override)

        self.Timeout = QtGui.QLabel(self.verticalLayoutWidget)
        self.Timeout.setObjectName(_fromUtf8("Timeout"))
        self.verticalLayout_3.addWidget(self.Timeout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setMargin(11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))

        self.Acceleration = QtGui.QLabel(self.verticalLayoutWidget)
        self.Acceleration.setObjectName(_fromUtf8("Acceleration"))
        self.verticalLayout_8.addWidget(self.Acceleration, QtCore.Qt.AlignHCenter)

        self.Accel_Progress = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.Accel_Progress.setMinimumSize(QtCore.QSize(0, 25))
        self.Accel_Progress.setProperty("value", 24)
        self.Accel_Progress.setObjectName(_fromUtf8("Accel_Progress"))
        self.verticalLayout_8.addWidget(self.Accel_Progress)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_8.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)

        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setMargin(11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.Braking = QtGui.QLabel(self.verticalLayoutWidget)
        self.Braking.setObjectName(_fromUtf8("Braking"))
        self.verticalLayout_7.addWidget(self.Braking, QtCore.Qt.AlignHCenter)

        self.Braking_Progress = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.Braking_Progress.setProperty("value", 24)
        self.Braking_Progress.setObjectName(_fromUtf8("Braking_Progress"))
        self.verticalLayout_7.addWidget(self.Braking_Progress)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_7.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1039, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)

        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)

        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Steering_Label.setText(_translate("MainWindow", "PACMod indicator ", None))
        self.PACMod.setText(_translate("MainWindow", "PACMod", None))
        self.Override.setText(_translate("MainWindow", "Override", None))
        self.Timeout.setText(_translate("MainWindow", "Timeout", None))
        self.Acceleration.setText(_translate("MainWindow", "Acceleration", None))
        self.Braking.setText(_translate("MainWindow", "Braking", None))

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        # Inits
        self.setupUi(self)
        jg = JoyGui()

        # Connect Signals, Slots, and Emits here
        self.connect(self.Active_Indicator, SIGNAL("get_enabled()"), self.pac_active)


    # Define the callbacks here 

    @QtCore.pyqtSlot()
    def pac_active(self):
        sender()
        pass
    @QtCore.pyqtSlot()
    def is_timeout(self):
        pass
    @QtCore.pyqtSlot()
    def is_override(self):
        pass
    @QtCore.pyqtSlot()
    def something(self):
        pass
    @QtCore.pyqtSlot()
    def soemthing_else():
        pass
    @QtCore.pyqtSlot()
    def anotha_one(self):
        pass
    @QtCore.pyqtSlot()
    def it_aint_over_yet(self):
        pass
    @QtCore.pyqtSlot()
    def done(self):
        pass
    @QtCore.pyqtSlot()
    def psyche(self):
        pass
    #@QtCore.pyqtSignal
    def get_enabled(data):
        return data


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    #app.setStyle('Windows')
    window = MyApp()
    window.show()
    app.exec_()
#sys.exit(app.exec_())

