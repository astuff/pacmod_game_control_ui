#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Standard Library
from __future__ import division
import sys
import threading
import time

# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk

#ROS node and library
import rospy
import pynode
import interface

class PipeLine(threading.Thread):
    """
    Working thread subclass.
    """
    def __init__(self, data=None):
        """
        Object constructor.
        """
        super(PipeLine, self).__init__()
        self.stop = False
        self.data = data
        self.enabled_PL = None
        self.override_PL = None
        self.timeout_PL = None

    def cancel(self):
        """
        Request for a cancelation of the executing task.
        """
        self.stop = True


    def run(self):
        pass

    # def payload(self):
    #     """
    #     This function do the heavy work.
    #     Please override on subclasses.
    #     This function can use self.stop to know if a cancel was requested, also
    #     it can use self.data for any data it needs. self.data is set in the
    #     constructor when creating the thread.
    #     """
    #     raise Exception('Please subclass and implement WorkingThread.payload()')

    def get_enable(self):
        
        if rospy.is_shutdown():
            return None
        else:
            self.data = self.enabled_PL
            return self.data

    def get_override(self):

        if rospy.is_shutdown():
            return None
        else:
            self.data = self.override_PL
            return self.data
    
    def get_timeout(self):

        if rospy.is_shutdown():
            return None
        else:
            self.data = self.timeout_PL
            return self.data

