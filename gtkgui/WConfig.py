import os
import gtk
import ConfigParser
from os.path import expanduser

class GeneralWidget(gtk.HBox):
    label = 'General'
    def __init__(self):
        gtk.HBox.__init__(self)
        lblUrl = gtk.Label('url')
        self.entUrl = gtk.Entry()
        self.pack_start(lblUrl,0,0,5)
        self.pack_start(self.entUrl,0,0,5)
        lblPort = gtk.Label('Port')
        self.entPort = gtk.Entry()
        self.pack_start(lblPort,0,0,5)
        self.pack_start(self.entPort,0,0,5)

class PrinterWidget(gtk.VBox):
    label = 'ESC/POS printer'
    ptype = {'USB':'USB (idVendor:idDevice)',
             'Network':'URL (192.168.1.2)',
             'Serial': 'Serial (/dev/ttyS0)'
            }
    current_type = 'USB'

    def __init__(self,default_type = None):
        #TODO: 
        if default_type != None:
            self.current_type = default_type

        gtk.VBox.__init__(self)
        PrinterTypeBox = gtk.VBox()
        button = gtk.RadioButton(None,"USB")
        button.connect('toggled',self.toggled,'USB')
        PrinterTypeBox.pack_start(button,0,0,5)
        button = gtk.RadioButton(button,"Netowrk")
        button.connect('toggled',self.toggled,'Network')
        PrinterTypeBox.pack_start(button,0,0,5)
        button = gtk.RadioButton(button,"Serial")
        button.connect('toggled',self.toggled,'Serial')
        PrinterTypeBox.pack_start(button,0,0,5)
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
    def __init__(self,config_path):
        gtk.Window.__init__(self)
        self.set_default_size(200,200)
        notebook = gtk.Notebook()

        for page in ['General','Printer']:
            widget = pages[page]()
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

def run(handler):
    w = WConfig('some_path')
    gtk.main()

if __name__ == '__main__':
    w = WConfig('some_path')
    gtk.main()
