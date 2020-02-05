#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Standard lib
import os
import sys
import time

try:
    #Qt lib
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QObject
    from PyQt5.QtWidgets import QApplication, QAction

    #ROS lib
    import rospy
    # import std_msgs.msg, pacmod_msgs.msg
    from pacmod_msgs.msg import GlobalRpt, SystemRptFloat
    from std_msgs.msg import Float64, Bool

    #Main window
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
            _enable = msg.data # Set message for processing, if condition is met


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
        no braking = 0.0 and full braking = 1.0
        """
        global _veh_brake
        
        if _enable == True:
            _veh_brake = int(msg.output * _CONVERTER)
            #rospy.loginfo(rospy.get_name() + " Braking output: %f", (veh_brake))

    def subscribe(self):

        rospy.loginfo("Ready to publish... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(_PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.systemSub = rospy.Subscriber('/pacmod/as_tx/enabled',Bool,self.enabled_Check_CB, queue_size= 100)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',GlobalRpt,self.override_Check_CB, queue_size=100)
        self.throttleSub = rospy.Subscriber('/pacmod/parsed_tx/accel_rpt',SystemRptFloat,self.accel_Percent_CB,queue_size= 100)
        self.brakeSub = rospy.Subscriber('/pacmod/parsed_tx/brake_rpt',SystemRptFloat,self.brake_Percent_CB, queue_size= 100)


class MyThread(QThread):

    # Custom signals, keep as class level variable or they wont function properly
    accel_signal = pyqtSignal(int, name = "set_accel_bar")
    brake_signal = pyqtSignal(int, name = "set_brake_bar")
    enable_signal =pyqtSignal(bool, name = "set_enable")
    override_signal = pyqtSignal(bool, name = "set_override")
    timeout_signal = pyqtSignal(bool, name = "set_timeout")

    # Only QObjects can emit singals, and derives from QtCore
    def __init__(self):
        QThread.__init__(self)
        QObject.__init__(self)


    def run(self):

        # Overridden run method handles all main running logic
            while not rospy.is_shutdown():

                while (_enable == True) and (_override == False):
                    self.enable_signal.emit(_enable)
                    time.sleep(_PACMOD_RATE_IN_SEC)
                    self.accel_signal.emit(_veh_accel)
                    self.brake_signal.emit(_veh_brake)

                if (_enable == False) and (_override == False):
                    self.enable_signal.emit(_enable)
                    time.sleep(_PACMOD_RATE_IN_SEC)
                    self.accel_signal.emit(0)
                    time.sleep(_PACMOD_RATE_IN_SEC)
                    self.brake_signal.emit(0)
                    time.sleep(_PACMOD_RATE_IN_SEC)

    
                elif (_override == True) and (_enable == False):
                    self.enable_signal.emit(_enable)
                    self.override_signal.emit(_override)
                    time.sleep(_PACMOD_RATE_IN_SEC)
                    self.accel_signal.emit(0)
                    time.sleep(_PACMOD_RATE_IN_SEC)
                    self.brake_signal.emit(0)
                    time.sleep(_PACMOD_RATE_IN_SEC)

                elif (_override == True) and (_enable == True):
                    rospy.loginfo("ROS MSG ERROR")
                    break

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

        #QtAction, this connects the signal that triggers the closeEvent to shut down the application
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        
    #Signals and Slots go here
    @QtCore.pyqtSlot()
    def closeEvent(self,event):
        rospy.signal_shutdown("Window close event detected")
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
            ":/images/autonomouswheel(80).png"))

        elif (data == False) and (_override == False):
            self.pacmod_label.setStyleSheet("background-color: green; color: white")
            self.pacmod_label.setText("Ready")
            self.pac_wheel.setPixmap(QtGui.QPixmap(
            ":/images/overridewheel(80).png"))
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
        ":/images/overridewheel(80).png"))
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
        #,anonymous= False, log_level=rospy.INFO) #,disable_signals = False) 

        joy_gui = JoyGui()
        joy_gui.subscribe()

    except rospy.ROSInterruptException:
        rospy.logwarn("joy gui not initialized")

    #Init application window
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    window = MyApp()
    sys.exit(app.exec_())
