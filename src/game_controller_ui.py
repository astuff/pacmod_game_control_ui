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

class MyThread(QtCore.QThread):

    # Custom signals, keep as class level variable or they wont function properly
    accel_signal = pyqtSignal(int, name = "set_accel_bar")
    brake_signal = pyqtSignal(int, name = "set_brake_bar")
    enable_signal =pyqtSignal(bool, name = "set_enable")
    override_signal = pyqtSignal(bool, name = "set_override")
    timeout_signal = pyqtSignal(bool, name = "set_timeout")

    # Only QObjects can emit singals, and derives from QtCore
    def __init__(self):
        QtCore.QThread.__init__(self)
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
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: rgb(98, 177, 246); color: white"))
            self.pacmod_label.setText("Enabled")
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8(
            "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/autonomouswheel(80).png")))

        elif (data == False) and (_override == False):
            self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green; color: white"))
            self.pacmod_label.setText("Ready")
            self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8(
            "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png")))
        self.update()


    @QtCore.pyqtSlot(bool)
    def set_override(self,data):
        """
        If override is active, indicators are set to green, 
        push's status and changes background color
        """

        self.pacmod_label.setStyleSheet(_fromUtf8("background-color: green; color: white"))
        self.pacmod_label.setText("Over-Ride")
        self.pac_wheel.setPixmap(QtGui.QPixmap(_fromUtf8(
        "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/autonomy_images/overridewheel(80).png")))
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
        # 
        #anonymous= False, 
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
