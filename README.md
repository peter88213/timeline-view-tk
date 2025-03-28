# timeline-view-tk

A timeline viewer programmed with Python, using tkinter.

![Screenshot](docs/Screenshots/screen01.png)

The data is read from a csv file:

![Screenshot](docs/Screenshots/screen02.png)

The *nvtlview* class library provides the *tlv* widget that is addressed via its controller.

*Timeline_viewer* is a simple standalone application using *nvtlview* 
with a menu and a toolbar. 

- The application reads the timeline data from a csv file and displays it on a resizable 
  window.
- Events can be defined with a specific date or with an unspecific day.
- For the day zero, a reference date can be defined, so that events with unspecific dates 
  can be placed on a calendar scale.  
- The user can increase and reduce the time scale. 
- The user can scroll forward and back in time.
- The user can move the events along the time scale using the mouse.
- The user can adjust the events' durations using the mouse.

The *nvtlview* class library is used for the 
[novelibre timeline viewer plugin](https://github.com/peter88213/nv_tlview/),
for example.

## License

This is Open Source software, and *timeline-view-tk* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/timeline-view-tk/blob/main/LICENSE) file.


