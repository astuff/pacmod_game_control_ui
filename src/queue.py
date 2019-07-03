from __future__ import division
import Queue
import threading
from threading import Thread, Lock
import time 
import sys

MUTEX = Lock()

class MyQueue(threading.Thread):
    def __init__(self, data = None ,  group = None, target = None, name = None, args = (), kwargs = (), verbose = None):
        
        super(MyThread, self).__init__(group = group, target = target, name = name, verbose = verbose)
        self.args = args
        self.kwargs = kwargs
        self.data = data

    def run(self):
        """
        Override threading.Thread dummy run().
        """
        self.payload()
        pass

    def payload(self):
        """
        This function do the heavy work.
        Please override on subclasses.
        This function can use self.stop to know if a cancel was requested, 
        also it can use self.data for any data it needs. 
        self.data is set in the constructor when creating the thread.
        """
        raise Exception('Please subclass and implement WorkingThread.payload()')

    def cancel(self):
        """
        Request for a cancelation of the executing task.
        """
        self.stop = True



