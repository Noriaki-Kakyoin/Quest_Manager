import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import re

class Data(object):
    def __init__(self):
        self.label_selected_file = Gtk.Label()

        self.mission_name = ""
        self.selected_world = "Asgard"
        self.form_mission_name = ""
        self.assistant = Gtk.Assistant()
        self.label_real_mission_name = Gtk.Label()
        self.label_real_mission_name.set_sensitive(False)
        self.label_real_mission_name.set_halign(Gtk.Align.END)
        self.mission_name_entry = Gtk.Entry()
        self.mission_name_entry.set_placeholder_text("Nombre de la mision")
        self.mission_name_entry.set_max_length(50)
        self.mission_name_entry.connect('changed', self.on_entry_changed)
        
        self.assistant.connect('cancel', self.on_close_cancel)
        self.assistant.connect('close', self.on_close_cancel)
        self.assistant.connect('apply', self.on_apply)
        self.assistant.connect('prepare', self.on_prepare)

    @mission_name.setter
    def mission_name(self, text):
        self.mission_name = text
        
    @property
    def mission_name(self):
        return self.mission_name
        
        
    def on_close_cancel(self, assistant):
        assistant.destroy()
        Gtk.main_quit()

    def on_apply(self, assistant):
        # apply changes here; this is a fictional example so just do
        # nothing here
        pass

    def on_prepare(self, assistant, page):
        current_page = assistant.get_current_page()
        n_pages = assistant.get_n_pages()
        title = 'Sample assistant (%d of %d)' % (current_page + 1, n_pages)
        assistant.set_title(title)
        
    def on_entry_changed(self, widget):
        page_number = self.assistant.get_current_page()
        current_page = self.assistant.get_nth_page(page_number)
        text = self.mission_name_entry.get_text()
        self.meep(text)
        text = re.sub(' ', '_', text) 
        text = re.sub(r'[^\w]', '', text)
        form_mission_name = text
        
        if self.get():
            self.assistant.set_page_complete(current_page, True)
            self.label_real_mission_name.set_markup("<span style='italic'>M_{:03d}_<b>{}-{}</b></span>".format(1, selected_world, self.get()))
            self.label_real_mission_name.show()
        else:
            self.assistant.set_page_complete(current_page, False)
            self.label_real_mission_name.hide()
    
def do_assistant():
    dat = Data()
    
    dat.assistant.set_default_size(-1, 300)
    
    dat.label_selected_file.connect("activate-link", activate_link)
    
    create_page1(dat)
    create_page2(dat)
    create_page3(dat)

    dat.assistant.show()
        
def on_toggle_changed(widget, data):
    page_number = data.assistant.get_current_page()
    current_page = data.assistant.get_nth_page(page_number)
    status = widget.get_active()

    if status:
        data.assistant.set_page_complete(current_page, True)
    else:
        data.assistant.set_page_complete(current_page, False)
        
def activate_link(label, uri):
    if uri == 'keynav':
        label_selected_file.hide()
        label_selected_file.set_text("")

def create_page1(data):
    box = Gtk.Box()
    box.set_border_width(12)
    box.set_homogeneous(False)
    box.set_baseline_position(Gtk.BaselinePosition(0))
    
    btn_mission_selec = Gtk.ToggleButton()
    btn_mission_selec.connect('toggled', on_toggle_changed, data)
    img_mission = Gtk.Image()
    pb_text = Pixbuf.new_from_file(
        'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon32_text.png')

    lb = Gtk.Label("Quest")
    ico = Gtk.Image()
    ico.set_from_pixbuf(pb_text)
    btn_mission_selec.set_image(ico)
    btn_mission_selec.set_image_position(Gtk.PositionType(2))
    btn_mission_selec.set_label("Quest")
    btn_mission_selec.set_always_show_image(True)
 
    grid = Gtk.Grid()

    grid.attach(btn_mission_selec, 1, 2, 1, 1)

    box.add(grid)
    #box.set_child_packing(btn_mission_selec, False, False, 0, Gtk.PackType(0))
    #entry.connect('changed', on_entry_changed)

    box.show_all()
    data.assistant.append_page(box)
    data.assistant.set_page_title(box, 'Seleccionar tipo de proyecto')
    data.assistant.set_page_type(box, Gtk.AssistantPageType.INTRO)

    pixbuf = data.assistant.render_icon(Gtk.STOCK_DIALOG_INFO,
                                        Gtk.IconSize.DIALOG,
                                        None)

    data.assistant.set_page_header_image(box, pixbuf)

