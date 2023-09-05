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

from gi.repository import Adw, Gtk, Gio

@Gtk.Template(resource_path='/fr/imalonelynerd/Talisman/window.ui')
class TalismanGtkWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TalismanGtkWindow'
    main_window_title = "Talisman"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_pr_w(self):
        self._native = Gtk.FileChooserNative(
            title="Open File",
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
        print(file.peek_path()[-4:])
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
        rawdata = {}
        try:
            rawdata = json.loads(contents[1])
        except:
            self.send_error_dialog(
                self,
                _(f"Unable to open {file.get_basename()}"),
                _(f"This file isn't a compatible Talisman preset file\n({file.peek_path()}).")
            )
            return
        if rawdata.get("pl1name") == None or rawdata.get("pl2name") == None or rawdata.get("lp") == None or rawdata.get("timer") == None:
                self.send_error_dialog(
                    self,
                    _(f"Unable to open {file.get_basename()}"),
                    _(f"This file isn't a compatible Talisman preset file\n({file.peek_path()}).")
                )
                return

    def send_error_dialog(self, parent, title, content):
        dialog = Adw.MessageDialog.new(self, title, content)
        dialog.add_response("cancel", _("Cancel"))
        Gtk.Window.present(dialog)
        return



