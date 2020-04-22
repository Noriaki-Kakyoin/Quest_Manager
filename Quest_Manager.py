import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import re
import pathlib
import os
import datetime
import json

###############################################
# Check if /APPDATA/ROAMING/QuestManager folder has been created
homedir = os.getenv('APPDATA')
dir_default = os.path.join(homedir, 'QuestManager\\')
dir_tmp = os.path.join(homedir, 'QuestManager\\', 'tmp\\')
dir_quests = os.path.join(homedir, 'QuestManager\\', 'quests\\')
pathlib.Path(dir_tmp).mkdir(parents=True, exist_ok=True) 
pathlib.Path(dir_quests).mkdir(parents=True, exist_ok=True) 

_selected_quest = ""
quest_list = []

class Quest():
    def __init__(self, is_completed: bool, number: int, name: str, file: str, n_hist=0, n_dialog=0, last_modified=str(datetime.datetime.now()), h_textviews=[], world: str):
        self.is_completed = is_completed
        self.number = number
        self.name = name
        self.file = file
        self.n_hist = n_hist
        self.n_dialog = n_dialog
        self.last_modified = last_modified
        self.h_textviews = h_textviews
        self.world = world

    def add_hist(self):
        self.n_hist = self.n_hist + 1


    def get_hist(self):
        return self.h_textviews

class ImageButton(Gtk.EventBox):
    def __init__(self, name, tbm, id):
        super(Gtk.EventBox, self).__init__()

        # Load the images for the button
        pb_close = Pixbuf.new_from_file(
        'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon16_x.png')
        
        self.button_image = Gtk.Image()
        self.button_image.set_from_pixbuf(pb_close)

        self.name = name
        self.tbm = tbm
        self.id = id

        # Add the default image to the event box
        self.add(self.button_image)

        # Connect the signal listeners
        self.connect('button-press-event', self.on_button_pressed)
        self.connect('button-release-event', self.on_button_released)

    def get(self):
        return self

    def update_image(self, image_widget):
        self.remove(self.get_child())
        self.add(image_widget)
        self.button_pressed_image.show()

    def on_button_pressed(self, widget, event):
        print(self.id)
        #self.update_image(self.button_pressed_image)

    def on_button_released(self, widget, event):
        self.tbm.tabs[self.id].destroy()
        #self.update_image(self.button_image)

class TreeViewData:
    def __init__(self, is_completed, number, name, file, n_hist, n_dialog):
        self.is_completed = is_completed
        self.number = number
        self.name = name
        self.file = file
        self.n_hist = n_hist
        self.n_dialog = n_dialog

class Tabs_Manager(Gtk.HBox):
    def __init__(self, win):
        Gtk.HBox.__init__(self)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, .25))
        self.tabs = []
        self.btns = []
        self.textview = Gtk.TextView()

        self.win = win
    
    def get_tab(self):
        return self

    def destroy_all(self):
        for e in self.tabs:
            e.destroy()

    def add_tab(self, title):
        evnt = Gtk.EventBox()
        tab = Gtk.HBox()
        tab.set_size_request(-1, 40)
        evnt.add(tab)
        evnt.set_name('abc')

        print(title)

        evnt.connect('button-release-event', self.on_button_released)

        tab.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, .25))
        labl = Gtk.Label(title)
        btn = ImageButton("a", self, len(self.tabs))
        self.btns.append(btn)

        tab.pack_start(labl, False, False, 10)
        tab.pack_start(btn.get(), False, False, 10)
        self.pack_start(evnt, False, False, 1)

        self.tabs.append(evnt)

        self.win.show_all()

    def on_button_pressed(self, widget, event):
        print()
        #self.update_image(self.button_pressed_image)

    def on_button_released(self, widget, event):
        name = Gtk.Buildable.get_name(widget)
        print(name)

