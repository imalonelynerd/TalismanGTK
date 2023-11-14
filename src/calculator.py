from gi.repository import Gtk, Adw, GLib, Gdk, Gio


@Gtk.Template(resource_path="/fr/imalonelynerd/Talisman/calculator.ui")
class CalculatorWindow(Adw.Window):
    __gtype_name__ = "CalculatorWindow"

    def __init__(self, parent_window, player_info, **kwargs):
        super().__init__(**kwargs)
