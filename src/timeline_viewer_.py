"""A timeline viewer application using tkinter.

Version @release
Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version.

This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details.
"""
import locale
import os
import sys
from tkinter import messagebox
from tkinter import ttk

from nvtlview.tlv_controller import TlvController
import tkinter as tk
from tlv_model.tlv_data_model import TlvDataModel
from tlviewer.tlviewer_commands import TlviewerCommands
from tlviewer.tlviewer_menu import TlviewerMenu
from tlviewer.tlviewer_toolbar import TlviewerToolbar
from tlviewer.tlviewer_path_bar import TlviewerPathBar

WINDOW_GEOMETRY = '1200x800'
SUBSTITUTE_MISSING_TIME = True
LOCALIZE_DATE = True


class TimelineViewer(TlviewerCommands):

    def __init__(self):

        if LOCALIZE_DATE:
            locale.setlocale(locale.LC_TIME, "")
            # enabling localized time display

        self.root = tk.Tk()
        self.root.title('Timeline viewer')
        self.root.geometry(WINDOW_GEOMETRY)

        settings = {
            'substitute_missing_time':tk.BooleanVar(value=SUBSTITUTE_MISSING_TIME),
        }
        self._mainMenu = TlviewerMenu(self.root, settings)
        self.root.config(menu=self._mainMenu)

        self.mdl = TlvDataModel()
        mainWindow = ttk.Frame(self.root)
        mainWindow.pack(fill='both', expand=True)
        self._pathBar = TlviewerPathBar(mainWindow, self.mdl, text='', anchor='w', padx=5, pady=3)
        self._pathBar.pack(side='bottom', expand=False, fill='x')
        self.mdl.add_observer(self._pathBar)
        self._toolbar = TlviewerToolbar(mainWindow, largeIcons=False, enableHovertips=True)
        self._toolbar.pack(side='bottom', fill='x', padx=5, pady=2)

        self.tlv = TlvController(
            self.mdl,
            mainWindow,
            LOCALIZE_DATE,
            settings,
            onDoubleClick=self.open_section,
            )
        self.mdl.add_observer(self.tlv)
        self.bind_events()
        self.prjFilePath = None

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self._mainMenu.disable_menu()
        self._toolbar.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self._mainMenu.enable_menu()
        self._toolbar.enable_menu()

    def read_data(self, filePath):
        self.mdl.clear()
        try:
            self.mdl.read_data(filePath)
        except Exception as ex:
            self.mdl.clear()
            self.prjFilePath = None
            self.disable_menu()
            messagebox.showerror(
                self.root.title(),
                message=_('Cannot read file'),
                detail=str(ex),
                )
        else:
            self.prjFilePath = filePath
        finally:
            self.refresh()

    def refresh(self, event=None):
        self.tlv.refresh()
        self.tlv.fit_window()
        self.enable_menu()
        self.show_path()

    def show_path(self):
        """Put text on the path bar."""
        if self.prjFilePath is None:
            filePath = ''
        else:
            filePath = os.path.normpath(self.prjFilePath)
        self._pathBar.config(text=filePath)

    def start(self):
        self.root.mainloop()


def main():
    app = TimelineViewer()
    try:
        filePath = sys.argv[1]
    except IndexError:
        filePath = None
    else:
        app.read_data(filePath)
    app.start()


if __name__ == '__main__':
    main()

