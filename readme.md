# Kiosk-Browser

A simple kiosk-browser for exams and stuff.
Prevents the user from accessing non-whitelisted sites or other sheneningans.

A full kiosk-environment can be achieved by additionally limiting the desktop environments features (e.g. running arbitrary programs) - for example by using a minimalist windowmanager like xmonad with a restrictive configuration.

# Features

* display and navigate webpages (duh)
    - back/forward through simple browsing-history
* url-whitelist
    - provide a plain-text file of regular expressions for url's to be whitelisted
    - the url called at the start is whitelisted automatically (to display a local file instead, call it like 'file:/example.html')
* custom user-agent

# Dependencies

Python3 with PyQt5 and PyQt5-webengine.
