#!/usr/bin/env python
# -*- coding: utf-8 -*-

#STD lib
import os
import sys
import time

try:
    #Qt lib
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import  QObject, pyqtSignal
    from PyQt5.QtGui import QFont 
    from PyQt5.QtWidgets import QLabel, QApplication, QAction
    

    #ROS lib
    import rospy
    import std_msgs.msg, pacmod_msgs.msg
    from pacmod_msgs.msg import GlobalRpt, SystemRptFloat
    from std_msgs.msg import Float64, Bool

    #Main window
    from mythread import *
    from ui_mainwindow import *


except ImportError():
    rospy.loginfo("Module import error")

#Node name
_pyNode = "joy_gui"

_CONVERTER = 100
_PACMOD_RATE = 30
_PACMOD_RATE_IN_SEC = 0.33

_enable = False
_override = False
_veh_accel = 0.0
_veh_brake = 0.0

_last_Enable = ''
_last_Override = ''



class JoyGui(object):
    
    def enabled_Check_CB(self, msg):
        """
        Checks if Pacmod is enabled and returns status
        """

        global _last_Enable
        global _enable

        # Checks for repetitive messages
        if msg.data != _last_Enable:
            _last_Enable = msg.data
            rospy.loginfo("NEW msg: PACMod Enabled = %s", msg.data)
            _enable = msg.data # Set message for processing, if conditional is met


    def override_Check_CB(self,msg):
        """
        Checks if driver has overridden game controller
        """

        global _last_Override
        global _override

        # Checks for repetitive messages
        if msg.override_active != _last_Override:
            _last_Override = msg.override_active
            rospy.loginfo("NEW msg: Override = %s", msg.override_active)
            _override = msg.override_active

    def accel_Percent_CB(self, msg):
        """
        Retrieves throttle position as a float number signifying percent:
        fully closed = 0.0 and fully open = 1.0
        """
        global _veh_accel

        if _enable == True:
            _veh_accel = int(msg.output * _CONVERTER)
            #rospy.loginfo(rospy.get_name() + " Acceleration output: %f", (veh_accel)) # Sends info to log

    def brake_Percent_CB(self,msg):
        """
        Retrieves braking position as a float number signifying percent:
        no braking = 0.0 and fully braking = 1.0
        """
        global _veh_brake
        
        if _enable == True:
            _veh_brake = int(msg.output * _CONVERTER)
            #rospy.loginfo(rospy.get_name() + " Braking output: %f", (veh_brake))

    def subscribe(self):

        # Send module state to Log for troubleshooting
        rospy.loginfo("Ready to publish... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(_PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.systemSub = rospy.Subscriber('/pacmod/as_tx/enabled',std_msgs.msg.Bool,self.enabled_Check_CB, queue_size= 100)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.override_Check_CB, queue_size=100)
        self.throttleSub = rospy.Subscriber('/pacmod/parsed_tx/accel_rpt',pacmod_msgs.msg.SystemRptFloat,self.accel_Percent_CB,queue_size= 100)
        self.brakeSub = rospy.Subscriber('/pacmod/parsed_tx/brake_rpt',pacmod_msgs.msg.SystemRptFloat,self.brake_Percent_CB, queue_size= 100)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):

        # Initialize subclasses
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self,QtWidgets.QMainWindow)

        #Initialize/show UI
        self.setupUi(self)
        self.setStyleSheet("background-color: black")
        self.show()

        # Init thread and connect signals to slots to do work
        self.Thread = MyThread()
        self.Thread.enable_signal.connect(self.set_enable)
        self.Thread.override_signal.connect(self.set_override)
        self.Thread.accel_signal.connect(self.set_accel_bar)
        self.Thread.brake_signal.connect(self.set_brake_bar)
        self.Thread.start()

        #QtAction, triggers closeEvent to shut down application
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        
    #Signals and Slots here
    @QtCore.pyqtSlot()
    def closeEvent(self,event):
        #rospy.signal_shutdown("Window close event detected")
        self.Thread.exit()
        QtWidgets.QApplication.exit()
        
        self.destroy()
        
    @QtCore.pyqtSlot(bool)
    def set_enable(self, data):
        """
        if Pacmod enabled, Sets indicator to blue, 
        push's status and changes background color
        """

        if data == True:
            self.pacmod_label.setStyleSheet("background-color: rgb(98, 177, 246); color: white")
            self.pacmod_label.setText("Enabled")
            self.pac_wheel.setPixmap(QtGui.QPixmap(
            "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/autonomouswheel(80).png"))

        elif (data == False) and (_override == False):
            self.pacmod_label.setStyleSheet("background-color: green; color: white")
            self.pacmod_label.setText("Ready")
            self.pac_wheel.setPixmap(QtGui.QPixmap(
            "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png"))
        self.update()

    @QtCore.pyqtSlot(bool)
    def set_override(self,data):
        """
        If override is active, indicators are set to green, 
        push's status and changes background color
        """

        self.pacmod_label.setStyleSheet("background-color: green; color: white")
        self.pacmod_label.setText("Over-Ride")
        self.pac_wheel.setPixmap(QtGui.QPixmap(
        "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png"))
        self.update()

    @QtCore.pyqtSlot(int)
    def set_accel_bar(self,data):
        """
        Sets acceleration percentage when pacmod game control is enabled
        """

        self.acceleration_bar.setProperty("value", data)

    @QtCore.pyqtSlot(int)
    def set_brake_bar(self,data):
        """
        Sets braking percentage when pacmod game control is enabled
        """

        self.braking_bar.setProperty("value", data)

if __name__ == "__main__":

    try:
        # init Qnode here 
        rospy.init_node(_pyNode)
        #,anonymous= False, 
        #log_level=rospy.INFO,
        #disable_signals = False)

        joy_gui = JoyGui()
        joy_gui.subscribe()

    except rospy.ROSInterruptException:
        rospy.logwarn("joy gui Error")

    #Init application window
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle('cleanlooks')
    window = MyApp()
    sys.exit(app.exec_())