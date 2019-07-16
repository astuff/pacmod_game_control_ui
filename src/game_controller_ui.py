#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 
# Created by: PyQt4 UI code generator 4.11.4

import os
import sys
import time

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtCore import QObject
from PyQt4.QtCore import *
from PyQt4.QtGui import QLabel

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from pacmod_msgs.msg import *

#Node name 
pyNode = "joy_gui"

#Global constant
CONVERTER = 100
PACMOD_RATE = 30
PACMOD_RATE_IN_SEC = 0.33

# Controls for ROS MSG'S
enable = False
override = False

veh_accel = 0.0
veh_brake = 0.0

# Helper variables, Controls message frequency 
last_Enable = ''
last_Override = ''

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
        MainWindow.resize(610, 591)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pac_wheel_label = QtGui.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pac_wheel_label.setFont(font)
        self.pac_wheel_label.setObjectName(_fromUtf8("pac_wheel_label"))
        self.pac_wheel_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.pac_wheel_label, QtCore.Qt.AlignHCenter)
        self.pac_wheel = QtGui.QLabel(self.centralWidget)
        self.pac_wheel.setText(_fromUtf8(""))
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/sw_512_128x128.png")))
        self.pac_wheel.setObjectName(_fromUtf8("pac_wheel"))
        self.pac_wheel.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.pac_wheel, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pacmod_label = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacmod_label.sizePolicy().hasHeightForWidth())
        self.pacmod_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pacmod_label.setFont(font)
        self.pacmod_label.setObjectName(_fromUtf8("pacmod_label"))
        self.pacmod_label.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.QFrame.setstylesheet() # maybe a work around for border radius
        self.pacmod_label.setStyleSheet( _fromUtf8("background-color: rgb(136, 138, 133);"))
        self.pacmod_label.setAlignment(Qt.AlignVCenter)
        self.pacmod_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizontalLayout_2.addWidget(self.pacmod_label, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.acceleration_label = QtGui.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.acceleration_label.setFont(font)
        self.acceleration_label.setObjectName(_fromUtf8("acceleration_label"))
        self.acceleration_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.acceleration_label, QtCore.Qt.AlignHCenter)
        self.acceleration_bar = QtGui.QProgressBar(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceleration_bar.sizePolicy().hasHeightForWidth())
        self.acceleration_bar.setSizePolicy(sizePolicy)
        self.acceleration_bar.setProperty("value", 0)
        self.acceleration_bar.setObjectName(_fromUtf8("acceleration_bar"))
        self.verticalLayout_3.addWidget(self.acceleration_bar)
        self.braking_label = QtGui.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.braking_label.setFont(font)
        self.braking_label.setObjectName(_fromUtf8("braking_label"))
        self.braking_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.braking_label, QtCore.Qt.AlignHCenter)
        self.braking_bar = QtGui.QProgressBar(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.braking_bar.sizePolicy().hasHeightForWidth())
        self.braking_bar.setSizePolicy(sizePolicy)
        self.braking_bar.setProperty("value", 0)
        self.braking_bar.setObjectName(_fromUtf8("braking_bar"))
        self.verticalLayout_3.addWidget(self.braking_bar)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.as_logo = QtGui.QLabel(self.centralWidget)
        self.as_logo.setText(_fromUtf8(""))
        self.as_logo.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/AS only dark(128).jpg")))
        self.as_logo.setObjectName(_fromUtf8("as_logo"))
        self.as_logo.setAlignment(QtCore.Qt.AlignRight)
        self.horizontalLayout.addWidget(self.as_logo, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 610, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuPacmod_Game_Control = QtGui.QMenu(self.menuBar)
        self.menuPacmod_Game_Control.setObjectName(_fromUtf8("menuPacmod_Game_Control"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuPacmod_Game_Control.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Pacmod game control", None))
        self.pac_wheel_label.setText(_translate("MainWindow", "Pacmod Indicator", None))
        self.pacmod_label.setText(_translate("MainWindow", "Pacmod Status:", None))
        self.acceleration_label.setText(_translate("MainWindow", "Acceleration", None))
        self.braking_label.setText(_translate("MainWindow", "Braking", None))
        self.menuPacmod_Game_Control.setTitle(_translate("MainWindow", "Pacmod Game Control", None))

class JoyGui(object):
    
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
            #rospy.loginfo("I heard a NEW msg: PACMod Enabled = %s", msg.data)
            enable = msg.data # Set message for processing


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
            #rospy.loginfo("I heard a NEW msg: Override = %s", msg.override_active)
            override = msg.override_active # Set message for proccessing



    def accel_Percent_CB(self, msg):
        """
        Retrieves throttle position as a float number signifying percent:
        fully closed = 0.0 and fully open = 1.0
        """
        global veh_accel

        if enable == True:
            veh_accel = int(msg.output * CONVERTER)
            #rospy.loginfo(rospy.get_name() + " Acceleration output: %f", (veh_accel)) # Sends info to log

    def brake_Percent_CB(self,msg):
        """
        Retrieves braking position as a float number signifying percent:
        no braking = 0.0 and fully braking = 1.0
        """
        global veh_brake
        
        if enable == True:
            veh_brake = int(msg.output * CONVERTER)
            #rospy.loginfo(rospy.get_name() + " Braking output: %f", (veh_brake)) # Sends info to log

    def overArray(self,msg):

        # [1] = brake system on lexus and truck
        # [3] = steering on truck
        # [5] = steering on lexus

        print "Now in over ride checker"

        print "Brake = " + msg.overridden_status[1].value

        print "Steer = " + msg.overridden_status[5].value

        #print msg.overridden_status[5].value

    def subscribe(self):

        # Send module state to Log for troubleshooting
        rospy.loginfo("Ready to publish... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.systemSub = rospy.Subscriber('/pacmod/as_tx/enabled',std_msgs.msg.Bool,self.enabled_Check_CB, queue_size= 100)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.override_Check_CB, queue_size=100)
        self.throttleSub = rospy.Subscriber('/pacmod/parsed_tx/accel_rpt',pacmod_msgs.msg.SystemRptFloat,self.accel_Percent_CB,queue_size= 100)
        self.brakeSub = rospy.Subscriber('/pacmod/parsed_tx/brake_rpt',pacmod_msgs.msg.SystemRptFloat,self.brake_Percent_CB, queue_size= 100)
        self.allSysOver = rospy.Subscriber('/pacmod/as_tx/all_system_statuses',pacmod_msgs.msg.AllSystemStatuses, self.overArray, queue_size=100)

class MyThread(QtCore.QThread):

    # Custom signals, keep a class level variable or they wont function properly
    accel_signal = pyqtSignal(int, name = "set_accel_bar")
    brake_signal = pyqtSignal(int, name = "set_brake_bar")
    enable_signal =pyqtSignal(bool, name = "set_enable")
    override_signal = pyqtSignal(bool, name = "set_override")
    timeout_signal = pyqtSignal(bool, name = "set_timeout")

    # Only QObjects can emit singals
    def __init__(self):
        QtCore.QThread.__init__(self)
        QObject.__init__(self)


    def run(self):

        # Overridden run method handles all main running logic
        try:
            while not rospy.is_shutdown():

                while (enable == True) and (override == False):

                    self.enable_signal.emit(enable)
                    time.sleep(PACMOD_RATE_IN_SEC)

                    self.accel_signal.emit(veh_accel)
                    time.sleep(PACMOD_RATE_IN_SEC)

                    self.brake_signal.emit(veh_brake)
                    time.sleep(PACMOD_RATE_IN_SEC)

                if (enable == False) and (override == False):
                    self.enable_signal.emit(enable)
                    time.sleep(PACMOD_RATE_IN_SEC)
                    self.accel_signal.emit(0)
                    time.sleep(PACMOD_RATE_IN_SEC)
                    self.brake_signal.emit(0)
                    time.sleep(PACMOD_RATE_IN_SEC)
    
                elif (override == True) and (enable == False):
                    self.enable_signal.emit(enable)
                    self.override_signal.emit(override)
                    time.sleep(PACMOD_RATE_IN_SEC)

                elif (override == True) and (enable == True):
                    print "Something went wrong..."
        except:
            pass

class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        # Initialize subclasses
        QObject.__init__(self)
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self,QtGui.QMainWindow)

        #Initialize/show UI
        self.setupUi(self)
        self.setStyleSheet("background-color: white;");
        self.show()

        # Init thread and connect signals to slots to do work
        self.Thread = MyThread()
        self.Thread.enable_signal.connect(self.set_enable)
        self.Thread.override_signal.connect(self.set_override)
        self.Thread.accel_signal.connect(self.set_accel_bar)
        self.Thread.brake_signal.connect(self.set_brake_bar)
        self.Thread.start()

        self.connect(self, SIGNAL('triggered()'), self.closeEvent)

    #Signals and Slots here
    @QtCore.pyqtSlot()
    def closeEvent(self,event):

        # Kills all active nodes, will even attempt to close /rosout
        # nodes = os.popen("rosnode list").readlines()
        # for i in range(len(nodes)):
        #     nodes[i] = nodes[i].replace("\n","")

        # for node in nodes:
        #     os.system("rosnode kill "+ node)

        print "Close event detected\nGame control node shutting down..."
        rospy.signal_shutdown("an exception")
        self.destroy()
        #self.deleteLater()
        event.accept()
        
    @QtCore.pyqtSlot(bool)
    def set_enable(self, data):

        """
        if Pacmod enabled, Sets indicator to blue, 
        push's status and changes background color
        """

        if data == True:
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(98, 177, 246)"))
            self.pacmod_label.setText("Pacmod Status: Enabled")
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/autonomouswheel.png")))

        elif data == False and (override == False):
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/sw_512_128x128.png")))
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(136, 138, 133)")) 
            self.pacmod_label.setText("Pacmod Status: Ready")
        self.update()


    @QtCore.pyqtSlot(bool)
    def set_override(self):

        """
        If override is active, indicators are set to green, 
        push's status and changes background color
        """

        self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green"))
        self.pacmod_label.setText("Pacmod Status: Over-Ride")
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/overridewheel.png")))
        self.update()


    @QtCore.pyqtSlot(int)
    def set_accel_bar(self,data):

        """
        Sets acceleration percentage when pacmod game control is active
        """

        self.acceleration_bar.setProperty("value", data)

    @QtCore.pyqtSlot(int)
    def set_brake_bar(self,data):

        """
        Sets braking percentage when pacmod game control is active
        """

        self.braking_bar.setProperty("value", data)


if __name__ == "__main__":
    
    # init Qnode here 
    rospy.init_node(pyNode)
    joy_gui = JoyGui()
    joy_gui.subscribe()

    #Init application window
    app = QtGui.QApplication(sys.argv)
    #app.setStyle('motif')
    window = MyApp()
    sys.exit(app.exec_())