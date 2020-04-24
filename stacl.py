import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simple Notebook Example")
        self.set_border_width(3)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.notebook.set_scrollable(True)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label("Default Page!"))
        self.notebook.append_page(self.page1, Gtk.Label("Plain Title"))

        self.notebook.set_tab_detachable(self.page1, True)

        self.page2 = Gtk.Box()
        self.header = Gtk.HBox()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label("A page with an image for a Title."))
        self.header.pack_start(Gtk.Label("hello"), False, False, 0)
        self.notebook.append_page(
            self.page2, self.header
        )

        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label("A page with an image for a Title."))
        self.notebook.append_page(
            self.page3, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        )

        self.page4 = Gtk.Box()
        self.page4.set_border_width(10)
        self.page4.add(Gtk.Label("A page with an image for a Title."))
        self.notebook.append_page(
            self.page4, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        )

        self.page5 = Gtk.Box()
        self.page5.set_border_width(10)
        self.page5.add(Gtk.Label("A page with an image for a Title."))
        self.notebook.append_page(
            self.page5, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        )


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()