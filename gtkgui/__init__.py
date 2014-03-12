#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gtk
import multiprocessing
import signal
import ConfigParser
import io
from os.path import expanduser
import WConfig

default_config = """[General]
host = localhost
port = 8069
[Printer]
type = USB
idVendor = 0x0416
idDevice = 0x5011
host = 192.168.1.2
dev = /dev/ttyS0
WidthA = 44
widthB = 34
pxWidth = 206
charSet = \\x1b\\x52\\x12
"""

class SystrayIconApp:
    proxypos_process = None
    server = None
    server_label = 'Start'
    def __init__(self,handler):
        #Check for config file
        config_path = expanduser("~") +"/.proxypos/config"
        if not os.path.exists(config_path):
            os.makedirs(config_path)
            configfile = open(config_path+'/config.cfg','wb')
            configfile.write(default_config)
            configfile.close()

        self.server = handler.Server()
        self.tray = gtk.StatusIcon()
        self.tray.set_from_stock(gtk.STOCK_ABOUT)
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.set_tooltip(('ProxyPoS configurator'))

    def on_right_click(self, widget, event_type,event_time):
        self.make_menu(widget, event_type, event_time)

    def make_menu(self, widget,event_type, event_time):
        menu = gtk.Menu()

        self.start = gtk.MenuItem(self.server_label)
        self.start.show()
        menu.append(self.start)
        self.start.connect('activate',self.start_stop_server)

        config = gtk.MenuItem('Configure')
        config.show()
        menu.append(config)
        config.connect('activate',self.configure_form)
        
        config = gtk.MenuItem('Reprint ticket')
        config.show()
        menu.append(config)
        config.connect('activate',self.reprint_ticket)

        about = gtk.MenuItem('About')
        about.show()
        menu.append(about)
        about.connect('activate',self.show_about_dialog)

        quit = gtk.MenuItem('Quit')
        quit.show()
        menu.append(quit)
        quit.connect('activate', self.quit)
        menu.popup(None, None, gtk.status_icon_position_menu, event_type, event_time)

    def quit(self, widget):
        if self.proxypos_process != None:
            if self.proxypos_process.is_alive():
                self.proxypos_process.terminate()
        gtk.main_quit()

    def start_stop_server(self,widget):
        if self.server_label == 'Start':
            self.proxypos_process = multiprocessing.Process(target=self.server.run)
            self.proxypos_process.start()
            self.server_label = 'Stop'
        elif self.server_label == 'Stop':
            self.proxypos_process.terminate()
            self.server_label = 'Start'

    def configure_form(self,widget):
        WConfig.run()

    def reprint_ticket(self,widget):
        pass

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
	about_dialog.set_destroy_with_parent (True)
	about_dialog.set_icon_name ("SystrayIcon")
	about_dialog.set_name('ProxyPoS GUI')
	about_dialog.set_version('0.1')
	about_dialog.set_copyright("(C) 2014 Alejandro Armagnac")
	about_dialog.set_comments(("GUI for ProxyPoS to configure\nyour ESC/POS printer to be used in\nOpenERP"))
	about_dialog.set_authors(['Alejandro Armagnac <aarmagnac@yahoo.com.mx>'])
	about_dialog.run()
	about_dialog.destroy()

def run(handler):
    SystrayIconApp(handler)
    gtk.main()
