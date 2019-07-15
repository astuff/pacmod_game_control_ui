#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/calib_fenoglio/on_the_fly/qtpy_dump/game_control_version1/game_control_version1/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtCore import QObject
from PyQt4.QtCore import *
from qnode import JoyGui

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from pacmod_msgs.msg import *

pyNode = "joy_gui"

#Global constant
PACMOD_RATE = 30

# Helper variables to control message frequency 
last_Enable = ''
last_Override = ''
last_Timeout = ''

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


class JoyGui(object):
    
    def __init__(self):

        self.which_run = "spin" # spin or while

        # Gui update variables
        self.enable = False
        self.is_enable = False
        self.override = False
        self.is_override = False
        self.timeout = False
        self.is_timeout = False
        self.veh_accel = 0.0
        self.veh_brake = 0.0


    def enabled_Check_CB(self, msg):
        """
        Checks if Pacmod is enabled and returns status
        """
        self.is_enable = False
        # Checks for repetitive messages
        global last_Enable
        if msg.data != last_Enable:

            self.is_enable = True                   # control variable
            last_Enable = msg.data                  # Set message to new ros msg to compare to next incoming

            rospy.loginfo("I heard a NEW msg: PACMod Enabled = %s", msg.data) 

            # Set message for processing
            self.enable = msg.data

    def override_Check_CB(self,msg):
        """
        Checks if driver has taken back control of vehicle
        """
        # Checks for repetitive messages
        global last_Override
        if msg.override_active != last_Override:
            self.is_override =  True                    # control variable
            last_Override = msg.override_active
            rospy.loginfo("I heard a NEW msg: Override is %s", msg.override_active)

            # Set message for proccessing
            self.override = msg.override_active

    def timeout_Check_CB(self,msg):
        """
        Checks if the PACMod has timed out and become inactive
        """
        global last_Timeout
        # Checks for repetitive messages
        if msg.user_can_timeout != last_Timeout:
            self.is_timeout = True                  # control variable
            last_Timeout = msg.user_can_timeout
            rospy.loginfo("I heard a NEW msg: timeout is %s", msg.user_can_timeout)

            # Set message for processing
            self.timeout = msg.user_can_timeout

    def accel_Percent_CB(self, msg):
        """
        Retrieves throttle position as a float number signifying percent:
        fully closed = 0.0 and fully open = 1.0
        """
        # Sends info to log
        self.veh_accel = msg.output
        veh_accel = msg.output
        if self.veh_accel > 0.01:
            rospy.loginfo(rospy.get_name() + " Acceleration output: %f", (self.veh_accel)*100)


    def brake_Percent_CB(self,msg):
        """
        Retrieves braking position as a float number signifying percent:
        no braking = 0.0 and fully braking = 1.0
        """
        # Sends info to log
        self.veh_brake = msg.output
        if self.veh_brake > 0.01:
            rospy.loginfo(rospy.get_name() + " Braking output: %f", (self.veh_brake)*100)

    def subscribe(self):

        # Send module state to Log
        rospy.loginfo("Now I'm in Pub/Sub... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.systemSub = rospy.Subscriber('/pacmod/as_tx/enabled',std_msgs.msg.Bool,self.enabled_Check_CB, queue_size= 100)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.override_Check_CB, queue_size=100)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.timeout_Check_CB, queue_size=100)
        self.throttleSub = rospy.Subscriber('/pacmod/parsed_tx/accel_rpt',pacmod_msgs.msg.SystemRptFloat,self.accel_Percent_CB,queue_size= 100)
        self.brakeSub = rospy.Subscriber('/pacmod/parsed_tx/brake_rpt',pacmod_msgs.msg.SystemRptFloat,self.brake_Percent_CB, queue_size= 100)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(949, 628)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 931, 591))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.Main_vertical_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.Main_vertical_layout.setMargin(11)
        self.Main_vertical_layout.setSpacing(6)
        self.Main_vertical_layout.setObjectName(_fromUtf8("Main_vertical_layout"))
        self.wheel_layout = QtGui.QVBoxLayout()
        self.wheel_layout.setMargin(11)
        self.wheel_layout.setSpacing(6)
        self.wheel_layout.setObjectName(_fromUtf8("wheel_layout"))
        self.pac_wheel_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.pac_wheel_label.setObjectName(_fromUtf8("pac_wheel_label"))
        self.wheel_layout.addWidget(self.pac_wheel_label, QtCore.Qt.AlignHCenter)
        self.pac_wheel = QtGui.QLabel(self.verticalLayoutWidget)
        self.pac_wheel.setText(_fromUtf8(""))
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")))
        self.pac_wheel.setObjectName(_fromUtf8("pac_wheel"))
        self.wheel_layout.addWidget(self.pac_wheel, QtCore.Qt.AlignHCenter)
        self.Main_vertical_layout.addLayout(self.wheel_layout)
        self.text_layout = QtGui.QVBoxLayout()
        self.text_layout.setMargin(11)
        self.text_layout.setSpacing(6)
        self.text_layout.setObjectName(_fromUtf8("text_layout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.text_layout_2 = QtGui.QVBoxLayout()
        self.text_layout_2.setMargin(11)
        self.text_layout_2.setSpacing(6)
        self.text_layout_2.setObjectName(_fromUtf8("text_layout_2"))
        self.pacmod_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(136, 138, 133)"))
        self.pacmod_label.setObjectName(_fromUtf8("pacmod_label"))
        self.text_layout_2.addWidget(self.pacmod_label)
        self.time_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.time_label.setStyleSheet(_fromUtf8("background-color:rgb(136, 138, 133)"))
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.text_layout_2.addWidget(self.time_label)
        self.over_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.over_label.setStyleSheet(_fromUtf8("background-color:rgb(136, 138, 133)"))
        self.over_label.setObjectName(_fromUtf8("over_label"))
        self.text_layout_2.addWidget(self.over_label)
        self.horizontalLayout_2.addLayout(self.text_layout_2)
        self.text_layout.addLayout(self.horizontalLayout_2)
        self.Main_vertical_layout.addLayout(self.text_layout)
        self.Progress_layout = QtGui.QVBoxLayout()
        self.Progress_layout.setMargin(11)
        self.Progress_layout.setSpacing(6)
        self.Progress_layout.setObjectName(_fromUtf8("Progress_layout"))
        self.acceleration_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.acceleration_label.setObjectName(_fromUtf8("acceleration_label"))
        self.Progress_layout.addWidget(self.acceleration_label, QtCore.Qt.AlignHCenter)
        self.acceleration_bar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.acceleration_bar.setProperty("value", 0)
        self.acceleration_bar.setObjectName(_fromUtf8("acceleration_bar"))
        self.Progress_layout.addWidget(self.acceleration_bar)
        self.braking_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.braking_label.setObjectName(_fromUtf8("braking_label"))
        self.Progress_layout.addWidget(self.braking_label, QtCore.Qt.AlignHCenter)
        self.braking_bar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.braking_bar.setProperty("value", 0)
        self.braking_bar.setObjectName(_fromUtf8("braking_bar"))
        self.Progress_layout.addWidget(self.braking_bar)
        self.Main_vertical_layout.addLayout(self.Progress_layout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 949, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.acceleration_bar, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.acceleration_bar.setValue)
        QtCore.QObject.connect(self.braking_bar, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.braking_bar.setValue)
        QtCore.QObject.connect(self.pac_wheel, QtCore.SIGNAL(_fromUtf8("windowTitleChanged(QString)")), self.pacmod_label.setStyleSheet)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pac_wheel_label.setText(_translate("MainWindow", "PACMod Indicator", None))
        self.pacmod_label.setText(_translate("MainWindow", "PACMod Status: ", None))
        self.time_label.setText(_translate("MainWindow", "Timeout Status:", None))
        self.over_label.setText(_translate("MainWindow", "Over-ride Status:", None))
        self.acceleration_label.setText(_translate("MainWindow", "Acceleration", None))
        self.braking_label.setText(_translate("MainWindow", "Braking", None))


# class MyThread(QtCore.QThread, JoyGui):

#     accel_signal = pyqtSignal(float, name = "set_accel_bar")
#     brake_signal = pyqtSignal(float, name = "set_brake_bar")
#     enable_signal =pyqtSignal(bool, name = "set_enable")
#     override_signal = pyqtSignal(bool, name = "set_override")
#     timeout_signal = pyqtSignal(bool, name = "set_timeout")


#     def __init__(self):
#         QtCore.QThread.__init__(self)
#         QObject.__init__(self)
#         JoyGui.__init__(self)


#     def run(self):
#         while not rospy.is_shutdown():
#             if self.is_enable == True:
#                 self.enable_signal.emit(self.enable)
#                 time.sleep(0.3)


class MyApp(QtGui.QMainWindow, Ui_MainWindow, JoyGui):

    accel_signal = pyqtSignal(float, name = "set_accel_bar")
    brake_signal = pyqtSignal(float, name = "set_brake_bar")
    enable_signal =pyqtSignal(bool, name = "set_enable")
    override_signal = pyqtSignal(bool, name = "set_override")
    timeout_signal = pyqtSignal(bool, name = "set_timeout")

    def __init__(self, parent = None):

        # Initialize subclasses
        QObject.__init__(self)
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        JoyGui.__init__(self)

        #Initialize variables and UI
        self.setupUi(self)
        self.show()
        # self.Thread = MyThread()
        # self.Thread.enable_signal.connect(self.set_enable)
        # self.Thread.start()

        # Connect Signals and Slots here
        self.pac_wheel
        


    @QtCore.pyqtSlot(bool)
    def set_enable(self):
        """
        if Pacmod enabled, indicators are set to blue
        """
        print("inside set_enable")

        if self.enable == True:
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: blue"))
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/Desktop/Steer_Icon/autonomouswheel.png")))
                # self.statusSet2 = False
                # self.statusSet3 = False

        elif self.enable == False:
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")))

    @QtCore.pyqtSlot(bool)
    def set_timeout(self):
        """
        If timeout is active indicators are set to red
        """
        if self.timeout == True:
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: red"))
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/Desktop/Steer_Icon/steering-wheel-red.png")))
        else:
            pass

    @QtCore.pyqtSlot(bool)
    def set_override(self):

        """
        If override is active indicators are set to green
        """
        if self.override == True:
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green"))
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/Desktop/Steer_Icon/steering-wheelgreen.png")))
        else:
            pass
    def set_accel_bar(self):
        pass
    def set_brake_bar(self):
        pass

if __name__ == "__main__":

    # init Qnode here 
    rospy.init_node(pyNode)
    joy_gui = JoyGui()

    try:
        app 
        #app.setStyle('Windows')

    except:
        app = QtGui.QApplication(sys.argv)
        joy_gui.subscribe()
        window = MyApp()
        #window.show()
        sys.exit(app.exec_())



