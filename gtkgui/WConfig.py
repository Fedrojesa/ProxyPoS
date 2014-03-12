import os
import gtk


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

class PrinterWidget(gtk.HBox):
    label = 'ESC/POS printer'
    def __init__(self):
        gtk.HBox.__init__(self)
        lblUrl = gtk.Label('url')
        self.entUrl = gtk.Entry()
        self.pack_start(lblUrl,0,0,5)
        self.pack_start(self.entUrl,0,0,5)

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

if __name__ == '__main__':
    w = WConfig('some_path')
    gtk.main()
