#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#import sys
import time

try:

    from PyQt4 import QtCore, QtGui
    from PyQt4.QtCore import SIGNAL, SLOT, QObject, pyqtSignal, pyqtSlot
    from PyQt4.QtGui import QLabel, QApplication

    import rospy
    from std_msgs.msg import *
    from pacmod_msgs.msg import *
    from ui_mainwindow import *

except ImportError():
    rospy.loginfo("Module import error")

_fromUtf8 = QtCore.QString.fromUtf8

#Node name
pyNode = "joy_gui"

#Global constant
_CONVERTER = 100
_PACMOD_RATE = 30
_PACMOD_RATE_IN_SEC = 0.33

# Controls for ROS MSG'S
_enable = False
_override = False
_veh_accel = 0.0
_veh_brake = 0.0

# Helper variables, Controls message frequency 
_last_Enable = ''
_last_Override = ''

class JoyGui(object):
    
    def enabled_Check_CB(self, msg):
        """
        Checks if Pacmod is enabled and returns status
        """

        #Globals for GUI
        global _last_Enable
        global _enable

        # Checks for repetitive messages
        if msg.data != _last_Enable:
            _last_Enable = msg.data
            rospy.loginfo("NEW msg: PACMod Enabled = %s", msg.data)
            _enable = msg.data # Set message for processing


    def override_Check_CB(self,msg):
        """
        Checks if driver has taken back control of vehicle
        """
        # Globals for GUI
        global _last_Override
        global _override

        # Checks for repetitive messages
        if msg.override_active != _last_Override:
            _last_Override = msg.override_active
            rospy.loginfo("NEW msg: Override = %s", msg.override_active)
            _override = msg.override_active # Set message for proccessing

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
            _veh_brake = int(msg.output * _CONVERTER )
            #rospy.loginfo(rospy.get_name() + " Braking output: %f", (veh_brake)) # Sends info to log

    def subscribe(self):

        # Send module state to Log for troubleshooting
        rospy.loginfo("Ready to publish... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(_PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.enabled_sub = rospy.Subscriber('/pacmod/as_tx/enabled',std_msgs.msg.Bool,self.enabled_Check_CB, queue_size= 100)
        self.override_sub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.override_Check_CB, queue_size=100)
        self.throttle_sub = rospy.Subscriber('/pacmod/parsed_tx/accel_rpt',pacmod_msgs.msg.SystemRptFloat,self.accel_Percent_CB,queue_size= 100)
        self.brake_sub = rospy.Subscriber('/pacmod/parsed_tx/brake_rpt',pacmod_msgs.msg.SystemRptFloat,self.brake_Percent_CB, queue_size= 100)

class MyThread(QtCore.QThread):

    # Custom signals, keep as class level variable or they wont function properly
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
                    print ("Something went wrong...")
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
        self.setStyleSheet("background-color: black")
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
        
        self.Thread.exit()
        QtGui.QApplication.exit()
        
        self.destroy()
        
    @QtCore.pyqtSlot(bool)
    def set_enable(self, data):

        """
        if Pacmod enabled, Sets indicator to blue, 
        push's status and changes background color
        """

        if data == True:
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(98, 177, 246); color: white"))
            self.pacmod_label.setText("Enabled")
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/demo/standard_ws/src/pacmod_game_control_ui/autonomy_images/autonomouswheel(80).png")))

        elif data == False and (_override == False):
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green; color: white"))
            self.pacmod_label.setText("Ready")
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/demo/standard_ws/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png")))
        self.update()


    @QtCore.pyqtSlot(bool)
    def set_override(self):

        """
        If override is active, indicators are set to green, 
        push's status and changes background color
        """

        self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green; color: white"))
        self.pacmod_label.setText("Over-Ride")
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8("/home/demo/standard_ws/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png")))
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
    try:
        # init Qnode here 
        rospy.init_node(pyNode)
        joy_gui = JoyGui()
        joy_gui.subscribe()
    except rospy.ROSInterruptException:
        rospy.logwarn("joy_gui node error")
    
    #Init application window
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    window = MyApp()
    sys.exit(app.exec_())
