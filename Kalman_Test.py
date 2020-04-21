import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np
class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="HeaderBar Demo")

        s = Gdk.Screen.get_default()
        height = s.get_height() / 1.2

        self.set_border_width(1)
        self.set_default_size(720, height)

        self.treeview = None
        self.store = Gtk.ListStore(str, int, int)

        self.vpaned = Gtk.VPaned()
        self.matplotlib_canvas = None

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Mimico"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        # create menubar
        menubar = self._create_menubar()

        # create a toolbar
        toolbar = self._create_toolbar()

        # create the main content
        main_content = self._create_main_content()

        # layout
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.pack_start(menubar, False, False, 0)
        self.layout.pack_start(toolbar, False, False, 0)
        self.layout.pack_start(main_content, True, True, 0)
        self.add(self.layout)

        self.connect('destroy', Gtk.main_quit)
        self.show_all()

    def _create_menubar(self):
        # menu item 'Bar'
        item_bar1 = Gtk.MenuItem.new_with_label('Import CSV')
        #item_bar1.connect('activate', self.on_menu)
        item_bar2 = Gtk.MenuItem.new_with_label('Exit')
        #item_bar2.connect('activate', self.on_menu)
        item_bar3 = Gtk.MenuItem.new_with_label('Exit')
        #item_bar3.connect('activate', self.on_menu)
        # sub menu for 'Bar'
        menu_foo = Gtk.Menu.new()
        menu_foo.append(item_bar1)
        menu_foo.append(item_bar2)
        menu_foo.append(item_bar3)
        # main menu 'Foo' with attached sub menu
        item_foo = Gtk.MenuItem.new_with_label('File')
        item_foo.set_submenu(menu_foo)
        # the menubar itself
        menubar = Gtk.MenuBar.new()
        menubar.append(item_foo)
        return menubar

    def _create_toolbar(self):
        toolbar = Gtk.Toolbar.new()
        # button with label
        #bar_item = Gtk.ToolButton.new(None, 'Bar')
        #bar_item.connect('clicked', self.on_menu)
        #toolbar.insert(bar_item, -1)
        # button with icon

        pb_import = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_filesel.png')
        pb_export = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_export.png')
        pb_record = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_render_animation.png')
        pb_stop_record = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_rec.png')

        boc = Gtk.Box()
        lb = Gtk.Label("Import")
        ico = Gtk.Image()
        ico.set_from_pixbuf(pb_import)
        boc.add(ico)
        boc.add(lb)

        bar_item = Gtk.ToolButton.new()
        bar_item.set_name('IMPORT')
        bar_item.set_icon_widget(boc)
        bar_item.set_tooltip_text("Import CSV file")
        bar_item.connect('clicked', self.on_file_clicked)
        toolbar.insert(bar_item, -1)

        boc = Gtk.Box()
        lb = Gtk.Label("Export")
        ico = Gtk.Image()
        ico.set_from_pixbuf(pb_export)
        boc.add(ico)
        boc.add(lb)

        bar_item = Gtk.ToolButton.new()
        bar_item.set_icon_widget(boc)
        bar_item.set_tooltip_text("Export As...")
        bar_item.connect('clicked', self.on_file_clicked)
        toolbar.insert(bar_item, -1)
        separator = Gtk.SeparatorToolItem()
        toolbar.insert(separator, -1)

        boc = Gtk.Box()
        ico = Gtk.Image()
        ico.set_from_pixbuf(pb_record)
        boc.add(ico)

        bar_item = Gtk.ToolButton.new()
        bar_item.set_icon_widget(boc)
        bar_item.set_tooltip_text("Start capturing Mimico animation")
        bar_item.connect('clicked', self.on_file_clicked)
        toolbar.insert(bar_item, -1)
        separator = Gtk.SeparatorToolItem()

        boc = Gtk.Box()
        ico = Gtk.Image()
        ico.set_from_pixbuf(pb_stop_record)
        boc.add(ico)

        bar_item = Gtk.ToolButton.new()
        bar_item.set_sensitive(False)
        bar_item.set_icon_widget(boc)
        bar_item.set_tooltip_text("Stop current animation")
        bar_item.connect('clicked', self.on_file_clicked)
        toolbar.insert(bar_item, -1)
        return toolbar

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "Please choose a file",
            self,
            Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            ),
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            self.add_csv(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV files")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "Please choose a folder",
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK),
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_csv(self, csv_file):
        self.store.append([csv_file, 1, 20])

    def _create_main_content(self):
        ###################################################################
        ##### LISTBOX WITH CSV INFO
        ###################################################################
        # creating the treeview, making it use the filter as a model, and adding the columns
        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.treeview = Gtk.TreeView(self.store)
        self.treeview.connect('cursor-changed', self.selection_changed)

        for i, column_title in enumerate(
                ["File", "Number of Samples", "Estimated Duration (s)"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

        ###################################################################
        ##### MATPLOTLIB CODE
        ###################################################################
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        a.plot(t, s)

        canvas = FigureCanvas(f)  # a Gtk.DrawingArea

        self.vpaned.set_wide_handle(True)
        self.vpaned.set_position(250)
        self.vpaned.pack1(self.grid, False, False)
        self.vpaned.pack2(canvas, True, True)

        return self.vpaned


    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
                self.current_filter_language is None
                or self.current_filter_language == "None"
        ):
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def selection_changed(self, treeview):
        (model, iter) = treeview.get_selection().get_selected()
        self.plot_csv(model[iter][0])

    def plot_csv(self, csv_file):
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        a.plot(t, s, color='gold')

        canvas = FigureCanvas(f)  # a Gtk.DrawingArea
        self.vpaned.pack2(None, True, True)
        self.queue_draw()


win = HeaderBarWindow()
win.set_position(Gtk.WindowPosition.CENTER)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
