dot_nuke
========

This is stuff I like to have in my ~/.nuke folder. It makes my life easier while using [Nuke from The Foundry](http://www.thefoundry.co.uk/).

I'm a freelancer, so I sit down at a new workstation in a new studio pretty often. I want to use my own Nuke customizations (captured here in this tb.nuke repository), but I don't want to make any permanent changes to the studio's Nuke config. This is the least intrusive way I have found to use my own magic without disrupting anyone else's pre-existing magic.

Here's what I do: download this repo, unzip it into the user folder (the directory where the .nuke directory lives) and make sure it's named "tb.nuke". Then add this one line to the init.py inside .nuke:

```
import os.path
nuke.pluginAddPath(os.path.expanduser("~/tb.nuke"))
```

If os.path is not being imported already, you may need to do this first:
```
import os.path
```

When I leave the studio, I can delete the "tb.nuke" folder and remove the line from menu.py and it's like I was never there. 
