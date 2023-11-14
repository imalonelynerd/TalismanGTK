from gi.repository import Gtk, Adw, GLib, Gdk, Gio
from .talutils import Calculator

@Gtk.Template(resource_path="/fr/imalonelynerd/Talisman/calculator.ui")
class CalculatorWindow(Adw.Window):
    __gtype_name__ = "CalculatorWindow"

    before = Gtk.Template.Child()
    ope = Gtk.Template.Child()
    value = Gtk.Template.Child()
    after = Gtk.Template.Child()

    br = Gtk.Template.Child()
    be = Gtk.Template.Child()
    clearb = Gtk.Template.Child()

    add = Gtk.Template.Child()
    rem = Gtk.Template.Child()
    mul = Gtk.Template.Child()
    div = Gtk.Template.Child()
    equ = Gtk.Template.Child()

    b0 = Gtk.Template.Child()
    b1 = Gtk.Template.Child()
    b2 = Gtk.Template.Child()
    b3 = Gtk.Template.Child()
    b4 = Gtk.Template.Child()
    b5 = Gtk.Template.Child()
    b6 = Gtk.Template.Child()
    b7 = Gtk.Template.Child()
    b8 = Gtk.Template.Child()
    b9 = Gtk.Template.Child()

    def num_input(self, _r1, key, _r2, _r3):
        if key == Gdk.KEY_Escape:
            self.close()

    def __init__(self, parent_window, player_info, **kwargs):
        super().__init__(**kwargs)
        self.parent_window = parent_window
        self.player_info = player_info
        self.calc = Calculator()

        self.set_title(_(f"Update {self.player_info.getPlayerName()}'s LP..."))
        self.set_transient_for(parent_window)

        event_controller = Gtk.EventControllerKey()
        event_controller.connect("key-pressed", self.num_input)
        self.add_controller(event_controller)

        self.br.connect("clicked", self.remchar)
        self.be.connect("clicked", self.updateLP)
        self.clearb.connect("clicked", self.clear)

        button_ids = [self.b0,
                    self.b1, self.b2, self.b3,
                    self.b4, self.b5, self.b6,
                    self.b7, self.b8, self.b9]

        for k in range(len(button_ids)):
            btn = button_ids[k]
            btn.connect("clicked", lambda *_, val=k: self.addchar(val))

        self.add.connect("clicked", lambda *_, val=0: self.setope(val))
        self.rem.connect("clicked", lambda *_, val=1: self.setope(val))
        self.mul.connect("clicked", lambda *_, val=2: self.setope(val))
        self.div.connect("clicked", lambda *_, val=3: self.setope(val))
        self.equ.connect("clicked", lambda *_, val=4: self.setope(val))

        self.before.set_text(str(self.player_info.getLP()))

        self.value.connect('value_changed', self.refresh)

        self.setope(1)
        #self.refresh()
        self.present()

    def addchar(self, nb : int):
        res = self.value.get_text()
        if(res == "0"):
            res = str(nb)
        else:
            res = res + str(nb)
        if(int(res) < 0):
            res = "0"
        if(int(res) > 100000):
            res = "100000"
        self.value.set_text(res)
        self.refresh()

    def remchar(self, _):
        res = self.value.get_text()
        if(len(res) == 1):
            res = "0"
        else:
            res = res[:-1]
        self.value.set_text(res)
        self.refresh()

    def refresh(self, _ = 0):
        if(self.value.get_text == ""):
            self.value.set_text("0")
        self.ope.set_text(self.calc.getFormatedOpe())
        self.after.set_text(str(self.calc.calculate(self.player_info.getLP(), int(self.value.get_text()))))

    def setope(self, ope : int):
        assert 0 <= ope <= 4
        self.calc.setOpe(ope)
        self.refresh()

    def clear(self, _):
        self.value.set_text("0")
        self.setope(1)

    def updateLP(self, _):
        self.player_info.setLP(int(self.after.get_text()))
        self.close()





