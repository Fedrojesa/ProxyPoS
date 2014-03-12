import os
import gtk
import ConfigParser
from os.path import expanduser

class GeneralWidget(gtk.HBox):
    label = 'General'
    def __init__(self,config):
        gtk.HBox.__init__(self)
        lblUrl = gtk.Label('url')
        self.entUrl = gtk.Entry()
        self.entUrl.set_text(config.get('General','host'))
        self.pack_start(lblUrl,0,0,5)
        self.pack_start(self.entUrl,0,0,5)
        lblPort = gtk.Label('Port')
        self.entPort = gtk.Entry()
        self.entPort.set_text(config.get('General','port'))
        self.pack_start(lblPort,0,0,5)
        self.pack_start(self.entPort,0,0,5)

class PrinterWidget(gtk.VBox):
    label = 'ESC/POS printer'
    ptype = {'USB':'USB (idVendor:idProduct)',
             'Network':'URL (192.168.1.2)',
             'Serial': 'Serial (/dev/ttyS0)'
            }
    current_type = 'USB'

    def __init__(self,config):

        self.current_type = config.get('Printer','type')
        gtk.VBox.__init__(self)
        PrinterTypeBox = gtk.VBox()
        button = gtk.RadioButton(None,"USB")
        button.connect('toggled',self.toggled,'USB')
        if self.current_type == 'USB':
            button.set_active(True)

        PrinterTypeBox.pack_start(button,0,0,5)
        button = gtk.RadioButton(button,"Netowrk")
        button.connect('toggled',self.toggled,'Network')
        if self.current_type == 'Network':
            button.set_active(True)

        PrinterTypeBox.pack_start(button,0,0,5)
        button = gtk.RadioButton(button,"Serial")
        button.connect('toggled',self.toggled,'Serial') 
        PrinterTypeBox.pack_start(button,0,0,5)
        if self.current_type == 'Serial':
            button.set_active(True)

        self.pack_start(PrinterTypeBox,0,0,5)

        PrinterConfigBox = gtk.HBox()
        self.lblTypeConfig = gtk.Label(self.ptype[self.current_type])
        self.entTypeConfig = gtk.Entry()
        PrinterConfigBox.pack_start(self.lblTypeConfig,0,0,5)
        PrinterConfigBox.pack_start(self.entTypeConfig,0,0,5)
        self.pack_start(PrinterConfigBox,0,0,5)

    def toggled(self,widget, data=None):
        if widget.get_active() == True:
            current_type = data
            self.lblTypeConfig.set_label(self.ptype[data])

pages ={ 'General': GeneralWidget,
         'Printer': PrinterWidget,
       }

class WConfig(gtk.Window):
    widgets = {}
    config_path = expanduser("~") +"/.proxypos/config"
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_default_size(200,200)
        notebook = gtk.Notebook()
        
        #Read current configuration
        config = ConfigParser.RawConfigParser()
        config.read(self.config_path +"/config.cfg")

        for page in ['General','Printer']:
            widget = pages[page](config)
            label = gtk.Label(widget.label)
            self.widgets[page] = widget
            notebook.append_page(widget,label)

        self.connect('destroy', lambda w: gtk.main_quit())

        self.add(notebook)
        self.show_all()

    def save(self, widget):
        pass

    def cancel(self, widget):
        pass

def run():
    w = WConfig()
    gtk.main()

if __name__ == '__main__':
    w = WConfig('some_path')
    gtk.main()
