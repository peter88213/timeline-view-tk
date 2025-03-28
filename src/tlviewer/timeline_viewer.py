"""A timeline viewer application using tkinter.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
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

WINDOW_GEOMETRY = '1200x800'
SUBSTITUTE_MISSING_TIME = True
LOCALIZE_DATE = False


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
        self.mainMenu = TlviewerMenu(self.root, settings)
        self.root.config(menu=self.mainMenu)

        self.mdl = TlvDataModel()
        mainWindow = ttk.Frame(self.root)
        mainWindow.pack(fill='both', expand=True)
        self.pathBar = tk.Label(mainWindow, text='', anchor='w', padx=5, pady=3)
        self.pathBar.pack(side='bottom', expand=False, fill='x')
        self.toolbar = TlviewerToolbar(mainWindow, largeIcons=False, enableHovertips=True)
        self.toolbar.pack(side='bottom', fill='x', padx=5, pady=2)

        self.tlvCtrl = TlvController(
            self.mdl,
            mainWindow,
            LOCALIZE_DATE,
            settings,
            )
        self.mdl.add_observer(self.tlvCtrl)
        self.bind_events()
        self.prjFilePath = None

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self.mainMenu.disable_menu()
        self.toolbar.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self.mainMenu.enable_menu()
        self.toolbar.enable_menu()

    def read_data(self, filePath):
        if self.prjFilePath is not None:
            self.close_project()
        try:
            self.mdl.read_data(filePath)
        except Exception as ex:
            messagebox.showerror(
                self.root.title(),
                message='Cannot load file',
                detail=str(ex),
                )
        else:
            self.prjFilePath = filePath
            self.refresh()

    def refresh(self, event=None):
        self.tlvCtrl.refresh()
        self.tlvCtrl.fit_window()
        self.enable_menu()
        self.show_path()

    def show_path(self):
        """Put text on the path bar."""
        if self.prjFilePath is None:
            filePath = ''
        else:
            filePath = os.path.normpath(self.prjFilePath)
        self.pathBar.config(text=filePath)

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

