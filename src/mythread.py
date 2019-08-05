#!/usr/bin/env python
import os
import sys
import time
import rospy

from ui_mainwindow import pyqtSignal, QObject, 
# from PyQt5 import QtCore
# from PyQt5.QtCore import  QObject, pyqtSignal, QThread
from game_controller_ui import _override, _enable, _veh_accel, _veh_brake, _PACMOD_RATE_IN_SEC, QThread

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
                    rospy.loginfo("ROS MSG ERROR, over-ride and enabled cannot both be True")
                    break