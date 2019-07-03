#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
import rospy
import sys
import threading
import time
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GObject
import pynode


class WorkingThread(threading.Thread):
    """
    Working thread subclass.
    """
    def __init__(self, data=None):
        """
        Object constructor.
        """
        super(WorkingThread, self).__init__()
        self.stop = False
        self.data = data

    def cancel(self):
        """
        Request for a cancelation of the executing task.
        """
        self.stop = True

    def run(self):
        """
        Override threading.Thread dummy run().
        """
        self.payload()

    def payload(self):
        """
        This function do the heavy work.
        Please override on subclasses.
        This function can use self.stop to know if a cancel was requested, also
        it can use self.data for any data it needs. self.data is set in the
        constructor when creating the thread.
        """
        raise Exception('Please subclass and implement WorkingThread.payload()')


class LoadingWindow(Gtk.Window):
    """
    Show and handle a loading window.
    """

    def __init__(self, parent=None, label=None):
        """
        The object constructor.
        """

        # Variables to hold Pynode data
        self.enabled = True
        self.timeout = None
        self.override = None

        # Loop helper Variables
        self.statusSet1 = False
        self.statusSet2 = False
        self.statusSet3 = False

        # Create Gui from XML 
        builder = Gtk.Builder()
        win_Show = Gtk.Window
        fileName = "/home/calib_fenoglio/enabled/src/joy_enabled/src/Joy_enabled.glade"
        builder.add_from_file(fileName)

        # Get the main objects
        self.mainWin = builder.get_object("main_window")
        self.overStat = builder.get_object("override_status")
        self.engageStat = builder.get_object("engaged_status")
        self.timeoutStat =builder.get_object("timeout_status")
        self.pacmodEnable = builder.get_object("steering_indicator")
        win_Show.show_all(self.mainWin)

        # Configure objects
        self.overStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message"), "Null")
        self.engageStat.push(Gtk.Statusbar.get_context_id(self.engageStat," Status Message "), "Pacmod Disabled")
        self.timeoutStat.push(Gtk.Statusbar.get_context_id(self.timeoutStat, " Status Message "), "Null")

        # Connect signals
        builder.connect_signals(self)

    def close(self):
        """
        Close the loading window.
        This should be called when the workthread has finished it's work.
        This can be called outside the Gtk main thread.
        """
        self.workthread = None
        GObject.idle_add(self.wait.hide)

    def cancel(self, widget=None):
        """
        Close the loading window.
        This should be called when the workthread has finished it's work.
        This can be called outside the Gtk main thread.
        """
        if self.workthread is not None:
            self.workthread.cancel()
            self.close()

    def gtk_main_quit(self, widget):
        """
        Quits Gtk Main loop, and ceases all processes when window closed
        """
        print("Gtk main_quit event triggered: program will now exit ")
        #sys.exit(0)
        Gtk.main_quit()

    def set_enabled(self,widget,data):
        """
        Push's messages to enaged status bar when Pacmod enabled, 
        defaults to pacmod disabled when pacmod is off
        """
        if self.enabled == True:
            GObject.idle_add(self.engageStat.push(Gtk.Statusbar.get_context_id(self.engageStat," Status Message "), "Pacmod Enabled"))
            GObject.idle_add(self.pacmodEnable.set_from_file("/home/calib_fenoglio/Desktop/Blue_Steer_Icon/autonomouswheel.png"))
            self.statusSet2 = False
            self.statusSet3 = False

        if self.enabled == False:
            GObject.idle_add(self.pacmodEnable.set_from_file("/home/calib_fenoglio/sb_joy_glade/src/joy_glade/src/sw_512_128x128.png"))
        
    def set_override(self, Widget, data):
        """
        Push's messages to override status bar when Pacmod enabled, defaults to NUll when pacmod disabled
        """
        if self.override == True:
            self.engageStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message "), " Override Engaged")
            self.statusSet1 = False
            self.statusSet3 = False
        else:
            self.overStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message"), "Null")
        
    def set_timeout(self, Widget, data):
        """
        Push's messages to timeout status bar when Pacmod enabled, 
        defaults NUll when pacmod disabled
        """
        if self.timeout == True:
            self.engageStat.push(Gtk.Statusbar.get_context_id(self.timeoutStat," Status Message "), "Pacmod Timed out")
            self.statusSet1 = False
            self.statusSet2 = False
        else:
            self.engageStat.push(Gtk.Statusbar.get_context_id(self.timeoutStat," Status Message "), "NULL")


class MyWorkingThread(WorkingThread):

    def payload(self):
        lW = LoadingWindow()

        while not rospy.is_shutdown():
            # Push status messages While node is running
            if ((lW.enabled is not None) and lW.statusSet1 == False): 
                #self.engageStat.emit("set_enabled", self.enabled)
                lW.set_enabled(lW.engageStat,lW.enabled)
                lW.statusSet1 = True
            elif ((self.override is not None) and self.statusSet2 == False):
                #self.overStat.emit("set_override", self.override)
                self.set_override(self.overStat,self.override)
                self.statusSet2 = True
            elif ((self.timeout is not None) and self.statusSet3 == False):
                #self.timeoutStat.emit("set_timeout", self.timeout)
                self.set_timeout(self.timeoutStat, self.timeout)
                self.statusSet3 = True

if __name__ == '__main__':
    GObject.threads_init()

    window = LoadingWindow()

    def _launch_work(widget):
        workthread = MyWorkingThread(window)
        workthread.start()

    _launch_work
    #window.show_all()
    Gtk.main()