def create_page2(data):
    box = Gtk.VBox(homogeneous=False,
                   spacing=12)
    box.set_border_width(12)
    
    box_filechooser = Gtk.HBox()
    box_filechooser.set_spacing(60)
    
    box_worldchooser = Gtk.HBox()
    box_worldchooser.set_spacing(180)
    
    button_selec_file = Gtk.Button("Seleccionar Archivo")
    button_selec_file.connect("clicked", on_file_clicked)
    
    box_btn_files = Gtk.HBox()
    box_btn_files.pack_start(button_selec_file, False, False, 5)
    
    av = Gtk.Label()
    av.set_markup("(Opcional) Quest Anterior <span style='italic'>(*.msn)</span>")
    
    box_filechooser.pack_start(av, False, True, 0)
    box_filechooser.pack_end(box_btn_files, True, False, 0)
    
    world_store = Gtk.ListStore(str)
    worlds = [
        "Asgård",
        "Midgård",
        "Helheim",
        "Vieja Persia"
    ]
    for world in worlds:
        world_store.append([world])

    world_combo = Gtk.ComboBox.new_with_model(world_store)
    world_combo.connect("changed", on_combo_changed, data.mission_name_entry, data.label_real_mission_name)
    renderer_text = Gtk.CellRendererText()
    world_combo.pack_start(renderer_text, True)
    world_combo.add_attribute(renderer_text, "text", 0)
    world_combo.set_active(0)
    
    box_worldchooser.pack_start(Gtk.Label("Seleccionar Mundo"), False, True, 0)
    box_worldchooser.pack_start(world_combo, False, False, 5)
    
    box_label_file = Gtk.HBox()
    box_label_file.set_halign(Gtk.Align.END)
    box_label_file.pack_start(data.label_selected_file, False, False, 0)
    
    box.pack_start(data.mission_name_entry, False, False, 0)
    box.pack_start(data.label_real_mission_name, False, False, 0)
    box.pack_start(box_filechooser, False, False, 5)
    box.pack_start(box_label_file, False, False, 5)
    box.pack_start(box_worldchooser, False, False, 5)

    box.show_all()
    
    data.label_real_mission_name.hide()
    data.label_selected_file.hide()
    

    data.assistant.append_page(box)
    data.assistant.set_page_complete(box, False)
    data.assistant.set_page_title(box, 'Setup')
    data.assistant.set_page_type(box, Gtk.AssistantPageType.CONTENT)

    pixbuf = data.assistant.render_icon(Gtk.STOCK_DIALOG_INFO,
                                        Gtk.IconSize.DIALOG,
                                        None)
    data.assistant.set_page_header_image(box, pixbuf)
   

def create_page3(data):
    box = Gtk.VBox(homogeneous=False,
                   spacing=12)
    box.set_border_width(0)
    
    label = Gtk.Label(mission_name)
    
    textview = Gtk.TextView()
    textview.set_border_window_size(Gtk.TextWindowType.TEXT, 2)
    buffer = textview.get_buffer()
    
    print(data.mission_name_entry.get_text())
    print(data.get())
    
    markup = "<span>NOMBRE MISION   = <b>{}</b></span>".format(data.mission_name_entry.get_text())
    
    buffer.insert_markup(buffer.get_end_iter(), markup, -1)
    
    box.pack_start(label, False, False, 0)
    box.pack_start(textview, False, False, 0)
    box.show_all()
    
    data.assistant.append_page(box)
    data.assistant.set_page_complete(box, True)
    data.assistant.set_page_title(box, 'Confirmacion')
    data.assistant.set_page_type(box, Gtk.AssistantPageType.CONFIRM)

    pixbuf = data.assistant.render_icon(Gtk.STOCK_DIALOG_INFO,
                                        Gtk.IconSize.DIALOG,
                                        None)
    data.assistant.set_page_header_image(box, pixbuf)