class Assistant(object):
    def __init__(self, tbm, win):
        self.label_selected_file = Gtk.Label()

        self.tbm = tbm
        self.win = win

        self._mission_name = ""
        self.selected_world = "Asgard"
        self.form_mission_name = ""
        self.assistant = Gtk.Assistant()
        self.label_real_mission_name = Gtk.Label()
        self.label_real_mission_name.set_sensitive(False)
        self.label_real_mission_name.set_halign(Gtk.Align.END)
        self.mission_name_entry = Gtk.Entry()
        self.mission_name_entry.set_placeholder_text("Nombre de la mision")
        self.mission_name_entry.set_max_length(50)
        self.textview = Gtk.TextView()
        self.textview.set_border_window_size(Gtk.TextWindowType.TEXT, 2)
        self.buffer = self.textview.get_buffer()

        self.assistant.connect('cancel', self.on_close_cancel)
        self.assistant.connect('close', self.on_close_cancel)
        self.assistant.connect('apply', self.on_apply)
        self.assistant.connect('prepare', self.on_prepare)

    @property
    def mission_name(self):
        return self._mission_name

    @mission_name.setter
    def mission_name(self, text):
        self._mission_name = text

    @property
    def selected_quest(self):
        global _selected_quest
        return _selected_quest

    @selected_quest.setter
    def selected_quest(self, text):
        global _selected_quest
        _selected_quest = text
         
    def on_close_cancel(self, assistant):
        assistant.destroy()

    def on_apply(self, assistant):
        ################################
        ### Create quest file
        ################################

        quest_file = os.path.join(homedir, 'QuestManager\\', 'quests\\', self.label_real_mission_name.get_text() + ".qst")

        print('>>>>>' + selected_world)

        new_quest = Quest(False, len(quest_list) + 1, self.mission_name_entry.get_text(), quest_file, selected_world)

        with open(quest_file, 'w') as q:
            json.dump(new_quest.__dict__, q)

        quest_list.append(new_quest)

        self.win.add_treeview_entry(new_quest)
        self.tbm.add_tab(self.mission_name_entry.get_text())

    def on_prepare(self, assistant, page):
        current_page = assistant.get_current_page()
        n_pages = assistant.get_n_pages()
        title = 'Sample assistant (%d of %d)' % (current_page + 1, n_pages)
        assistant.set_title(title)

def on_entry_changed(widget, data, win):
    global _mission_name
    page_number = data.assistant.get_current_page()
    current_page = data.assistant.get_nth_page(page_number)
    text = data.mission_name_entry.get_text()
    mission_name = text
    text = re.sub(' ', '_', text) 
    text = re.sub(r'[^\w]', '', text)
    widget.set_text(text)
    form_mission_name = text
    data.buffer.delete(data.buffer.get_start_iter(), data.buffer.get_end_iter())

    if mission_name:
        data.assistant.set_page_complete(current_page, True)
        data.label_real_mission_name.set_markup("<span style='italic'>M_{:03d}_<b>{}-{}</b></span>".format(len(quest_list) + 1, selected_world, text))
        data.label_real_mission_name.show()
        
        markup = """> NOMBRE QUEST     = <b>{}</b>\n> FORMATO               = <span style='italic'>M_{:03d}_<b>{}-{}</b></span>\n> QUEST ANTERIOR   = <b>{}</b>\n> MAPA                      = <b>{}</b>""".format(text, len(quest_list) + 1, selected_world, text, data.selected_quest, selected_world)
        data.buffer.insert_markup(data.buffer.get_end_iter(), markup, -1)
    else:
        data.assistant.set_page_complete(current_page, False)
        data.label_real_mission_name.hide()
 
def do_assistant(tbm, win):
    dat = Assistant(tbm, win)
    dat.assistant.set_default_size(-1, 300)
    
    dat.label_selected_file.connect("activate-link", activate_link, dat, win)
    
    create_page1(dat)
    create_page2(dat, win)

    dat.assistant.show()
        
