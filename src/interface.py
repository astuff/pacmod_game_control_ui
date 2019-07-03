#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import threading
import time

#ROS & Gtk libraries
import rospy
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GObject, Gdk

#Local modules
import pynode 
    
class MyWindow(GObject.GObject):

    def __init__(self, parent=None, label=None):
        """
        Object constructor.
        """

        # Node instance 
        self.joy = pynode.JoyGui(self)

        # Variables to hold Pynode data
        self.enabled = None
        self.timeout = None
        self.override = None

        # Loop helper Variables
        self.statusSet1 = False
        self.statusSet2 = False
        self.statusSet3 = False

        # Create Gui from XML 
        builder = Gtk.Builder()
        win_Show = Gtk.Window
        fileName = "/home/calib_fenoglio/pacmod_game_control_ui/src/pacmod_game_control_ui/src/Joy_enabled.glade"
        builder.add_from_file(fileName)

        # Get the main objects
        self.mainWin = builder.get_object("main_window")
        self.overStat = builder.get_object("override_status")
        self.engageStat = builder.get_object("engaged_status")
        self.timeoutStat = builder.get_object("timeout_status")
        self.pacmodEnable = builder.get_object("steering_indicator")
        win_Show.show_all(self.mainWin)


        # Get Id's 
        self.overStat_ID = self.overStat.get_context_id("overStatBar")
        self.engageStat_ID = self.engageStat.get_context_id("enableStatBar")
        self.timeoutStat_ID = self.timeoutStat.get_context_id("timeoutStatBar")

        # Configure objects
        self.overStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message"), "Null")
        self.engageStat.push(Gtk.Statusbar.get_context_id(self.engageStat," Status Message "), "Pacmod Disabled")
        self.timeoutStat.push(Gtk.Statusbar.get_context_id(self.timeoutStat, " Status Message "), "Null")

        # Connect signals
        builder.connect_signals(self)
        
    def gtk_main_quit(self, widget):
        """
        Quits Gtk Main loop, and ceases all processes when window closed
        """
        print("Gtk main_quit event triggered: program will now exit ")
        sys.exit(0)

    def set_enabled(self, widget, data):
        """
        Push's messages to enaged status bar when Pacmod enabled, 
        defaults to pacmod disabled when pacmod is off
        """
        if self.enabled == True:
            self.engageStat.push(self.engageStat.get_context_id("Statusbar"), "Pacmod Enabled")
            self.pacmodEnable.set_from_file("/home/calib_fenoglio/Desktop/Steer_Icon/autonomouswheel.png")

            self.statusSet2 = False
            self.statusSet3 = False

        if self.enabled == False:
            self.pacmodEnable.set_from_file("/home/calib_fenoglio/sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")
        
    def set_override(self, Widget, data):
        """
        Push's messages to override status bar when Pacmod enabled, defaults to NUll on start
        """
        if self.override == True:
            self.engageStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message "), " Pacmod Disabled")
            self.overStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message "), " Override Engaged")
            self.pacmodEnable.set_from_file("/home/calib_fenoglio/Desktop/Steer_Icon/steering-wheel-green.png")

            self.statusSet1 = False
            self.statusSet3 = False
        else:
            self.overStat.push(Gtk.Statusbar.get_context_id(self.overStat," Status Message"), "Null")
        
    def set_timeout(self, Widget, data):
        """
        Push's messages to timeout status bar when Pacmod enabled, 
        defaults NUll on start
        """
        if self.timeout == True:
            self.pacmodEnable.set_from_file("/home/calib_fenoglio/Desktop/Steer_Icon/steering-wheel-red.png")
            self.engageStat.push(Gtk.Statusbar.get_context_id(self.engageStat," Status Message "), "Pacmod Disabled")
            self.timeoutStat.push(Gtk.Statusbar.get_context_id(self.timeoutStat," Status Message "), "Pacmod Timed out")

            self.statusSet1 = False
            self.statusSet2 = False
        else:
            self.timeoutStat.push(Gtk.Statusbar.get_context_id(self.timeoutStat," Status Message "), "NULL")

    #Gtk.main_level() > 0

    def run(self):
        while not rospy.is_shutdown():
            if ((self.enabled is not None) and self.statusSet1 == False): 
                self.set_enabled(self.engageStat, self.enabled)
                self.statusSet1 = True
            elif ((self.override is not None) and self.statusSet2 == False):
                self.set_override(self.overStat,self.override)
                self.statusSet2 = True
            elif ((self.timeout is not None) and self.statusSet3 == False):
                self.set_timeout(self.timeoutStat, self.timeout)
                self.statusSet3 = True

if __name__ == "__main__":

    # Call once to initiate multiple threads, additional calls will terminate threads
    GObject.threads_init()
    
    #Opens application window
    win = MyWindow()

    thread = threading.Thread(target=win.run)
    thread.daemon = True
    thread.start()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # executor.submit(run, MyWindow)
    
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()

    #executor.submit(do_ros, MyWorkingThread)