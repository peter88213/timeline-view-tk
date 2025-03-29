"""Provide a mixin class for the timeline viewer commands.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from nvtlview.platform.platform_settings import KEYS
from nvtlview.tlv_locale import _
from tlviewer.tlviewer_globals import HELP_URL
from tlviewer.tlviewer_globals import HOME_URL


class TlviewerCommands:

    def about(self, event=None):
        """Display a legal notice window.
        
        Important: after building the program, __doc__ will be the timeline_viewer docstring.
        """
        messagebox.showinfo(
            message='Timeline viewer',
            detail=__doc__,
            title=_('About Timeline viewer')
            )

    def bind_events(self):
        # Bind the commands to the controller.
        event_callbacks = {
            '<<about>>': self.about,
            '<<close_project>>': self.close_project,
            '<<close_view>>': self.on_quit,
            '<<create_project>>':self.create_project,
            '<<disable_undo>>': self.disable_undo_button,
            '<<enable_undo>>': self.enable_undo_button,
            '<<fit_window>>': self.tlvCtrl.fit_window,
            '<<go_to_first>>': self.tlvCtrl.go_to_first,
            '<<go_to_last>>': self.tlvCtrl.go_to_last,
            '<<increase_scale>>': self.tlvCtrl.increase_scale,
            '<<open_help>>': self.open_help,
            '<<open_homepage>>': self.open_homepage,
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

    def close_project(self, event=None):
        """Close the novelibre project without saving and reset the user interface.
        
        To be extended by subclasses.
        """
        self.mdl.clear()
        self.prjFilePath = None
        self.show_path()
        self.disable_menu()

    def create_project(self, event=None):
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
            self.mdl.clear()
            self.prjFilePath = filePath
            self.show_path()
            self.save_project()

    def disable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='disabled')

    def enable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='normal')

    def on_quit(self, event=None):
        sys.exit(0)

    def open_help(self, event=None):
        webbrowser.open(HELP_URL)

    def open_homepage(self, event=None):
        webbrowser.open(HOME_URL)

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

    def open_section(self, scId):
        print(scId)

    def reload_project(self, event=None):
        if self.prjFilePath is not None:
            self.read_data(self.prjFilePath)

    def save_as(self, event=None):
        if self.prjFilePath is None:
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

