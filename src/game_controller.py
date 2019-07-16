#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
import time

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtCore import QObject
from PyQt4.QtCore import *

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from pacmod_msgs.msg import *

#Node name 
pyNode = "joy_gui"

#Global constant
PACMOD_RATE = 30
PACMOD_RATE_IN_SEC = 0.33

#
CONVERTER = 100

# Helper variables, Controls message frequency 
last_Enable = ''
last_Override = ''
last_accel = 0
last_brake = 0

# Controls for ROS MSG'S
enable = False
override = False
veh_accel = 0.0
veh_brake = 0.0

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
        pass

    def enabled_Check_CB(self, msg):
        """
        Checks if Pacmod is enabled and returns status
        """

        #Globals for GUI
        global last_Enable
        global enable

        # Checks for repetitive messages
        if msg.data != last_Enable:
            last_Enable = msg.data
            rospy.loginfo("I heard a NEW msg: PACMod Enabled = %s", msg.data) 

            # Set message for processing
            enable = msg.data


    def override_Check_CB(self,msg):
        """
        Checks if driver has taken back control of vehicle
        """
        # Globals for GUI
        global last_Override
        global override
     
        # Checks for repetitive messages
        if msg.override_active != last_Override:
            last_Override = msg.override_active
            rospy.loginfo("I heard a NEW msg: Override = %s", msg.override_active)
            override = msg.override_active # Set message for proccessing



    def accel_Percent_CB(self, msg):
        """
        Retrieves throttle position as a float number signifying percent:
        fully closed = 0.0 and fully open = 1.0
        """
        global veh_accel

        if (abs(msg.output - last_accel) * CONVERTER) > 1:
            veh_accel = int(msg.output * CONVERTER)
            rospy.loginfo(rospy.get_name() + " Acceleration output: %f", (veh_accel)) # Sends info to log
        elif msg.output  < 0.01:
            veh_accel = 0



    def brake_Percent_CB(self,msg):
        """
        Retrieves braking position as a float number signifying percent:
        no braking = 0.0 and fully braking = 1.0
        """
        global veh_brake
        
        if (abs(msg.output - last_brake) * CONVERTER) > 1:
            veh_brake = int(msg.output * CONVERTER)
            rospy.loginfo(rospy.get_name() + " Braking output: %f", (veh_brake)) # Sends info to log
        elif msg.output < 0.01:
            veh_accel = 0

    def subscribe(self):

        # Send module state to Log
        rospy.loginfo("Ready to publish... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.systemSub = rospy.Subscriber('/pacmod/as_tx/enabled',std_msgs.msg.Bool,self.enabled_Check_CB, queue_size= 100)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.override_Check_CB, queue_size=100)
        self.throttleSub = rospy.Subscriber('/pacmod/parsed_tx/accel_rpt',pacmod_msgs.msg.SystemRptFloat,self.accel_Percent_CB,queue_size= 100)
        self.brakeSub = rospy.Subscriber('/pacmod/parsed_tx/brake_rpt',pacmod_msgs.msg.SystemRptFloat,self.brake_Percent_CB, queue_size= 100)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(828, 585)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 721, 511))
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
        self.wheel_layout.addWidget(self.pac_wheel_label, QtCore.Qt.AlignHCenter,QtCore.Qt.AlignVCenter)
        self.pac_wheel = QtGui.QLabel(self.verticalLayoutWidget)
        self.pac_wheel.setText(_fromUtf8(""))
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")))
        self.pac_wheel.setObjectName(_fromUtf8("pac_wheel"))
        self.wheel_layout.addWidget(self.pac_wheel, QtCore.Qt.AlignHCenter,QtCore.Qt.AlignVCenter)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.acceleration_bar.sizePolicy().hasHeightForWidth())
        self.acceleration_bar.setSizePolicy(sizePolicy)
        self.acceleration_bar.setProperty("value", 0)
        self.acceleration_bar.setObjectName(_fromUtf8("acceleration_bar"))
        self.Progress_layout.addWidget(self.acceleration_bar)
        self.braking_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.braking_label.setObjectName(_fromUtf8("braking_label"))
        self.Progress_layout.addWidget(self.braking_label, QtCore.Qt.AlignHCenter)
        self.braking_bar = QtGui.QProgressBar(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.braking_bar.sizePolicy().hasHeightForWidth())
        self.braking_bar.setSizePolicy(sizePolicy)
        self.braking_bar.setProperty("value", 0)
        self.braking_bar.setObjectName(_fromUtf8("braking_bar"))
        self.Progress_layout.addWidget(self.braking_bar)
        self.Main_vertical_layout.addLayout(self.Progress_layout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 828, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Pacmod Game Control", None))
        self.pac_wheel_label.setText(_translate("MainWindow", "PACMod Indicator", None))
        self.pacmod_label.setText(_translate("MainWindow", "PACMod Status: ", None))
        self.acceleration_label.setText(_translate("MainWindow", "Acceleration", None))
        self.braking_label.setText(_translate("MainWindow", "Braking", None))


class MyThread(QThread):

    accel_signal = pyqtSignal(int, name = "set_accel_bar")
    brake_signal = pyqtSignal(int, name = "set_brake_bar")
    enable_signal =pyqtSignal(bool, name = "set_enable")
    override_signal = pyqtSignal(bool, name = "set_override")
    timeout_signal = pyqtSignal(bool, name = "set_timeout")


    def __init__(self):
        QtCore.QThread.__init__(self)
        QObject.__init__(self)



    def run(self):
    
        while not rospy.is_shutdown():
            if (enable == True)  and (override == False):
                self.enable_signal.emit(enable)
                time.sleep(PACMOD_RATE_IN_SEC)
                while (enable == True) and (override == False):
                    self.enable_signal.emit(enable)
                    time.sleep(PACMOD_RATE_IN_SEC)

                    if veh_accel > 0.1:
                        self.accel_signal.emit(veh_accel)
                        time.sleep(PACMOD_RATE_IN_SEC)
                        self.brake_signal.emit(veh_brake)
                        time.sleep(PACMOD_RATE_IN_SEC)

                    elif veh_brake > 0.1:
                        self.brake_signal.emit(veh_brake)
                        time.sleep(PACMOD_RATE_IN_SEC)
                        self.accel_signal.emit(veh_accel)
                        time.sleep(PACMOD_RATE_IN_SEC)

            if enable == False and (override == False):
                self.enable_signal.emit(enable)
                #time.sleep(0.3)
                self.accel_signal.emit(veh_accel)
                #time.sleep(0.3)
                self.brake_signal.emit(veh_brake)
                #time.sleep(0.3)
   
            if override == True and enable == False:
                self.enable_signal.emit(enable)
                self.override_signal.emit(override)
                time.sleep(0.3)




class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        # Initialize subclasses
        QObject.__init__(self)
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self,QtGui.QMainWindow)

        #Initialize variables and UI
        self.setupUi(self)
        self.show()
        self.Thread = MyThread()
        self.Thread.enable_signal.connect(self.set_enable)
        self.Thread.override_signal.connect(self.set_override)
        self.Thread.accel_signal.connect(self.set_accel_bar)
        self.Thread.brake_signal.connect(self.set_brake_bar)
        self.Thread.start()

        # Connect Signals and Slots here
        
    @QtCore.pyqtSlot(bool)
    def set_enable(self, data):
        """
        if Pacmod enabled, indicators are set to blue
        """
        if data == True:
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(98, 177, 246)"))
            self.pacmod_label.setText("PACMod Status: Enabled")
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/Desktop/Steer_Icon/autonomouswheel.png")))

        elif enable == False and (override == False):
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")))
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(136, 138, 133)")) 
            self.pacmod_label.setText("PACMod Status: Ready")
        self.update()


    @QtCore.pyqtSlot(bool)
    def set_override(self):

        """
        If override is active indicators are set to green
        """
        self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green"))
        self.pacmod_label.setText("PACMod Status: Over-Ride")
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/Desktop/Steer_Icon/overridewheel.png")))
        self.update()


    @QtCore.pyqtSlot(int)
    def set_accel_bar(self):
        self.acceleration_bar.setProperty("value", veh_accel)

    @QtCore.pyqtSlot(int)
    def set_brake_bar(self):
        self.braking_bar.setProperty("value", veh_brake)

if __name__ == "__main__":

    # init Qnode here 
    rospy.init_node(pyNode)
    joy_gui = JoyGui()

    try:
        app 

    except:
        joy_gui.subscribe()
        app = QtGui.QApplication(sys.argv)
        #app.setStyle('Fusion')
        window = MyApp()
        sys.exit(app.exec_())





