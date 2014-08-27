dot_nuke
========

This is stuff I like to have in my ~/.nuke folder. It makes my life easier while using Nuke from The Foundry.

I'm a freelancer, so I sit down at a new workstation in a new studio pretty often. I want to use my own Nuke customizations (captured here in this tb.nuke repository), but I don't want to make any permanent changes to the studio's Nuke config.

The best way I've found to do both of those things is to download this repo, unzip it into the user folder (the directory where the .nuke directory lives) and make sure it's named "tb.nuke". Then add this one line to the meny.py inside .nuke:

```
nuke.pluginAddPath(os.path.expanduser("~/tb.nuke"))
```

If os.path is not being imported already, you may need to do this first:
```
import os.path
```

When I leave, I can delete the "tb.nuke" folder, and if I forget to remove the line from menu.py, it's not going to cause any trouble.