def on_toggle_changed(widget, data):
    page_number = data.assistant.get_current_page()
    current_page = data.assistant.get_nth_page(page_number)
    status = widget.get_active()

    if status:
        data.assistant.set_page_complete(current_page, True)
    else:
        data.assistant.set_page_complete(current_page, False)
        
def activate_link(label, uri, data, win):
    if uri == 'keynav':
        data.label_selected_file.hide()
        data.label_selected_file.set_text("")
        data.selected_quest = ""

        data.buffer.delete(data.buffer.get_start_iter(), data.buffer.get_end_iter())
        markup = """> NOMBRE QUEST     = <b>{}</b>\n> FORMATO               = <span style='italic'>M_{:03d}_<b>{}-{}</b></span>\n> QUEST ANTERIOR   = <b>{}</b>\n> MAPA                      = <b>{}</b>""".format(data.mission_name_entry.get_text(), len(quest_list) + 1, selected_world, data.mission_name_entry.get_text(), data.selected_quest, selected_world)
        data.buffer.insert_markup(data.buffer.get_end_iter(), markup, -1)

def create_page1(data):
    box = Gtk.Box()
    box.set_border_width(12)
    box.set_homogeneous(False)
    box.set_baseline_position(Gtk.BaselinePosition(0))
    
    btn_mission_selec = Gtk.ToggleButton()
    btn_mission_selec.connect('toggled', on_toggle_changed, data)
    img_mission = Gtk.Image()
    pb_text = Pixbuf.new_from_file(
        'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon32_text.png')

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

def create_page2(data, win):
    box = Gtk.VBox(homogeneous=False,
                   spacing=12)
    box.set_border_width(12)
    
    box_filechooser = Gtk.HBox()
    box_filechooser.set_spacing(60)
    
    box_worldchooser = Gtk.HBox()
    box_worldchooser.set_spacing(180)

    data.mission_name_entry.connect('changed', on_entry_changed, data, win)

    button_selec_file = Gtk.Button("Seleccionar Archivo")
    button_selec_file.connect("clicked", on_file_clicked_assis, data)
    
    box_btn_files = Gtk.HBox()
    box_btn_files.pack_start(button_selec_file, False, False, 5)
    
    av = Gtk.Label()
    av.set_markup("(Opcional) Quest Anterior <span style='italic'>(*.qst)</span>")
    
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
    world_combo.connect("changed", on_combo_changed, data.mission_name_entry, data.label_real_mission_name, data, win)
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
    create_page3(data, data.mission_name_entry)
   

def create_page3(data, ent):
    box = Gtk.VBox(homogeneous=False,
                   spacing=12)
    box.set_border_width(0)
    
    label = Gtk.Label("Confirme los siguientes datos")
    
    print(data.mission_name_entry.get_text())
    
    box.pack_start(label, False, False, 0)
    box.pack_start(data.textview, False, False, 0)
    box.show_all()
    
    data.assistant.append_page(box)
    data.assistant.set_page_complete(box, True)
    data.assistant.set_page_title(box, 'Confirmacion')
    data.assistant.set_page_type(box, Gtk.AssistantPageType.CONFIRM)

    pixbuf = data.assistant.render_icon(Gtk.STOCK_DIALOG_INFO,
                                        Gtk.IconSize.DIALOG,
                                        None)
    data.assistant.set_page_header_image(box, pixbuf)

def on_combo_changed(combo, widget, widgetd, data, win):
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
    data.buffer.delete(data.buffer.get_start_iter(), data.buffer.get_end_iter())
    
    if text:
        widgetd.set_markup("<span style='italic'>M_{:03d}_<b>{}-{}</b></span>".format(len(quest_list) + 1, selected_world, text))
        markup = """> NOMBRE QUEST     = <b>{}</b>\n> FORMATO               = <span style='italic'>M_{:03d}_<b>{}-{}</b></span>\n> QUEST ANTERIOR   = <b>{}</b>\n> MAPA                      = <b>{}</b>""".format(text, len(quest_list) + 1, selected_world, text, data.selected_quest, selected_world)
        data.buffer.insert_markup(data.buffer.get_end_iter(), markup, -1)
        widgetd.show()
    else:
        widgetd.hide()
        entry = combo.get_child()

