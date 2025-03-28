"""A timeline viewer application using tkinter.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from nvtlview.platform.platform_settings import KEYS
from nvtlview.tlv_controller import TlvController
import tkinter as tk
from tlv_model.tlv_data_model import TlvDataModel
from tlviewer.tlviewer_menu import TlviewerMenu
from tlviewer.tlviewer_toolbar import TlviewerToolbar

WINDOW_GEOMETRY = '1200x800'
SUBSTITUTE_MISSING_TIME = True
LOCALIZE_DATE = False


class TimelineViewer:

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
        self._bind_events()
        self.prjFilePath = None

    def close_project(self, event=None):
        """Close the novelibre project without saving and reset the user interface.
        
        To be extended by subclasses.
        """
        self.mdl.clear()
        self.prjFilePath = None
        self.show_path()
        self.disable_menu()

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self.mainMenu.disable_menu()
        self.toolbar.disable_menu()

    def disable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self.mainMenu.enable_menu()
        self.toolbar.enable_menu()

    def enable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='normal')

    def on_quit(self, event=None):
        sys.exit(0)

    def open_project(self, event=None):
        if self.prjFilePath:
            initDir = os.path.dirname(self.prjFilePath)
        else:
            initDir = './'

        filePath = filedialog.askopenfilename(
            filetypes=[
                ('Comma separated values', '.csv'),
                ('All files', '.*'),
            ],
            defaultextension='.csv',
            initialdir=initDir
            )
        if filePath:
            self.read_data(filePath)

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

    def reload_project(self, event=None):
        if self.prjFilePath is not None:
            self.read_data(self.prjFilePath)

    def save_as(self, event=None):
        if not self.prjFilePath:
            return

        if self.prjFilePath:
            initDir = os.path.dirname(self.prjFilePath)
        else:
            initDir = './'

        filePath = filedialog.asksaveasfilename(
            filetypes=[
                ('Comma separated values', '.csv'),
                ('All files', '.*'),
            ],
            defaultextension='.csv',
            initialdir=initDir
            )
        if filePath:
            self.prjFilePath = filePath
            self.save_project()
            self.refresh()

    def save_project(self, event=None):
        if self.prjFilePath:
            try:
                self.mdl.write_data(self.prjFilePath)
            except Exception as ex:
                messagebox.showerror(
                    self.root.title(),
                    message='Cannot save file',
                    detail=str(ex),
                    )

    def show_path(self):
        """Put text on the path bar."""
        if self.prjFilePath is None:
            filePath = ''
        else:
            filePath = os.path.normpath(self.prjFilePath)
        self.pathBar.config(text=filePath)

    def start(self):
        self.root.mainloop()

    def _bind_events(self):
        # Bind the commands to the controller.
        event_callbacks = {
            '<<close_project>>': self.close_project,
            '<<close_view>>': self.on_quit,
            '<<disable_undo>>': self.disable_undo_button,
            '<<enable_undo>>': self.enable_undo_button,
            '<<fit_window>>': self.tlvCtrl.fit_window,
            '<<go_to_first>>': self.tlvCtrl.go_to_first,
            '<<go_to_last>>': self.tlvCtrl.go_to_last,
            '<<increase_scale>>': self.tlvCtrl.increase_scale,
            '<<open_project>>': self.open_project,
            '<<page_back>>': self.tlvCtrl.page_back,
            '<<page_forward>>': self.tlvCtrl.page_forward,
            '<<reduce_scale>>': self.tlvCtrl.reduce_scale,
            '<<refresh_view>>': self.tlvCtrl.refresh,
            '<<reload_project>>': self.reload_project,
            '<<reset_casc>>': self.tlvCtrl.reset_casc,
            '<<save_as>>': self.save_as,
            '<<save_project>>': self.save_project,
            '<<scroll_back>>': self.tlvCtrl.scroll_back,
            '<<scroll_forward>>': self.tlvCtrl.scroll_forward,
            '<<set_casc_relaxed>>': self.tlvCtrl.set_casc_relaxed,
            '<<set_casc_tight>>': self.tlvCtrl.set_casc_tight,
            '<<set_day_scale>>': self.tlvCtrl.set_day_scale,
            '<<set_hour_scale>>': self.tlvCtrl.set_hour_scale,
            '<<set_year_scale>>': self.tlvCtrl.set_year_scale,
            '<<undo>>': self.tlvCtrl.undo,
            KEYS.OPEN_PROJECT[0]: self.open_project,
            KEYS.RELOAD_PROJECT[0]: self.reload_project,
            KEYS.SAVE_AS[0]: self.save_as,
            KEYS.SAVE_PROJECT[0]: self.save_project,
        }
        for sequence, callback in event_callbacks.items():
            self.root.bind(sequence, callback)


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

