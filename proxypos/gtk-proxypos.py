#!/usr/bin/env python2

from proxypos import proxypos_core
from proxypos import  gtkgui
#For local testing comment avobe lines
#uncoment below
#import proxypos_core
#import gtkgui

if __name__ == "__main__":
    gtkgui.run(proxypos_core)
