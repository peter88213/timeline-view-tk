"""A timeline viewer application using tkinter.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import sys
from tkinter import ttk
from tkinter import messagebox

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
        mainMenu = TlviewerMenu(self.root, settings)
        self.root.config(menu=mainMenu)

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

    def disable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='disabled')

    def enable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='normal')

    def on_quit(self, event=None):
        sys.exit(0)

    def read_data(self, filePath):
        try:
            self.mdl.read_data(filePath)
        except Exception as ex:
            messagebox.showerror(
                self.root.title(),
                message='Cannot load file',
                detail=str(ex),
                )
            return

        self.tlvCtrl.refresh()
        self.tlvCtrl.fit_window()
        self.show_path(filePath)

    def show_path(self, message):
        """Put text on the path bar."""
        self.pathBar.config(text=message)

    def start(self):
        self.root.mainloop()

    def _bind_events(self):
        # Bind the commands to the controller.
        event_callbacks = {
            '<<refresh_view>>': self.tlvCtrl.refresh,
            '<<go_to_first>>': self.tlvCtrl.go_to_first,
            '<<go_to_last>>': self.tlvCtrl.go_to_last,
            '<<set_hour_scale>>': self.tlvCtrl.set_hour_scale,
            '<<set_day_scale>>': self.tlvCtrl.set_day_scale,
            '<<set_year_scale>>': self.tlvCtrl.set_year_scale,
            '<<fit_window>>': self.tlvCtrl.fit_window,
            '<<set_casc_tight>>': self.tlvCtrl.set_casc_tight,
            '<<set_casc_relaxed>>': self.tlvCtrl.set_casc_relaxed,
            '<<reset_casc>>': self.tlvCtrl.reset_casc,
            '<<page_back>>': self.tlvCtrl.page_back,
            '<<page_forward>>': self.tlvCtrl.page_forward,
            '<<scroll_back>>': self.tlvCtrl.scroll_back,
            '<<scroll_forward>>': self.tlvCtrl.scroll_forward,
            '<<reduce_scale>>': self.tlvCtrl.reduce_scale,
            '<<increase_scale>>': self.tlvCtrl.increase_scale,
            '<<undo>>': self.tlvCtrl.undo,
            '<<disable_undo>>': self.disable_undo_button,
            '<<enable_undo>>': self.enable_undo_button,
            '<<close_view>>': self.on_quit,
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

