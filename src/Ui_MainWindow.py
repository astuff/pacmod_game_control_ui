#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Qt lib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import  QObject, pyqtSignal
from PyQt5.QtGui import QFont 
from PyQt5.QtWidgets import QLabel, QApplication, QAction

# Try block for multilingual support
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(454, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pac_wheel_label = QtWidgets.QLabel(self.centralWidget)
        self.pac_wheel = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pac_wheel.sizePolicy().hasHeightForWidth())
        self.pac_wheel.setSizePolicy(sizePolicy)
        self.pac_wheel.setText(_fromUtf8(""))
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8(
        "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png")))
        self.pac_wheel.setObjectName(_fromUtf8("pac_wheel"))
        self.verticalLayout_2.addWidget(self.pac_wheel, QtCore.Qt.AlignLeft)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.pacmod_label = QtWidgets.QLabel(self.centralWidget)
        self.pacmod_label.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
        self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green"))
        self.pacmod_label.setObjectName(_fromUtf8("pacmod_label"))
        self.pacmod_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pacmod_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pacmod_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.pac_wheel.setSizePolicy(sizePolicy)
        self.horizontalLayout_2.addWidget(self.pacmod_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.acceleration_label = QtWidgets.QLabel(self.centralWidget)
        self.acceleration_label.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
        self.acceleration_label.setObjectName(_fromUtf8("acceleration_label"))
        self.acceleration_label.setStyleSheet(_fromUtf8("color: white"))
        self.acceleration_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.acceleration_label, QtCore.Qt.AlignHCenter)
        self.acceleration_bar = QtWidgets.QProgressBar(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceleration_bar.sizePolicy().hasHeightForWidth())
        self.acceleration_bar.setSizePolicy(sizePolicy)
        self.acceleration_bar.setProperty("value", 0)
        self.acceleration_bar.setObjectName(_fromUtf8("acceleration_bar"))
        self.acceleration_bar.setStyleSheet(_fromUtf8("color: white"))
        self.verticalLayout_3.addWidget(self.acceleration_bar)
        self.braking_label = QtWidgets.QLabel(self.centralWidget)
        self.braking_label.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
        self.braking_label.setObjectName(_fromUtf8("braking_label"))
        self.braking_label.setStyleSheet(_fromUtf8("color: white"))
        self.braking_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.braking_label, QtCore.Qt.AlignHCenter)
        self.braking_bar = QtWidgets.QProgressBar(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.braking_bar.sizePolicy().hasHeightForWidth())
        self.braking_bar.setSizePolicy(sizePolicy)
        self.braking_bar.setProperty("value", 0)
        self.braking_bar.setObjectName(_fromUtf8("braking_bar"))
        self.braking_bar.setStyleSheet(_fromUtf8("color: white"))
        self.verticalLayout_3.addWidget(self.braking_bar)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.as_logo = QtWidgets.QLabel(self.centralWidget)
        self.as_logo.setText(_fromUtf8(""))
        self.as_logo.setPixmap(QtGui.QPixmap(_fromUtf8(
        "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/as_no_bg(80).png")))
        self.as_logo.setAlignment(QtCore.Qt.AlignRight)
        self.as_logo.setObjectName(_fromUtf8("as_logo"))
        self.horizontalLayout.addWidget(self.as_logo, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "PACMod game control", None))
        self.pacmod_label.setText(_translate("MainWindow", "Ready", None))
        self.acceleration_label.setText(_translate("MainWindow", "Acceleration", None))
        self.braking_label.setText(_translate("MainWindow", "Braking", None))