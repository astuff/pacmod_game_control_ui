#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division

# import threading
# import gi
# gi.require_version("Gtk","3.0")
# from gi.repository import Gtk, GObject


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


class LoadingWindow(object):
    """
    Show and handle a loading window.
    """

    def __init__(self, parent=None, label=None):
        """
        The object constructor.
        """

    def __init__(self):
        super(LoadingWindow,self,title="JoyStick Gui").__init__()
        self.init_ui()


    def __init__(self, parent=None, label=None):
        """
        Object constructor.
        """

        # Variables to hold Pynode data
        self.enabled = True
        self.timeout = None
        self.override = None
        self.workthread = None

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

        if parent is not None:
            self.wait.set_transient_for(parent)
        if label is not None:
            self.label.set_markup(label)

        # Connect signals
        builder.connect_signals(self)

    def show(self, pulses, workthread):
        """
        Show loading window.
        This needs to be called from Gtk main thread. Show the loading dialog
        just before starting the workthread.
        """
        if self.workthread is not None:
            print('There is a workthread active. Please call close() '
                  'or cancel() before starting a new loading event.')
            return False

        if workthread is not None:
            if not isinstance(workthread, WorkingThread):
                raise Exception(
                        'The thread needs to be a subclass of WorkingThread.'
                    )
            self.workthread = workthread

        self.pulses = max(pulses, 1)
        self._count = 0
        self.progress.set_fraction(0.0)
        self.progress.set_text('')
        self.wait.show()
        return False

    def pulse(self, text=None):
        """
        Pulse one step forward the progress bar.
        This can be called outside the Gtk main thread.
        """
        self._count += 1
        fraction = min(1.0, self._count / self.pulses)

        if text is None:
            text = '{0:0.1f}%'.format(fraction*100)

        GObject.idle_add(self.progress.set_fraction, fraction)
        GObject.idle_add(self.progress.set_text, text)

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
        sys.exit(0)

    def set_enabled(self,widget,data):
        """
        Push's messages to enaged status bar when Pacmod enabled, 
        defaults to pacmod disabled when pacmod is off
        """
        if self.enabled == True:
            self.engageStat.push(Gtk.Statusbar.get_context_id(self.engageStat," Status Message "), "Pacmod Enabled")
            self.pacmodEnable.set_from_file("/home/calib_fenoglio/Desktop/Blue_Steer_Icon/autonomouswheel.png")
            self.statusSet2 = False
            self.statusSet3 = False

        if self.enabled == False:
            self.pacmodEnable.set_from_file("/home/calib_fenoglio/sb_joy_glade/src/joy_glade/src/sw_512_128x128.png")
        
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