def on_file_clicked_assis(widget, data):
    dialog = Gtk.FileChooserDialog(
        "Please choose a file",
        data.assistant,
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
        data.label_selected_file.set_markup("<span style='italic'>{} <a href='keynav'>remover</a></span>".format(dialog.get_filename()))
        data.label_selected_file.show()
        data.selected_quest = str(dialog.get_filename())
        
        data.buffer.delete(data.buffer.get_start_iter(), data.buffer.get_end_iter())
        markup = """> NOMBRE QUEST     = <b>{}</b>\n> FORMATO               = <span style='italic'>M_{:03d}_<b>{}-{}</b></span>\n> QUEST ANTERIOR   = <b>{}</b>\n> MAPA                      = <b>{}</b>""".format(data.mission_name_entry.get_text(), 1, selected_world, data.mission_name_entry.get_text(), data.selected_quest, selected_world)
        data.buffer.insert_markup(data.buffer.get_end_iter(), markup, -1)
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")
        data.label_selected_file.set_text("")
        data.label_selected_file.hide()
        data.selected_quest = ""

        data.buffer.delete(data.buffer.get_start_iter(), data.buffer.get_end_iter())
        markup = """> NOMBRE QUEST     = <b>{}</b>\n> FORMATO               = <span style='italic'>M_{:03d}_<b>{}-{}</b></span>\n> QUEST ANTERIOR   = <b>{}</b>\n> MAPA                      = <b>{}</b>""".format(data.mission_name_entry.get_text(), 1, selected_world, data.mission_name_entry.get_text(), data.selected_quest, selected_world)
        data.buffer.insert_markup(data.buffer.get_end_iter(), markup, -1)

    dialog.destroy()

def add_filters(dialog):
    filter_text = Gtk.FileFilter()
    filter_text.set_name("Quest Files")
    filter_text.add_pattern("*.qst")
    dialog.add_filter(filter_text)

class HeaderBarWindow(Gtk.Window):
    (COLUMN_FIXED,
     COLUMN_DESCRIPTION,
     COLUMN_DESCRIPTION,
     COLUMN_NUMBER,
     COLUMN_NUMBER) = range(5)
    def __init__(self):
        Gtk.Window.__init__(self, title=" Manager")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        s = Gdk.Screen.get_default()
        height = s.get_height() / 1.2

        self.set_border_width(1)
        self.set_default_size(720, height)

        self.tabs = Tabs_Manager(self)

        self.theme_dark = True

        ##############################################
        # Scan quest folder
        
        for file in os.listdir(dir_quests):
            if file.endswith(".qst"):
                with open(os.path.join(dir_quests, file), 'r') as f:
                    quest_dict = json.load(f)
                    quest_list.append(Quest(quest_dict['is_completed'], quest_dict['number'], quest_dict['name'], quest_dict['file'], quest_dict['n_hist'], quest_dict['n_dialog'], quest_dict['last_modified'], quest_dict['h_textviews']))

        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", self.theme_dark)  # if you want use dark theme, set second arg to True


        self.treeview = None
        
        self.store = Gtk.ListStore(bool, int, str, int, int, str)

        self.vpaned = Gtk.Paned(orientation=Gtk.Orientation(1))
        self.matplotlib_canvas = None

        self.textview = Gtk.TextView()
        self.buffer = self.textview.get_buffer()

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Quest Manager"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="video-display-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)
        button.connect("clicked", self.toggle_theme)

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
        self.layout.pack_start(self.tabs.get_tab(), False, False, 0)
        self.layout.pack_start(main_content, False, True, 0)
        self.add(self.layout)

        self.connect('destroy', Gtk.main_quit)
        self.show_all()
    
    def toggle_theme(self, widget):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", (not self.theme_dark))  # if you want use dark theme, set second arg to True
        self.theme_dark = not self.theme_dark

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
            'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon16_new.png')
        pb_import = Pixbuf.new_from_file(
            'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon16_filesel.png')
        pb_export = Pixbuf.new_from_file(
            'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon16_export.png')
        pb_record = Pixbuf.new_from_file(
            'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon16_render_animation.png')
        pb_stop_record = Pixbuf.new_from_file(
            'C:\\Users\\Odin\\Desktop\\Quest_Manager\\icons\\icon16_rec.png')

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
        do_assistant(self.tabs, self)
        
        

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

    def add_treeview_entry(self, quest):
        print('completed: {}\nnumber: {}\nname: {}\nn_hist: {}\nn_dialog: {}\nfile: {}\n'.format(quest.is_completed, quest.number, quest.name, quest.n_hist, quest.n_dialog, quest.file))
        self.store.append([quest.is_completed, quest.number, quest.name, quest.n_hist, quest.n_dialog, quest.file])
        self.show_all()

    def _create_main_content(self):
        ###################################################################
        ##### LISTBOX WITH CSV INFO
        ###################################################################
        # creating the treeview, making it use the filter as a model, and adding the columns
        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.connect('cursor-changed', self.selection_changed)

        for i, column_title in enumerate(
                ["Completa", "Numero", "Nombre", "Cant. Historias", "Cant. Dialogos", "Archivo"]
        ):
            if i == 0:
                renderer = Gtk.CellRendererToggle()
                renderer.connect('toggled', self.is_fixed_toggled, self.store)

                column = Gtk.TreeViewColumn(column_title, renderer, active=self.COLUMN_FIXED)
                column.set_min_width(50)
                column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
                column.set_resizable(True)
                column.set_reorderable(True)
            elif i == 2:
                renderer = Gtk.CellRendererText()
                renderer.set_property("editable", True)
                column = Gtk.TreeViewColumn(column_title, renderer, text=i, active=self.COLUMN_FIXED)
                column.set_min_width(50)
                column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
                column.set_resizable(True)
                column.set_reorderable(True)
            else:
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i, active=self.COLUMN_FIXED)
                column.set_min_width(50)
                column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
                column.set_resizable(True)
                column.set_reorderable(True)
            
            self.treeview.append_column(column)
        
        for quest in quest_list:
            self.add_treeview_entry(quest)


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

        gride = Gtk.Grid()

        stack = Gtk.Stack()
        stack.set_hhomogeneous(True)
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP)

        stack.set_hexpand(True)
        stack.set_vexpand(True)
        gride.attach(stack, 1, 0, 1, 1)

        stacksidebar = Gtk.StackSidebar()
        stacksidebar.set_stack(stack)
        gride.attach(stacksidebar, 0, 0, 1, 1)

        stack.add_titled(self.vpaned, 'quest', 'Lista de Quest                               ')
        stack.add_titled(Gtk.Label(), 'story', 'Historia General')
        stack.add_titled(Gtk.Label(), 'dialogue', 'Dialogos')
        stack.add_titled(Gtk.Label(), 'cutscene', 'Cut-Scenes')

        return gride


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

    def is_fixed_toggled(self, cell, path_str, model):
        # get toggled iter
        iter_ = model.get_iter(path_str)
        is_fixed = model.get_value(iter_, self.COLUMN_FIXED)

        # do something with value
        is_fixed ^= 1

        model.set_value(iter_, self.COLUMN_FIXED, is_fixed)

        qst = quest_list[int(path_str)]
        qst.is_completed = bool(is_fixed)

        with open(qst.file, 'w') as q:
            json.dump(qst.__dict__, q)


win = HeaderBarWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
