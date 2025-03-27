"""A timeline viewer application using tkinter.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import sys
from tkinter import ttk

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

        def disable_undo_button(self, event=None):
            toolbar.undoButton.config(state='disabled')

        def enable_undo_button(self, event=None):
            toolbar.undoButton.config(state='normal')

        def on_quit(event=None):
            sys.exit(0)

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
        toolbar = TlviewerToolbar(mainWindow, largeIcons=False, enableHovertips=True)
        toolbar.pack(side='bottom', fill='x', padx=5, pady=2)

        self.tlvCtrl = TlvController(
            self.mdl,
            mainWindow,
            LOCALIZE_DATE,
            settings,
            )
        self.mdl.add_observer(self.tlvCtrl)

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
            '<<disable_undo>>': disable_undo_button,
            '<<enable_undo>>': enable_undo_button,
            '<<close_view>>': on_quit,
        }
        for sequence, callback in event_callbacks.items():
            self.root.bind(sequence, callback)

    def read_data(self, filePath):
        self.mdl.read_data(filePath)
        self.tlvCtrl.refresh()
        self.tlvCtrl.fit_window()

    def start(self):
        self.root.mainloop()


def main(filePath=None):
    app = TimelineViewer()
    if filePath is not None:
        app.read_data(filePath)
    app.start()


if __name__ == '__main__':
    main(sys.argv[1])
