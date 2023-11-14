from gi.repository import Gtk, Adw, GLib, Gdk, Gio
import random

@Gtk.Template(resource_path="/fr/imalonelynerd/Talisman/tools.ui")
class ToolsWindow(Adw.Window):
    __gtype_name__ = "ToolsWindow"

    coinf = Gtk.Template.Child()
    dicef = Gtk.Template.Child()

    coin = Gtk.Template.Child()
    dice = Gtk.Template.Child()

    coint = Gtk.Template.Child()
    dicet = Gtk.Template.Child()

    roll = Gtk.Template.Child()
    flip = Gtk.Template.Child()

    def num_input(self, _r1, key, _r2, _r3):
        if key == Gdk.KEY_Escape:
            self.close()

    def __init__(self, parent_window, **kwargs):
        super().__init__(**kwargs)
        self.parent_window = parent_window
        self.present()

        self.set_title(_("Tools"))
        self.set_transient_for(parent_window)

        event_controller = Gtk.EventControllerKey()
        event_controller.connect("key-pressed", self.num_input)
        self.add_controller(event_controller)

        self.roll.connect('clicked',self.roll_dice_pre)
        self.flip.connect('clicked',self.flip_coin_pre)

    def roll_dice_pre(self, _):
        self.dice.set_opacity(0.5)
        self.dicet.set_text('Rolling...') #_ ?
        GLib.timeout_add(400, self.roll_dice)


    def roll_dice(self):
        self.dice.set_opacity(1)
        res = random.randint(1,6)
        self.dice.set_from_icon_name(f"dice{res}")
        self.dicet.set_text(f"{res}")

    def flip_coin_pre(self, _):
        self.coin.set_opacity(0.5)
        self.coint.set_text('Flipping...') #_ ?
        GLib.timeout_add(400, self.flip_coin)


    def flip_coin(self):
        self.coin.set_opacity(1)
        res = random.randint(1,2)
        self.coin.set_from_icon_name(f"coin{res}")
        match(res):
            case 1:
                 self.coint.set_text("Tails") #_('Tails')
            case 2:
                 self.coint.set_text("Head")  #_('Head')
