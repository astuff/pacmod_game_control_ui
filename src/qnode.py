#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Library
import sys
import time
import threading
# ROS and MSG's
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from pacmod_msgs.msg import *

#import interface

pyNode = "joy_gui"

#Global constant
PACMOD_RATE = 30

# Helper variables for message frequency control
last_Enable = ''
last_Override = ''
last_Timeout = ''

MUTEX = threading.Lock()

class JoyGui(object):

    def __init__(self):

        self.which_run = "spin" # spin or while

        # Gui update variables
        self.enable = None
        self.override = None
        self.timeout = None


    def enabled_Check_CB(self, msg):
        """
        Checks if Pacmod is enabled and returns status
        """

        with MUTEX:

            # Checks for repetitive messages
            global last_Enable
            if msg.data != last_Enable:
                last_Enable = msg.data
                rospy.loginfo("I heard a NEW msg: PACMod Enabled = %s", msg.data)

                # Set message for processing
                self.enable = msg.data

    def override_Check_CB(self,msg):
        """
        Checks if driver has taken back control of vehicle
        """

        with MUTEX:


            # Checks for repetitive messages
            global last_Override
            if msg.override_active != last_Override:
                last_Override = msg.override_active
                rospy.loginfo("I heard a NEW msg: Override is %s", msg.override_active)

                # Set message for proccessing
                self.override = msg.override_active

    def timeout_Check_CB(self,msg):
        """
        Checks if the PACMod has timed out and become inactive
        """

        with MUTEX:

            # Checks for repetitive messages
            global last_Timeout
            if msg.user_can_timeout != last_Timeout:
                last_Timeout = msg.user_can_timeout
                rospy.loginfo("I heard a NEW msg: timeout is %s", msg.user_can_timeout)

                # Set message for processing
                self.timeout = msg.user_can_timeout

    def publishAndSubscribe(self):

        # Send module state to Log 
        rospy.loginfo("Now I'm in Pub/Sub... \n")

        # Set to match Pacmod rate
        self.rate = rospy.Rate(PACMOD_RATE) # 30 HZ

        # #ROS Subscriber values 
        self.systemSub = rospy.Subscriber('/pacmod/as_tx/enabled',std_msgs.msg.Bool,self.enabled_Check_CB, queue_size= 100)  
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.override_Check_CB, queue_size=10)
        self.sysOverRideSub = rospy.Subscriber('/pacmod/parsed_tx/global_rpt',pacmod_msgs.msg.GlobalRpt,self.timeout_Check_CB, queue_size=10)

    def run(self, which_run="spin"):
        """ Node runs using while statement.

            Default runs 'spin'

            "while" will register as a while loop
        """
        rospy.loginfo("Now I'm in Run... \n")
        if (self.which_run is "while"):
            while not rospy.is_shutdown():
                # --- add stuff here ---
                self.rate.sleep()
        else:
            rospy.loginfo("Now I'm in Run Spin... \n")
            rospy.spin()

if __name__ == "__main__":

    rospy.init_node(pyNode)
    joyGui = JoyGui()

    try:
        joyGui.publishAndSubscribe()
        joyGui.run("while")

    except rospy.ROSInterruptException:
        rospy.logwarn("JoyGui Error")
        