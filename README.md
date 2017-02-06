Security Risks of .desktop Shortcuts
====================================

After reading a [Reddit post](https://www.reddit.com/r/linux/comments/gbgoh/til_one_can_drop_any_selected_text_onto_gnome/) by "wander_homer", I was reminded to look at how .desktop shortcut files are handled on modern Linux systems.

A .desktop file which has the executable bit set will be parsed specially by file managers such as Nautilus. Rather than showing the true filename and file type Nautilus will display the application name and icon which is specified in the .desktop file. This allows for a malicious .desktop shortcut to easily masquerade as a safe file type.

Nautilus 3.22 added support for the automatic extraction of zip files and other archives when opened. This greatly increases the risk of this type of social engineering attack as a regular user will now have no opportunity to view the real file type before executing the command in the .desktop file.

These risks have been discussed are not new, they have been [discussed for more than 10 years](https://lwn.net/Articles/178409/). However serious thought needs to be given to mitigate these risks if Linux is to scale safely to more users.

### Example .desktop files

This repository contains a script for generating a malicious .desktop file which stealthy executes a Python payload. The payload cleans up the desktop shortcut and replace itself with a legitimate decoy file.

[sketchy.zip](https://github.com/DonnchaC/desktop-file-social-engineering/raw/master/sketchy.zip)
