[![Download the latest release](docs/img/download-button.png)](https://github.com/peter88213/timeline-view-tk/raw/main/dist/timeline_viewer_v0.1.0.pyzw)
[![Changelog](docs/img/changelog-button.png)](docs/changelog.md)
[![Feedback](docs/img/news-button.png)](https://github.com/peter88213/timeline-view-tk/discussions)
[![Online help](docs/img/help-button.png)](https://peter88213.github.io/timeline-view-tk/help/)


# timeline-view-tk

A timeline viewer programmed with Python, using tkinter.

![Screenshot](docs/Screenshots/screen01.png)

The data is read from a csv file:

![Screenshot](docs/Screenshots/screen02.png)

The *nvtlview* class library provides the *tlv* widget that is addressed via its controller.

*Timeline_viewer* is a simple standalone application using *nvtlview* 
with a menu and a toolbar. 

## Features

- The application reads the timeline data from a csv file and displays it on a resizable 
  window.
- Events can be defined with a specific date or with an unspecific day.
- For the day zero, you can define a reference date, so that events with unspecific dates 
  can be placed on a calendar scale.  
- You can increase and reduce the time scale. 
- You can scroll forward and back in time.
- You can move the events along the time scale using the mouse.
- You can adjust the events' durations using the mouse.
- The application is ready for internationalization with GNU gettext. German translations are provided. 

The *nvtlview* class library is used for the 
[novelibre timeline viewer plugin](https://github.com/peter88213/nv_tlview/),
for example.

## Requirements

- Windows or Linux. Mac OS support is experimental.
- [Python](https://www.python.org/) version 3.6+. 

---

[Changelog](docs/changelog.md)

[Feedback](https://github.com/peter88213/novelibre/discussions)

---

## Download and install

### Default: Executable Python zip archive

Download the latest release [timeline_viewer_v0.1.0.pyzw](https://github.com/peter88213/timeline-view-tk/raw/main/dist/timeline_viewer_v0.1.0.pyzw)

- Launch *timeline_viewer_v0.1.0.pyzw* by double-clicking (Windows/Linux desktop),
- or execute `python timeline_viewer_v0.1.0.pyzw` (Windows), resp. `python3 timeline_viewer_v0.1.0.pyzw` (Linux) on the command line.

#### Important

Many web browsers recognize the download as an executable file and offer to open it immediately. 
This starts the installation.

However, depending on your security settings, your browser may 
initially  refuse  to download the executable file. 
In this case, your confirmation or an additional action is required. 
If this is not possible, you have the option of downloading 
the zip file. 


### Alternative: Zip file

The package is also available in zip format: [timeline_viewer_v0.1.0.zip](https://github.com/peter88213/timeline-view-tk/raw/main/dist/timeline_viewer_v0.1.0.zip)

- Extract the *timeline_viewer_v0.1.0* folder from the downloaded zipfile "timeline_viewer_v0.1.0.zip".
- Move into this new folder and launch *setup.pyw* by double-clicking (Windows/Linux desktop), 
- or execute `python setup.pyw` (Windows), resp. `python3 setup.pyw` (Linux) on the command line.

You may wish to install plugins; the [update checker](https://github.com/peter88213/nv_updater/) is highly recommended.

---

## Credits

- The toolbar icons are based on the [Eva Icons](https://akveo.github.io/eva-icons/#/), published under the [MIT License](http://www.opensource.org/licenses/mit-license.php). The original black and white icons were adapted for this application by the maintainer. 

---

## License

This is Open Source software, and *timeline-view-tk* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/timeline-view-tk/blob/main/LICENSE) file.


