# window.py
#
# Copyright 2023 Nerd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import datetime

from .talutils import *

from .calculator import *
from .tools import *

from gi.repository import Adw, Gtk, GLib, Gio


@Gtk.Template(resource_path='/fr/imalonelynerd/Talisman/window.ui')
class TalismanGtkWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TalismanGtkWindow'
    main_window_title = "Talisman"
    default_icon_name = "fr.imalonelynerd.Talisman"

    # Setup page componements

    p1nick = Gtk.Template.Child()
    p2nick = Gtk.Template.Child()

    lp = Gtk.Template.Child()

    timer_type = Gtk.Template.Child()
    cnt = Gtk.Template.Child()
    playt = Gtk.Template.Child()
    addt = Gtk.Template.Child()

    start = Gtk.Template.Child()
    eraseb = Gtk.Template.Child()

    stack = Gtk.Template.Child()
    setup = Gtk.Template.Child()
    duel = Gtk.Template.Child()
    toast = Gtk.Template.Child()

    # Duel page

    p1duel = Gtk.Template.Child()
    p2duel = Gtk.Template.Child()

    p1lp = Gtk.Template.Child()
    p2lp = Gtk.Template.Child()

    p1time = Gtk.Template.Child()
    p2time = Gtk.Template.Child()

    switchp = Gtk.Template.Child()
    dtype = Gtk.Template.Child()

    toolsb = Gtk.Template.Child()
    noteb = Gtk.Template.Child()
    ff = Gtk.Template.Child()

    p1c = Gtk.Template.Child()
    p2c = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_type.connect('notify', self.on_timer_change)
        self.eraseb.connect('clicked', self.erase_inputs)
        self.timer_type.set_selected(0)
        self.cnt.hide()
        self.playt.hide()
        self.addt.hide()
        self.start.connect('clicked', self.start_duel)
        self.ff.connect('clicked', self.forfeit_b)
        self.toolsb.connect('clicked', self.set_tools)

    # LOAD PRESET

    def load_preset_w(self):
        self._native = Gtk.FileChooserNative(
            title=_("Open File"),
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel",
        )
        self._native.connect("response", self.on_open_response)
        self._native.show()

    def on_open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(dialog.get_file())
        self._native = None

    def open_file(self, file):
        if file.peek_path()[-4:] != ".tal":
            self.show_error_dialog(
                self,
                _(f"Unable to open {file.get_basename()}"),
                _(f"This file isn't a compatible Talisman preset file\n({file.peek_path()}).")
            )
            return
        file.load_contents_async(None, self.load_data_to_ui)

    def load_data_to_ui(self, file, result):
        contents = file.load_contents_finish(result)
        if not contents[0]:
            self.send_error_dialog(
                self,
                _(f"Unable to open {file.get_basename()}"),
                _(f"This file can't be reached ({file.peek_path()}).")
            )
            return
        if not self.test_file(contents[1]):
            self.send_error_dialog(
                self,
                _(f"Unable to open {file.get_basename()}"),
                _(f"This file isn't a compatible Talisman preset file\n({file.peek_path()}).")
            )
            return
        rawdata = json.loads(contents[1])
        self.p1nick.set_text(rawdata["pl1name"])
        self.p2nick.set_text(rawdata["pl2name"])
        self.lp.set_text(rawdata["lp"])

        choice = int(rawdata["timer"]["choice"])

        self.timer_type.set_selected(choice - 1)

        if choice == 2:
            self.cnt.set_text(rawdata["timer"]["countdown"])
        elif choice == 3:
            self.cnt.set_text(rawdata["timer"]["time"])
            self.addt.set_text(rawdata["timer"]["bonus"])
        self.send_toast(_("Preset loaded successfully !"))
        return

    def test_file(self, content):
        rawdata = {}
        try:
            rawdata = json.loads(content)
        except:
            return False
        if (rawdata.get("pl1name") == None
                or rawdata.get("pl2name") == None
                or rawdata.get("lp") == None
                or rawdata.get("timer") == None
                or rawdata["timer"].get("choice") == None
        ):
            return False
        choice = rawdata["timer"].get("choice")
        if (choice == "2"
                and rawdata["timer"].get("countdown") is None
        ):
            return False
        if (choice == "3"
                and (rawdata["timer"].get("time") is None
                     or rawdata["timer"].get("bonus") is None)
        ):
            return False
        return True

    # SAVE PRESET

    def save_preset_w(self):
        self._native = Gtk.FileChooserNative(
            title=_("Save File As"),
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE,
            accept_label="_Save",
            cancel_label="_Cancel",
        )
        self._native.connect("response", self.on_save_response)
        d = datetime.datetime.now()
        title = f"preset{d.hour}{d.minute}_{d.day}{d.month}{d.year}.tal"
        self._native.set_current_name(title)
        self._native.show()

    def on_save_response(self, native, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.save_file(native.get_file())
        self._native = None

    def save_file(self, file):
        timer_type = self.timer_type.get_selected()
        p1 = self.p1nick.get_text()
        p2 = self.p2nick.get_text()
        if p1 == "":
            p1 = "Player 1"
        if p2 == "":
            p2 = "Player 2"
        preset = {
            "pl1name": p1,
            "pl2name": p2,
            "lp": self.lp.get_text(),
            "timer": {
                "choice": str(timer_type + 1),
            }
        }

        if timer_type == 1:
            preset["timer"]["countdown"] = self.cnt.get_text();
        if timer_type == 2:
            preset["timer"]["time"] = self.playt.get_text();
            preset["timer"]["bonus"] = self.addt.get_text();

        text = json.dumps(preset)
        bytes = GLib.Bytes.new(text.encode('utf-8'))
        file.replace_contents_bytes_async(bytes,
                                          None,
                                          False,
                                          Gio.FileCreateFlags.NONE,
                                          None,
                                          self.save_file_complete)

    def save_file_complete(self, file, result):
        res = file.replace_contents_finish(result)
        if not res:
            self.send_error_dialog(
                self,
                _(f"Unable to save {file.get_basename()}"),
                _("Please try again.")
            )
            return
        self.send_toast(_("Preset saved successfully !"))

    # GENERAL FUNCS

    def send_error_dialog(self, parent, title, content):
        dialog = Adw.MessageDialog.new(self, title, content)
        dialog.add_response("cancel", _("Cancel"))
        Gtk.Window.present(dialog)
        return

    def send_toast(self, text):
        self.toast.add_toast(Adw.Toast(title=text))
        return

    def on_timer_change(self, _w, _):
        val = self.timer_type.get_selected()
        if val == 0:
            self.cnt.hide()
            self.playt.hide()
            self.addt.hide()
        if val == 1:
            self.cnt.show()
            self.playt.hide()
            self.addt.hide()
        if val == 2:
            self.cnt.hide()
            self.playt.show()
            self.addt.show()
        return

    def start_duel(self, _w):
        self.p1 = Player(self.p1nick.get_text(), int(self.lp.get_text()))
        self.p2 = Player(self.p2nick.get_text(), int(self.lp.get_text()))

        self.settings = Settings(
            self.timer_type.get_selected(),
            [
                int(self.cnt.get_text()),
                int(self.playt.get_text()),
                int(self.addt.get_text())
            ]
        )

        self.tournament = Tournament(self.p1, self.p2, self.settings)
        if(self.tournament.p1.getPlayerName() == ""):
            self.tournament.p1.setPlayerName(_("Player 1"))
        if(self.tournament.p2.getPlayerName() == ""):
            self.tournament.p2.setPlayerName(_("Player 2"))
        self.p1duel.set_text(self.tournament.p1.getPlayerName())
        self.p2duel.set_text(self.tournament.p2.getPlayerName())

        self.p1lp.set_text(str(self.tournament.p1.getFormatedLP()))
        self.p2lp.set_text(str(self.tournament.p2.getFormatedLP()))
        self.p1lp.set_use_markup(True)
        self.p2lp.set_use_markup(True)

        self.p1time.set_label(str(self.tournament.p1.getTimer()))
        self.p2time.set_label(str(self.tournament.p2.getTimer()))

        self.calc1 = self.p1c.connect('clicked',lambda *_, infos=self.tournament.p1: self.set_calculator(infos))
        self.calc2 = self.p2c.connect('clicked',lambda *_, infos=self.tournament.p2: self.set_calculator(infos))

        if (self.tournament.settings.getTimerType() != 2):
            self.p1time.hide()
            self.p2time.hide()
            self.switchp.hide()

        self.dtype.set_text(self.tournament.settings.getTimerName())

        self.eraseb.hide()
        self.stack.set_visible_child_name("duel")
        return

    def erase_inputs(self, _w):
        self.p1nick.set_text("")
        self.p2nick.set_text("")
        self.lp.set_text("8000")
        self.cnt.set_text("120")
        self.playt.set_text("120")
        self.addt.set_text("10")
        self.send_toast(_("Inputs deleted successfully !"))
        return

    def forfeit_m(self, widget, _):
        if self.stack.get_visible_child_name() != "setup":
            self.forfeit_pre()
        else:
            self.erase_inputs(widget)
        return

    def forfeit_b(self, _w):
        self.forfeit_pre()
        return

    def forfeit_pre(self):
        dialog = Adw.MessageDialog.new(
            self,
            _("Forfeit duel ?"),
            _("You are about to forfeit this duel. Are you sure about that ?")
        )
        dialog.add_response("cancel", _("No..."))
        dialog.add_response("ff", _("I'm sure"))
        dialog.set_response_appearance("ff", Adw.ResponseAppearance.DESTRUCTIVE);
        dialog.set_close_response("cancel")
        dialog.connect('response', self.forfeit)
        Gtk.Window.present(dialog)

    def forfeit(self, _w, response):
        if response == "ff":
            self.stack.set_transition_type(2)
            self.stack.set_visible_child_name("setup")
            self.stack.set_transition_type(3)
            self.eraseb.show()
            self.p1c.disconnect(self.calc1)
            self.p2c.disconnect(self.calc2)
            self.p1time.show()
            self.p2time.show()
            self.switchp.show()
            self.send_toast(_("Forfeited !"))
        return

    def set_calculator(self, infos):
        calcw = CalculatorWindow(self, infos)
        calcw.connect("close_request", self.update_lp)

    def update_lp(self, _):
        print(self.tournament.p1.getLP(), self.tournament.p2.getLP())
        self.refresh()

    def refresh(self):
        self.p1lp.set_text(self.tournament.p1.getFormatedLP())
        self.p2lp.set_text(self.tournament.p2.getFormatedLP())
        self.p1lp.set_use_markup(True)
        self.p2lp.set_use_markup(True)

    def set_tools(self, _):
        toolsw = ToolsWindow(self)
