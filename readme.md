# Quick Shortcuts GUI in Python
The program looks for the options.yaml file where a user can configure a
hotkey, program shortcuts, text entry shortcuts and individual keystrokes or
hotkeys.

When invoked with the configured main hotkey, the program displays a
simple button box power by PyMsgBox, just modified to make the box always on
top. Here the user can select from their configured shortcuts.

This is a bare-bones proof-of-concept to replace the start menu and auto-hotkey for
various tasks.

## Features
- Tray icon with title and right click to close.
- Unlimited shortcuts, text entry shortcuts, and basic keyboard automation via
  a simple yaml file.
- Configurable hotkey to invoke the button box, then point and click to select
  the desired shortcut.
- Pep8 styled python, featuring threading, conditionals, callbacks, loops,
  functions and dataclasses, and (incomplete) type hinting.