def on_combo_changed(combo, widget, widgetd):
    global selected_world
    tree_iter = combo.get_active_iter()
    if tree_iter is not None:
        model = combo.get_model()
        name = model[tree_iter][:2][0]
        name = re.sub('å', 'a', name) 
        name = re.sub(' ', '', name) 
        selected_world = name
    else:
        text = widget.get_text()
        text = re.sub(' ', '_', text) 
        text = re.sub(r'[^\w]', '', text)
        form_mission_name = text
        
        selected_world = entry.get_text()
    global mission_name
    text = widget.get_text()
    mission_name = text
    text = re.sub(' ', '_', text) 
    text = re.sub(r'[^\w]', '', text)
    form_mission_name = text
    
    if text:
        widgetd.set_markup("<span style='italic'>M_{:03d}_<b>{}-{}</b></span>".format(1, selected_world, text))
        widgetd.show()
    else:
        widgetd.hide()
        entry = combo.get_child()

def on_file_clicked( widget):
    global assistant
    dialog = Gtk.FileChooserDialog(
        "Please choose a file",
        assistant,
        Gtk.FileChooserAction.OPEN,
        (
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        ),
    )

    add_filters(dialog)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        print("Open clicked")
        print("File selected: " + dialog.get_filename())
        label_selected_file.set_markup("<span style='italic'>{} <a href='keynav'>remover</a></span>".format(dialog.get_filename()))
        label_selected_file.show()
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")
        label_selected_file.set_text("")
        label_selected_file.hide()

    dialog.destroy()

def add_filters(dialog):
    filter_text = Gtk.FileFilter()
    filter_text.set_name("Quest Files")
    filter_text.add_pattern("*.msn")
    dialog.add_filter(filter_text)

class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Quest Manager")

        s = Gdk.Screen.get_default()
        height = s.get_height() / 1.2

        self.set_border_width(1)
        self.set_default_size(720, height)

        self.treeview = None
        self.store = Gtk.ListStore(str, int, int)

        self.vpaned = Gtk.Paned(orientation=Gtk.Orientation(1))
        self.matplotlib_canvas = None

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Quest Manager"
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
        item_bar0 = Gtk.MenuItem.new_with_label('Nuevo...')
        item_bar1 = Gtk.MenuItem.new_with_label('Importar Quest')
        #item_bar1.connect('activate', self.on_menu)
        item_bar2 = Gtk.MenuItem.new_with_label('Guardar')
        #item_bar1.connect('activate', self.on_menu)
        item_bar2 = Gtk.MenuItem.new_with_label('Exportar...')
        #item_bar2.connect('activate', self.on_menu)
        item_bar3 = Gtk.MenuItem.new_with_label('Exit')
        #item_bar3.connect('activate', self.on_menu)
        # sub menu for 'Bar'
        menu_foo = Gtk.Menu.new()
        menu_foo.append(item_bar0)
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

        pb_new = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_new.png')
        pb_import = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_filesel.png')
        pb_export = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_export.png')
        pb_record = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_render_animation.png')
        pb_stop_record = Pixbuf.new_from_file(
            'C:\\Users\\Bloomberg\\PycharmProjects\\IMUAnalyser\\icons\\icon16_rec.png')

        boc = Gtk.Box()
        lb = Gtk.Label("Nuevo")
        ico = Gtk.Image()
        ico.set_from_pixbuf(pb_new)
        boc.add(ico)
        boc.add(lb)

        bar_item = Gtk.ToolButton.new()
        bar_item.set_name('NEW')
        bar_item.set_icon_widget(boc)
        bar_item.set_tooltip_text("Crear nuevo...")
        bar_item.connect('clicked', self.new_file_click)
        toolbar.insert(bar_item, -1)

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
    
    def new_file_click(self, widget):
        do_assistant()
        
        

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

        self.vpaned.set_wide_handle(True)
        self.vpaned.set_position(250)
        self.vpaned.pack1(self.grid, False, False)
        #self.vpaned.pack2(canvas, True, True)

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
        #self.plot_csv(model[iter][0])



win = HeaderBarWindow()
win.set_position(Gtk.WindowPosition.CENTER)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
